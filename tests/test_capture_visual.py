"""CPU-only capture regressions; fixture engines are NOT native Godot gates."""
from contextlib import contextmanager
import importlib.util
import json
import os
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import MagicMock, patch
import zlib

SPEC = importlib.util.spec_from_file_location('exovant_capture', Path(__file__).with_name('capture_visual.py'))
cv = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(cv)


def chunk(kind, data):
    return struct.pack('>I', len(data)) + kind + data + struct.pack('>I', zlib.crc32(kind + data) & 0xffffffff)


def png():
    return (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', 2, 2, 8, 2, 0, 0, 0))
            + chunk(b'IDAT', zlib.compress(b'\0' + b'\x80\x90\xa0' * 2 + b'\0' + b'\x80\x90\xa0' * 2))
            + chunk(b'IEND', b''))


@contextmanager
def no_display(xvfb, env, log_path, timeout):
    log_path.write_text('DISPLAY FIXTURE: no native renderer exercised\n')
    yield env


ENGINE = r'''#!EXECUTABLE -S
from pathlib import Path
import os, subprocess, sys, time
root = Path(sys.argv[sys.argv.index('--path') + 1])
image = root/'evidence/runtime.png'
mode = os.environ['EXO_CAPTURE_TEST_MODE']
data = bytes.fromhex(os.environ['EXO_CAPTURE_TEST_PNG'])
if mode == 'child_timeout':
    child = subprocess.Popen([sys.executable, '-S', '-c', 'import signal,time; signal.signal(signal.SIGTERM,signal.SIG_IGN); time.sleep(30)'])
    (root/'evidence/child.pid').write_text(str(child.pid))
if mode == 'reuse_inode':
    old = next((root/'evidence/captures').glob('*/previous-runtime.png'))
    os.link(old, image)
    os.utime(image, None)
elif mode == 'symlink':
    image.symlink_to(os.environ['EXO_CAPTURE_SYMLINK_TARGET'])
elif mode != 'missing':
    image.write_bytes(b'invalid' if mode == 'corrupt' else data)
    if mode == 'stale': os.utime(image, (1000, 1000))
if mode != 'no_marker': print('CAPTURE_SAVED', flush=True)
if mode == 'duplicate_marker': print('CAPTURE_SAVED', flush=True)
if mode == 'script_error': print('SCRIPT ERROR: fixture failure', file=sys.stderr, flush=True)
if mode == 'error': print('\\x1b[31mERROR: fixture failure\\x1b[0m'.encode().decode('unicode_escape'), file=sys.stderr, flush=True)
if mode == 'warning': print('WARNING: optional renderer hint', flush=True)
if mode == 'warning_error_word': print('WARNING: optional ERROR.md was not supplied', flush=True)
if mode in ('timeout', 'child_timeout'): time.sleep(30)
sys.exit(9 if mode == 'nonzero' else 0)
'''


class CaptureTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='exovant-capture-test-')
        self.root = Path(self.temp.name)
        (self.root/'evidence').mkdir()
        self.old = self.root/'evidence/runtime.png'
        self.old.write_bytes(b'previous evidence must survive')
        os.utime(self.old, (1000, 1000))
        self.engine = self.root/'fixture_engine.py'
        self.engine.write_text(ENGINE.replace('EXECUTABLE', sys.executable))
        self.engine.chmod(0o700)
        self.env = {'EXO_CAPTURE_TEST_MODE': 'warning', 'EXO_CAPTURE_TEST_PNG': png().hex()}

    def tearDown(self):
        self.temp.cleanup()

    def run_capture(self, mode, **kwargs):
        env = dict(self.env, EXO_CAPTURE_TEST_MODE=mode)
        with patch.dict(os.environ, env), patch.object(cv, 'virtual_display', no_display):
            return cv.capture(self.root, self.engine, **kwargs)

    def receipt(self):
        files = list((self.root/'evidence/captures').glob('*/receipt.json'))
        self.assertEqual(len(files), 1)
        return json.loads(files[0].read_text())

    def assert_failed(self, mode, **kwargs):
        with self.assertRaises(cv.CaptureError):
            self.run_capture(mode, **kwargs)
        result = self.receipt()
        self.assertFalse(result['passed'])
        self.assertEqual(self.old.read_bytes(), b'previous evidence must survive')
        self.assertEqual(self.old.stat().st_mtime, 1000)
        return result

    def test_valid_frame_and_warning_pass_preserve_old_logs(self):
        for name in ('display.log', 'visual-run.log'):
            (self.root/'evidence'/name).write_text('historical log')
        directory = self.run_capture('warning')
        self.assertTrue(self.receipt()['passed'])
        self.assertEqual((directory/'runtime.png').read_bytes(), png())
        self.assertEqual(self.old.read_bytes(), png())
        self.assertEqual((directory/'previous-runtime.png').read_bytes(), b'previous evidence must survive')
        for name in ('display.log', 'visual-run.log'):
            self.assertEqual((self.root/'evidence'/name).read_text(), 'historical log')

    def test_no_historical_image_success(self):
        self.old.unlink()
        directory = self.run_capture('warning')
        self.assertFalse((directory/'previous-runtime.png').exists())
        self.assertEqual(self.old.read_bytes(), png())

    def test_same_pixels_in_fresh_file_are_not_a_false_stale_failure(self):
        self.old.write_bytes(png())
        directory = self.run_capture('warning')
        self.assertTrue(self.receipt()['passed'])
        self.assertNotEqual((directory/'previous-runtime.png').stat().st_ino, (directory/'runtime.png').stat().st_ino)

    def test_script_error_exit_zero_even_with_marker_and_png(self):
        self.assert_failed('script_error')

    def test_ansi_engine_error_exit_zero_even_with_marker_and_png(self):
        self.assert_failed('error')

    def test_nonzero_exit_even_with_marker_and_png(self):
        self.assertEqual(self.assert_failed('nonzero')['returncode'], 9)

    def test_missing_marker_even_with_fresh_png(self):
        self.assert_failed('no_marker')

    def test_duplicate_marker_rejected(self):
        self.assert_failed('duplicate_marker')

    def test_missing_current_png_despite_historical_evidence(self):
        self.assert_failed('missing')

    def test_stale_mtime_rejected(self):
        self.assert_failed('stale')

    def test_corrupt_png_rejected(self):
        self.assert_failed('corrupt')

    def test_timeout_even_with_marker_and_png(self):
        result = self.assert_failed('timeout', timeout=1)
        self.assertTrue(result['timed_out'])
        directory = self.root/result['evidence_directory']
        self.assertIn('CAPTURE_SAVED', (directory/'visual-run.log').read_text())
        self.assertEqual((directory/'runtime.png').read_bytes(), png())

    def test_timeout_kills_owned_child_not_unrelated_process(self):
        outsider = subprocess.Popen([sys.executable, '-S', '-c', 'import time; time.sleep(30)'], start_new_session=True)
        try:
            self.assert_failed('child_timeout', timeout=1.5)
            child = int((self.root/'evidence/child.pid').read_text())
            procstat = Path(f'/proc/{child}/stat')
            for _ in range(30):
                if not procstat.exists() or procstat.read_text().split()[2] == 'Z':
                    break
                time.sleep(.02)
            else:
                self.fail('owned child still running after timeout cleanup')
            self.assertIsNone(outsider.poll(), 'unrelated process was terminated')
        finally:
            outsider.terminate()
            outsider.wait(timeout=3)

    def test_previous_inode_replay_rejected(self):
        self.assert_failed('reuse_inode')

    def test_warning_containing_error_filename_is_not_fatal(self):
        self.run_capture('warning_error_word')
        self.assertTrue(self.receipt()['passed'])

    def test_concurrent_capture_refused_before_moving_evidence(self):
        with cv.writer_lock(self.root):
            with self.assertRaisesRegex(cv.CaptureError, 'another capture'):
                self.run_capture('warning')
        self.assertEqual(self.old.read_bytes(), b'previous evidence must survive')
        self.assertFalse((self.root/'evidence/captures').exists())
        self.run_capture('warning')
        self.assertTrue(self.receipt()['passed'])

    def test_existing_symlink_refused_without_touching_target(self):
        target = self.root/'original.png'
        target.write_bytes(b'outside evidence')
        self.old.unlink()
        self.old.symlink_to(target)
        with self.assertRaises(cv.CaptureError):
            self.run_capture('warning')
        self.assertEqual(target.read_bytes(), b'outside evidence')
        self.assertTrue(self.old.is_symlink())

    def test_generated_symlink_refused_and_old_restored(self):
        target = self.root/'original.png'
        target.write_bytes(png())
        with patch.dict(os.environ, {'EXO_CAPTURE_SYMLINK_TARGET': str(target)}):
            self.assert_failed('symlink')
        self.assertEqual(target.read_bytes(), png())
        self.assertFalse(self.old.is_symlink())

    def test_missing_engine_fails_preserves_previous(self):
        self.engine.unlink()
        self.assert_failed('warning')

    def test_invalid_timeouts_never_launch(self):
        for value in (0, -1, float('nan'), float('inf')):
            with self.subTest(value=value), self.assertRaises(cv.CaptureError):
                self.run_capture('warning', timeout=value)
        self.assertFalse((self.root/'evidence/captures').exists())

    def test_cli_failure_never_prints_captured(self):
        with patch.object(cv, 'capture', side_effect=cv.CaptureError('fixture')):
            with patch('builtins.print') as out:
                self.assertEqual(cv.main(['--godot', str(self.engine)]), 1)
        self.assertFalse(any(str(call.args[0]).startswith('Captured:') for call in out.call_args_list))

    def test_unique_invocations_do_not_overwrite_previous_evidence(self):
        first = self.run_capture('warning')
        first_receipt = (first/'receipt.json').read_bytes()
        first_log = (first/'visual-run.log').read_bytes()
        second = self.run_capture('warning')
        self.assertNotEqual(first, second)
        self.assertEqual((first/'receipt.json').read_bytes(), first_receipt)
        self.assertEqual((first/'visual-run.log').read_bytes(), first_log)
        self.assertEqual((first/'runtime.png').read_bytes(), png())


class ContainerAndDisplayTests(unittest.TestCase):
    def test_png_crc_truncation_and_trailing_bytes_rejected(self):
        good = png()
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/'test.png'
            for payload in (good[:-4], good+b'extra', good[:45]+b'X'+good[46:], b''):
                with self.subTest(length=len(payload)):
                    path.write_bytes(payload)
                    with self.assertRaises(cv.CaptureError):
                        cv.png_metadata(path)

    def test_marker_must_be_an_exact_line(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/'test.png'; path.write_bytes(png())
            with self.assertRaises(cv.CaptureError):
                cv.validate_capture('not CAPTURE_SAVED\n', path, 0, 0)

    def test_display_readiness_timeout_stops_own_server(self):
        server = MagicMock(); server.poll.return_value = None
        with tempfile.TemporaryDirectory() as tmp, patch.object(cv.subprocess, 'Popen', return_value=server), patch.object(cv.socket, 'create_connection', side_effect=ConnectionRefusedError), patch.object(cv, 'stop_owned') as stop:
            with self.assertRaisesRegex(cv.CaptureError, 'readiness timeout'):
                with cv.virtual_display('fixture-xvfb', {}, Path(tmp)/'display.log', .001):
                    self.fail('display timeout was allowed through')
            stop.assert_called_once_with(server)

    def test_display_exit_is_rejected(self):
        server = MagicMock(); server.poll.return_value = 2
        with tempfile.TemporaryDirectory() as tmp, patch.object(cv.subprocess, 'Popen', return_value=server), patch.object(cv.socket, 'create_connection', side_effect=ConnectionRefusedError), patch.object(cv, 'stop_owned') as stop:
            with self.assertRaisesRegex(cv.CaptureError, 'exited'):
                with cv.virtual_display('fixture-xvfb', {}, Path(tmp)/'display.log', .1):
                    self.fail('dead display was allowed through')
            stop.assert_called_once_with(server)

    def test_occupied_display_is_never_started_or_killed(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(cv.socket, 'create_connection', return_value=MagicMock()), patch.object(cv.subprocess, 'Popen') as start, patch.object(cv, 'stop_owned') as stop:
            with self.assertRaisesRegex(cv.CaptureError, 'occupied'):
                with cv.virtual_display('fixture-xvfb', {}, Path(tmp)/'display.log', .1):
                    self.fail('occupied display was allowed through')
            start.assert_not_called()
            stop.assert_not_called()


if __name__ == '__main__':
    unittest.main()
