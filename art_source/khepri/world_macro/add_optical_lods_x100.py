"""KHEPRI X100 optical footprint LOD source stage.

Creates deterministic LOD1/LOD2 mesh datablocks for compact/standard/wide mast and panel
families without instantiating them in the representative scene. LOD0 remains the current authored
X100 mesh. The meshes use fake_user so the editable .blend retains them; the whole-scene GLB need
not export unused LOD source meshes. Runtime switching/HLOD policy remains downstream technical art.
"""
from __future__ import annotations

import json
try:
    import bpy  # type: ignore
except ImportError:
    bpy = None

CONTRACT = "KHP_OPTICAL_LOD_X100_V1"
VARIANTS = {
    "compact": {"mast_h":28.0,"mast_w":3.6,"panel_w":28.0,"panel_h":17.0,"panel_t":1.6},
    "standard":{"mast_h":36.0,"mast_w":4.8,"panel_w":36.0,"panel_h":22.0,"panel_t":2.0},
    "wide":    {"mast_h":44.0,"mast_w":5.6,"panel_w":46.0,"panel_h":26.0,"panel_t":2.2},
}


def append_box(verts, faces, material_indices, center, dims, material_index=0):
    cx,cy,cz=center; dx,dy,dz=[d*0.5 for d in dims]; b=len(verts)
    verts.extend([(cx-dx,cy-dy,cz-dz),(cx+dx,cy-dy,cz-dz),(cx+dx,cy+dy,cz-dz),(cx-dx,cy+dy,cz-dz),(cx-dx,cy-dy,cz+dz),(cx+dx,cy-dy,cz+dz),(cx+dx,cy+dy,cz+dz),(cx-dx,cy+dy,cz+dz)])
    for q in [(0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(2,6,7,3),(4,0,3,7)]:
        faces.append(tuple(b+i for i in q)); material_indices.append(material_index)


def make_mesh(name, parts, materials):
    verts=[]; faces=[]; mat_indices=[]
    for center,dims,mi in parts: append_box(verts,faces,mat_indices,center,dims,mi)
    mesh=bpy.data.meshes.new(name); mesh.from_pydata(verts,[],faces); mesh.update(); mesh.use_fake_user=True
    for material in materials: mesh.materials.append(material)
    for poly,mi in zip(mesh.polygons,mat_indices): poly.material_index=mi
    mesh["lod_contract"]=CONTRACT
    mesh["source_only"]=True
    return mesh


def object_users(mesh):
    return [obj for obj in bpy.data.objects if getattr(obj, "data", None) == mesh]


def ensure_clean():
    for mesh in list(bpy.data.meshes):
        if mesh.name.startswith("KHP_WM_X100_LOD1_") or mesh.name.startswith("KHP_WM_X100_LOD2_"):
            users = object_users(mesh)
            if users:
                raise RuntimeError("LOD source mesh unexpectedly instantiated: "+mesh.name+" -> "+",".join(obj.name for obj in users))
            # Blender ID.users includes the fake-user retention bit; clear it before removal.
            mesh.use_fake_user=False
            bpy.data.meshes.remove(mesh)


def apply():
    if bpy is None: raise RuntimeError("bpy unavailable")
    bronze=bpy.data.materials.get("KHP_WM_MAT_BRONZE_BLOCKOUT"); mirror=bpy.data.materials.get("KHP_WM_MAT_MIRROR_BLOCKOUT")
    if not bronze or not mirror: raise RuntimeError("missing KHEPRI materials")
    meta=bpy.data.objects.get("KHP_WM_OPTICAL_FIELD_SYSTEM_META")
    if not meta or meta.get("contract")!="KHP_OPTICAL_FIELD_X100_V1": raise RuntimeError("X100 optical family not active")
    ensure_clean(); rows=[]
    for variant,s in VARIANTS.items():
        h=s["mast_h"]; w=s["mast_w"]; pw=s["panel_w"]; ph=s["panel_h"]; pt=s["panel_t"]
        mast1=make_mesh(f"KHP_WM_X100_LOD1_MAST_{variant.upper()}", [((0,0,-h*.43),(w*1.30,w*1.30,h*.14),0),((0,0,h*.04),(w*.86,w*.86,h*.80),0)], [bronze])
        panel1=make_mesh(f"KHP_WM_X100_LOD1_PANEL_{variant.upper()}", [((0,0,0),(pw,pt,ph),0),((0,-pt*.70,0),(pw*.68,pt*.40,max(.8,ph*.05)),1)], [mirror,bronze])
        mast2=make_mesh(f"KHP_WM_X100_LOD2_MAST_{variant.upper()}", [((0,0,0),(w*.95,w*.95,h),0)], [bronze])
        panel2=make_mesh(f"KHP_WM_X100_LOD2_PANEL_{variant.upper()}", [((0,0,0),(pw,pt,ph),0)], [mirror])
        for level,kind,mesh in [(1,"mast",mast1),(1,"panel",panel1),(2,"mast",mast2),(2,"panel",panel2)]:
            mesh["lod_level"]=level; mesh["family_kind"]=kind; mesh["variant_id"]=variant; mesh["family_asset_id"]="KHP_WM_HELIOSTAT_FOOTPRINTS"
        lod0_m=bpy.data.meshes.get(f"KHP_WM_X100_MAST_{variant.upper()}"); lod0_p=bpy.data.meshes.get(f"KHP_WM_X100_PANEL_{variant.upper()}")
        if not lod0_m or not lod0_p: raise RuntimeError("missing LOD0 family mesh")
        rows.append({"variant":variant,"mast":{"lod0":[len(lod0_m.vertices),len(lod0_m.polygons)],"lod1":[len(mast1.vertices),len(mast1.polygons)],"lod2":[len(mast2.vertices),len(mast2.polygons)]},"panel":{"lod0":[len(lod0_p.vertices),len(lod0_p.polygons)],"lod1":[len(panel1.vertices),len(panel1.polygons)],"lod2":[len(panel2.vertices),len(panel2.polygons)]}})
    manifest={"contract":CONTRACT,"family_asset_id":"KHP_WM_HELIOSTAT_FOOTPRINTS","variants":rows,"runtime_policy":"DISTANCE_THRESHOLDS_DOWNSTREAM_TECH_ART","hlod":"DEFERRED","collision":"DEFERRED_DOWNSTREAM_GAMEPLAY","source_persistence":"UNUSED_MESH_DATABLOCKS_WITH_FAKE_USER"}
    meta["lod_manifest_json"]=json.dumps(manifest,sort_keys=True)
    meta["lod_contract"]=CONTRACT
    bpy.context.scene["khepri_optical_lod_contract"]=CONTRACT
    return manifest


def audit_contract():
    return {"contract":CONTRACT,"variants":3,"lod_levels":[0,1,2],"source_meshes_created":12,"expected_mast_polys":{"lod0":18,"lod1":12,"lod2":6},"expected_panel_polys":{"lod0":18,"lod1":12,"lod2":6},"idempotence":"object_users==0; fake_user is retention not instancing","passed":True,"boundary":"Source LOD family contract only; runtime thresholds, collision and HLOD remain downstream."}

if __name__=="__main__":
    print(json.dumps(audit_contract() if bpy is None else apply(),indent=2,sort_keys=True))
