"""Fail-closed Linux CPU capture; requires Xvfb, xkbcomp and Mesa.

This verifies the capture transport, not art, performance or normal gameplay.
The existing game's --capture still repositions the player. Evidence is kept
per invocation; no engine/gameplay source or existing log is overwritten.
"""
from pathlib import Path
import argparse
from contextlib import contextmanager
import datetime
import fcntl
import hashlib
import json
import math
import os
import re
import secrets
import shutil
import signal
import socket
import stat
import struct
import subprocess
import sys
import tempfile
import time
import zlib


class CaptureError(RuntimeError):
    """The invocation did not produce qualified capture evidence."""


def stop_owned(process, grace=1.0):
    """Stop only the process group created by our start_new_session=True.

    Kill remaining descendants even when their parent already exited. Never
    use pkill, a display's PID, or a process inferred from a stale receipt.
    """
    try:
        os.killpg(process.pid, signal.SIGTERM)
    except ProcessLookupError:
        pass
    try:
        process.wait(timeout=grace)
    except subprocess.TimeoutExpired:
        pass
    finally:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        process.wait(timeout=grace)


@contextmanager
def writer_lock(root):
    """Cooperative capture-only lock, not a studio/Fleet authorization."""
    folder = root / '.tools'
    folder.mkdir(exist_ok=True)
    fd = os.open(folder / 'capture.lock', os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
    try:
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise CaptureError('another capture owns this checkout') from exc
        yield
    finally:
        # Keep the inode: unlinking a flock file creates split-brain locks.
        os.close(fd)


@contextmanager
def virtual_display(xvfb, env, log_path, timeout):
    display = 100 + os.getpid() % 400
    port = 6000 + display
    # Do not attach to, terminate, or take over an already listening display.
    try:
        with socket.create_connection(('127.0.0.1', port), .1):
            raise CaptureError('selected display is occupied; no takeover attempted')
    except OSError:
        pass
    with tempfile.TemporaryDirectory(prefix='exovant-display-') as tmp:
        auth = Path(tmp) / 'authority'
        fields = [b'', str(display).encode(), b'MIT-MAGIC-COOKIE-1', secrets.token_bytes(16)]
        auth.write_bytes(struct.pack('>H', 65535) + b''.join(
            struct.pack('>H', len(x)) + x for x in fields))
        auth.chmod(0o600)
        env = dict(env, DISPLAY=f'127.0.0.1:{display}', XAUTHORITY=str(auth))
        with log_path.open('w') as log:
            server = subprocess.Popen([
                xvfb, f':{display}', '-screen', '0', '1280x720x24',
                '-nolisten', 'unix', '-nolisten', 'local', '-listen', 'tcp',
                '-auth', str(auth)], env=env, stdout=log, stderr=log,
                start_new_session=True)
            try:
                deadline = time.monotonic() + timeout
                while True:
                    if server.poll() is not None:
                        raise CaptureError('virtual display exited before readiness')
                    try:
                        with socket.create_connection(('127.0.0.1', port), .1):
                            if server.poll() is not None:
                                raise CaptureError('virtual display exited during readiness')
                            break
                    except OSError:
                        if time.monotonic() >= deadline:
                            raise CaptureError('virtual display readiness timeout')
                        time.sleep(.05)
                yield env
            finally:
                stop_owned(server)


def png_metadata(path):
    """Check the PNG container/CRCs; this is not raster or visual approval."""
    if path.is_symlink() or not path.is_file():
        raise CaptureError('PNG missing or not a regular file')
    if path.stat().st_size > 32 * 1024 * 1024:
        raise CaptureError('PNG exceeds the 32 MiB capture limit')
    data = path.read_bytes()
    if not data.startswith(b'\x89PNG\r\n\x1a\n'):
        raise CaptureError('invalid PNG signature')
    pos, chunks, idat_size = 8, [], 0
    width = height = 0
    while pos < len(data):
        if len(data) - pos < 12:
            raise CaptureError('truncated PNG chunk')
        size = struct.unpack_from('>I', data, pos)[0]
        kind = data[pos + 4:pos + 8]
        end = pos + 12 + size
        if end > len(data):
            raise CaptureError('truncated PNG payload')
        payload = data[pos + 8:pos + 8 + size]
        crc = struct.unpack_from('>I', data, pos + 8 + size)[0]
        if zlib.crc32(kind + payload) & 0xffffffff != crc:
            raise CaptureError('PNG CRC mismatch')
        if not chunks and kind != b'IHDR':
            raise CaptureError('PNG IHDR must be first')
        if kind == b'IHDR':
            if chunks or size != 13:
                raise CaptureError('invalid or repeated PNG IHDR')
            width, height = struct.unpack_from('>II', payload)
            if not width or not height:
                raise CaptureError('empty PNG dimensions')
        elif kind == b'IDAT':
            idat_size += size
        elif kind == b'IEND':
            if size or end != len(data) or not idat_size:
                raise CaptureError('invalid PNG end or missing image data')
        chunks.append(kind)
        pos = end
    if not chunks or chunks[-1] != b'IEND':
        raise CaptureError('PNG IEND missing')
    return {'width': width, 'height': height, 'bytes': len(data),
            'sha256': hashlib.sha256(data).hexdigest(),
            'validation': 'container_crc_only_not_visual_approval'}


def validate_capture(log, image, returncode, started_ns, previous_identity=None):
    if returncode != 0:
        raise CaptureError(f'engine exit code {returncode}')
    clean = re.sub(r'\x1b\[[0-?]*[ -/]*[@-~]', '', log)
    if re.search(r'^\s*(?:SCRIPT ERROR|ERROR|FATAL(?: ERROR)?)(?::|\s*$)', clean, re.M):
        raise CaptureError('engine reported a fatal/error diagnostic')
    if clean.splitlines().count('CAPTURE_SAVED') != 1:
        raise CaptureError('expected exactly one CAPTURE_SAVED marker')
    if image.is_symlink() or not image.is_file():
        raise CaptureError('current invocation produced no regular PNG')
    info = image.stat()
    if info.st_mtime_ns < started_ns:
        raise CaptureError('PNG predates this engine invocation')
    if previous_identity == (info.st_dev, info.st_ino):
        raise CaptureError('PNG reuses the previous evidence inode')
    return png_metadata(image)


def copy_atomic(source, target):
    fd, name = tempfile.mkstemp(prefix='.capture-copy-', dir=target.parent)
    os.close(fd)
    try:
        shutil.copy2(source, name)
        os.replace(name, target)
    finally:
        Path(name).unlink(missing_ok=True)


def restore_snapshot(data, metadata, target):
    """Restore the original bytes/metadata even after a hard-link replay."""
    fd, name = tempfile.mkstemp(prefix='.capture-snapshot-', dir=target.parent)
    try:
        with os.fdopen(fd, 'wb') as out:
            out.write(data)
        os.chmod(name, stat.S_IMODE(metadata.st_mode))
        os.utime(name, ns=(metadata.st_atime_ns, metadata.st_mtime_ns))
        os.replace(name, target)
    finally:
        Path(name).unlink(missing_ok=True)


def capture(root, godot, xvfb='Xvfb', xlibs='', timeout=90, display_timeout=5):
    root = Path(root).resolve()
    for value in (timeout, display_timeout):
        if not math.isfinite(value) or value <= 0:
            raise CaptureError('timeouts must be finite and positive')
    env = dict(os.environ, LIBGL_ALWAYS_SOFTWARE='1')
    if xlibs:
        env['LD_LIBRARY_PATH'] = str(Path(xlibs).resolve())
    with writer_lock(root):
        evidence = root / 'evidence'
        evidence.mkdir(exist_ok=True)
        runtime = evidence / 'runtime.png'
        if runtime.is_symlink() or (runtime.exists() and not runtime.is_file()):
            raise CaptureError('refusing non-regular existing runtime.png')
        captures = evidence / 'captures'
        captures.mkdir(exist_ok=True)
        run_dir = Path(tempfile.mkdtemp(prefix='capture-', dir=captures))
        previous = run_dir / 'previous-runtime.png'
        image = run_dir / 'runtime.png'
        log_path = run_dir / 'visual-run.log'
        receipt = {'status': 'failed', 'passed': False,
                   'scope': 'CPU capture transport; game --capture repositions player',
                   'runner_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                   'executed_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                   'returncode': None, 'timed_out': False,
                   'evidence_directory': str(run_dir.relative_to(root)),
                   'art_approval': False, 'normal_playthrough': False}
        previous_identity = None
        previous_data = None
        old = None
        if runtime.exists():
            old = runtime.stat()
            if old.st_size > 32 * 1024 * 1024:
                raise CaptureError('previous PNG exceeds safe snapshot limit; untouched')
            previous_data = runtime.read_bytes()
            receipt['previous_sha256'] = hashlib.sha256(previous_data).hexdigest()
            previous_identity = (old.st_dev, old.st_ino)
            runtime.rename(previous)
        try:
            with virtual_display(xvfb, env, run_dir / 'display.log', display_timeout) as child_env:
                started_ns = time.time_ns()
                receipt['engine_started_ns'] = started_ns
                with log_path.open('w') as out:
                    process = subprocess.Popen([
                        str(Path(godot).resolve()), '--path', str(root),
                        '--rendering-method', 'gl_compatibility', '--audio-driver', 'Dummy',
                        '--', '--capture'], env=child_env, stdout=out, stderr=out,
                        start_new_session=True)
                    try:
                        receipt['returncode'] = process.wait(timeout=timeout)
                    except subprocess.TimeoutExpired as exc:
                        receipt['timed_out'] = True
                        raise CaptureError('engine capture timeout') from exc
                    finally:
                        stop_owned(process)
                receipt['image'] = validate_capture(
                    log_path.read_text(errors='replace'), runtime,
                    receipt['returncode'], started_ns, previous_identity)
            receipt.update(status='passed', passed=True)
        except BaseException as exc:
            receipt['error'] = f'{type(exc).__name__}: {exc}'
            if isinstance(exc, (KeyboardInterrupt, SystemExit)):
                raise
            raise CaptureError(f'{receipt["error"]}; evidence: {run_dir}') from exc
        finally:
            # Each artifact is moved only after our engine group has stopped.
            # Failed attempts remain inspectable; prior evidence is restored.
            if runtime.exists() or runtime.is_symlink():
                runtime.rename(image)
            if previous_data is not None:
                restore_snapshot(previous_data, old, previous)
            if receipt['passed'] and image.is_file() and not image.is_symlink():
                copy_atomic(image, runtime)
            elif previous.exists():
                copy_atomic(previous, runtime)
            (run_dir / 'receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
        return run_dir


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--godot', required=True)
    parser.add_argument('--xvfb', default='Xvfb')
    parser.add_argument('--xlibs', default='')
    parser.add_argument('--timeout', type=float, default=90)
    parser.add_argument('--display-timeout', type=float, default=5)
    args = parser.parse_args(argv)
    try:
        directory = capture(Path(__file__).resolve().parents[1], **vars(args))
    except (CaptureError, OSError) as exc:
        print(f'Capture failed: {exc}', file=sys.stderr)
        return 1
    print('Captured:', directory / 'runtime.png')
    print('Receipt:', directory / 'receipt.json')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
