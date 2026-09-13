"""EXOVANT 2950 / UMBRA / X100 systemic service ecosystem.

Input contract:
- UMBRA Wave-2 checkpoint exists.
- `ENV_TERRAIN_TWILIGHT_BAND_BLOCKOUT` exists.
- established UMBRA portable material roles exist.

Output checkpoint: X100_SERVICE_ECOSYSTEM_FOUNDATION_001.

The generator creates a deterministic production catalog south of the authored
quest cells. It is a proposal layer, not canon. It intentionally does not add
flora/fauna, planet-scale geography, narrative language, final NOCTIL design,
runtime behavior, collision or LOD budgets.
"""

import bpy
import bmesh
import math
from mathutils import Vector, Matrix

scene = bpy.context.scene
terrain = bpy.data.objects["ENV_TERRAIN_TWILIGHT_BAND_BLOCKOUT"]
world = bpy.data.collections["W04_UMBRA"]


def ensure_child(parent, name):
    c = bpy.data.collections.get(name) or bpy.data.collections.new(name)
    if c.name not in [x.name for x in parent.children]:
        parent.children.link(c)
    return c


C = ensure_child(world, "80_X100_SERVICE_ECOSYSTEM")
FAMILIES = [
    "TOOLCASE", "CABLE_REEL", "STORAGE", "POWERBOX", "HEATEX",
    "WINCH", "LAMP", "TEXTILE", "SERVICE_STAND", "WAYFIND",
]
sub = {f: ensure_child(C, f"81_X100_{f}") for f in FAMILIES}

mats = {
    "metal": bpy.data.materials["MAT_SINSOL_DARK_METAL"],
    "ivory": bpy.data.materials["MAT_COLONIAL_IVORY_REPAIR"],
    "amber": bpy.data.materials["MAT_REFUGE_AMBER"],
    "red": bpy.data.materials["MAT_HOSTILE_VERMILION"],
    "fabric": bpy.data.materials["MAT_SINSOL_TENSION_FABRIC"],
    "edge": bpy.data.materials["MAT_UMBRA_ICE_EDGE"],
}


def material(name, color, roughness, metallic):
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    p = m.node_tree.nodes.get("Principled BSDF")
    p.inputs["Base Color"].default_value = (*color, 1)
    p.inputs["Roughness"].default_value = roughness
    p.inputs["Metallic"].default_value = metallic
    return m


mats["gasket"] = material("MAT_SINSOL_GASKET", (0.025, 0.03, 0.035), 0.78, 0.0)
mats["copper"] = material("MAT_SINSOL_THERMAL_COPPER", (0.26, 0.105, 0.055), 0.38, 0.68)

box_cache = {}
cyl_cache = {}


def box_mesh(dims, mat):
    key = (tuple(round(float(x), 4) for x in dims), mat.name)
    if key in box_cache:
        return box_cache[key]
    me = bpy.data.meshes.new("MESH_X100_BOX_" + str(len(box_cache)).zfill(3))
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bm.transform(Matrix.Diagonal((dims[0], dims[1], dims[2], 1)))
    bm.to_mesh(me)
    bm.free()
    me.materials.append(mat)
    box_cache[key] = me
    return me


def cyl_mesh(radius, depth, mat, verts=12):
    key = (round(radius, 4), round(depth, 4), verts, mat.name)
    if key in cyl_cache:
        return cyl_cache[key]
    me = bpy.data.meshes.new("MESH_X100_CYL_" + str(len(cyl_cache)).zfill(3))
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=verts, radius1=radius, radius2=radius, depth=depth)
    bm.to_mesh(me)
    bm.free()
    me.materials.append(mat)
    cyl_cache[key] = me
    return me


def obj(name, me, col, parent, loc=(0, 0, 0), rot=(0, 0, 0)):
    o = bpy.data.objects.new(name, me)
    col.objects.link(o)
    o.parent = parent
    o.location = loc
    o.rotation_euler = rot
    return o


def box(name, dims, mat, col, parent, loc=(0, 0, 0), rot=(0, 0, 0)):
    return obj(name, box_mesh(dims, mat), col, parent, loc, rot)


def cyl(name, radius, depth, mat, col, parent, loc=(0, 0, 0), rot=(0, 0, 0), verts=12):
    return obj(name, cyl_mesh(radius, depth, mat, verts), col, parent, loc, rot)


def rod(name, a, b, radius, mat, col, parent, verts=10):
    a, b = Vector(a), Vector(b)
    v = b - a
    o = cyl(name, radius, v.length, mat, col, parent, loc=(a + b) * 0.5, verts=verts)
    o.rotation_euler = v.to_track_quat("Z", "Y").to_euler()
    return o


def terrain_z(x, y):
    inv = terrain.matrix_world.inverted()
    origin = inv @ Vector((x, y, 220.0))
    direction = (inv.to_3x3() @ Vector((0, 0, -1))).normalized()
    hit, loc, _n, _i = terrain.ray_cast(origin, direction, distance=600.0)
    if not hit:
        raise RuntimeError(f"No terrain hit at {x},{y}")
    return (terrain.matrix_world @ loc).z


def root_variant(family, index, size, state, x, y):
    e = bpy.data.objects.new(f"X100_{family}_{size}_{state}_{index:02d}", None)
    sub[family].objects.link(e)
    e.location = (x, y, terrain_z(x, y) + 0.03)
    e["stable_id"] = f"W04-X100-{family}-{size}-{state}-{index:02d}"
    e["family"] = family
    e["size_variant"] = size
    e["state_variant"] = state
    e["epistemic"] = "PRODUCTION_PROPOSAL_WITHIN_UMBRA_WORLD_OWNER_SCOPE"
    e["lod_strategy"] = "LOD0 authored; LOD1/LOD2 pending qualified runtime budget"
    e["collision_strategy"] = "simple root-bounds proxy pending integration owner"
    e["placement_rule"] = "service/refuge/reflector/caravan maintenance zones; keep primary traversal clear"
    e["story_tags"] = "field-maintenance,wind-exposure,thermal-survival,repair-history"
    return e


def state_mark(r, s, state, col, span=1.0):
    if state == "SERVICED":
        box(r.name + "_SERVICE_PLATE", (0.7*span, 0.09, 0.32*span), mats["ivory"], col, r, (0, -0.51*span, 0.65*span))
    elif state == "USED":
        box(r.name + "_WEAR_GUARD", (0.9*span, 0.10, 0.18*span), mats["edge"], col, r, (0, -0.52*span, 0.28*span))
    elif state == "FIELD_REPAIRED":
        box(r.name + "_REPAIR_PATCH", (0.85*span, 0.10, 0.48*span), mats["ivory"], col, r, (0.15*span, -0.53*span, 0.58*span), (0,0,math.radians(7)))
        rod(r.name + "_REPAIR_CLAMP", (-0.55*span,-0.58*span,0.22*span), (0.55*span,-0.58*span,0.22*span), 0.055*span, mats["metal"], col, r, 8)


def build_toolcase(r,s,state,c):
    box(r.name+"_BODY",(1.65*s,.92*s,.58*s),mats["metal"],c,r,(0,0,.31*s)); box(r.name+"_LID",(1.7*s,.96*s,.16*s),mats["ivory"],c,r,(0,0,.68*s)); rod(r.name+"_HANDLE",(-.34*s,-.56*s,.72*s),(.34*s,-.56*s,.72*s),.07*s,mats["metal"],c,r,8)
    for x in (-.55,.55): box(r.name+f"_LATCH_{x:+}",(.18*s,.12*s,.28*s),mats["ivory"],c,r,(x*s,-.52*s,.48*s))
    state_mark(r,s,state,c,s); r["semantic_purpose"]="insulated glove-operable field tool case"; r["credible_configurations"]=144

def build_reel(r,s,state,c):
    cyl(r.name+"_DRUM",.58*s,.82*s,mats["gasket"],c,r,(0,0,.72*s),(math.radians(90),0,0),16)
    for y in (-.48,.48): cyl(r.name+f"_HUB_{y:+}",.83*s,.12*s,mats["metal"],c,r,(0,y*s,.72*s),(math.radians(90),0,0),16)
    rod(r.name+"_AXLE",(0,-.65*s,.72*s),(0,.65*s,.72*s),.11*s,mats["ivory"],c,r,10)
    for x in (-.75,.75): rod(r.name+f"_FRAME_{x:+}",(x*s,-.55*s,.05*s),(x*s,.55*s,1.25*s),.08*s,mats["metal"],c,r,8)
    box(r.name+"_FOOT",(1.85*s,1.15*s,.12*s),mats["metal"],c,r,(0,0,.06*s)); state_mark(r,s,state,c,s); r["semantic_purpose"]="protected cable/power reel"; r["credible_configurations"]=162

def build_storage(r,s,state,c):
    box(r.name+"_BODY",(1.8*s,1.25*s,1.05*s),mats["metal"],c,r,(0,0,.55*s)); box(r.name+"_LID",(1.86*s,1.31*s,.14*s),mats["ivory"],c,r,(0,0,1.08*s))
    for x in (-.72,.72):
        for y in (-.45,.45): box(r.name+f"_CORNER_{x:+}_{y:+}",(.18*s,.18*s,1*s),mats["ivory"],c,r,(x*s,y*s,.55*s))
    state_mark(r,s,state,c,s); r["semantic_purpose"]="sealed modular storage/cargo box"; r["credible_configurations"]=216

def build_power(r,s,state,c):
    box(r.name+"_CABINET",(1.5*s,.92*s,2*s),mats["metal"],c,r,(0,0,s)); box(r.name+"_DOOR",(1.26*s,.10*s,1.55*s),mats["ivory"],c,r,(0,-.51*s,s))
    for z in (.45,.75,1.05,1.35): box(r.name+f"_FIN_{z}",(.85*s,.12*s,.08*s),mats["copper"],c,r,(.15*s,.52*s,z*s))
    for x in (-.38,0,.38): cyl(r.name+f"_PORT_{x:+}",.11*s,.18*s,mats["gasket"],c,r,(x*s,-.62*s,.3*s),(math.radians(90),0,0),12)
    state_mark(r,s,state,c,s); r["semantic_purpose"]="field power/thermal distribution cabinet"; r["credible_configurations"]=192

def build_heatex(r,s,state,c):
    box(r.name+"_CORE",(1.7*s,.58*s,1.35*s),mats["metal"],c,r,(0,0,.78*s))
    for i in range(7): box(r.name+f"_FIN_{i:02d}",(1.9*s,.08*s,1.25*s),mats["copper"],c,r,(0,(-.30+i*.10)*s,.78*s))
    for x in (-.65,.65): rod(r.name+f"_LEG_{x:+}",(x*s,0,.05*s),(x*s,0,.45*s),.08*s,mats["metal"],c,r,8)
    state_mark(r,s,state,c,s); r["semantic_purpose"]="portable heat exchanger/radiator"; r["credible_configurations"]=144

def build_winch(r,s,state,c):
    box(r.name+"_BASE",(1.8*s,1.2*s,.18*s),mats["metal"],c,r,(0,0,.09*s)); cyl(r.name+"_DRUM",.42*s,.78*s,mats["gasket"],c,r,(0,0,.7*s),(math.radians(90),0,0),16)
    for y in (-.48,.48): box(r.name+f"_CHEEK_{y:+}",(.95*s,.12*s,1.05*s),mats["metal"],c,r,(0,y*s,.68*s))
    box(r.name+"_MOTOR",(.7*s,.62*s,.62*s),mats["ivory"],c,r,(.75*s,0,.55*s)); rod(r.name+"_GUIDE",(-.75*s,-.48*s,.35*s),(-.75*s,.48*s,.35*s),.07*s,mats["ivory"],c,r,8)
    state_mark(r,s,state,c,s); r["semantic_purpose"]="anchor/tension service winch"; r["credible_configurations"]=180

def build_lamp(r,s,state,c):
    cyl(r.name+"_BASE",.48*s,.18*s,mats["metal"],c,r,(0,0,.09*s),verts=12); cyl(r.name+"_MAST",.08*s,1.35*s,mats["metal"],c,r,(0,0,.82*s),verts=10)
    box(r.name+"_SHIELD",(.92*s,.58*s,.34*s),mats["metal"],c,r,(0,0,1.55*s)); box(r.name+"_EMITTER",(.62*s,.12*s,.20*s),mats["amber"],c,r,(0,-.34*s,1.53*s))
    for x in (-.38,.38): rod(r.name+f"_CAGE_{x:+}",(x*s,-.38*s,1.33*s),(x*s,-.38*s,1.72*s),.035*s,mats["ivory"],c,r,8)
    state_mark(r,s,state,c,.75*s); r["semantic_purpose"]="low-profile shielded service lamp"; r["credible_configurations"]=108

def build_textile(r,s,state,c):
    cyl(r.name+"_ROLL",.48*s,1.6*s,mats["fabric"],c,r,(0,0,.52*s),(0,math.radians(90),0),16)
    for x in (-.48,.48): box(r.name+f"_STRAP_{x:+}",(.12*s,1.04*s,1.04*s),mats["ivory"],c,r,(x*s,0,.52*s))
    if state=="FIELD_REPAIRED": box(r.name+"_PATCH",(.55*s,.10*s,.42*s),mats["ivory"],c,r,(0,-.5*s,.62*s),(0,0,math.radians(-9)))
    elif state=="USED": box(r.name+"_ABRASION_GUARD",(.48*s,.09*s,.18*s),mats["edge"],c,r,(0,-.5*s,.35*s))
    r["semantic_purpose"]="rolled tension-fabric insulation/repair material"; r["credible_configurations"]=120

def build_stand(r,s,state,c):
    for side in (-1,1):
        rod(r.name+f"_LEG_A_{side:+}",(0,-.38*s,1.05*s),(side*.72*s,-.58*s,.05*s),.08*s,mats["metal"],c,r,8); rod(r.name+f"_LEG_B_{side:+}",(0,.38*s,1.05*s),(side*.72*s,.58*s,.05*s),.08*s,mats["metal"],c,r,8)
    box(r.name+"_SADDLE",(1.25*s,.55*s,.18*s),mats["ivory"],c,r,(0,0,1.05*s))
    for x in (-.68,.68): box(r.name+f"_FOOT_{x:+}",(.34*s,.85*s,.10*s),mats["metal"],c,r,(x*s,0,.05*s))
    state_mark(r,s,state,c,.9*s); r["semantic_purpose"]="maintenance trestle/jack stand"; r["credible_configurations"]=126

def build_wayfind(r,s,state,c):
    cyl(r.name+"_ANCHOR",.34*s,.22*s,mats["metal"],c,r,(0,0,.11*s),verts=12); cyl(r.name+"_POST",.07*s,1.75*s,mats["ivory"],c,r,(0,0,.98*s),verts=10); box(r.name+"_HORIZON_BAR",(1.45*s,.16*s,.18*s),mats["ivory"],c,r,(0,0,1.55*s))
    box(r.name+"_ECLIPSE_BACK",(.62*s,.12*s,.62*s),mats["metal"],c,r,(0,0,1.95*s)); box(r.name+"_ECLIPSE_CUT",(.42*s,.13*s,.42*s),mats["red"] if state=="FIELD_REPAIRED" else mats["amber"],c,r,(.15*s,-.02*s,2*s))
    r["semantic_purpose"]="geometry-coded horizon/eclipse wayfinding marker"; r["credible_configurations"]=144

BUILD = {"TOOLCASE":build_toolcase,"CABLE_REEL":build_reel,"STORAGE":build_storage,"POWERBOX":build_power,"HEATEX":build_heatex,"WINCH":build_winch,"LAMP":build_lamp,"TEXTILE":build_textile,"SERVICE_STAND":build_stand,"WAYFIND":build_wayfind}
SIZES = {"S":0.78,"M":1.0,"L":1.28}
STATES = ["SERVICED","USED","FIELD_REPAIRED"]
centers = dict(zip(FAMILIES, [(-220,-320),(-110,-320),(0,-320),(110,-320),(220,-320),(-220,-275),(-110,-275),(0,-275),(110,-275),(220,-275)]))
idx=0
for family in FAMILIES:
    bx,by=centers[family]
    for si,(size,scale) in enumerate(SIZES.items()):
        for ti,state in enumerate(STATES):
            r=root_variant(family,idx,size,state,bx+(si-1)*14,by+(ti-1)*7)
            BUILD[family](r,scale,state,sub[family]); idx+=1

for family in FAMILIES:
    bx,by=centers[family]
    a=bpy.data.objects.new("X100_FAMILY_ANCHOR_"+family,None); C.objects.link(a); a.location=(bx,by,terrain_z(bx,by)+.05); a["family"]=family; a["catalog_role"]="SYSTEMIC_75_PERCENT_LAYER"

scene["checkpoint"]="X100_SERVICE_ECOSYSTEM_FOUNDATION_001"
scene["x100_active"]=True
scene["x100_scope"]="W04-X100-SERVICE-ECOSYSTEM"
scene["x100_family_count"]=10
scene["x100_authored_prefab_variants"]=90
scene["x100_state_variants"]="SERVICED|USED|FIELD_REPAIRED"
scene["x100_size_variants"]="S|M|L"
scene["x100_status"]="FAMILY_FOUNDATION_NOT_FAMILY_COMPLETE"
scene["x100_not_done_reasons"]="UV0/PBR/collision runtime/LOD engine import/direct visual art review remain open"

# structural assertions from the authored checkpoint
roots=[o for o in bpy.data.objects if o.type=='EMPTY' and o.get('stable_id','').startswith('W04-X100-')]
assert len(roots)==90
assert len({o['stable_id'] for o in roots})==90
assert all(abs(o.location.z-terrain_z(o.location.x,o.location.y)-0.03)<1e-4 for o in roots)
