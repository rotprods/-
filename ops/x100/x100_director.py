#!/usr/bin/env python3
"""EXOVANT-X100 V2 global density director.

Aggregates claim/world evidence receipts into a conservative 84-cell world-density matrix.
Fleet remains authority for ownership. This tool never claims or mutates assets.
"""
from __future__ import annotations
from pathlib import Path
import argparse, json, math

DIMENSION_CELLS = {
    "macro_world": ["planetary_representation","atmosphere_climate","geology_hydrology","regional_layout","transport_network","landmarks_vistas"],
    "meso_architecture": ["settlement_logic","residential","civic_commercial","industrial","interiors","utilities_infrastructure"],
    "micro_assets": ["props","machinery","tools_equipment","cultural_objects","microgeometry","decals_residue"],
    "ecology": ["flora","fauna","food_chain","habitats","world_impacts","seasonal_health_states"],
    "civilization": ["manufacturing","construction","domestic_life","culture_ritual","mobility","repair_maintenance"],
    "gameplay": ["traversal","combat","puzzle","interaction","cover_readability","destruction_state_change"],
    "material_causality": ["material_families","manufacturing_response","wear","weathering","damage","repair"],
    "variation": ["size","regional","material","temporal","gameplay","configuration"],
    "temporal_states": ["era_0_original","era_1_modification","era_2_current","pristine","used","damaged_abandoned"],
    "storytelling": ["current_state","past_state","damage_evidence","repair_evidence","abandonment_adaptation","cultural_clues"],
    "audiovisual_language": ["lighting","weather_atmosphere","soundscape","motifs","distant_vistas","local_fx"],
    "optimization": ["lod","hlod_impostor","collision","streaming","instancing_drawcalls","performance_profile"],
    "reusability": ["modular_kits","procedural_generators","placement_rules","snapping_interfaces","shared_materials","prefab_assemblies"],
    "qa": ["canon","art","realism","geometry_uv_material","engine_runtime","visual_regression_human"],
}

MATURITY = {
    "unknown": 0.0,
    "planned": 0.05,
    "implemented": 0.20,
    "locally_validated": 0.40,
    "systemic_complete": 0.55,
    "empirically_qualified": 0.65,
    "human_approved": 0.82,
    "production_complete": 0.95,
    "released": 1.0,
}

class DirectorError(ValueError): pass

def load(path): return json.loads(Path(path).read_text())

def validate_receipt(r):
    required=("receipt_id","world_id","claim_id","branch","evidence")
    missing=[k for k in required if not r.get(k)]
    if missing: raise DirectorError("receipt missing: "+",".join(missing))
    seen=set()
    for row in r["evidence"]:
        d=row.get("dimension");c=row.get("cell");m=row.get("maturity","unknown")
        if d not in DIMENSION_CELLS: raise DirectorError(f"unknown dimension {d}")
        if c not in DIMENSION_CELLS[d]: raise DirectorError(f"unknown cell {d}/{c}")
        if m not in MATURITY: raise DirectorError(f"unknown maturity {m}")
        key=(d,c)
        if key in seen: raise DirectorError(f"duplicate cell in receipt {d}/{c}")
        seen.add(key)
        if m != "unknown" and not row.get("evidence_refs"):
            raise DirectorError(f"evidence refs required for {d}/{c}")
    return True

def empty_world(world_id):
    return {
        "world_id":world_id,
        "cells":{d:{c:{"maturity":"unknown","score":0.0,"receipts":[]} for c in cells} for d,cells in DIMENSION_CELLS.items()},
        "receipts":[],
    }

def aggregate(world_ids, receipts):
    worlds={w:empty_world(w) for w in world_ids}
    for r in receipts:
        validate_receipt(r)
        w=r["world_id"]
        if w not in worlds: raise DirectorError(f"receipt world not in catalog: {w}")
        worlds[w]["receipts"].append(r["receipt_id"])
        for e in r["evidence"]:
            cell=worlds[w]["cells"][e["dimension"]][e["cell"]]
            score=MATURITY[e["maturity"]]
            if score > cell["score"]:
                cell["score"]=score;cell["maturity"]=e["maturity"]
            cell["receipts"].append({"receipt_id":r["receipt_id"],"claim_id":r["claim_id"],"branch":r["branch"],"maturity":e["maturity"],"evidence_refs":e.get("evidence_refs",[])})
    return worlds

def coverage_from_cells(world):
    return {d: sum(c["score"] for c in cells.values())/len(cells) for d,cells in world["cells"].items()}

def geometric_score(coverage, weights, critical):
    if any(coverage.get(d,0.0) <= 0 for d in critical): return 0.0
    if any(coverage.get(d,0.0) <= 0 for d in weights): return 0.0
    return math.exp(sum(weights[d]*math.log(coverage[d]) for d in weights))

def pressure(coverage, weights, eps=.025, lam=1.5, power=2.0):
    eff={d:weights[d]*(1+lam*((1-coverage.get(d,0))**power)) for d in weights};tot=sum(eff.values()) or 1
    eff={d:v/tot for d,v in eff.items()};raw={d:eff[d]/max(eps,coverage.get(d,0)) for d in eff};rt=sum(raw.values()) or 1
    return {d:raw[d]/rt for d in raw}

def known_geomean(coverage, weights):
    known={d:v for d,v in coverage.items() if v>0}
    if not known:return 0.0
    tw=sum(weights[d] for d in known)
    return math.exp(sum((weights[d]/tw)*math.log(known[d]) for d in known))

def summarize(worlds, cfg):
    weights=cfg["dimensions"];critical=cfg["critical_dimensions"];rows=[]
    for wid,w in worlds.items():
        cov=coverage_from_cells(w);score=geometric_score(cov,weights,critical);known=known_geomean(cov,weights);prs=pressure(cov,weights,cfg["gradient"]["epsilon"],cfg["gradient"]["bottleneck_lambda"],cfg["gradient"]["bottleneck_power"])
        missing=sum(1 for d in w["cells"].values() for c in d.values() if c["score"]==0)
        per_dim_unknown={d:sum(1 for c in cells.values() if c["score"]==0) for d,cells in w["cells"].items()}
        bottleneck_cells=[]
        for d in sorted(weights,key=lambda x:(-prs[x],x)):
            for c,cell in w["cells"][d].items():
                if cell["score"]==0:bottleneck_cells.append({"dimension":d,"cell":c,"pressure":round(prs[d],6)})
                if len(bottleneck_cells)>=12:break
            if len(bottleneck_cells)>=12:break
        rows.append({"world_id":wid,"strict_score_pct":round(score*100,4),"known_evidence_geomean_pct":round(known*100,4),"evidence_cell_coverage_pct":round((84-missing)/84*100,4),"measured_cells":84-missing,"unknown_cells":missing,"unknown_cells_by_dimension":per_dim_unknown,"coverage":{k:round(v,4) for k,v in cov.items()},"top_pressure":sorted(({"dimension":d,"pressure":round(v,6)} for d,v in prs.items()),key=lambda x:(-x["pressure"],x["dimension"]))[:5],"bottleneck_cells":bottleneck_cells,"receipt_count":len(w["receipts"])})
    return sorted(rows,key=lambda r:(r["strict_score_pct"],-r["unknown_cells"],r["world_id"]))

def candidate_queue(summary, fleet):
    claimed={}
    for c in fleet.get("claims",[]):
        for s in c.get("scopes",[]):
            w=str(s.get("world","")).lower();claimed.setdefault(w,[]).append({"claim_id":c.get("id"),"status":c.get("status"),"facet":s.get("facet"),"owner":c.get("owner")})
    q=[]
    for row in summary:
        existing=claimed.get(row["world_id"],[])
        for p in row["top_pressure"]:
            q.append({"world_id":row["world_id"],"dimension":p["dimension"],"gradient_pressure":p["pressure"],"world_score_pct":row["strict_score_pct"],"unknown_cells":row["unknown_cells"],"existing_claims":existing,"requires_fleet_preflight":True})
    return sorted(q,key=lambda x:(-x["gradient_pressure"],x["world_score_pct"],x["world_id"],x["dimension"]))

POSITIVE=("critical_path","dependency_unlock","player_visibility","reuse_value","art_importance","systemic_yield","gameplay_value","evidence_confidence","image_grounding_bonus")
NEGATIVE=("collision_risk","unresolved_dependency","slop_risk","technical_cost")

def rank_portfolio(opportunities, worlds, cfg):
    by_summary={r["world_id"]:r for r in summarize(worlds,cfg)}
    cw=cfg.get("candidate_weights",{})
    rows=[]
    for o in opportunities:
        w=o["world_id"];d=o["dimension"]
        if w not in worlds: raise DirectorError(f"opportunity world unknown: {w}")
        if d not in DIMENSION_CELLS: raise DirectorError(f"opportunity dimension unknown: {d}")
        cov=coverage_from_cells(worlds[w]);prs=pressure(cov,cfg["dimensions"],cfg["gradient"]["epsilon"],cfg["gradient"]["bottleneck_lambda"],cfg["gradient"]["bottleneck_power"])
        score=prs[d]*float(o.get("expected_delta",0))*float(cw.get("marginal_gain",4.0))
        for f in POSITIVE: score += float(o.get(f,0))*float(cw.get(f,0))
        for f in NEGATIVE: score -= float(o.get(f,0))*float(cw.get(f,0))
        if o.get("claimed_by_other"): score-=1e6
        if o.get("blocked_irreversible"): score-=1e5
        row=dict(o);row.update({"gradient_pressure":round(prs[d],6),"portfolio_score":round(score,8),"world_strict_score_pct":by_summary[w]["strict_score_pct"],"world_known_evidence_pct":by_summary[w]["known_evidence_geomean_pct"],"fleet_preflight_required":True})
        rows.append(row)
    return sorted(rows,key=lambda x:(-x["portfolio_score"],x["world_id"],x.get("id","")))

def build_baseline(catalog, cfg, receipts, fleet, opportunities=None):
    world_ids=[str(w["id"]).lower() for w in catalog.get("worlds",[])]
    worlds=aggregate(world_ids,receipts);summary=summarize(worlds,cfg)
    return {"schema_version":1,"protocol":"EXOVANT-X100-V2","authority":"Derived lower-bound from evidence receipts. Fleet remains ownership authority; unknown cells remain unknown.","world_count":len(world_ids),"cell_contract":{"dimensions":len(DIMENSION_CELLS),"cells_per_dimension":6,"cells_per_world":84,"maturity_scores":MATURITY},"summary":summary,"candidate_queue":candidate_queue(summary,fleet),"portfolio_rank":rank_portfolio(opportunities or [],worlds,cfg),"worlds":worlds}

def _main(argv=None):
    p=argparse.ArgumentParser();p.add_argument("--catalog",required=True);p.add_argument("--config",required=True);p.add_argument("--fleet",required=True);p.add_argument("--receipts-dir");p.add_argument("--receipts-file");p.add_argument("--opportunities");p.add_argument("--out",required=True);ns=p.parse_args(argv)
    receipts=[]
    if ns.receipts_dir:
        for f in sorted(Path(ns.receipts_dir).glob("*.json")): receipts.append(load(f))
    if ns.receipts_file:
        data=load(ns.receipts_file);receipts.extend(data if isinstance(data,list) else data.get("receipts",[]))
    if not receipts:
        raise DirectorError("no evidence receipts supplied")
    opps=load(ns.opportunities) if ns.opportunities else [];out=build_baseline(load(ns.catalog),load(ns.config),receipts,load(ns.fleet),opps);Path(ns.out).write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n");print(json.dumps({"worlds":out["world_count"],"receipts":len(receipts),"queue":len(out["candidate_queue"])}));return 0

if __name__=="__main__": raise SystemExit(_main())
