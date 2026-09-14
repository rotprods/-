"""Apply SYLVA R16 macro-root load-correlated taper.

Input: accepted R15 scene.
Scope: ONLY six `SYLVA_ROOT_PRIMARY_R01..R06` Bezier point radius values plus
contract metadata. Control-point coordinates/endpoints, terrain, routes, collision,
streaming hierarchy and PR6 provider geometry are immutable in this wave.
"""
from __future__ import annotations

import bpy

CONTRACT = "SYLVA_MACRO_ROOT_TAPER_R16"
PROFILES = {
    "SYLVA_ROOT_PRIMARY_R01": {"anchor":"PUERTO@point2","radii":[0.75,0.95,1.32,1.05,0.82]},
    "SYLVA_ROOT_PRIMARY_R02": {"anchor":"BOSQUE@point2","radii":[0.72,0.92,1.30,1.02,0.78]},
    "SYLVA_ROOT_PRIMARY_R03": {"anchor":"VESPER@point2","radii":[0.70,0.90,1.34,1.04,0.80]},
    "SYLVA_ROOT_PRIMARY_R04": {"anchor":"NETWORK_JUNCTION_MIDSPAN","radii":[0.78,0.92,1.18,1.08,0.82]},
    "SYLVA_ROOT_PRIMARY_R05": {"anchor":"NETWORK_JUNCTION_MIDSPAN","radii":[0.75,0.92,1.20,1.10,0.82]},
    "SYLVA_ROOT_PRIMARY_R06": {"anchor":"VESPER_APPROACH@point4","radii":[0.70,0.82,0.94,1.08,1.28]},
}

def main():
    root = bpy.data.objects.get("SYLVA_WORLD_ROOT")
    if not root or root.get("build_status") != "WAVE1M_PREFETCH_POLICY_NORMALIZATION_R15":
        raise RuntimeError("Expected accepted R15 input")
    if root.get("macro_root_biomech_contract"):
        raise RuntimeError("Macro-root biomech contract already present")

    changed=[]
    for name,spec in PROFILES.items():
        obj=bpy.data.objects.get(name)
        if obj is None or obj.type!='CURVE' or len(obj.data.splines)!=1:
            raise RuntimeError("Missing/invalid root: "+name)
        spline=obj.data.splines[0]
        if spline.type!='BEZIER' or len(spline.bezier_points)!=5:
            raise RuntimeError("R16 requires 5-point Bezier root: "+name)
        before=[[float(p.co.x),float(p.co.y),float(p.co.z)] for p in spline.bezier_points]
        for p,radius in zip(spline.bezier_points,spec['radii']):
            p.radius=float(radius)
        after=[[float(p.co.x),float(p.co.y),float(p.co.z)] for p in spline.bezier_points]
        if before!=after:
            raise RuntimeError("Control-point coordinate drift: "+name)
        obj["macro_root_biomech_contract"]=CONTRACT
        obj["macro_root_load_anchor"]=spec['anchor']
        obj["macro_root_radius_profile"]="|".join(f"{v:.3f}" for v in spec['radii'])
        obj["macro_root_cross_section_status"]="CIRCULAR_PROXY_FINAL_SECTION_PENDING"
        obj["macro_root_centerline_locked"] = True
        changed.append(name)

    root["macro_root_biomech_contract"] = CONTRACT
    root["macro_root_cross_section_status"] = "CIRCULAR_PROXY_FINAL_SECTION_PENDING"
    root["build_status"] = "WAVE1N_MACRO_ROOT_BIOMECH_R16"
    bpy.context.view_layer.update()
    bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
    return {
        "status":"R16_MACRO_ROOT_TAPER_APPLIED",
        "contract":CONTRACT,
        "roots_updated":changed,
        "geometry_centerlines_changed":False,
        "cross_section_status":"CIRCULAR_PROXY_FINAL_SECTION_PENDING"
    }

if __name__ == "__main__":
    print(main())
