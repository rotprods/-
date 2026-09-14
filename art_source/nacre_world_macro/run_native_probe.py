"""Run the isolated NACRE R5 Godot import gate against an exact GLB.

Usage:
  python3 art_source/nacre_world_macro/run_native_probe.py \
    --godot .tools/Godot_v4.7.2-stable_linux.x86_64 \
    --glb /path/to/exact/nacre-r5.glb \
    --out evidence/nacre-r5-native

This wrapper does not download anything and never substitutes another asset. It copies the
provided GLB into a temporary standalone Godot project, performs an editor import, runs the
GDScript assertions, and writes a fleet-compatible native-receipt.json plus logs.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent
PROBE_TEMPLATE = ROOT / "native_probe"
ASSET_NAME = "nacre_r5.glb"
RECEIPT_PREFIX = "NACRE_NATIVE_RECEIPT="


def sha256_file(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def run(cmd: list[str], cwd: pathlib.Path, log_path: pathlib.Path, timeout: int) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        cmd,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        timeout=timeout,
        check=False,
    )
    log_path.write_text(result.stdout, encoding="utf-8")
    return result


def extract_probe_receipt(text: str) -> dict:
    for line in reversed(text.splitlines()):
        if line.startswith(RECEIPT_PREFIX):
            return json.loads(line[len(RECEIPT_PREFIX):])
    raise ValueError("probe output did not contain NACRE_NATIVE_RECEIPT")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--godot", required=True, type=pathlib.Path)
    parser.add_argument("--glb", required=True, type=pathlib.Path)
    parser.add_argument("--out", required=True, type=pathlib.Path)
    parser.add_argument("--timeout", type=int, default=180)
    args = parser.parse_args()

    godot = args.godot.resolve()
    glb = args.glb.resolve()
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)

    if not godot.is_file():
        raise SystemExit(f"Godot executable not found: {godot}")
    if not glb.is_file():
        raise SystemExit(f"GLB not found: {glb}")
    if glb.stat().st_size < 20 or glb.read_bytes()[:4] != b"glTF":
        raise SystemExit("input is not a GLB 2.x container (missing glTF magic)")

    asset_sha = sha256_file(glb)
    version = subprocess.run(
        [str(godot), "--version"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        timeout=30,
        check=False,
    ).stdout.strip()

    executed_at = dt.datetime.now(dt.timezone.utc).isoformat()
    with tempfile.TemporaryDirectory(prefix="nacre-r5-native-") as tmp:
        project = pathlib.Path(tmp)
        shutil.copy2(PROBE_TEMPLATE / "project.godot", project / "project.godot")
        shutil.copy2(PROBE_TEMPLATE / "probe.gd", project / "probe.gd")
        shutil.copy2(glb, project / ASSET_NAME)

        import_log = out / "godot-import.log"
        probe_log = out / "godot-probe.log"
        import_result = run(
            [str(godot), "--headless", "--path", str(project), "--editor", "--import", "--quit-after", "3"],
            project,
            import_log,
            args.timeout,
        )

        import_text = import_result.stdout
        import_error_markers = [line for line in import_text.splitlines() if "ERROR" in line.upper() or "SCRIPT ERROR" in line.upper()]
        probe_result = run(
            [str(godot), "--headless", "--path", str(project), "--script", "res://probe.gd"],
            project,
            probe_log,
            args.timeout,
        )

        receipt_error = None
        probe_receipt: dict = {}
        try:
            probe_receipt = extract_probe_receipt(probe_result.stdout)
        except Exception as exc:
            receipt_error = str(exc)

        passed = (
            import_result.returncode == 0
            and not import_error_markers
            and probe_result.returncode == 0
            and receipt_error is None
            and bool(probe_receipt.get("passed"))
        )

        receipt = {
            "passed": passed,
            "artifact_sha256": asset_sha,
            "artifact_bytes": glb.stat().st_size,
            "executed_at": executed_at,
            "engine": version or "Godot version unavailable",
            "claim_id": "CLM-NACRE-WORLD-MACRO-001",
            "checkpoint": "NACRE-R5-NATIVE",
            "import_returncode": import_result.returncode,
            "probe_returncode": probe_result.returncode,
            "import_error_markers": import_error_markers,
            "probe_receipt": probe_receipt,
            "receipt_parse_error": receipt_error,
            "evidence_refs": [str(import_log), str(probe_log)],
        }
        receipt_path = out / "native-receipt.json"
        receipt_path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(receipt_path)
        return 0 if passed else 2


if __name__ == "__main__":
    sys.exit(main())
