from __future__ import annotations
import argparse
import hashlib
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

AUTH = {
    "L0-recollection": 0,
    "L1-retrieved": 1,
    "L2-persisted": 2,
    "L3-verified": 3,
    "L4-enforced": 4,
    "L5-proven-in-use": 5,
}
EVENT_CLASSES = {
    "failure","success","correction","incident","review-finding","workflow-pattern",
    "tool-routing","authority-defect","persistence-defect","security-defect","performance-pattern"
}
STATUSES = {
    "observed","evidence-pending","evidenced","analyzed","candidate","persisted","verified",
    "enforced","proven-in-use","rejected","duplicate","conflicted","superseded","stale",
    "revalidation-required","observed-no-promotable-learning"
}
EVIDENCE_KINDS = {
    "runtime","test","repository","log","source-file","issue","pull-request","review",
    "conversation","external-primary","external-secondary"
}
RELATIONS = {"NEW","DUPLICATE","EXTENDS","CONTRADICTS","SUPERSEDES","REVALIDATES"}
TARGET_TYPES = {
    "none","test","invariant","guardrail","linter","prompt","skill","routing-rule","adr",
    "playbook","state-rule","benchmark","eval","runbook","security-control","graph"
}
CHECK_STATUSES = {"not-applicable","pending","pass","fail","refused"}
TERMINAL_BAD = {"rejected", "conflicted", "stale", "revalidation-required"}
ID_RE = re.compile(r"^LRN-[A-Za-z0-9._:-]+$")
SAFE_COMPONENT_RE = re.compile(r"^[A-Za-z0-9._:-]+$")

class AprendeError(Exception):
    pass

def _now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

def _canonical_json(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))

def _pretty_json(obj):
    return json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n"

def event_digest(event):
    return hashlib.sha256(_canonical_json(event).encode("utf-8")).hexdigest()

def validate_component(value, field):
    if not isinstance(value, str) or not value or not SAFE_COMPONENT_RE.fullmatch(value):
        raise AprendeError(f"unsafe {field}")
    if value in {".", ".."}:
        raise AprendeError(f"unsafe {field}")
    return value

def validate_event(event):
    required = [
        "learning_id","timestamp","event_class","status","scope","authority_before",
        "authority_after","evidence","analysis","knowledge_relation","promotion",
        "verification","unknowns","provenance"
    ]
    missing = [k for k in required if k not in event]
    if missing:
        raise AprendeError("missing: " + ",".join(missing))
    if not isinstance(event["learning_id"], str) or not ID_RE.fullmatch(event["learning_id"]):
        raise AprendeError("invalid learning_id")
    if event["event_class"] not in EVENT_CLASSES:
        raise AprendeError("invalid event_class")
    if event["status"] not in STATUSES:
        raise AprendeError("invalid status")
    if event["authority_before"] not in AUTH or event["authority_after"] not in AUTH:
        raise AprendeError("invalid authority")
    if AUTH[event["authority_after"]] < AUTH[event["authority_before"]] and event["status"] not in {"stale","revalidation-required","superseded"}:
        raise AprendeError("authority regression without demotion state")

    if not isinstance(event["evidence"], list) or not event["evidence"]:
        raise AprendeError("evidence required")
    for evidence in event["evidence"]:
        if not isinstance(evidence, dict) or evidence.get("kind") not in EVIDENCE_KINDS:
            raise AprendeError("invalid evidence kind")
        if not isinstance(evidence.get("ref"), str) or not evidence["ref"].strip():
            raise AprendeError("invalid evidence ref")
        if not isinstance(evidence.get("claim"), str) or not evidence["claim"].strip():
            raise AprendeError("invalid evidence claim")

    relation = event.get("knowledge_relation", {}).get("relation")
    if relation not in RELATIONS:
        raise AprendeError("invalid knowledge relation")

    promotion = event.get("promotion", {})
    if promotion.get("target_type") not in TARGET_TYPES:
        raise AprendeError("invalid promotion target_type")
    if promotion.get("target_type") != "none" and not promotion.get("target_ref"):
        raise AprendeError("promotion target_ref required")

    if not isinstance(event.get("provenance"), dict):
        raise AprendeError("invalid provenance")
    prov = event["provenance"]
    for k in ("agent_id","chat_id","chat_id_source"):
        if k not in prov:
            raise AprendeError("missing provenance." + k)
    validate_component(prov["agent_id"], "agent_id")
    validate_component(prov["chat_id"], "chat_id")
    if prov["chat_id_source"] not in {"platform","user-supplied","session-alias"}:
        raise AprendeError("invalid chat_id_source")

    v = event["verification"]
    for k in ("retrieval_test","runtime_test","adversarial_review"):
        if k not in v or not isinstance(v[k], dict) or "status" not in v[k]:
            raise AprendeError("verification incomplete")
        if v[k]["status"] not in CHECK_STATUSES:
            raise AprendeError("invalid verification status")

    if AUTH[event["authority_after"]] >= 3:
        if v["retrieval_test"]["status"] != "pass":
            raise AprendeError("L3+ requires retrieval pass")
        if v["adversarial_review"]["status"] != "pass":
            raise AprendeError("L3+ requires adversarial pass")
    if AUTH[event["authority_after"]] >= 4:
        if not v.get("anti_recurrence_control"):
            raise AprendeError("L4+ requires anti recurrence control")
        if v["runtime_test"]["status"] != "pass":
            raise AprendeError("L4+ requires runtime pass")
    if event["status"] in TERMINAL_BAD and AUTH[event["authority_after"]] >= 4:
        raise AprendeError("bad terminal state cannot self-certify L4+")
    return True

class LearningHub:
    def __init__(self, root):
        self.root = Path(root)
        self.events_root = self.root / "agents"
        self.index_root = self.root / "index"
        self.graph_root = self.root / "graph"
        for p in (self.events_root, self.index_root, self.graph_root):
            p.mkdir(parents=True, exist_ok=True)

    def event_path(self, event):
        p = event["provenance"]
        agent = validate_component(p["agent_id"], "agent_id")
        chat = validate_component(p["chat_id"], "chat_id")
        lid = validate_component(event["learning_id"], "learning_id")
        return self.events_root / agent / "chats" / chat / "events" / f"{lid}.json"

    def persist(self, event):
        validate_event(event)
        path = self.event_path(event)
        path.parent.mkdir(parents=True, exist_ok=True)
        digest = event_digest(event)
        if path.exists():
            old = json.loads(path.read_text(encoding="utf-8"))
            if old.get("_meta", {}).get("content_digest") == digest:
                return path
            raise AprendeError("append-only violation: learning_id already exists with different content")

        payload = dict(event)
        payload["_meta"] = {"persisted_at": _now(), "content_digest": digest}
        tmp = path.with_suffix(".json.tmp")
        tmp.write_text(_pretty_json(payload), encoding="utf-8")
        os.replace(tmp, path)
        self.rebuild_projections()
        return path

    def iter_events(self):
        for p in sorted(self.events_root.glob("*/chats/*/events/*.json")):
            try:
                yield p, json.loads(p.read_text(encoding="utf-8"))
            except Exception as ex:
                raise AprendeError(f"invalid event JSON {p}: {ex}") from ex

    def expected_projections(self):
        ledger_rows = []
        by_agent, by_chat, by_class = {}, {}, {}
        graph = []
        for path, e in self.iter_events():
            rel = str(path.relative_to(self.root))
            p = e["provenance"]
            ledger_rows.append({
                "learning_id": e["learning_id"],
                "path": rel,
                "digest": e.get("_meta", {}).get("content_digest"),
                "timestamp": e["timestamp"],
            })
            by_agent.setdefault(p["agent_id"], []).append(rel)
            by_chat.setdefault(p["chat_id"], []).append(rel)
            by_class.setdefault(e["event_class"], []).append(rel)
            graph += [
                {"from": e["learning_id"], "type": "OCCURRED_IN_CHAT", "to": p["chat_id"]},
                {"from": e["learning_id"], "type": "EXECUTED_BY", "to": p["agent_id"]},
            ]
            for ev in e.get("evidence", []):
                graph.append({"from": e["learning_id"], "type": "EVIDENCED_BY", "to": ev["ref"]})
            fam = e.get("analysis", {}).get("family_or_pattern")
            if fam:
                graph.append({"from": e["learning_id"], "type": "INSTANCE_OF", "to": fam})
        return ledger_rows, by_agent, by_chat, by_class, graph

    def rebuild_projections(self):
        rows, by_agent, by_chat, by_class, graph = self.expected_projections()
        (self.root/"events.jsonl").write_text("".join(_canonical_json(r)+"\n" for r in rows), encoding="utf-8")
        for name, data in [("by-agent.json",by_agent),("by-chat.json",by_chat),("by-class.json",by_class)]:
            (self.index_root/name).write_text(_pretty_json(data), encoding="utf-8")
        (self.graph_root/"edges.json").write_text(_pretty_json(graph), encoding="utf-8")

    def retrieve(self, query):
        if not isinstance(query, str) or not query.strip():
            raise AprendeError("query must be non-empty")
        q = query.casefold()
        hits = []
        for path, e in self.iter_events():
            if q in _canonical_json(e).casefold():
                hits.append({
                    "learning_id": e["learning_id"],
                    "path": str(path.relative_to(self.root)),
                    "authority": e["authority_after"],
                    "status": e["status"],
                    "agent_id": e["provenance"]["agent_id"],
                    "chat_id": e["provenance"]["chat_id"],
                    "chat_id_source": e["provenance"]["chat_id_source"],
                })
        return hits

    def audit(self):
        problems = []
        seen = set()
        try:
            events = list(self.iter_events())
        except AprendeError as ex:
            return [str(ex)]

        for path, e in events:
            clean = {k: v for k, v in e.items() if k != "_meta"}
            try:
                validate_event(clean)
            except Exception as ex:
                problems.append(f"{path}: {ex}")
                continue

            expected_path = self.event_path(clean)
            if expected_path.resolve() != path.resolve():
                problems.append(f"path/provenance mismatch {clean['learning_id']}")
            lid = clean["learning_id"]
            if lid in seen:
                problems.append(f"duplicate event id {lid}")
            seen.add(lid)

            meta = e.get("_meta", {})
            if meta.get("content_digest") != event_digest(clean):
                problems.append(f"digest mismatch {lid}")

        rows, by_agent, by_chat, by_class, graph = self.expected_projections()
        expected_ledger = "".join(_canonical_json(r)+"\n" for r in rows)
        ledger_path = self.root/"events.jsonl"
        actual_ledger = ledger_path.read_text(encoding="utf-8") if ledger_path.exists() else ""
        if actual_ledger != expected_ledger:
            problems.append("events.jsonl projection drift")

        expected_files = {
            self.index_root/"by-agent.json": _pretty_json(by_agent),
            self.index_root/"by-chat.json": _pretty_json(by_chat),
            self.index_root/"by-class.json": _pretty_json(by_class),
            self.graph_root/"edges.json": _pretty_json(graph),
        }
        for path, expected in expected_files.items():
            actual = path.read_text(encoding="utf-8") if path.exists() else ""
            if actual != expected:
                problems.append(f"projection drift {path.relative_to(self.root)}")
        return problems

def main(argv=None):
    parser = argparse.ArgumentParser(prog="aprende-runtime")
    sub = parser.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("audit"); a.add_argument("root")
    r = sub.add_parser("retrieve"); r.add_argument("root"); r.add_argument("query")
    b = sub.add_parser("rebuild-projections"); b.add_argument("root")
    args = parser.parse_args(argv)
    hub = LearningHub(args.root)
    if args.cmd == "audit":
        problems = hub.audit()
        if problems:
            for x in problems:
                print("FAIL", x)
            return 1
        print("OK learning hub audit")
        return 0
    if args.cmd == "retrieve":
        print(json.dumps(hub.retrieve(args.query), ensure_ascii=False, indent=2))
        return 0
    if args.cmd == "rebuild-projections":
        hub.rebuild_projections()
        print("OK projections rebuilt")
        return 0

if __name__ == "__main__":
    raise SystemExit(main())

