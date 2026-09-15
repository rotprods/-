"""Optional Linux CPU-render capture with strict freshness/error validation."""
from pathlib import Path
import argparse
import contextlib
import fcntl
import json
import os
import secrets
import signal
import socket
import struct
import subprocess
import tempfile
import time
import zlib

ERROR_TOKENS = ("SCRIPT ERROR", "ERROR:")
CAPTURE_MARKER = "CAPTURE_SAVED"
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def _read_png(path: Path) -> dict:
    """Validate PNG framing/chunks/CRCs without depending on Pillow."""
    data = path.read_bytes()
    if not data.startswith(PNG_SIGNATURE):
        raise RuntimeError("Capture is not a PNG")
    offset = len(PNG_SIGNATURE)
    chunks = []
    saw_ihdr = False
    saw_iend = False
    while offset < len(data):
        if offset + 12 > len(data):
            raise RuntimeError("Capture PNG has truncated chunk header")
        length = struct.unpack(">I", data[offset:offset + 4])[0]
        kind = data[offset + 4:offset + 8]
        end = offset + 12 + length
        if end > len(data):
            raise RuntimeError("Capture PNG has truncated chunk payload")
        payload = data[offset + 8:offset + 8 + length]
        expected = struct.unpack(">I", data[offset + 8 + length:end])[0]
        actual = zlib.crc32(kind + payload) & 0xFFFFFFFF
        if expected != actual:
            raise RuntimeError("Capture PNG CRC mismatch")
        if not chunks and kind != b"IHDR":
            raise RuntimeError("Capture PNG first chunk is not IHDR")
        if kind == b"IHDR":
            if saw_ihdr or length != 13:
                raise RuntimeError("Capture PNG invalid IHDR")
            saw_ihdr = True
        if kind == b"IEND":
            if saw_iend or length != 0:
                raise RuntimeError("Capture PNG invalid IEND")
            saw_iend = True
            if end != len(data):
                raise RuntimeError("Capture PNG contains trailing data")
        chunks.append(kind.decode("ascii", errors="replace"))
        offset = end
    if not saw_ihdr or not saw_iend:
        raise RuntimeError("Capture PNG missing required chunks")
    return {"bytes": len(data), "chunks": chunks}


def _kill_process_group(proc: subprocess.Popen, grace: float = 2.0) -> None:
    if proc.poll() is not None:
        return
    try:
        os.killpg(proc.pid, signal.SIGTERM)
    except ProcessLookupError:
        return
    try:
        proc.wait(timeout=grace)
        return
    except subprocess.TimeoutExpired:
        pass
    try:
        os.killpg(proc.pid, signal.SIGKILL)
    except ProcessLookupError:
        return
    proc.wait(timeout=grace)


def _wait_for_display(server: subprocess.Popen, port: int, attempts: int = 50) -> None:
    for _ in range(attempts):
        if server.poll() is not None:
            raise RuntimeError("Virtual display failed; inspect attempt display.log")
        try:
            with socket.create_connection(("127.0.0.1", port), .1):
                return
        except OSError:
            time.sleep(.1)
    raise RuntimeError("Virtual display did not become reachable")


def _snapshot(path: Path):
    if not path.exists():
        return None
    stat = path.stat()
    return {
        "bytes": path.read_bytes(),
        "inode": stat.st_ino,
        "mtime_ns": stat.st_mtime_ns,
        "size": stat.st_size,
    }


def _restore(path: Path, previous) -> None:
    if previous is None:
        path.unlink(missing_ok=True)
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(previous["bytes"])
    os.utime(path, ns=(previous["mtime_ns"], previous["mtime_ns"]))


def _validate_run(run: subprocess.CompletedProcess, log_text: str, image: Path,
                  previous, started_ns: int) -> dict:
    if run.returncode:
        raise RuntimeError(f"Render failed with exit {run.returncode}")
    for token in ERROR_TOKENS:
        if token in log_text:
            raise RuntimeError(f"Render log contains fatal token: {token}")
    marker_count = log_text.count(CAPTURE_MARKER)
    if marker_count != 1:
        raise RuntimeError(f"Expected exactly one {CAPTURE_MARKER}, got {marker_count}")
    if not image.is_file():
        raise RuntimeError("Capture marker emitted but runtime.png is absent")
    stat = image.stat()
    if stat.st_mtime_ns < started_ns:
        raise RuntimeError("runtime.png predates this capture attempt")
    if previous is not None and stat.st_ino == previous["inode"]:
        raise RuntimeError("runtime.png reused the previous inode")
    png = _read_png(image)
    return {
        "passed": True,
        "returncode": run.returncode,
        "marker_count": marker_count,
        "image_mtime_ns": stat.st_mtime_ns,
        "image_inode": stat.st_ino,
        "png": png,
    }


def capture(args) -> Path:
    root = Path(__file__).resolve().parents[1]
    evidence = root / "evidence"
    evidence.mkdir(exist_ok=True)
    image = evidence / "runtime.png"
    previous = _snapshot(image)
    lock_path = evidence / ".capture_visual.lock"
    lock_file = lock_path.open("a+")
    try:
        try:
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise RuntimeError("Another capture_visual attempt owns the local capture lock") from exc
        attempt = evidence / "capture-attempts" / f"{time.time_ns()}-{os.getpid()}"
        attempt.mkdir(parents=True, exist_ok=False)
        display_log_path = attempt / "display.log"
        render_log_path = attempt / "visual-run.log"
        receipt_path = attempt / "receipt.json"
        env = os.environ.copy()
        if args.xlibs:
            env["LD_LIBRARY_PATH"] = str(Path(args.xlibs).resolve())
        display = 100 + os.getpid() % 400
        env["DISPLAY"] = f"127.0.0.1:{display}"
        env["LIBGL_ALWAYS_SOFTWARE"] = "1"
        server = None
        started_ns = time.time_ns()
        receipt = {"passed": False, "started_ns": started_ns, "display": display}
        try:
            with tempfile.TemporaryDirectory(prefix="exovant-display-") as tmp:
                auth = Path(tmp) / "authority"
                fields = [b"", str(display).encode(), b"MIT-MAGIC-COOKIE-1", secrets.token_bytes(16)]
                auth.write_bytes(struct.pack(">H", 65535) + b"".join(struct.pack(">H", len(x)) + x for x in fields))
                auth.chmod(0o600)
                with display_log_path.open("w") as display_log:
                    server = subprocess.Popen(
                        [args.xvfb, f":{display}", "-screen", "0", "1280x720x24", "-nolisten", "unix",
                         "-nolisten", "local", "-listen", "tcp", "-auth", str(auth)],
                        env=env, stdout=display_log, stderr=display_log, start_new_session=True)
                    _wait_for_display(server, 6000 + display)
                    cmd = [str(Path(args.godot).resolve()), "--path", str(root), "--rendering-method",
                           "gl_compatibility", "--audio-driver", "Dummy", "--", "--capture"]
                    try:
                        run = subprocess.run(cmd, env=env, capture_output=True, text=True,
                                             timeout=args.timeout, start_new_session=True)
                    except subprocess.TimeoutExpired as exc:
                        output = (exc.stdout or "") + (exc.stderr or "")
                        render_log_path.write_text(output if isinstance(output, str) else output.decode(errors="replace"))
                        raise RuntimeError(f"Render timed out after {args.timeout}s") from exc
                    log_text = (run.stdout or "") + (run.stderr or "")
                    render_log_path.write_text(log_text)
                    receipt.update(_validate_run(run, log_text, image, previous, started_ns))
                    attempt_image = attempt / "runtime.png"
                    attempt_image.write_bytes(image.read_bytes())
                    receipt["attempt_image"] = str(attempt_image.relative_to(root))
                    receipt["render_log"] = str(render_log_path.relative_to(root))
                    receipt["display_log"] = str(display_log_path.relative_to(root))
                    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n")
                    # Compatibility logs are copied only after a successful, validated attempt.
                    (evidence / "visual-run.log").write_text(log_text)
                    (evidence / "display.log").write_text(display_log_path.read_text())
                    print("Captured:", image)
                    return image
        except Exception as exc:
            receipt["error"] = str(exc)
            with contextlib.suppress(Exception):
                receipt_path.write_text(json.dumps(receipt, indent=2) + "\n")
            _restore(image, previous)
            raise
        finally:
            if server is not None:
                _kill_process_group(server)
    finally:
        with contextlib.suppress(Exception):
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)
        lock_file.close()


def parse_args(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--godot", required=True)
    p.add_argument("--xvfb", default="Xvfb")
    p.add_argument("--xlibs", default="")
    p.add_argument("--timeout", type=float, default=90)
    return p.parse_args(argv)


if __name__ == "__main__":
    capture(parse_args())
