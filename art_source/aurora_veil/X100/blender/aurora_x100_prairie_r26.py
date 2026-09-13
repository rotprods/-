"""Aurora Veil / EXOVANT-X100 — Hierba de dos sombras systemic prairie.

Workunit: AUR-X100-PRAIRIE-ECO-001
Validated remote revision: 26 / Blender 5.2.
Canonical species: Hierba de dos sombras. This generator never invents a new species.

The multiplier is intra-specific morphology + deterministic ecological placement:
- juvenile, mature-short, mature-tall, trampled-path, senescent, temporal-edge;
- six authored patches covering all three bounded echo fields, two route contexts
  and one control/background context;
- LOD1/LOD2 blend-only meshes rebuilt from LOD0 blade groups while preserving
  exact X/Y/Z patch envelope;
- no per-blade collision;
- extra offset ground-shadow evidence only near bounded temporal fields.

Final texture/card/impostor strategy, engine vegetation switching and measured
performance remain blocked by EXO-012 / target hardware and are not claimed here.
"""
import bpy
import math
import random
from collections import Counter
from mathutils import Vector
from mathutils.bvhtree import BVHTree

WORKUNIT = "AUR-X100-PRAIRIE-ECO-001"
ROOT = "AURORA_VEIL_ROOT"
PATCH_COLLECTION = "30_X100_PRAIRIE_PATCHES"
SHADOW_COLLECTION = "31_X100_PRAIRIE_SHADOWS"
QA_COLLECTION = "32_X100_PRAIRIE_QA"
PATCH_CENTERS = [(-520,-140),(50,155),(550,-170),(-300,25),(300,5),(0,420)]
PATCH_RADIUS = 94.0
SPACING = 12.0
FIELDS = [(-430.0,-230.0,1.0,"AUR-TMP-FIELD-A"),(50.0,60.0,1.4,"AUR-TMP-FIELD-B"),(460.0,-170.0,1.8,"AUR-TMP-FIELD-C")]
ROUTE = [Vector((-1600,350)),Vector((0,-50)),Vector((1650,250))]
MORPH = {
    "JUVENILE": {"height":(.20,.34), "blades":(3,4), "lean":(.02,.10), "width":(.012,.021), "cause":"growth stage"},
    "MATURE_SHORT": {"height":(.42,.60), "blades":(4,5), "lean":(.03,.12), "width":(.014,.025), "cause":"growth/competition state"},
    "MATURE_TALL": {"height":(.68,.96), "blades":(5,6), "lean":(.05,.18), "width":(.015,.028), "cause":"mature low-disturbance growth"},
    "TRAMPLED_PATH": {"height":(.15,.28), "blades":(3,5), "lean":(.35,.75), "width":(.014,.026), "cause":"repeated traversal contact"},
    "SENESCENT": {"height":(.40,.72), "blades":(2,4), "lean":(.08,.24), "width":(.012,.023), "cause":"age/senescence"},
    "TEMPORAL_EDGE": {"height":(.50,.82), "blades":(4,6), "lean":(.04,.15), "width":(.014,.027), "cause":"bounded local temporal-offset habitat cue"},
}


def ensure_collection(name, root):
    c = bpy.data.collections.get(name)
    if c is None:
        c = bpy.data.collections.new(name)
        root.children.link(c)
    return c


def clear_collection(c):
    for obj in list(c.objects):
        bpy.data.objects.remove(obj, do_unlink=True)


def terrain_bvh():
    terrain = bpy.data.objects["AURORA_MACRO_TERRAIN"]
    return BVHTree.FromObject(terrain, bpy.context.evaluated_depsgraph_get())


def ground_sampler(bvh):
    def sample(x, y):
        hit = bvh.ray_cast(Vector((x,y,1000)), Vector((0,0,-1)), 2000)[0]
        if not hit:
            raise RuntimeError(f"No terrain at {x}, {y}")
        return hit.z
    return sample


def segment_distance(x, y, a, b):
    p = Vector((x,y)); d = b-a
    t = max(0.0, min(1.0, (p-a).dot(d) / max(d.length_squared, 1e-8)))
    return (p-(a+d*t)).length


def route_distance(x, y):
    return min(segment_distance(x,y,ROUTE[i],ROUTE[i+1]) for i in range(2))


def field_info(x, y):
    return min([(math.hypot(x-fx,y-fy), delay, field_id) for fx,fy,delay,field_id in FIELDS], key=lambda row: row[0])


def material(name, base, roughness):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*base, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = 0.0
    return m


def materials():
    grass = bpy.data.materials.get("M_AUR_TWO_SHADOW_GRASS") or material("M_AUR_TWO_SHADOW_GRASS", (0.075,0.16,0.09), .78)
    sen = material("AUR_X100_MAT_GRASS_SENESCENT", (0.19,0.18,0.10), .88)
    shadow = material("AUR_X100_MAT_TEMPORAL_SECOND_SHADOW", (0.008,0.012,0.018), .96)
    bsdf = shadow.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Alpha"].default_value = .36
    try: shadow.surface_render_method = "DITHERED"
    except Exception: pass
    return grass, sen, shadow


def stellar_shadow_direction():
    sun = bpy.data.objects.get("SUN_VELAR_LOW")
    d = (sun.matrix_world.to_quaternion() @ Vector((0,0,-1))) if sun else Vector((1,0,-1))
    v = Vector((d.x,d.y))
    return v.normalized() if v.length > 1e-5 else Vector((1,0))


def add_blade(vertices, faces, material_indices, x, y, z, height, width, yaw, lean, material_index):
    side = Vector((math.cos(yaw), math.sin(yaw))) * width * 0.5
    lean_v = Vector((math.cos(yaw+1.1), math.sin(yaw+1.1))) * lean
    i = len(vertices)
    vertices += [
        (x-side.x,y-side.y,z), (x+side.x,y+side.y,z),
        (x+side.x+lean_v.x,y+side.y+lean_v.y,z+height),
        (x-side.x+lean_v.x,y-side.y+lean_v.y,z+height),
    ]
    faces += [(i,i+1,i+2),(i,i+2,i+3)]
    material_indices += [material_index, material_index]


def build_lod0_mesh(name, tufts, grass, sen):
    vertices=[]; faces=[]; material_indices=[]
    for tuft in tufts:
        count=tuft["blades"]
        for blade_index in range(count):
            yaw=tuft["yaw"] + blade_index*(math.pi/max(1,count)) + tuft["rng"]*.17
            h=tuft["height"]*(.82+.18*(blade_index+1)/max(1,count))
            add_blade(vertices,faces,material_indices,tuft["x"]+math.cos(yaw)*.06,tuft["y"]+math.sin(yaw)*.06,tuft["z"],h,tuft["width"],yaw,tuft["lean"],1 if tuft["morph"]=="SENESCENT" else 0)
    mesh=bpy.data.meshes.new(name); mesh.from_pydata(vertices,[],faces); mesh.materials.append(grass); mesh.materials.append(sen)
    for poly, index in zip(mesh.polygons, material_indices): poly.material_index=index
    mesh.update(); return mesh


def rebuild_lod_from_lod0(source, name, stride):
    groups=len(source.vertices)//4
    coordinates=[v.co for v in source.vertices]
    extreme_vertices={
        min(range(len(coordinates)),key=lambda i:coordinates[i].x), max(range(len(coordinates)),key=lambda i:coordinates[i].x),
        min(range(len(coordinates)),key=lambda i:coordinates[i].y), max(range(len(coordinates)),key=lambda i:coordinates[i].y),
        min(range(len(coordinates)),key=lambda i:coordinates[i].z), max(range(len(coordinates)),key=lambda i:coordinates[i].z),
    }
    keep=set(range(0,groups,stride)) | {index//4 for index in extreme_vertices}
    vertices=[]; faces=[]; material_indices=[]
    for group in sorted(keep):
        base=len(vertices)
        vertices.extend([tuple(source.vertices[group*4+i].co) for i in range(4)])
        faces += [(base,base+1,base+2),(base,base+2,base+3)]
        source_poly=min(group*2,len(source.polygons)-1)
        material_indices += [source.polygons[source_poly].material_index]*2
    old=bpy.data.meshes.get(name)
    if old:
        old.use_fake_user=False
        if old.users==0: bpy.data.meshes.remove(old)
    mesh=bpy.data.meshes.new(name); mesh.from_pydata(vertices,[],faces)
    for m in source.materials: mesh.materials.append(m)
    for poly,index in zip(mesh.polygons,material_indices): poly.material_index=index
    mesh.update(); mesh.use_fake_user=True
    return mesh, len(keep), groups


def build_shadow_mesh(name, tufts, shadow_material, direction):
    vertices=[]; faces=[]
    for tuft in tufts:
        if tuft["morph"] != "TEMPORAL_EDGE": continue
        center=Vector((tuft["x"],tuft["y"])) + direction*(.12*tuft["delay"]+.04)
        length=max(.18,tuft["height"]*.72); width=max(.025,tuft["width"]*1.35)
        side=Vector((-direction.y,direction.x))*width*.5; end=center+direction*length; i=len(vertices)
        vertices += [
            (center.x-side.x,center.y-side.y,tuft["z"]+.012),
            (center.x+side.x,center.y+side.y,tuft["z"]+.012),
            (end.x+side.x,end.y+side.y,tuft["z"]+.012),
            (end.x-side.x,end.y-side.y,tuft["z"]+.012),
        ]
        faces += [(i,i+1,i+2),(i,i+2,i+3)]
    mesh=bpy.data.meshes.new(name); mesh.from_pydata(vertices,[],faces); mesh.materials.append(shadow_material); mesh.update(); return mesh


def build():
    scene=bpy.context.scene; root=bpy.data.collections.get(ROOT) or scene.collection
    patch_collection=ensure_collection(PATCH_COLLECTION,root); shadow_collection=ensure_collection(SHADOW_COLLECTION,root); qa_collection=ensure_collection(QA_COLLECTION,root)
    for c in (patch_collection,shadow_collection,qa_collection): clear_collection(c)

    for obj in bpy.data.objects:
        if obj.name.startswith("AUR_GRASS_ECHO_"):
            obj.hide_render=True
            obj["superseded_by"]=WORKUNIT

    grass, sen, shadow_material = materials(); direction=stellar_shadow_direction(); sample_ground=ground_sampler(terrain_bvh())
    counts=Counter(); total_tufts=0; total_shadow=0; patch_rows=[]

    for patch_index,(cx,cy) in enumerate(PATCH_CENTERS):
        rng=random.Random(295000+patch_index*7919); tufts=[]; cells=int(math.ceil(PATCH_RADIUS/SPACING))
        for gx in range(-cells,cells+1):
            for gy in range(-cells,cells+1):
                x=cx+gx*SPACING+rng.uniform(-3.2,3.2); y=cy+gy*SPACING+rng.uniform(-3.2,3.2)
                if math.hypot(x-cx,y-cy)>PATCH_RADIUS: continue
                d_path=route_distance(x,y); d_field,delay,field_id=field_info(x,y)
                if d_field<46 or d_path<6: continue
                if rng.random() > (.48 if d_path<24 else .88): continue
                if d_path<24: morph="TRAMPLED_PATH"
                elif d_field<=132: morph="TEMPORAL_EDGE"
                else:
                    r=rng.random(); morph="JUVENILE" if r<.14 else ("SENESCENT" if r<.25 else ("MATURE_SHORT" if r<.62 else "MATURE_TALL"))
                spec=MORPH[morph]
                tufts.append({
                    "x":x,"y":y,"z":sample_ground(x,y),"height":rng.uniform(*spec["height"]),
                    "blades":rng.randint(*spec["blades"]),"lean":rng.uniform(*spec["lean"]),
                    "width":rng.uniform(*spec["width"]),"yaw":rng.uniform(0,math.tau),"morph":morph,
                    "delay":delay,"field_id":field_id,"rng":rng.random(),
                })
                counts[morph]+=1

        lod0=build_lod0_mesh(f"AUR_X100_PRAIRIE_PATCH_{patch_index:02d}_LOD0_MESH",tufts,grass,sen)
        obj=bpy.data.objects.new(f"AUR_X100_PRAIRIE_PATCH_{patch_index:02d}",lod0); patch_collection.objects.link(obj)
        obj["asset_id"]="AUR-VEG-001"; obj["species"]="Hierba de dos sombras"; obj["patch_id"]=f"AUR-PRAIRIE-PATCH-{patch_index:02d}"
        obj["seed"]=295000+patch_index*7919; obj["tuft_count"]=len(tufts); obj["collision_policy"]="NONE_PER_BLADE"; obj["x100_workunit"]=WORKUNIT
        obj["placement_rule"]="deterministic terrain-contact; field core/path clear; trampled and temporal morphotypes causal"

        for level,stride in ((1,3),(2,8)):
            lod_mesh, kept, source_groups = rebuild_lod_from_lod0(lod0,f"{obj.name}_LOD{level}_MESH",stride)
            meta=bpy.data.objects.new(f"META_{obj.name}_LOD{level}",None); qa_collection.objects.link(meta)
            meta["asset_id"]="AUR-VEG-001"; meta["patch_id"]=obj["patch_id"]; meta["lod"]=f"LOD{level}"; meta["mesh_datablock"]=lod_mesh.name
            meta["retained_blades"]=kept; meta["source_blades"]=source_groups; meta["strategy"]="blade-group reduction with X/Y/Z extrema preservation; patch envelope exact"
            meta["engine_status"]="CONTRACT_ONLY_EXO_012_BLOCKED"; meta["x100_workunit"]=WORKUNIT

        shadow_mesh=build_shadow_mesh(f"AUR_X100_PRAIRIE_PATCH_{patch_index:02d}_TEMPORAL_SHADOW_MESH",tufts,shadow_material,direction)
        shadow_count=sum(1 for tuft in tufts if tuft["morph"]=="TEMPORAL_EDGE")
        if len(shadow_mesh.vertices)>0:
            shadow_obj=bpy.data.objects.new(f"AUR_X100_PRAIRIE_PATCH_{patch_index:02d}_TEMPORAL_SHADOW",shadow_mesh); shadow_collection.objects.link(shadow_obj)
            shadow_obj["asset_id"]="AUR-VEG-001-SHADOW-EVIDENCE"; shadow_obj["source_patch"]=obj.name; shadow_obj["temporal_shadow_tufts"]=shadow_count
            shadow_obj["rule"]="extra offset ground-shadow evidence only inside bounded temporal annulus; primary shadow remains physical scene lighting"
            shadow_obj["collision_policy"]="NONE"; shadow_obj["x100_workunit"]=WORKUNIT
        total_shadow+=shadow_count; total_tufts+=len(tufts)
        patch_rows.append({"patch":patch_index,"center":[cx,cy],"tufts":len(tufts),"temporal_shadow_tufts":shadow_count,"triangles":len(lod0.polygons)})

    for name,spec in MORPH.items():
        meta=bpy.data.objects.new("META_AUR_VEG_001_"+name,None); qa_collection.objects.link(meta)
        meta["asset_id"]="AUR-VEG-001"; meta["species"]="Hierba de dos sombras"; meta["morphotype"]=name; meta["height_range_m"]=list(spec["height"])
        meta["blade_count_range"]=list(spec["blades"]); meta["causality"]=spec["cause"]; meta["canon_status"]="CANON_SPECIES / PROPOSAL_MORPHOTYPE"; meta["x100_workunit"]=WORKUNIT
    qa_collection.hide_render=True

    scene["x100_prairie_workunit"]=WORKUNIT; scene["x100_prairie_tufts"]=total_tufts; scene["x100_prairie_morphotypes"]=len(MORPH)
    scene["x100_prairie_temporal_shadow_tufts"]=total_shadow; scene["x100_prairie_lod_method"]="blade-group reduction + X/Y/Z extrema preservation"
    scene["status"]="X100_PRAIRIE_SYSTEM_R26_LOD_QA"
    return {"status":scene["status"],"patches":patch_rows,"total_tufts":total_tufts,"morphotypes":dict(counts),"temporal_shadow_tufts":total_shadow}


if __name__ == "__main__":
    print(build())
