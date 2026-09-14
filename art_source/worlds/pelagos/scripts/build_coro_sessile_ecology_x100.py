"""PELAGOS /EXOVANT-X100 — Coro sessile ecology systemic generator v1.

Claim: PEL/ECO/SESSILE-X100-004

This file is a deterministic Blender-side semantic rebuild authority for the first
producer/filter/decomposer sessile guild foundation. These guilds are reversible
FUNCTIONAL PROPOSALS. They do not replace canonical Pelagos species and do not assert
a complete trophic chain, reproduction system, or population density.
"""
import bpy
import math
import random
from mathutils import Vector
from mathutils.bvhtree import BVHTree

CLAIM = "PEL/ECO/SESSILE-X100-004"
COLLECTION = "14_CORO_SESSILE_ECO_X100_V1"
STATES = ("colonizing", "mature", "disturbed_recovering", "senescent")
VARIANTS = ("compact", "standard", "spread")
STATE_VARIANT = {
    "colonizing": "compact",
    "mature": "standard",
    "disturbed_recovering": "spread",
    "senescent": "standard",
}

FAMILIES = (
    ("FILTER_FAN", "PEL-ECO-SESSILE-FILTER-FAN-001", "current_facing_filter_fan"),
    ("PHOTIC_RIBBON", "PEL-ECO-SESSILE-PHOTIC-RIBBON-001", "photic_primary_producer_ribbon"),
    ("DETRITUS_MAT", "PEL-ECO-SESSILE-DETRITUS-MAT-001", "detritus_decomposer_mat"),
    ("MINERAL_TUBE", "PEL-ECO-SESSILE-MINERAL-TUBE-001", "mineral_tube_chemo_decomposer"),
    ("NURSERY_CRUST", "PEL-ECO-SESSILE-NURSERY-CRUST-001", "calcifying_juvenile_nursery_crust"),
    ("FOULING_FILTER", "PEL-ECO-SESSILE-FOULING-FILTER-001", "persistent_wet_interface_filter_cluster"),
    ("DECAY_BIOFILM", "PEL-ECO-SESSILE-DECAY-BIOFILM-001", "organic_decay_decomposer_biofilm"),
    ("CURRENT_BIOFILTER", "PEL-ECO-SESSILE-CURRENT-BIOFILTER-001", "porous_current_biofilter"),
    ("LEE_DETRITUS", "PEL-ECO-SESSILE-LEE-DETRITUS-001", "lee_zone_detritus_aggregation"),
)

# 6 x 6 deterministic proof patch = 36 physical roots. Placement is projected to
# bathymetry at runtime; these are XY requests, never hard-coded Z guesses.
ANCHOR_XY = [(40 + 10*c, 120 + 10*r) for r in range(6) for c in range(6)]

STATE_PARAMS = {
    "colonizing": (0.62, 0.58, 0.22),
    "mature": (1.00, 1.00, 0.00),
    "disturbed_recovering": (0.82, 0.78, 0.35),
    "senescent": (0.76, 0.70, 0.48),
}
VARIANT_SPREAD = {"compact": 0.78, "standard": 1.00, "spread": 1.18}


def _collection(name):
    c = bpy.data.collections.get(name)
    if c is None:
        c = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(c)
    return c


def _reset_collection(name):
    old = bpy.data.collections.get(name)
    if old:
        for o in list(old.objects):
            bpy.data.objects.remove(o, do_unlink=True)
        bpy.data.collections.remove(old)
    return _collection(name)


def _link_only(obj, col):
    for c in list(obj.users_collection):
        c.objects.unlink(obj)
    col.objects.link(obj)


def _mat(name, color, roughness=0.6, metallic=0.0):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    bs = m.node_tree.nodes.get("Principled BSDF")
    bs.inputs["Base Color"].default_value = (*color, 1.0)
    bs.inputs["Roughness"].default_value = roughness
    bs.inputs["Metallic"].default_value = metallic
    return m


def _semantic(obj, asset_id, role, state, variant, extra=None):
    data = {
        "asset_id": asset_id,
        "role": role,
        "claim_id": CLAIM,
        "state": state,
        "variant": variant,
        "collision_policy": "none_or_soft_query",
        "canon_status": "PROPOSAL_FUNCTIONAL_GUILD",
    }
    if extra:
        data.update(extra)
    for k, v in data.items():
        obj[k] = v


def _parent_local(obj, root):
    obj.parent = root
    obj.matrix_parent_inverse.identity()


def _cube(name, loc, dims, mat, root, asset_id, role, state, variant, col, extra=None, rot=None):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    o = bpy.context.object
    o.name = name
    o.dimensions = dims
    if rot:
        o.rotation_euler = rot
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    o.data.materials.append(mat)
    _link_only(o, col)
    if not o.data.uv_layers:
        o.data.uv_layers.new(name="UVMap")
    _semantic(o, asset_id, role, state, variant, extra)
    _parent_local(o, root)
    return o


def _cyl(name, loc, radius, depth, mat, root, asset_id, role, state, variant, col, extra=None, vertices=12, rot=None):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=loc)
    o = bpy.context.object
    o.name = name
    if rot:
        o.rotation_euler = rot
    o.data.materials.append(mat)
    _link_only(o, col)
    _semantic(o, asset_id, role, state, variant, extra)
    _parent_local(o, root)
    return o


def _ico(name, loc, radius, mat, root, asset_id, role, state, variant, col, extra=None, scale=None):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=radius, location=loc)
    o = bpy.context.object
    o.name = name
    if scale:
        o.scale = scale
        bpy.context.view_layer.objects.active = o
        o.select_set(True)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        o.select_set(False)
    o.data.materials.append(mat)
    _link_only(o, col)
    _semantic(o, asset_id, role, state, variant, extra)
    _parent_local(o, root)
    return o


def _bathymetry_bvh():
    bath = bpy.data.objects["PEL_ENV_Bathymetry_2200m"]
    dg = bpy.context.evaluated_depsgraph_get()
    ev = bath.evaluated_get(dg)
    me = ev.to_mesh()
    M = ev.matrix_world
    verts = [M @ v.co for v in me.vertices]
    polys = [tuple(p.vertices) for p in me.polygons]
    bvh = BVHTree.FromPolygons(verts, polys, all_triangles=False)
    return ev, bvh


def _substrate(bvh, x, y):
    hit, normal, _, _ = bvh.ray_cast(Vector((x, y, 180.0)), Vector((0, 0, -1)), 400.0)
    if hit is None:
        raise RuntimeError(f"No bathymetry hit at {(x, y)}")
    return hit, normal.normalized()


def _state_evidence(root, code, aid, state, variant, spread, mats, col):
    if state == "colonizing":
        _ico(root.name+"_JUVENILE", (0,0,0.07), .13, mats["producer_pale"], root, aid,
             "juvenile_growth_front", state, variant, col, {"era":"ECO_STATE_COLONIZING"}, (1.5,1.2,.4))
    elif state == "mature":
        _ico(root.name+"_ACTIVE_CORE", (0,0,0.09), .15, mats["filter"], root, aid,
             "active_mature_core", state, variant, col, {"era":"ECO_STATE_MATURE"}, (1.4,1.0,.5))
    elif state == "disturbed_recovering":
        _ico(root.name+"_REPAIR_GROWTH", (.18*spread,-.10,.12), .15, mats["producer_pale"], root, aid,
             "localized_recovery_growth", state, variant, col, {"era":"ECO_STATE_RECOVERY"}, (1.5,.7,.45))
    else:
        for i in range(3):
            _ico(f"{root.name}_DETRITUS_{i}", ((-.22+i*.22)*spread,.20,.05), .12, mats["detritus"], root, aid,
                 "senescent_detritus", state, variant, col, {"era":"ECO_STATE_SENESCENT"}, (1.4,1.0,.35))


def _build_family(root, code, aid, state, variant, mats, col):
    growth, density, _ = STATE_PARAMS[state]
    spread = VARIANT_SPREAD[variant]
    rng = random.Random(f"{code}:{state}")

    if code == "FILTER_FAN":
        _ico(root.name+"_BASE", (0,0,.08), .24*spread, mats["calcified"], root, aid, "anchoring_holdfast", state, variant, col, scale=(1.6,1.2,.35))
        count = max(3, int(7*density))
        for i in range(count):
            y=(i-(count-1)/2)*.16*spread; h=(.75+.25*rng.random())*growth
            _cube(f"{root.name}_FAN_{i}", (.10,y,h*.5), (.055,.34*spread,h), mats["filter"], root, aid,
                  "current_facing_filter_lamina", state, variant, col, {"current_facing":"+X"}, (0,math.radians(-12),0))

    elif code == "PHOTIC_RIBBON":
        _ico(root.name+"_BASE", (0,0,.06), .26*spread, mats["producer"], root, aid, "producer_holdfast", state, variant, col, scale=(1.7,1.4,.3))
        count=max(4,int(9*density))
        for i in range(count):
            a=-.7+1.4*(i/max(1,count-1)); h=(.55+.45*rng.random())*growth
            _cube(f"{root.name}_RIBBON_{i}", (.12*a,.10*a,h*.5), (.075,.14*spread,h), mats["producer_pale"], root, aid,
                  "photic_ribbon_blade", state, variant, col, {"light_band":"photic_exposed"}, (math.radians(4*a),math.radians(-14),a*.35))

    elif code == "DETRITUS_MAT":
        for i in range(max(4,int(10*density))):
            ang=i*2.399; rr=(.18+.05*i)*spread
            _ico(f"{root.name}_MAT_{i}", (math.cos(ang)*rr,math.sin(ang)*rr,.035), .20*(.8+.4*rng.random()), mats["decomposer"], root, aid,
                 "detritus_decomposer_patch", state, variant, col, {"resource":"detritus","placement":"lee_or_low_flow"}, (1.5,1.2,.22))

    elif code == "MINERAL_TUBE":
        _ico(root.name+"_BASE", (0,0,.05), .28*spread, mats["mineral"], root, aid, "mineral_substrate_crust", state, variant, col, scale=(1.5,1.3,.28))
        count=max(4,int(11*density))
        for i in range(count):
            ang=2*math.pi*i/count; rr=.12+.18*(i%2); h=(.28+.42*rng.random())*growth
            _cyl(f"{root.name}_TUBE_{i}", (math.cos(ang)*rr*spread,math.sin(ang)*rr*spread,h*.5), .055*(.8+.3*rng.random()), h,
                 mats["mineral"], root, aid, "chemo_decomposer_tube", state, variant, col, {"resource":"mineral_gradient"}, 10)

    elif code == "NURSERY_CRUST":
        for i in range(max(4,int(9*density))):
            ang=i*2.0; rr=(.12+.055*i)*spread; x=math.cos(ang)*rr; y=math.sin(ang)*rr
            _ico(f"{root.name}_CRUST_{i}", (x,y,.035), .18, mats["calcified"], root, aid, "calcifying_nursery_crust", state, variant, col,
                 {"ecological_effect":"juvenile_settlement_substrate"}, (1.8,1.3,.2))
            if i % 3 == 0:
                _cyl(f"{root.name}_BUD_{i}", (x,y,.11), .04, .20*growth, mats["producer_pale"], root, aid, "juvenile_calcifying_bud", state, variant, col, vertices=8)

    elif code == "FOULING_FILTER":
        count=max(5,int(13*density))
        for i in range(count):
            ang=2*math.pi*i/count; rr=(.18+.16*(i%3)/2)*spread; h=(.16+.30*rng.random())*growth
            _cyl(f"{root.name}_CONE_{i}", (math.cos(ang)*rr,math.sin(ang)*rr,h*.5), .07*(.8+rng.random()*.4), h, mats["fouling"], root, aid,
                 "fouling_filter_tube", state, variant, col, {"substrate_options":"mineral|wet_infrastructure","current_facing":"radial"}, 8)

    elif code == "DECAY_BIOFILM":
        _ico(root.name+"_RESOURCE", (0,0,.09), .24, mats["detritus"], root, aid, "organic_resource_residue", state, variant, col, {"resource":"organic_decay"}, (1.3,1.0,.45))
        for i in range(max(5,int(12*density))):
            ang=2.2*i; rr=(.16+.045*i)*spread
            _ico(f"{root.name}_FILM_{i}", (math.cos(ang)*rr,math.sin(ang)*rr,.025), .14, mats["decomposer"], root, aid,
                 "decomposer_biofilm_lobe", state, variant, col, scale=(1.8,1.3,.15))

    elif code == "CURRENT_BIOFILTER":
        for i in range(max(4,int(8*density))):
            x=(i%2)*.20-.10; y=(i//2)*.15-.22; z=.16+(i%3)*.18*growth
            _ico(f"{root.name}_LOBE_{i}", (x*spread,y*spread,z), .20*(.9+rng.random()*.25), mats["filter"], root, aid,
                 "porous_biofilter_lobe", state, variant, col, {"current_facing":"+X","ecological_effect":"suspended_particle_filter"}, (1.15,.85,1.25))

    else:  # LEE_DETRITUS
        for i in range(max(5,int(11*density))):
            x=(-.38+i*.085)*spread; y=.10*math.sin(i*.9)
            _ico(f"{root.name}_MOUND_{i}", (x,y,.035), .16*(.9+rng.random()*.25), mats["detritus"], root, aid,
                 "lee_zone_detritus_mound", state, variant, col, {"placement":"downcurrent_lee","current_vector":"+X"}, (1.7,1.0,.20))

    _state_evidence(root, code, aid, state, variant, spread, mats, col)


def main():
    col = _reset_collection(COLLECTION)
    mats = {
        "producer": _mat("PEL_ECO_X100_Producer", (.16,.34,.24), .72),
        "producer_pale": _mat("PEL_ECO_X100_ProducerPale", (.36,.52,.38), .66),
        "filter": _mat("PEL_ECO_X100_FilterTissue", (.17,.30,.31), .54),
        "mineral": _mat("PEL_ECO_X100_MineralTube", (.31,.35,.29), .78, .02),
        "calcified": _mat("PEL_ECO_X100_Calcified", (.50,.54,.45), .82, .01),
        "detritus": _mat("PEL_ECO_X100_Detritus", (.12,.10,.07), .90),
        "decomposer": _mat("PEL_ECO_X100_Decomposer", (.19,.16,.11), .84),
        "fouling": _mat("PEL_ECO_X100_Fouling", (.08,.20,.14), .80),
        "debug": _mat("PEL_ECO_X100_TechDebug", (.10,.02,.14), .90),
    }
    ev, bvh = _bathymetry_bvh()
    roots=[]
    for fi,(code,aid,purpose) in enumerate(FAMILIES):
        for si,state in enumerate(STATES):
            idx=fi*4+si; x,y=ANCHOR_XY[idx]; hit,n=_substrate(bvh,x,y); variant=STATE_VARIANT[state]
            root=bpy.data.objects.new(f"PEL_SESS_{code}_{state.upper()}", None); col.objects.link(root)
            root.location=hit; root.rotation_mode='QUATERNION'; root.rotation_quaternion=n.to_track_quat('Z','Y')
            for k,v in {
                "asset_id":aid, "role":"sessile_ecology_root", "family":code, "purpose":purpose,
                "state":state, "variant":variant, "claim_id":CLAIM, "canon_status":"PROPOSAL_FUNCTIONAL_GUILD",
                "substrate":"bathymetry_mineral", "substrate_z":float(hit.z), "substrate_normal":tuple(float(q) for q in n),
                "current_vector_world":(1.0,0.0,0.0), "collision_policy":"none_or_soft_query",
                "min_traversal_clearance_m":2.0,
            }.items(): root[k]=v
            _build_family(root,code,aid,state,variant,mats,col); roots.append(root)

    # One hidden shared family LOD1 exemplar each; engine thresholds intentionally unresolved.
    for fi,(code,aid,_) in enumerate(FAMILIES):
        tr=bpy.data.objects.new(f"PEL_SESS_{code}_LOD1_ROOT", None); col.objects.link(tr); tr.location=(0,0,-500-fi*2)
        tr['asset_id']=aid+'-LOD1'; tr['role']='lod1_family_root'; tr['technical']=True
        p=_ico(f"PEL_SESS_{code}_LOD1_PROXY", (0,0,.18), .35, mats['debug'], tr, aid+'-LOD1', 'lod1_family_envelope', 'technical', 'technical', col, {'technical':True}, (1.5,1.2,.55))
        p.hide_render=True; p.hide_viewport=True

    meta=bpy.data.objects.new("PEL_SESS_X100_META", None); col.objects.link(meta)
    meta['claim_id']=CLAIM; meta['family_count']=9; meta['authored_state_roots']=36
    meta['variants']=3; meta['states']=4; meta['direct_configurations']=108
    meta['placement_multiplier']='substrate x slope x current x light x disturbance'
    meta['trophic_truth']='FUNCTIONAL_GUILD_PROPOSALS_ONLY__DETAILED_CHAIN_UNKNOWN'
    ev.to_mesh_clear(); bpy.context.view_layer.update()
    return roots

if __name__ == '__main__':
    main()
