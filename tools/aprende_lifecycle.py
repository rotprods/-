from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from aprende_runtime import AprendeError, LearningHub, _canonical_json, _now, validate_component

CHAT_ID_SOURCES = {"platform", "user-supplied", "session-alias"}
RECEIPT_KINDS = {"BOOTSTRAP", "CLOSE", "HANDOFF"}
LEARNING_OUTCOMES = {"not-evaluated", "no-promotable-learning", "learning-persisted"}


def _digest(value):
    return hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def _semantic_receipt(value):
    return {k: v for k, v in value.items() if k not in {"receipt_digest", "timestamp"}}


def _validate_source(value):
    if value not in CHAT_ID_SOURCES:
        raise AprendeError("invalid chat_id_source")
    return value


class SessionLifecycle:
    def __init__(self, root):
        self.root = Path(root)
        self.hub = LearningHub(root)

    def receipt_path(self, agent_id, chat_id):
        agent = validate_component(agent_id, "agent_id")
        chat = validate_component(chat_id, "chat_id")
        return self.root / "agents" / agent / "chats" / chat / "session-events.jsonl"

    def _rows(self, agent_id, chat_id):
        path = self.receipt_path(agent_id, chat_id)
        if not path.exists():
            return []
        rows = []
        for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except Exception as ex:
                raise AprendeError(f"invalid session receipt JSON line {line_no}: {ex}") from ex
            rows.append(row)
        return rows

    def _append(self, receipt):
        path = self.receipt_path(receipt["agent_id"], receipt["chat_id"])
        path.parent.mkdir(parents=True, exist_ok=True)
        receipt = dict(receipt)
        rows = self._rows(receipt["agent_id"], receipt["chat_id"])
        identity = (receipt["run_id"], receipt["kind"])
        for old in rows:
            if (old.get("run_id"), old.get("kind")) != identity:
                continue
            if _digest(_semantic_receipt(old)) == _digest(_semantic_receipt(receipt)):
                return path
            raise AprendeError("conflicting duplicate session receipt")
        receipt["receipt_digest"] = _digest({k: v for k, v in receipt.items() if k != "receipt_digest"})
        with path.open("a", encoding="utf-8") as handle:
            handle.write(_canonical_json(receipt) + "\n")
        return path

    def _validate_identity(self, agent_id, chat_id, chat_id_source, run_id, parent_agent_id=None):
        validate_component(agent_id, "agent_id")
        validate_component(chat_id, "chat_id")
        validate_component(run_id, "run_id")
        _validate_source(chat_id_source)
        if parent_agent_id is not None:
            validate_component(parent_agent_id, "parent_agent_id")

    def _learning_exists(self, learning_id):
        validate_component(learning_id, "learning_id")
        for _, event in self.hub.iter_events():
            if event.get("learning_id") == learning_id:
                return True
        return False

    def bootstrap(self, agent_id, chat_id, chat_id_source, run_id, query=None, parent_agent_id=None):
        self._validate_identity(agent_id, chat_id, chat_id_source, run_id, parent_agent_id)
        problems = self.hub.audit()
        if problems:
            raise AprendeError("learning hub audit failed: " + "; ".join(problems))
        hits = self.hub.retrieve(query) if query else []
        receipt = {
            "kind": "BOOTSTRAP",
            "timestamp": _now(),
            "agent_id": agent_id,
            "chat_id": chat_id,
            "chat_id_source": chat_id_source,
            "run_id": run_id,
            "parent_agent_id": parent_agent_id,
            "query": query,
            "retrieved_learning_ids": [hit["learning_id"] for hit in hits],
            "learning_outcome": "not-evaluated",
            "handoff_ref": None,
        }
        return self._append(receipt), hits

    def close(self, agent_id, chat_id, chat_id_source, run_id, learning_ids=None, handoff_ref=None,
              parent_agent_id=None, outcome=None):
        self._validate_identity(agent_id, chat_id, chat_id_source, run_id, parent_agent_id)
        rows = self._rows(agent_id, chat_id)
        bootstraps = [r for r in rows if r.get("run_id") == run_id and r.get("kind") == "BOOTSTRAP"]
        if not bootstraps:
            raise AprendeError("close requires prior bootstrap receipt")
        bootstrap = bootstraps[0]
        if bootstrap.get("chat_id_source") != chat_id_source or bootstrap.get("parent_agent_id") != parent_agent_id:
            raise AprendeError("close provenance differs from bootstrap")
        ids = list(learning_ids or [])
        if len(ids) != len(set(ids)):
            raise AprendeError("duplicate learning reference")
        missing = [learning_id for learning_id in ids if not self._learning_exists(learning_id)]
        if missing:
            raise AprendeError("unknown learning reference: " + ",".join(missing))
        expected_outcome = "learning-persisted" if ids else "no-promotable-learning"
        if outcome is not None and outcome != expected_outcome:
            raise AprendeError("learning_outcome conflicts with learning references")
        receipt = {
            "kind": "CLOSE",
            "timestamp": _now(),
            "agent_id": agent_id,
            "chat_id": chat_id,
            "chat_id_source": chat_id_source,
            "run_id": run_id,
            "parent_agent_id": parent_agent_id,
            "query": None,
            "retrieved_learning_ids": [],
            "learning_outcome": expected_outcome,
            "learning_ids": ids,
            "handoff_ref": handoff_ref,
        }
        return self._append(receipt)

    def handoff(self, agent_id, chat_id, chat_id_source, run_id, handoff_ref, learning_ids=None,
                parent_agent_id=None):
        self._validate_identity(agent_id, chat_id, chat_id_source, run_id, parent_agent_id)
        if not isinstance(handoff_ref, str) or not handoff_ref.strip():
            raise AprendeError("handoff_ref required")
        rows = self._rows(agent_id, chat_id)
        closes = [r for r in rows if r.get("run_id") == run_id and r.get("kind") == "CLOSE"]
        if not closes:
            raise AprendeError("handoff requires terminal close receipt")
        ids = list(learning_ids or closes[0].get("learning_ids", []))
        missing = [learning_id for learning_id in ids if not self._learning_exists(learning_id)]
        if missing:
            raise AprendeError("unknown learning reference: " + ",".join(missing))
        receipt = {
            "kind": "HANDOFF",
            "timestamp": _now(),
            "agent_id": agent_id,
            "chat_id": chat_id,
            "chat_id_source": chat_id_source,
            "run_id": run_id,
            "parent_agent_id": parent_agent_id,
            "query": None,
            "retrieved_learning_ids": [],
            "learning_outcome": closes[0].get("learning_outcome", "not-evaluated"),
            "learning_ids": ids,
            "handoff_ref": handoff_ref,
        }
        return self._append(receipt)

    def audit_receipts(self):
        problems = []
        for path in sorted((self.root / "agents").glob("*/chats/*/session-events.jsonl")):
            agent_id = path.parents[2].name
            chat_id = path.parent.name
            seen = set()
            try:
                rows = self._rows(agent_id, chat_id)
            except AprendeError as ex:
                problems.append(f"{path}: {ex}")
                continue
            for row in rows:
                try:
                    self._validate_identity(
                        row.get("agent_id"), row.get("chat_id"), row.get("chat_id_source"),
                        row.get("run_id"), row.get("parent_agent_id")
                    )
                except Exception as ex:
                    problems.append(f"{path}: {ex}")
                    continue
                if row.get("agent_id") != agent_id or row.get("chat_id") != chat_id:
                    problems.append(f"session path/provenance mismatch {path}")
                if row.get("kind") not in RECEIPT_KINDS:
                    problems.append(f"invalid receipt kind {path}")
                if row.get("learning_outcome") not in LEARNING_OUTCOMES:
                    problems.append(f"invalid learning outcome {path}")
                clean = {k: v for k, v in row.items() if k != "receipt_digest"}
                if row.get("receipt_digest") != _digest(clean):
                    problems.append(f"receipt digest mismatch {path}")
                ident = (row.get("run_id"), row.get("kind"))
                if ident in seen:
                    problems.append(f"duplicate lifecycle phase {ident}")
                seen.add(ident)
                for learning_id in row.get("learning_ids", []):
                    if not self._learning_exists(learning_id):
                        problems.append(f"unknown learning ref {learning_id}")
            run_ids = {r.get("run_id") for r in rows}
            for run_id in run_ids:
                run_rows = [r for r in rows if r.get("run_id") == run_id]
                kinds = {r.get("kind") for r in run_rows}
                if ("CLOSE" in kinds or "HANDOFF" in kinds) and "BOOTSTRAP" not in kinds:
                    problems.append(f"terminal lifecycle without bootstrap {run_id}")
                if "HANDOFF" in kinds and "CLOSE" not in kinds:
                    problems.append(f"handoff without close {run_id}")
        return problems


def main(argv=None):
    parser = argparse.ArgumentParser(prog="aprende-lifecycle")
    sub = parser.add_subparsers(dest="cmd", required=True)
    audit = sub.add_parser("audit")
    audit.add_argument("root")
    boot = sub.add_parser("bootstrap")
    boot.add_argument("root")
    boot.add_argument("agent_id")
    boot.add_argument("chat_id")
    boot.add_argument("chat_id_source")
    boot.add_argument("run_id")
    boot.add_argument("--query")
    close = sub.add_parser("close")
    close.add_argument("root")
    close.add_argument("agent_id")
    close.add_argument("chat_id")
    close.add_argument("chat_id_source")
    close.add_argument("run_id")
    close.add_argument("--learning-id", action="append", default=[])
    args = parser.parse_args(argv)
    lifecycle = SessionLifecycle(args.root)
    if args.cmd == "audit":
        problems = lifecycle.audit_receipts()
        if problems:
            for problem in problems:
                print("FAIL", problem)
            return 1
        print("OK session lifecycle audit")
        return 0
    if args.cmd == "bootstrap":
        path, hits = lifecycle.bootstrap(args.agent_id, args.chat_id, args.chat_id_source, args.run_id, args.query)
        print(json.dumps({"receipt": str(path), "hits": hits}, ensure_ascii=False, indent=2))
        return 0
    if args.cmd == "close":
        path = lifecycle.close(args.agent_id, args.chat_id, args.chat_id_source, args.run_id, args.learning_id)
        print(json.dumps({"receipt": str(path)}, ensure_ascii=False, indent=2))
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

