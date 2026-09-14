"""PELAGOS canonical ecology anatomy foundation.

Task: PEL/ECO/009
Blender: 5.2+
Units: 1 BU = 1 metre

CANON is limited to each organism's ecological/gameplay role from EXOVANT_DATA/BIBLIA.
Anatomy, dimensions, locomotion/support mechanisms and rig layout below are reversible
PROPOSALS that translate those roles into physically legible, rig-ready blockouts.

Assets:
- PEL-ECO-JELLY-001 — Medusa mnémica
- PEL-ECO-EEL-001 — Anguila de vidrio
- PEL-ECO-BOV-001 — Bóvido de arrecife
- PEL-ECO-SCRIBE-001 — Coral escriba hero specimen

The Coral escriba generator deliberately creates only a hero interactive specimen.
Background coral population remains owned by PEL/BIOME/007 to avoid duplicate systems.
"""
import bpy
import math
from mathutils import Vector

COLLECTION = "51_ECOLOGY_ANATOMY_V1"
WORLD = "pelagos"


def material(name):
    m = bpy.data.materials.get(name)
    if not m:
        raise RuntimeError(f"Missing required material: {name}")
    return m


M_CORAL = material("PEL_MAT_LivingCoral_Tissue")
M_MEMORY = material("PEL_MAT_MemoryCyan_Biolum")
M_MINERAL = material("PEL_MAT_BlackMineral_Wet")


def blockout_material(name, color, roughness=0.5, metallic=0.0):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = color
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    m["world"] = WORLD
    m["production_state"] = "BIOLOGY_BLOCKOUT_MATERIAL_NOT_FINAL"
    m["runtime_status"] = "FINAL_SHADER_PENDING"
    return m


M_PALE = blockout_material("PEL_ECO_PaleMembrane_Blockout", (0.16, 0.28, 0.31, 1), 0.34)
M_TISSUE = blockout_material("PEL_ECO_DeepTissue_Blockout", (0.075, 0.14, 0.13, 1), 0.55)
M_RASP = blockout_material("PEL_ECO_RaspKeratin_Blockout", (0.19, 0.17, 0.12, 1), 0.68, 0.03)


def reset_collection():
    root = bpy.data.collections.get("PELAGOS_WORLD")
    if root is None:
        raise RuntimeError("PELAGOS_WORLD missing")
    old = bpy.data.collections.get(COLLECTION)
    if old:
        for obj in list(old.objects):
            bpy.data.objects.remove(obj, do_unlink=True)
        bpy.data.collections.remove(old)
    col = bpy.data.collections.new(COLLECTION)
    root.children.link(col)
    return col


def hide_old_proxies():
    prefixes = [
        "PEL_ECO_MnemonicJelly_",
        "PEL_ECO_GlassEel",
        "PEL_ECO_ReefBovine_",
        "PEL_ECO_ScribeCoral_",
    ]
    count = 0
    for obj in bpy.data.objects:
        if any(obj.name.startswith(p) for p in prefixes):
            obj.hide_render = True
            obj.hide_set(True)
            obj["production_state"] = "SUPERSEDED_ECOLOGY_PROXY"
            obj["superseded_by"] = COLLECTION
            count += 1
    return count


def assign(obj, mat):
    if hasattr(obj.data, "materials"):
        obj.data.materials.clear()
        obj.data.materials.append(mat)


def relink(obj, col):
    for collection in list(obj.users_collection):
        collection.objects.unlink(obj)
    col.objects.link(obj)


def tag(obj, asset_id, role, rig="none", collision="none"):
    obj["asset_id"] = asset_id
    obj["world"] = WORLD
    obj["role"] = role
    obj["production_state"] = "ANATOMY_BLOCKOUT_V1"
    obj["rig_intent"] = rig
    obj["collision_intent"] = collision
    return obj


def parent_keep_world(obj, parent):
    matrix = obj.matrix_world.copy()
    obj.parent = parent
    obj.matrix_world = matrix


def empty(col, name, loc, asset_id, role, parent=None):
    obj = bpy.data.objects.new(name, None)
    col.objects.link(obj)
    obj.location = loc
    obj.empty_display_type = "PLAIN_AXES"
    obj.empty_display_size = 0.35
    tag(obj, asset_id, role, "socket")
    if parent:
        parent_keep_world(obj, parent)
    return obj


def sphere(col, name, loc, dims, mat, asset_id, role, collision="none", segments=28, rings=14):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segments, ring_count=rings, location=loc)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    assign(obj, mat)
    relink(obj, col)
    tag(obj, asset_id, role, "deform" if collision == "none" else "rigid", collision)
    return obj


def cylinder(col, name, p, q, radius, mat, asset_id, role, collision="none", vertices=16):
    p, q = Vector(p), Vector(q)
    direction = q - p
    length = direction.length
    if length <= 1e-5:
        raise RuntimeError(f"Zero-length segment: {name}")
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=length, location=(p + q) * 0.5)
    obj = bpy.context.object
    obj.name = name
    obj.rotation_euler = direction.to_track_quat("Z", "Y").to_euler()
    assign(obj, mat)
    relink(obj, col)
    tag(obj, asset_id, role, "deform", collision)
    return obj


def cone(col, name, p, q, r1, r2, mat, asset_id, role, collision="none", vertices=16):
    p, q = Vector(p), Vector(q)
    direction = q - p
    length = direction.length
    bpy.ops.mesh.primitive_cone_add(vertices=vertices, radius1=r1, radius2=r2, depth=length, location=(p + q) * 0.5)
    obj = bpy.context.object
    obj.name = name
    obj.rotation_euler = direction.to_track_quat("Z", "Y").to_euler()
    assign(obj, mat)
    relink(obj, col)
    tag(obj, asset_id, role, "deform", collision)
    return obj


def cube(col, name, loc, dims, mat, asset_id, role, collision="none"):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    assign(obj, mat)
    relink(obj, col)
    tag(obj, asset_id, role, "rigid", collision)
    return obj


def torus(col, name, loc, major, minor, mat, asset_id, role, rotation=(0, 0, 0)):
    bpy.ops.mesh.primitive_torus_add(
        major_radius=major,
        minor_radius=minor,
        major_segments=40,
        minor_segments=10,
        location=loc,
        rotation=rotation,
    )
    obj = bpy.context.object
    obj.name = name
    assign(obj, mat)
    relink(obj, col)
    tag(obj, asset_id, role)
    return obj


def curve(col, name, points, bevel, mat, asset_id, role):
    data = bpy.data.curves.new(name + "_CURVE", "CURVE")
    data.dimensions = "3D"
    data.resolution_u = 3
    data.bevel_depth = bevel
    data.bevel_resolution = 2
    spline = data.splines.new("BEZIER")
    spline.bezier_points.add(len(points) - 1)
    for point, co in zip(spline.bezier_points, points):
        point.co = co
        point.handle_left_type = "AUTO"
        point.handle_right_type = "AUTO"
    obj = bpy.data.objects.new(name, data)
    col.objects.link(obj)
    assign(obj, mat)
    tag(obj, asset_id, role, "deform")
    return obj


def metadata(col, name, loc, asset_id, canon_role, scale_fields, locomotion, support, feeding_sensing, habitat):
    obj = empty(col, name, loc, asset_id, "ecology_metadata")
    obj["canon_ecological_role"] = canon_role
    obj["dimension_status"] = "PROPOSAL_BLOCKOUT"
    for key, value in scale_fields.items():
        obj[key] = value
    obj["locomotion_proposal"] = locomotion
    obj["support_logic_proposal"] = support
    obj["feeding_sensing_proposal"] = feeding_sensing
    obj["habitat_adaptation_proposal"] = habitat
    obj["final_materials"] = "PENDING"
    obj["engine_status"] = "NOT_IMPORTED"
    obj["human_scale_reference_asset_id"] = "PEL-SCALE-HUMAN"
    return obj


def build_jelly(col):
    aid = "PEL-ECO-JELLY-001"
    center = Vector((-80, 180, 38))
    meta = metadata(
        col,
        "PEL_JELLY_METADATA",
        center,
        aid,
        "transmits luminous memory; information belongs to living individuals",
        {"bell_diameter_m_proposal": 3.6, "bell_height_m_proposal": 1.8, "tentacle_reach_m_proposal": 7.2},
        "pulsatile bell jet + passive current riding",
        "hydrostatic bell with circumferential muscle ring",
        "oral filter arms + photophore/memory-node ring + tentacular chemo/acoustic sense",
        "midwater reef channels; compliant body avoids rigid load skeleton",
    )
    meta["measured_visible_bbox_m"] = [4.909, 4.909, 8.308]
    root = empty(col, "PEL_JELLY_Root", center, aid, "rig_root", meta)
    sphere(col, "PEL_JELLY_Bell", center, (3.6, 3.6, 1.8), M_PALE, aid, "propulsion_bell")
    torus(col, "PEL_JELLY_MuscleRing", center + Vector((0, 0, -0.25)), 1.48, 0.16, M_TISSUE, aid, "circumferential_propulsion_muscle")
    for i in range(6):
        angle = math.tau * i / 6
        start = center + Vector((math.cos(angle)*0.65, math.sin(angle)*0.65, -0.7))
        end = center + Vector((math.cos(angle), math.sin(angle), -4.1))
        arm = curve(col, f"PEL_JELLY_OralArm_{i:02d}", [start, (start+end)*0.5 + Vector((0,0,0.3)), end], 0.11, M_TISSUE, aid, "oral_filter_arm")
        arm["feeding_role"] = "particulate/filter capture proposal"
    for i in range(12):
        angle = math.tau * i / 12
        start = center + Vector((math.cos(angle)*1.35, math.sin(angle)*1.35, -0.5))
        end = center + Vector((math.cos(angle)*2.4, math.sin(angle)*2.4, -7.0 - (i % 3)*0.2))
        socket = empty(col, f"PEL_JELLY_TentacleSocket_{i:02d}", start, aid, "tentacle_socket", root)
        tentacle = curve(col, f"PEL_JELLY_Tentacle_{i:02d}", [start, start + Vector((math.cos(angle)*0.4, math.sin(angle)*0.4, -2.2)), end], 0.055, M_PALE, aid, "sensory_tentacle")
        tentacle["socket"] = socket.name
    for i in range(16):
        angle = math.tau * i / 16
        sphere(col, f"PEL_JELLY_MemoryNode_{i:02d}", center + Vector((math.cos(angle)*1.42, math.sin(angle)*1.42, 0.05 + 0.18*math.sin(angle*2))), (0.22,0.22,0.22), M_MEMORY, aid, "memory_photophore", segments=16, rings=8)
    return aid


def build_eel(col):
    aid = "PEL-ECO-EEL-001"
    center = Vector((-145, 92, 17))
    meta = metadata(
        col, "PEL_EEL_METADATA", center, aid,
        "hunts by following repeated sound",
        {"length_m_proposal": 5.8, "max_body_diameter_m_proposal": 0.72},
        "anguilliform whole-body undulation",
        "flexible cartilage-like vertebral chain, no heavy axial bone",
        "forward jaw + lateral-line resonance organs tuned to repeated acoustic patterns",
        "reef channels; low-drag body and compliant fins",
    )
    meta["measured_visible_bbox_m"] = [6.339, 1.147, 0.92]
    root = empty(col, "PEL_EEL_Root", center, aid, "rig_root", meta)
    spine = []
    for i in range(11):
        point = center + Vector(((i-5)*0.52, 0.20*math.sin(i*0.8), 0.12*math.cos(i*0.6)))
        spine.append(point)
        empty(col, f"PEL_EEL_SpineJoint_{i:02d}", point, aid, "spine_joint", root)
    for i in range(10):
        taper = 0.34 * (1 - abs(i-4.5)/8.0)
        cylinder(col, f"PEL_EEL_BodySeg_{i:02d}", spine[i], spine[i+1], max(0.16, taper), M_PALE, aid, "axial_body_segment", "simple")
    sphere(col, "PEL_EEL_Head", spine[-1] + Vector((0.34,0,0)), (1.05,0.78,0.72), M_PALE, aid, "sensory_head", "simple", 24, 12)
    cube(col, "PEL_EEL_JawUpper", spine[-1] + Vector((0.78,0,0.09)), (0.62,0.42,0.16), M_TISSUE, aid, "jaw_upper", "simple")
    cube(col, "PEL_EEL_JawLower", spine[-1] + Vector((0.78,0,-0.13)), (0.62,0.42,0.12), M_TISSUE, aid, "jaw_lower", "simple")
    for side in (-1, 1):
        for i, point in enumerate(spine[2:10]):
            sphere(col, f"PEL_EEL_LateralNode_{side}_{i:02d}", point + Vector((0, side*0.30, 0)), (0.12,0.12,0.12), M_MEMORY, aid, "lateral_line_resonance_node", segments=12, rings=6)
    curve(col, "PEL_EEL_DorsalFinRail", [p + Vector((0,0,0.32)) for p in spine[1:9]], 0.055, M_PALE, aid, "dorsal_fin_support")
    curve(col, "PEL_EEL_VentralFinRail", [p + Vector((0,0,-0.28)) for p in spine[1:8]], 0.045, M_PALE, aid, "ventral_fin_support")
    return aid


def build_bovid(col):
    aid = "PEL-ECO-BOV-001"
    center = Vector((150, -120, 11))
    meta = metadata(
        col, "PEL_BOV_METADATA", center, aid,
        "maintains reef channels while grazing",
        {"body_length_m_proposal": 4.4, "shoulder_height_m_proposal": 1.9, "mass_class_proposal": "large amphibious grazer"},
        "slow six-limb substrate walking + short buoyant hops",
        "three paired load stations distribute mass on brittle reef",
        "ventral mineralized rasp comb + pressure/vibration sensing pads",
        "shallow reef terraces; broad contact pads reduce substrate damage",
    )
    meta["measured_visible_bbox_m"] = [5.47, 2.72, 2.537]
    root = empty(col, "PEL_BOV_Root", center, aid, "rig_root", meta)
    sphere(col, "PEL_BOV_Torso", center + Vector((0,0,1.15)), (4.4,1.95,1.8), M_TISSUE, aid, "torso_mass", "simple", 32, 16)
    sphere(col, "PEL_BOV_Head", center + Vector((2.15,0,0.95)), (1.45,1.35,1.15), M_TISSUE, aid, "grazing_head", "simple", 24, 12)
    cube(col, "PEL_BOV_RaspPlate", center + Vector((2.62,0,0.48)), (0.85,1.08,0.18), M_RASP, aid, "ventral_rasp_plate", "simple")
    for i in range(7):
        y = -0.42 + i*0.14
        cone(col, f"PEL_BOV_RaspTooth_{i:02d}", center + Vector((3.00,y,0.50)), center + Vector((3.24,y,0.36)), 0.06, 0.025, M_MINERAL, aid, "rasp_tooth", vertices=10)
    for pair, x in enumerate((-1.35, 0.0, 1.35)):
        for side in (-1, 1):
            hip = center + Vector((x, side*0.82, 1.35))
            knee = center + Vector((x + 0.12*(1 if pair == 2 else -1), side*1.02, 0.62))
            foot = center + Vector((x + 0.18, side*1.12, 0.08))
            empty(col, f"PEL_BOV_Hip_{pair}_{side}", hip, aid, "limb_root_joint", root)
            empty(col, f"PEL_BOV_Knee_{pair}_{side}", knee, aid, "limb_joint", root)
            cylinder(col, f"PEL_BOV_UpperLeg_{pair}_{side}", hip, knee, 0.20, M_TISSUE, aid, "upper_limb", "simple", 14)
            cylinder(col, f"PEL_BOV_LowerLeg_{pair}_{side}", knee, foot, 0.16, M_TISSUE, aid, "lower_limb", "simple", 14)
            sphere(col, f"PEL_BOV_FootPad_{pair}_{side}", foot, (0.62,0.48,0.20), M_MINERAL, aid, "broad_reef_contact_pad", "simple", 16, 8)
    for i, x in enumerate((-1.2, -0.4, 0.4, 1.2)):
        plate = cube(col, f"PEL_BOV_VibrationPlate_{i:02d}", center + Vector((x,0,2.10)), (0.48,0.18,0.72), M_MEMORY, aid, "vibration_sensory_plate")
        plate.rotation_euler.y = math.radians(12*(i-1.5))
    return aid


def build_scribe(col):
    aid = "PEL-ECO-SCRIBE-001"
    center = Vector((210, -20, 4))
    meta = metadata(
        col, "PEL_SCRIBE_METADATA", center, aid,
        "incorporates vibration into its growth",
        {"hero_colony_height_nominal_proposal_m": 6.8, "hero_colony_diameter_m_proposal": 5.4},
        "sessile growth; no locomotion",
        "mineralized basal plate + compliant branched tissue",
        "mechanosensory growth plates record repeated vibration as branch/ring morphology",
        "high-flow reef channel edges; growth orientation uses local-flow proposal from PEL/BIOME/007",
    )
    meta["measured_visible_bbox_m"] = [5.57, 5.57, 7.18]
    meta["hero_colony_visible_bbox_height_measured_m"] = 7.18
    meta["height_discrepancy_status"] = "DOCUMENTED_BLOCKOUT_EXTENTS_NOT_CANON_CONFLICT"
    meta["depends_on"] = "PEL/BIOME/007 deterministic coral growth system"
    meta["duplication_control"] = "hero interactive specimen only; background population owned by PEL/BIOME/007"
    sphere(col, "PEL_SCRIBE_BasalColony", center, (4.8,4.8,1.1), M_MINERAL, aid, "mineralized_basal_plate", "simple", 28, 14)
    for branch in range(8):
        angle = math.tau * branch / 8
        base = center + Vector((math.cos(angle)*1.1, math.sin(angle)*1.1, 0.4))
        mid = center + Vector((math.cos(angle)*1.8, math.sin(angle)*1.8, 3.0))
        tip = center + Vector((math.cos(angle)*2.4, math.sin(angle)*2.4, 6.5 - (branch%3)*0.35))
        cylinder(col, f"PEL_SCRIBE_BranchA_{branch:02d}", base, mid, 0.30, M_CORAL, aid, "recording_branch", vertices=14)
        cone(col, f"PEL_SCRIBE_BranchB_{branch:02d}", mid, tip, 0.28, 0.11, M_CORAL, aid, "recording_branch", vertices=14)
        for ring in range(3):
            point = mid.lerp(tip, (ring+1)/4)
            torus(col, f"PEL_SCRIBE_GrowthRing_{branch:02d}_{ring:02d}", point, 0.34 + 0.07*ring, 0.055, M_MEMORY, aid, "vibration_growth_record", (math.pi/2,0,angle))
        sphere(col, f"PEL_SCRIBE_MemoryNode_{branch:02d}", tip, (0.26,0.26,0.26), M_MEMORY, aid, "terminal_memory_node", segments=14, rings=7)
    return aid


def build():
    col = reset_collection()
    hidden = hide_old_proxies()
    assets = [build_jelly(col), build_eel(col), build_bovid(col), build_scribe(col)]
    return {
        "collection": COLLECTION,
        "assets": assets,
        "old_proxy_objects_hidden": hidden,
        "status": "ANATOMY_BLOCKOUT_V1",
        "pending": [
            "lead anatomy review",
            "final organic sculpt/retopology",
            "UV/bake/final biological shaders",
            "armatures/deformation",
            "locomotion/behavior animation",
            "engine collision/hitboxes",
            "LOD/crowd variants",
            "performance",
            "human art review",
        ],
    }


if __name__ == "__main__":
    print(build())
