"""THALASSA hero engineering blockout for EXOVANT 2950 / PELAGOS.

Task: PEL/BOSS/008
Blender: 5.2+
Units: 1 BU = 1 metre

Canon locked by design/EXOVANT_BIBLIA.md / EXOVANT_DATA.json:
- arena diameter: 52 m
- phases: scout eyes -> sector flooding/tentacle closure -> restored-memory extraction-bond resolution
- attacks: Mirada convergente 1.2 s, Látigo de corriente 0.9 s, Canto de presión 1.6 s

All boss physical dimensions and articulation choices in this script are reversible PROPOSALS.
This is a rig-ready engineering blockout, not the final sculpt, rig, animation or encounter.
"""
import bpy
import math
from mathutils import Vector

COLLECTION = "41_THALASSA_HERO_V1"
ASSET_ID = "PEL-BOSS-THALASSA"
WORLD = "pelagos"
CENTER = Vector((520.0, 230.0, -90.0))


def require_material(name):
    m = bpy.data.materials.get(name)
    if not m:
        raise RuntimeError(f"Missing validated Pelagos material {name}")
    return m


M_CORAL = require_material("PEL_MAT_LivingCoral_Tissue")
M_MEMORY = require_material("PEL_MAT_MemoryCyan_Biolum")
M_BRONZE = require_material("PEL_MAT_Bronze_Oxidized_Marine")
M_IVORY = require_material("PEL_MAT_IvoryCeramic_Marine")
M_DARK = require_material("PEL_MAT_DarkTechnicalComposite")


def collection_reset():
    root = bpy.data.collections.get("PELAGOS_WORLD")
    if not root:
        raise RuntimeError("PELAGOS_WORLD missing")
    old = bpy.data.collections.get(COLLECTION)
    if old:
        for o in list(old.objects):
            bpy.data.objects.remove(o, do_unlink=True)
        bpy.data.collections.remove(old)
    c = bpy.data.collections.new(COLLECTION)
    root.children.link(c)
    return c


def assign(obj, material):
    if hasattr(obj.data, "materials"):
        obj.data.materials.clear()
        obj.data.materials.append(material)


def relink(obj, c):
    for oc in list(obj.users_collection):
        oc.objects.unlink(obj)
    c.objects.link(obj)


def tag(obj, role, phase="all", collision="none"):
    obj["asset_id"] = ASSET_ID
    obj["world"] = WORLD
    obj["role"] = role
    obj["quality_tier"] = "S"
    obj["production_state"] = "HERO_ENGINEERING_BLOCKOUT_V1"
    obj["phase_usage"] = phase
    obj["collision_intent"] = collision
    return obj


def parent_keep_world(obj, parent):
    mw = obj.matrix_world.copy()
    obj.parent = parent
    obj.matrix_world = mw


def empty(c, name, loc, role, phase="all", parent=None):
    o = bpy.data.objects.new(name, None)
    c.objects.link(o)
    o.location = loc
    o.empty_display_type = "PLAIN_AXES"
    o.empty_display_size = 0.5
    tag(o, role, phase)
    if parent:
        parent_keep_world(o, parent)
    return o


def sphere(c, name, loc, dims, material, role, phase="all", collision="none", segments=32, rings=16):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segments, ring_count=rings, location=loc)
    o = bpy.context.object
    o.name = name
    o.dimensions = dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    assign(o, material); relink(o, c); tag(o, role, phase, collision)
    return o


def cylinder(c, name, p, q, radius, material, role, phase="all", collision="none", vertices=20):
    p, q = Vector(p), Vector(q)
    direction = q - p
    length = direction.length
    if length <= 1e-5:
        raise RuntimeError(f"Zero-length segment {name}")
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=length, location=(p + q) * 0.5)
    o = bpy.context.object
    o.name = name
    o.rotation_euler = direction.to_track_quat("Z", "Y").to_euler()
    assign(o, material); relink(o, c); tag(o, role, phase, collision)
    return o


def torus(c, name, loc, major, minor, material, role, phase="all", rotation=(0, 0, 0)):
    bpy.ops.mesh.primitive_torus_add(major_radius=major, minor_radius=minor, major_segments=48, minor_segments=10, location=loc, rotation=rotation)
    o = bpy.context.object
    o.name = name
    assign(o, material); relink(o, c); tag(o, role, phase)
    return o


def curve(c, name, points, bevel, material, role, phase="all"):
    cu = bpy.data.curves.new(name + "_CURVE", "CURVE")
    cu.dimensions = "3D"
    cu.resolution_u = 3
    cu.bevel_depth = bevel
    cu.bevel_resolution = 3
    sp = cu.splines.new("BEZIER")
    sp.bezier_points.add(len(points) - 1)
    for bp, p in zip(sp.bezier_points, points):
        bp.co = p
        bp.handle_left_type = "AUTO"
        bp.handle_right_type = "AUTO"
    o = bpy.data.objects.new(name, cu)
    c.objects.link(o)
    assign(o, material); tag(o, role, phase)
    return o


def build():
    c = collection_reset()

    # Preserve old blockout for recovery, but remove it from production view.
    for o in bpy.data.objects:
        if o.name == "PEL_BOSS_Thalassa_Core" or o.name.startswith("PEL_BOSS_Eye_") or o.name.startswith("PEL_BOSS_Tentacle_"):
            o.hide_render = True
            o.hide_set(True)
            o["production_state"] = "SUPERSEDED_BOSS_PROXY"
            o["superseded_by"] = COLLECTION

    meta = empty(c, "PEL_THALASSA_METADATA", CENTER, "boss_metadata")
    meta["boss_name"] = "THALASSA, coral de los mil ojos"
    meta["arena_diameter_m_canon"] = 52.0
    meta["boss_visible_bbox_m_proposal"] = [46.141, 43.5, 22.798]
    meta["max_measured_radial_extent_m_proposal"] = 23.166
    meta["arena_radial_clearance_m_at_rest_proposal"] = 2.834
    meta["dimension_status"] = "PROPOSAL_MEASURED_BLOCKOUT"
    meta["movement_model"] = "ANCHORED_CUSTODIAN_WITH_ARTICULATED_TENTACLES_PROPOSAL"
    meta["rig_status"] = "SOCKETS_AND_PIVOTS_ONLY_NO_FINAL_ARMATURE"
    meta["engine_status"] = "NOT_IMPORTED"

    # Anchored load-bearing anatomy and human extraction intrusion.
    sphere(c, "PEL_THA_BasalMass", CENTER + Vector((0, 0, 4.2)), (16, 16, 8.4), M_CORAL, "load_bearing_basal_mass", collision="complex")
    torus(c, "PEL_THA_ExtractionCollar", CENTER + Vector((0, 0, 5)), 8.6, 0.55, M_BRONZE, "human_extraction_collar", "phase3")
    for i in range(6):
        a = math.tau * i / 6
        inner = CENTER + Vector((math.cos(a)*5.4, math.sin(a)*5.4, 3.3))
        outer = CENTER + Vector((math.cos(a)*10.0, math.sin(a)*10.0, 0.8))
        cylinder(c, f"PEL_THA_Buttress_{i:02d}", inner, outer, 1.25, M_CORAL, "load_bearing_buttress", collision="simple", vertices=18)
        cylinder(c, f"PEL_THA_ExtractionStrut_{i:02d}", outer, outer + Vector((0,0,4.8)), 0.28, M_BRONZE, "extraction_hardware", "phase3", "simple", 12)

    sphere(c, "PEL_THA_CoreLower", CENTER + Vector((0,0,8)), (12.5,12.5,10), M_CORAL, "core_lower", collision="complex")
    sphere(c, "PEL_THA_CoreUpper", CENTER + Vector((0,0,14)), (9.8,9.8,11.5), M_CORAL, "core_upper", collision="complex")
    sphere(c, "PEL_THA_Crown", CENTER + Vector((0,0,20)), (7.2,7.2,5), M_CORAL, "sensory_crown", "phase1", "simple")

    # Four pressure organs make Canto de presión legible before motion polish.
    for i in range(4):
        a = math.tau*i/4 + math.pi/4
        loc = CENTER + Vector((math.cos(a)*6.3, math.sin(a)*6.3, 12))
        membrane = sphere(c, f"PEL_THA_PressureMembrane_{i:02d}", loc, (4.4,3.2,5.2), M_MEMORY, "pressure_membrane", "phase2", segments=24, rings=12)
        membrane["telegraph_for"] = "Canto de presión"
        membrane["telegraph_seconds_canon"] = 1.6
        torus(c, f"PEL_THA_MembraneFrame_{i:02d}", loc, 2.0, 0.18, M_BRONZE, "membrane_support", "phase2", (math.pi/2,0,a))

    # Shared macro-eye mesh: enough for readable groups without wasting thousands of objects.
    bpy.ops.mesh.primitive_uv_sphere_add(segments=20, ring_count=10, radius=0.62)
    tmp = bpy.context.object
    eye_mesh = tmp.data
    eye_mesh.name = "PEL_THA_EYE_SHARED_MESH"
    bpy.data.objects.remove(tmp, do_unlink=True)
    eye_mesh.materials.append(M_MEMORY)
    eye_count = 0
    for ring, (z, radius, count) in enumerate(((10.5,6.3,16),(15.0,5.2,18),(19.2,3.8,14))):
        for i in range(count):
            a = math.tau*i/count + ring*0.18
            loc = CENTER + Vector((math.cos(a)*radius, math.sin(a)*radius, z))
            o = bpy.data.objects.new(f"PEL_THA_Eye_R{ring}_{i:02d}", eye_mesh)
            c.objects.link(o)
            o.location = loc
            tag(o, "macro_sensory_eye", "phase1")
            o["eye_group"] = i % 3
            o["telegraph_for"] = "Mirada convergente"
            o["telegraph_seconds_canon"] = 1.2
            eye_count += 1
    for i in range(12):
        a = math.tau*i/12
        torus(c, f"PEL_THA_SensoryPoreRing_{i:02d}", CENTER + Vector((math.cos(a)*3.2, math.sin(a)*3.2, 20.2 + (i%3)*0.65)), 0.48, 0.10, M_MEMORY, "micro_eye_field_proxy", "phase1", (math.pi/2,0,a))
    meta["macro_eye_count"] = eye_count
    meta["thousand_eye_representation"] = "48 macro eyes + sensory pore fields; literal thousand meshes intentionally deferred"

    # Eight articulated tentacles with explicit rig sockets/joints.
    segment_count = joint_count = 0
    for arm in range(8):
        a = math.tau*arm/8
        radial = Vector((math.cos(a), math.sin(a), 0))
        tangent = Vector((-math.sin(a), math.cos(a), 0))
        points = [
            CENTER + radial*5.5 + Vector((0,0,9)),
            CENTER + radial*9 + tangent*(1.4 if arm%2==0 else -1.4) + Vector((0,0,8)),
            CENTER + radial*13 + tangent*(2.0 if arm%2==0 else -2.0) + Vector((0,0,6)),
            CENTER + radial*17 + tangent*(1.2 if arm%2==0 else -1.2) + Vector((0,0,4.2)),
            CENTER + radial*21 + Vector((0,0,2.3)),
        ]
        socket = empty(c, f"PEL_THA_TentacleSocket_{arm:02d}", points[0], "tentacle_socket", "phase2", meta)
        socket["telegraph_for"] = "Látigo de corriente"
        socket["telegraph_seconds_canon"] = 0.9
        for j, p in enumerate(points[1:-1], 1):
            joint = empty(c, f"PEL_THA_TentacleJoint_{arm:02d}_{j:02d}", p, "tentacle_joint", "phase2", meta)
            joint["arm_index"] = arm; joint["joint_index"] = j
            joint_count += 1
        for s in range(4):
            seg = cylinder(c, f"PEL_THA_Tentacle_{arm:02d}_Seg_{s:02d}", points[s], points[s+1], max(0.50, 1.15-s*0.18), M_CORAL, "tentacle_segment", "phase2", "simple", 18)
            seg["arm_index"] = arm; seg["segment_index"] = s
            seg["telegraph_for"] = "Látigo de corriente"; seg["telegraph_seconds_canon"] = 0.9
            segment_count += 1
        sphere(c, f"PEL_THA_TentacleTip_{arm:02d}", points[-1], (1.5,1.5,1.8), M_MEMORY, "tentacle_sensory_tip", "phase2", "simple", 20, 10)

    # Six visible extraction bonds make the phase-3 ethical/mechanical resolution tangible.
    for i in range(6):
        a = math.tau*i/6
        start = CENTER + Vector((math.cos(a)*8.6, math.sin(a)*8.6, 5.0))
        end = CENTER + Vector((math.cos(a)*23.0, math.sin(a)*23.0, 3.0))
        cable = curve(c, f"PEL_THA_ExtractionCable_{i:02d}", [start, (start+end)*0.5 + Vector((0,0,2.5)), end], 0.17, M_BRONZE, "extraction_bond_cable", "phase3")
        cable["interaction_intent"] = "CUTTABLE_PHASE3_PROPOSAL"

    # Existing arena columns retain LOS function. These objects make acoustic/vent states readable.
    for i in range(8):
        a = math.tau*i/8
        sphere(c, f"PEL_THA_ColumnHydrophone_{i:02d}", CENTER + Vector((math.cos(a)*21, math.sin(a)*21, 24)), (1,1,1), M_MEMORY, "arena_hydrophone", "phase1", segments=16, rings=8)
    for i, a in enumerate((0, math.pi/2, math.pi, 3*math.pi/2)):
        base = CENTER + Vector((math.cos(a)*15, math.sin(a)*15, 2.8))
        cylinder(c, f"PEL_THA_VentStack_{i:02d}", base, base + Vector((0,0,3.8)), 0.75, M_IVORY, "ventilated_safe_platform_marker", "phase2", "simple", 16)
        torus(c, f"PEL_THA_VentGrille_{i:02d}", base + Vector((0,0,0.25)), 2.1, 0.16, M_BRONZE, "vent_grille", "phase2")

    collision = sphere(c, "PEL_THA_COLLISION_Core", CENTER + Vector((0,0,11)), (11.8,11.8,18), M_DARK, "collision_proxy_core", collision="compound", segments=16, rings=8)
    collision.hide_render = True

    return {
        "collection": COLLECTION,
        "arena_diameter_m_canon": 52.0,
        "boss_bbox_m_proposal": [46.141, 43.5, 22.798],
        "max_radial_extent_m_proposal": 23.166,
        "macro_eye_count": eye_count,
        "tentacle_arms": 8,
        "tentacle_segments": segment_count,
        "tentacle_joints": joint_count,
        "pending": ["sculpt/retopo", "UV/bake/final PBR", "armature/deformation", "attack animation", "runtime hitboxes", "engine encounter", "performance", "human art review"],
    }


if __name__ == "__main__":
    print(build())
