"""Aurora Veil macro terrain relief contract r14.

Applies or removes the deterministic low-frequency morphology used by remote Blender
revision 14. It does not invent lithology, microdetail, final biome masks or navmesh.
Validated with Blender 5.2.

Usage inside the Aurora scene:
    apply_relief(+1)   # r12-base -> r14 morphology
    apply_relief(-1)   # matching r14 morphology -> r12-base approximation

Do not use inverse mode after changing terrain topology or this formula version.
"""
import bpy
import math
from mathutils import Vector
from mathutils.bvhtree import BVHTree

CONTRACT = "AUR-TERRAIN-RELIEF-v2-r14"
TERRAIN = "AURORA_MACRO_TERRAIN"
FIELD_IDS = ["AUR-TMP-FIELD-A", "AUR-TMP-FIELD-B", "AUR-TMP-FIELD-C"]
CORRIDOR = [(-1600.0,350.0),(0.0,-50.0),(1650.0,250.0)]


def smooth01(t):
    t=max(0.0,min(1.0,t))
    return t*t*(3.0-2.0*t)


def region_weight(x,a,b,feather=450.0):
    return smooth01((x-(a-feather))/feather) * smooth01(((b+feather)-x)/feather)


def point_segment_distance(px,py,a,b):
    ax,ay=a; bx,by=b; vx=bx-ax; vy=by-ay; wx=px-ax; wy=py-ay
    den=vx*vx+vy*vy
    t=0.0 if den==0 else max(0.0,min(1.0,(wx*vx+wy*vy)/den))
    qx=ax+t*vx; qy=ay+t*vy
    return math.hypot(px-qx,py-qy)


def protection_factor(x,y):
    d=min(point_segment_distance(x,y,CORRIDOR[0],CORRIDOR[1]),
          point_segment_distance(x,y,CORRIDOR[1],CORRIDOR[2]))
    f=smooth01((d-120.0)/300.0)
    anchors=[((-1600.0,350.0),380.0),((1650.0,250.0),200.0),
             ((-430.0,-230.0),105.0),((50.0,60.0),105.0),((460.0,-170.0),105.0)]
    for (ax,ay),r in anchors:
        da=math.hypot(x-ax,y-ay)
        f=min(f,smooth01((da-r)/(r*1.3)))
    return f


def relief_delta(x,y):
    wc=region_weight(x,-2600.0,-800.0)
    wp=region_weight(x,-800.0,800.0)
    wo=region_weight(x,800.0,2600.0)

    camp=(30.0*math.exp(-((y-920.0)/500.0)**2)
          -14.0*math.exp(-((y+880.0)/480.0)**2)
          +7.0*math.sin((x+1700.0)/620.0)*math.cos(y/780.0))*wc

    plain=(4.8*math.sin((x+130.0)/390.0)*math.cos((y-50.0)/520.0)
           +2.2*math.sin(y/340.0))*wp

    r=math.hypot(x-1650.0,y-250.0)
    amph=25.0*(1.0-math.exp(-(r/720.0)**2))-3.5*math.exp(-(r/280.0)**2)
    east=13.0*math.exp(-((x-2350.0)/460.0)**2)*(0.75+0.25*math.cos(y/650.0))
    orchard=(amph+east+3.5*math.sin(y/620.0))*wo

    broad=2.5*math.sin(x/1100.0)*math.sin(y/850.0)
    return (camp+plain+orchard+broad)*protection_factor(x,y)


def terrain_bvh(terrain):
    dg=bpy.context.evaluated_depsgraph_get()
    eo=terrain.evaluated_get(dg)
    em=eo.to_mesh()
    verts=[eo.matrix_world @ v.co for v in em.vertices]
    polys=[list(p.vertices) for p in em.polygons]
    bvh=BVHTree.FromPolygons(verts,polys,all_triangles=False)
    return eo,em,bvh


def surface_z(bvh,x,y):
    hit=bvh.ray_cast(Vector((x,y,10000.0)),Vector((0,0,-1)),20000.0)[0]
    if hit is None:
        raise RuntimeError(f"No terrain hit at {x},{y}")
    return hit.z


def reground_temporal_fields(terrain):
    eo,em,bvh=terrain_bvh(terrain)
    prod=bpy.data.collections.get("18_TEMPORAL_PRODUCTION")
    fixes={}
    if prod:
        for fid in FIELD_IDS:
            root=bpy.data.objects.get(fid+"_ROOT")
            ring=bpy.data.objects.get(fid+"_IDLE_RING")
            if not root or not ring:
                continue
            tz=surface_z(bvh,root.location.x,root.location.y)
            desired=tz+0.28
            delta=desired-ring.location.z
            for o in prod.objects:
                if o.get("field_id")==fid and o is not root:
                    o.location.z += delta
            root["terrain_surface_z_m"]=tz
            root["visual_base_offset_m"]=0.28
            root["terrain_contact_revision"]=14
            fixes[fid]=delta
    eo.to_mesh_clear()
    return fixes


def apply_relief(sign=1):
    if sign not in (+1,-1):
        raise ValueError("sign must be +1 or -1")
    terrain=bpy.data.objects[TERRAIN]
    mesh=terrain.data
    inv=terrain.matrix_world.inverted()

    for v in mesh.vertices:
        w=terrain.matrix_world @ v.co
        nw=Vector((w.x,w.y,w.z + sign*relief_delta(w.x,w.y)))
        v.co=inv @ nw
    mesh.update()

    # Move surface-only authored root objects with the same relief field. Hero zones and temporal
    # fields are protection-masked, so their authored deltas are effectively zero before exact reground.
    surface_cols=["02_R01_CAMP","03_R02_PLAIN","04_R03_ORCHARD","05_TEMPORAL",
                  "06_ECO_PROXY","07_POP_PROXY","08_VEHICLE_PROXY","18_TEMPORAL_PRODUCTION"]
    seen=set()
    for cname in surface_cols:
        c=bpy.data.collections.get(cname)
        if not c: continue
        for o in c.objects:
            if o.name in seen or o is terrain or o.type in {"CAMERA","LIGHT"} or o.parent is not None:
                continue
            seen.add(o.name)
            w=o.matrix_world.translation
            d=sign*relief_delta(w.x,w.y)
            if abs(d)>1e-5:
                o.location.z += d

    # Exact contact repair for local temporal proof geometry.
    fixes=reground_temporal_fields(terrain)

    # Portable-export QA must remain metadata-only. Geometric debug guides are removed.
    qa=bpy.data.collections.get("21_TERRAIN_QA")
    if qa:
        for o in list(qa.objects):
            if o.type!="EMPTY":
                bpy.data.objects.remove(o,do_unlink=True)
        qa["export_contract"]="EMPTY_METADATA_ONLY_NO_GEOMETRY"
        qa["corridor_polyline"]="(-1600,350)->(0,-50)->(1650,250)"
        qa["corridor_core_m"]=120.0
        qa["corridor_feather_m"]=300.0

    if sign>0:
        terrain["terrain_relief_revision"]=14
        terrain["relief_contract"]=CONTRACT
        terrain["rollback_contract"]="DETERMINISTIC_INVERSE_RELIEF_V2; source persisted in repo"
        terrain["rollback_base_revision"]=12
        terrain["geology_status"]="MORPHOLOGY_PROPOSAL; lithology not canonized"
        terrain["microdetail_status"]="NOT_STARTED"
        bpy.context.scene["terrain_contract_version"]=CONTRACT
        bpy.context.scene["status"]="WAVE2_TERRAIN_RELIEF_R14_CONTACT_EXPORT_QA"
    else:
        terrain["terrain_relief_revision"]=12
        terrain["relief_contract"]="ROLLED_BACK_FROM_"+CONTRACT
        bpy.context.scene["status"]="TERRAIN_ROLLBACK_TO_R12_BASE_APPROX"

    return {"sign":sign,"temporal_contact_deltas":fixes,"status":bpy.context.scene.get("status")}


if __name__ == "__main__":
    print(apply_relief(+1))
