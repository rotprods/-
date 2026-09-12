"""Optional Linux CPU-render capture. Requires Xvfb, xkbcomp and Mesa."""
from pathlib import Path
import argparse
import os
import secrets
import socket
import struct
import subprocess
import tempfile
import time

p = argparse.ArgumentParser()
p.add_argument("--godot", required=True)
p.add_argument("--xvfb", default="Xvfb")
p.add_argument("--xlibs", default="")
args = p.parse_args()
root = Path(__file__).resolve().parents[1]
env = os.environ.copy()
if args.xlibs:
    env["LD_LIBRARY_PATH"] = str(Path(args.xlibs).resolve())
display = 100 + os.getpid() % 400
env["DISPLAY"] = f"127.0.0.1:{display}"
env["LIBGL_ALWAYS_SOFTWARE"] = "1"
with tempfile.TemporaryDirectory(prefix="exovant-display-") as tmp:
    auth = Path(tmp) / "authority"
    fields = [b"", str(display).encode(), b"MIT-MAGIC-COOKIE-1", secrets.token_bytes(16)]
    auth.write_bytes(struct.pack(">H", 65535) + b"".join(struct.pack(">H",len(x))+x for x in fields))
    auth.chmod(0o600)
    env["XAUTHORITY"] = str(auth)
    with (root/"evidence/display.log").open("w") as log:
        server = subprocess.Popen([args.xvfb, f":{display}", "-screen", "0", "1280x720x24", "-nolisten", "unix", "-nolisten", "local", "-listen", "tcp", "-auth", str(auth)], env=env, stdout=log, stderr=log)
        try:
            for _ in range(50):
                if server.poll() is not None:
                    raise RuntimeError("Virtual display failed; inspect evidence/display.log")
                try:
                    with socket.create_connection(("127.0.0.1",6000+display),.1):
                        break
                except OSError:
                    time.sleep(.1)
            with (root/"evidence/visual-run.log").open("w") as out:
                run = subprocess.run([str(Path(args.godot).resolve()), "--path", str(root), "--rendering-method", "gl_compatibility", "--audio-driver", "Dummy", "--", "--capture"],env=env,stdout=out,stderr=out,timeout=90)
            if run.returncode:
                raise RuntimeError("Render failed; inspect evidence/visual-run.log")
            print("Captured:", root/"evidence/runtime.png")
        finally:
            server.terminate()
            server.wait(timeout=5)
