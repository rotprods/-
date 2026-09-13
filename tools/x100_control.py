#!/usr/bin/env python3
"""EXOVANT-X100 V2 deterministic density optimizer.

Pure-Python/no external deps. This module does not claim assets or mutate Fleet.
It ranks evidence-backed production gaps after ownership has been resolved.
"""
from __future__ import annotations
from pathlib import Path
import argparse, json, math, sys

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "ops/x100/config.json"

class X100Error(ValueError):
    pass

def load_json(path):
    return json.loads(Path(path).read_text())

def load_config(path=DEFAULT_CONFIG):
    cfg = load_json(path)
    validate_config(cfg)
    return cfg

def validate_config(cfg):
    dims = cfg.get("dimensions", {})
    if not dims:
        raise X100Error("dimensions missing")
    if abs(sum(float(v) for v in dims.values()) - 1.0) > 1e-9:
        raise X100Error("dimension weights must sum to 1")
    bad = [k for k,v in dims.items() if float(v) <= 0]
    if bad:
        raise X100Error("non-positive dimension weights: " + ",".join(bad))
    for k in cfg.get("critical_dimensions", []):
        if k not in dims:
            raise X100Error(f"unknown critical dimension {k}")
    target = cfg.get("hero_support_systemic_target", {})
    if abs(sum(float(v) for v in target.values()) - 1.0) > 1e-9:
        raise X100Error("hero/support/systemic target must sum to 1")
    return True

def _coverage_values(coverage, cfg):
    dims = cfg["dimensions"]
    missing = [d for d in dims if d not in coverage]
    if missing:
        raise X100Error("coverage missing dimensions: " + ",".join(missing))
    vals = {}
    for d in dims:
        v = coverage[d]
        if v is None:
            raise X100Error(f"coverage unmeasured: {d}")
        v = float(v)
        if not (0.0 <= v <= 1.0):
            raise X100Error(f"coverage {d} outside [0,1]")
        vals[d] = v
    return vals

def world_completeness(coverage, cfg):
    """Weighted geometric mean. Any exact zero dimension makes score zero."""
    vals = _coverage_values(coverage, cfg)
    if any(vals[d] == 0.0 for d in cfg["critical_dimensions"]):
        return 0.0
    log_sum = 0.0
    for d,w in cfg["dimensions"].items():
        v = vals[d]
        if v == 0.0:
            return 0.0
        log_sum += float(w) * math.log(v)
    return math.exp(log_sum)

def effective_weights(coverage, cfg):
    vals = _coverage_values(coverage, cfg)
    g = cfg["gradient"]
    lam = float(g["bottleneck_lambda"])
    power = float(g["bottleneck_power"])
    raw = {}
    for d, base in cfg["dimensions"].items():
        deficit = 1.0 - vals[d]
        raw[d] = float(base) * (1.0 + lam * (deficit ** power))
    total = sum(raw.values())
    return {d: raw[d]/total for d in raw}

def gradient_pressure(coverage, cfg):
    """Normalized log-gradient pressure d(log G)/dc_i ~= w_i/max(eps,c_i)."""
    vals = _coverage_values(coverage, cfg)
    eff = effective_weights(coverage, cfg)
    eps = float(cfg["gradient"]["epsilon"])
    raw = {d: eff[d] / max(eps, vals[d]) for d in eff}
    total = sum(raw.values()) or 1.0
    return {d: raw[d]/total for d in raw}

POSITIVE_FACTORS = (
    "critical_path","dependency_unlock","player_visibility","reuse_value",
    "art_importance","systemic_yield","gameplay_value","evidence_confidence",
    "image_grounding_bonus",
)
NEGATIVE_FACTORS = ("collision_risk","unresolved_dependency","slop_risk","technical_cost")

def score_candidate(candidate, coverage, cfg):
    dim = candidate["dimension"]
    if dim not in cfg["dimensions"]:
        raise X100Error(f"candidate {candidate.get('id')} unknown dimension {dim}")
    delta = float(candidate.get("expected_delta", 0.0))
    if delta < 0:
        raise X100Error("expected_delta must be >= 0")
    pressure = gradient_pressure(coverage, cfg)[dim]
    cw = cfg["candidate_weights"]
    score = pressure * delta * float(cw["marginal_gain"])
    for f in POSITIVE_FACTORS:
        score += float(candidate.get(f, 0.0)) * float(cw[f])
    for f in NEGATIVE_FACTORS:
        score -= float(candidate.get(f, 0.0)) * float(cw[f])
    if candidate.get("claimed_by_other"):
        score -= 1e6
    if candidate.get("blocked_irreversible"):
        score -= 1e5
    return score

def rank_candidates(candidates, coverage, cfg):
    rows = []
    for c in candidates:
        row = dict(c)
        row["x100_score"] = round(score_candidate(c, coverage, cfg), 8)
        rows.append(row)
    return sorted(rows, key=lambda x:(-x["x100_score"], str(x.get("id",""))))

def family_combinations(family):
    keys = ("size_variants","regional_variants","material_states","temporal_states","gameplay_states","configurations")
    total = 1
    for k in keys:
        v = int(family.get(k, 1))
        if v < 1:
            raise X100Error(f"{k} must be >=1")
        total *= v
    return total

def family_grade(family, cfg):
    n = family_combinations(family)
    t = cfg["kit_thresholds"]
    if n <= int(t["poor_max"]): grade="poor"
    elif n <= int(t["acceptable_max"]): grade="acceptable"
    elif n <= int(t["strong_max"]): grade="strong"
    else: grade="production_grade"
    return {"combinations":n,"grade":grade}

REQUIRED_FAMILY_FIELDS = (
    "stable_id","semantic_purpose","dimensions_validated","player_scale_validated",
    "silhouette_pass","manufacturing_logic_pass","uv0","material_slots","pivot",
    "transforms_clean","collision_strategy","gameplay_clearance","lod_strategy",
    "variants","state_variants","optimization","engine_import","visual_qa",
    "technical_qa","receipt","source_persisted","export_persisted","claim_handoff_updated"
)

def validate_family(family):
    missing=[k for k in REQUIRED_FAMILY_FIELDS if k not in family]
    if missing:
        return ["missing:"+k for k in missing]
    failures=[]
    for k in REQUIRED_FAMILY_FIELDS:
        v=family[k]
        if isinstance(v,bool) and not v:
            failures.append("false:"+k)
        elif v in (None,"",[],{}):
            failures.append("empty:"+k)
    if family.get("raw_ai_mesh_final") is True:
        failures.append("raw_ai_mesh_final_forbidden")
    return failures

def stage_for_score(score_pct, cfg):
    s=float(score_pct)
    for name,(lo,hi) in cfg["thresholds"].items():
        if float(lo) <= s < float(hi) or (name=="release_candidate" and s <= float(hi)):
            return name
    return "unknown"

def audit_world(doc, cfg):
    coverage=doc.get("coverage",{})
    try:
        score=world_completeness(coverage,cfg)
        pressure=gradient_pressure(coverage,cfg)
        measured=True
    except X100Error as e:
        return {"world_id":doc.get("world_id"),"measured":False,"error":str(e),"status":"MEASUREMENT_REQUIRED"}
    scale=doc.get("scale_coverage",{})
    missing_scales=[x for x in cfg["scale_levels"] if not scale.get(x,False)]
    result={
        "world_id":doc.get("world_id"),
        "measured":measured,
        "world_completeness":round(score*100,4),
        "stage":stage_for_score(score*100,cfg),
        "gradient_pressure":{k:round(v,6) for k,v in pressure.items()},
        "missing_scales":missing_scales,
        "world_density_gate": not missing_scales and score>=0.65,
    }
    return result

def _main(argv=None):
    p=argparse.ArgumentParser(prog="x100_control.py")
    p.add_argument("--config", default=str(DEFAULT_CONFIG))
    sub=p.add_subparsers(dest="cmd",required=True)
    sub.add_parser("validate-config")
    a=sub.add_parser("audit");a.add_argument("world_json")
    r=sub.add_parser("rank");r.add_argument("world_json");r.add_argument("candidates_json")
    f=sub.add_parser("family");f.add_argument("family_json")
    ns=p.parse_args(argv)
    cfg=load_config(ns.config)
    if ns.cmd=="validate-config":
        out={"ok":True,"protocol":cfg["protocol_id"],"weight_sum":sum(cfg["dimensions"].values())}
    elif ns.cmd=="audit":
        out=audit_world(load_json(ns.world_json),cfg)
    elif ns.cmd=="rank":
        world=load_json(ns.world_json);cands=load_json(ns.candidates_json)
        out=rank_candidates(cands,world["coverage"],cfg)
    elif ns.cmd=="family":
        fam=load_json(ns.family_json);out={"grade":family_grade(fam,cfg),"failures":validate_family(fam)}
    print(json.dumps(out,ensure_ascii=False,indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(_main())
