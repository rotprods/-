"""Run the project-native gates; fail on missing receipts or runtime script errors."""
from pathlib import Path
import argparse
import json
import re
import subprocess
import sys
import datetime
import time

parser = argparse.ArgumentParser()
parser.add_argument("--godot", required=True, help="Godot 4.7.2 executable")
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root / 'tools'))
from project_control import source_digest
from tool_ledger import record
run_id = 'native-' + datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
engine = str(Path(args.godot).expanduser().resolve())
evidence = root / "evidence"
evidence.mkdir(exist_ok=True)
commands = [
    ("import", ["--headless", "--editor", "--path", str(root), "--import"]),
    ("state-tests", ["--headless", "--path", str(root), "--script", "tests/test_state.gd"]),
    ("world-tests", ["--headless", "--path", str(root), "--script", "tests/test_world.gd", "--", "--test-world"]),
    ("input-tests", ["--headless", "--path", str(root), "--script", "tests/test_input.gd", "--", "--test-input"]),
    ("smoke", ["--headless", "--path", str(root), "--quit-after", "120"]),
]
results = []
for name, command in commands:
    started = time.monotonic()
    # A receipt from a previous run cannot make this run pass.
    receipt = evidence / f"{name}.json"
    if receipt.exists():
        receipt.unlink()
    try:
        run = subprocess.run([engine, *command], cwd=root, capture_output=True, text=True, timeout=120)
        log = run.stdout + run.stderr
        (evidence / f"{name}.log").write_text(log)
        ok = run.returncode == 0 and not re.search(r"SCRIPT ERROR:|^ERROR:|^FAIL ", log, re.M)
        if name in ("state-tests", "world-tests", "input-tests"):
            ok = ok and receipt.exists() and json.loads(receipt.read_text()).get("failed") == 0
        results.append({"gate": name, "passed": bool(ok), "exit_code": run.returncode})
        record(root / 'telemetry/tool_calls.jsonl', tool='godot.' + name, run_id=run_id, status='returned' if run.returncode == 0 else 'error', duration_ms=round((time.monotonic()-started)*1000), task_outcome='verified_success' if ok else 'verified_failure')
    except subprocess.TimeoutExpired:
        results.append({"gate": name, "passed": False, "reason": "timeout"})
        record(root / 'telemetry/tool_calls.jsonl', tool='godot.' + name, run_id=run_id, status='timeout', duration_ms=round((time.monotonic()-started)*1000), task_outcome='verified_failure')
    print(json.dumps(results[-1]))
    if not results[-1]["passed"]:
        break
(evidence / "gauntlet.json").write_text(json.dumps({"run_id":run_id,"executed_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),"source_digest":source_digest(root),"gates": results, "passed": len(results)==len(commands) and all(x["passed"] for x in results)}, indent=2))
sys.exit(0 if len(results)==len(commands) and all(x["passed"] for x in results) else 1)
