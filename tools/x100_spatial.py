#!/usr/bin/env python3
"""EXOVANT-X100 V2 spatial-semantic index.

Builds a deterministic 64-float vector per branch/claim from repository evidence.
Unknown physical coordinates remain explicitly unknown; zeroes never imply origin.
This is an awareness/retrieval projection, not a replacement for Fleet authority.
"""
from __future__ import annotations
from pathlib import Path
import argparse, hashlib, json, math, re, subprocess

ROOT=Path(__file__).resolve().parents[1]
DOMAIN_ORDER=[
    "macro","terrain","biome","architecture","interiors","infrastructure","props","materials",
    "vegetation","fauna","characters","vehicles","machinery","equipment","destruction","technical",
]
SCALE_ORDER=["L0","L1","L2","L3","L4","L5"]
STATUS_ORDER=["active","reserved","blocked","released","abandoned","unknown"]

def _json(path, default):
    p=Path(path)
    return json.loads(p.read_text()) if p.exists() else default

def worlds(root=ROOT):
    data=_json(Path(root)/"design/EXOVANT_DATA.json",{"worlds":[]})
    return [str(w["id"]).lower() for w in data.get("worlds",[])]

def normalize_domain(facet):
    s=str(facet or "").lower()
    synonyms={
        "macro-foundation":"macro","world-macro":"macro","environment":"biome",
        "structural-root-kit":"architecture","proxy-families":"props",
        "npc":"characters","character":"characters","vehicle":"vehicles",
        "collision":"technical","export":"technical","qa":"technical","lod":"technical",
    }
    for key,val in synonyms.items():
        if key in s:return val
    for d in DOMAIN_ORDER:
        if d in s:return d
    return "technical" if "art/" not in s and s else "macro"

def normalize_scale(text):
    s=str(text or "").upper()
    for x in SCALE_ORDER:
        if x in s:return x
    if "PLANET" in s or "ORBIT" in s:return "L0"
    if "REGION" in s:return "L1"
    if "DISTRICT" in s or "SETTLEMENT" in s:return "L2"
    if "ARCH" in s or "INTERIOR" in s:return "L3"
    if "PROP" in s or "ECO" in s:return "L4"
    if "MICRO" in s or "DETAIL" in s:return "L5"
    return None

def _hash_tail(tokens,n=17):
    out=[0.0]*n
    for token in sorted(set(str(x) for x in tokens if x)):
        h=hashlib.sha256(token.encode()).digest()
        bucket=int.from_bytes(h[:2],"big")%n
        sign=1.0 if h[2]&1 else -1.0
        out[bucket]+=sign
    norm=math.sqrt(sum(x*x for x in out)) or 1.0
    return [round(x/norm,6) for x in out]

def _spatial_features(spatial):
    if not spatial:
        return [0.0]*7
    center=spatial.get("center_m")
    extent=spatial.get("extent_m")
    if not (isinstance(center,list) and len(center)==3 and isinstance(extent,list) and len(extent)==3):
        return [0.0]*7
    vals=[]
    for v in center+extent:
        vals.append(round(math.tanh(float(v)/10000.0),6))
    return [1.0]+vals[:6]

def vectorize(entry, world_order):
    v=[]
    wid=str(entry.get("world") or "").lower()
    world_slots=list(world_order[:12])
    if len(world_slots)<12:
        world_slots += [None]*(12-len(world_slots))
    v.extend([1.0 if (w is not None and wid==w) else 0.0 for w in world_slots])
    scale=entry.get("scale")
    v.extend([1.0 if scale==s else 0.0 for s in SCALE_ORDER])
    domain=entry.get("domain")
    v.extend([1.0 if domain==d else 0.0 for d in DOMAIN_ORDER])
    status=entry.get("status","unknown")
    v.extend([1.0 if status==s else 0.0 for s in STATUS_ORDER])
    v.extend(_spatial_features(entry.get("spatial")))
    # 12 + 6 + 16 + 6 + 7 = 47; append 17 hashed semantic dims => 64
    tokens=[entry.get("branch"),entry.get("claim_id"),domain,scale,status]
    tokens += entry.get("paths",[]) + entry.get("asset_ids",[]) + entry.get("project_ids",[])
    v.extend(_hash_tail(tokens,17))
    if len(v)!=64:
        raise AssertionError(len(v))
    return v

def git_branches(root=ROOT):
    try:
        r=subprocess.run(
            ["git","for-each-ref","--format=%(refname:short)","refs/heads","refs/remotes/origin"],
            cwd=root,text=True,capture_output=True,check=True,timeout=10)
    except Exception:
        return []
    out=[]
    for line in r.stdout.splitlines():
        b=line.strip()
        if not b or b.endswith("/HEAD"):continue
        if b.startswith("origin/"):b=b[len("origin/"):]
        if b not in out:out.append(b)
    return sorted(out)

def infer_world(branch, world_order):
    slug=branch.lower().replace("_","-")
    matches=[w for w in world_order if re.search(r"(^|[/\-])"+re.escape(w)+r"([/\-]|$)",slug)]
    return matches[0] if len(matches)==1 else None

def build_index(root=ROOT, branch_snapshot=None):
    root=Path(root)
    world_order=worlds(root)
    fleet=_json(root/"ops/fleet/registry.json",{"claims":[]})
    entries=[]
    claimed_branches=set()
    for c in fleet.get("claims",[]):
        branch=c.get("branch")
        claimed_branches.add(branch)
        scopes=c.get("scopes",[])
        scope_worlds=sorted({str(s.get("world","")).lower() for s in scopes if s.get("world")})
        facets=[str(s.get("facet","")) for s in scopes]
        world=scope_worlds[0] if len(scope_worlds)==1 else None
        facet="|".join(facets)
        entry={
            "id":"claim:"+c["id"],
            "kind":"claim",
            "claim_id":c["id"],
            "branch":branch,
            "world":world,
            "domain":normalize_domain(facet),
            "scale":normalize_scale(facet),
            "status":c.get("status","unknown"),
            "owner":c.get("owner"),
            "epoch":c.get("epoch"),
            "paths":sorted(c.get("paths",[])),
            "asset_ids":sorted(c.get("asset_ids",[])),
            "project_ids":sorted(c.get("project_ids",[])),
            "spatial":c.get("spatial"),
            "epistemic":"FLEET_DOCUMENTED",
            "provenance":"ops/fleet/registry.json",
        }
        entry["vector"]=vectorize(entry,world_order)
        entries.append(entry)
    branches=branch_snapshot if branch_snapshot is not None else git_branches(root)
    for branch in sorted(set(branches)):
        if branch=="main" or branch in claimed_branches:continue
        world=infer_world(branch,world_order)
        entry={
            "id":"branch:"+branch,
            "kind":"branch_observation",
            "claim_id":None,
            "branch":branch,
            "world":world,
            "domain":"macro" if world else "technical",
            "scale":None,
            "status":"unknown",
            "owner":None,
            "epoch":None,
            "paths":[],
            "asset_ids":[],
            "project_ids":[],
            "spatial":None,
            "epistemic":"OBSERVED_BRANCH__SEMANTICS_INFERRED_FROM_NAME" if world else "OBSERVED_BRANCH_ONLY",
            "provenance":"git refs",
        }
        entry["vector"]=vectorize(entry,world_order)
        entries.append(entry)
    return {
        "schema_version":2,
        "protocol":"EXOVANT-X100-V2",
        "authority":"Projection only. Fleet registry/claims/branches remain authoritative.",
        "vector_contract":{"length":64,"unknown_spatial_is_not_origin":True},
        "world_order":world_order,
        "entries":sorted(entries,key=lambda e:e["id"]),
    }

def cosine(a,b):
    dot=sum(x*y for x,y in zip(a,b))
    na=math.sqrt(sum(x*x for x in a));nb=math.sqrt(sum(y*y for y in b))
    return 0.0 if not na or not nb else dot/(na*nb)

def spatial_overlap(a,b):
    sa=a.get("spatial");sb=b.get("spatial")
    if not sa or not sb:return None
    ca,ea=sa.get("center_m"),sa.get("extent_m")
    cb,eb=sb.get("center_m"),sb.get("extent_m")
    if not all(isinstance(x,list) and len(x)==3 for x in (ca,ea,cb,eb)):return None
    return all(abs(float(ca[i])-float(cb[i])) <= (float(ea[i])+float(eb[i]))/2 for i in range(3))

def nearest(index, entry_id, limit=10):
    by={e["id"]:e for e in index["entries"]}
    src=by[entry_id]
    rows=[]
    for e in index["entries"]:
        if e["id"]==entry_id:continue
        rows.append({
            "id":e["id"],"branch":e.get("branch"),"world":e.get("world"),
            "domain":e.get("domain"),"similarity":round(cosine(src["vector"],e["vector"]),6),
            "spatial_overlap":spatial_overlap(src,e),
            "epistemic":e.get("epistemic"),
        })
    return sorted(rows,key=lambda x:(-x["similarity"],x["id"]))[:limit]

def validate_index(index):
    errors=[]
    ids=[e["id"] for e in index.get("entries",[])]
    if len(ids)!=len(set(ids)):errors.append("duplicate entry IDs")
    for e in index.get("entries",[]):
        if len(e.get("vector",[]))!=64:errors.append("bad vector length:"+e.get("id","?"))
        if e.get("spatial") is None and any(e["vector"][40:47]):
            errors.append("unknown spatial encoded as known:"+e["id"])
    return errors

def _main(argv=None):
    p=argparse.ArgumentParser()
    sub=p.add_subparsers(dest="cmd",required=True)
    b=sub.add_parser("build");b.add_argument("--out",default="ops/x100/spatial-index.json")
    q=sub.add_parser("query");q.add_argument("entry_id");q.add_argument("--index",default="ops/x100/spatial-index.json");q.add_argument("--limit",type=int,default=10)
    v=sub.add_parser("validate");v.add_argument("--index",default="ops/x100/spatial-index.json")
    ns=p.parse_args(argv)
    if ns.cmd=="build":
        idx=build_index(ROOT);out=ROOT/ns.out;out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(idx,ensure_ascii=False,indent=2)+"\n")
        print(json.dumps({"entries":len(idx["entries"]),"errors":validate_index(idx)}));return 0 if not validate_index(idx) else 2
    idx=_json(ROOT/getattr(ns,"index"),{})
    if ns.cmd=="query":print(json.dumps(nearest(idx,ns.entry_id,ns.limit),ensure_ascii=False,indent=2));return 0
    errors=validate_index(idx);print(json.dumps({"errors":errors,"entries":len(idx.get("entries",[]))}));return 0 if not errors else 2

if __name__=="__main__":
    raise SystemExit(_main())
