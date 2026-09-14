"""Build Pelagos fauna rig/collision-policy foundations.

Requires build_ecology_anatomy_v1.py output. Blender 5.2+, metres.
Creates locomotion armatures for Medusa mnémica, Anguila de vidrio and Bóvido de arrecife.
Coral escriba intentionally remains static/procedural until an interaction justifies deformation.
No skin weights, locomotion clips, engine physics or final collision semantics are claimed.
"""
import bpy
from mathutils import Vector

ROOT = "PELAGOS_WORLD"
COLLECTION = "55_ECOLOGY_RIGS_V1"


def material(*names):
    for name in names:
        mat = bpy.data.materials.get(name)
        if mat:
            return mat
    return None


def ensure_collection():
    root = bpy.data.collections.get(ROOT)
    if root is None:
        raise RuntimeError("Build Pelagos World Foundation first")
    old = bpy.data.collections.get(COLLECTION)
    if old:
        for obj in list(old.objects):
            bpy.data.objects.remove(obj, do_unlink=True)
        bpy.data.collections.remove(old)
    col = bpy.data.collections.new(COLLECTION)
    root.children.link(col)
    return col


def tag(obj, aid, role, collision="none"):
    obj["asset_id"] = aid
    obj["world"] = "pelagos"
    obj["role"] = role
    obj["production_state"] = "ECOLOGY_RIG_FOUNDATION_V1"
    obj["quality_tier"] = "A"
    obj["collision_intent"] = collision
    return obj


def set_material(obj, mat):
    if mat and hasattr(obj.data, "materials") and not obj.data.materials:
        obj.data.materials.append(mat)


def make_armature(col, name, origin, bones, aid):
    data = bpy.data.armatures.new(name + "_DATA")
    obj = bpy.data.objects.new(name, data)
    col.objects.link(obj)
    obj.location = origin
    tag(obj, aid, "ecology_armature")
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")
    made = {}
    for bname, head_world, tail_world, parent in bones:
        bone = data.edit_bones.new(bname)
        bone.head = Vector(head_world) - Vector(origin)
        bone.tail = Vector(tail_world) - Vector(origin)
        if (bone.tail - bone.head).length < 0.02:
            bone.tail = bone.head + Vector((0, 0, 0.08))
        if parent and parent in made:
            bone.parent = made[parent]
        made[bname] = bone
    bpy.ops.object.mode_set(mode="OBJECT")
    obj.select_set(False)
    return obj


def curve_world_points(obj):
    points = []
    for spline in obj.data.splines:
        if spline.type == "BEZIER":
            local = [bp.co for bp in spline.bezier_points]
        else:
            local = [Vector((p.co.x, p.co.y, p.co.z)) for p in spline.points]
        points.extend([obj.matrix_world @ Vector(p) for p in local])
    return points


def sample_chain(points, max_segments):
    if len(points) < 2:
        return []
    if len(points) <= max_segments + 1:
        return points
    indices = [round(i * (len(points) - 1) / max_segments) for i in range(max_segments + 1)]
    return [points[i] for i in indices]


def move_to(obj, col):
    for old in list(obj.users_collection):
        old.objects.unlink(obj)
    col.objects.link(obj)
    return obj


def hidden_sphere(col, name, loc, scale, aid, role, collision, debug_mat):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=12, ring_count=6, location=loc)
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    move_to(obj, col)
    set_material(obj, debug_mat)
    tag(obj, aid, role, collision)
    obj.hide_render = True
    obj.display_type = "WIRE"
    return obj


def hidden_box(col, name, loc, dims, aid, role, collision, debug_mat):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    move_to(obj, col)
    set_material(obj, debug_mat)
    tag(obj, aid, role, collision)
    obj.hide_render = True
    obj.display_type = "WIRE"
    return obj


def hidden_cylinder_between(col, name, start, end, radius, aid, role, collision, debug_mat):
    start = Vector(start)
    end = Vector(end)
    vector = end - start
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=12,
        radius=radius,
        depth=vector.length,
        location=(start + end) * 0.5,
    )
    obj = bpy.context.object
    obj.name = name
    obj.rotation_euler = vector.to_track_quat("Z", "Y").to_euler()
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    move_to(obj, col)
    set_material(obj, debug_mat)
    tag(obj, aid, role, collision)
    obj.hide_render = True
    obj.display_type = "WIRE"
    return obj


def build_jelly(col, debug_mat):
    aid = "PEL-ECO-JELLY-001"
    origin = Vector((-80, 180, 38))
    bones = [
        ("root", origin, origin + Vector((0, 0, 0.35)), None),
        ("bell", origin - Vector((0, 0, 0.25)), origin + Vector((0, 0, 0.75)), "root"),
    ]
    oral = sorted(
        [o for o in bpy.data.objects if str(o.get("asset_id", "")) == aid and o.get("role") == "oral_filter_arm"],
        key=lambda o: o.name,
    )
    for index, obj in enumerate(oral):
        points = sample_chain(curve_world_points(obj), 2)
        parent = "bell"
        for segment in range(len(points) - 1):
            name = f"oral_{index:02d}_{segment:02d}"
            bones.append((name, points[segment], points[segment + 1], parent))
            parent = name
    tentacles = sorted(
        [o for o in bpy.data.objects if str(o.get("asset_id", "")) == aid and o.get("role") == "sensory_tentacle"],
        key=lambda o: o.name,
    )
    for index, obj in enumerate(tentacles):
        points = sample_chain(curve_world_points(obj), 3)
        parent = "bell"
        for segment in range(len(points) - 1):
            name = f"tentacle_{index:02d}_{segment:02d}"
            bones.append((name, points[segment], points[segment + 1], parent))
            parent = name
    rig = make_armature(col, "PEL_JELLY_RIG", origin, bones, aid)
    rig["rig_policy"] = "bell contraction + oral arm filtering + independent sensory tentacle chains"
    rig["skin_weights"] = "NOT_AUTHORED"
    hidden_sphere(
        col, "PEL_JELLY_QUERY_Bell", origin, (1.8, 1.8, 0.95),
        "PEL-ECO-JELLY-COL", "overlap_query_bell", "overlap_trigger_proposal", debug_mat,
    )
    meta = bpy.data.objects.get("PEL_JELLY_METADATA")
    if meta:
        meta["rig_status"] = f"ARMATURE_FOUNDATION_{len(bones)}_BONES_NO_SKIN_WEIGHTS"
        meta["collision_policy"] = "NON_BLOCKING_BELL_OVERLAP_QUERY_PROPOSAL; tentacles no solid collision"
        meta["locomotion"] = "BELL_PULSATION_PROPOSAL"
    return rig


def build_eel(col, debug_mat):
    aid = "PEL-ECO-EEL-001"
    origin = Vector((-145, 92, 17))
    segments = sorted(
        [o for o in bpy.data.objects if str(o.get("asset_id", "")) == aid and o.get("role") == "axial_body_segment"],
        key=lambda o: o.matrix_world.translation.x,
    )
    head = next(
        (o for o in bpy.data.objects if str(o.get("asset_id", "")) == aid and o.get("role") == "sensory_head"),
        None,
    )
    points = [o.matrix_world.translation.copy() for o in segments]
    if head:
        points.append(head.matrix_world.translation.copy())
    bones = [("root", origin, origin + Vector((0.2, 0, 0)), None)]
    parent = "root"
    for index in range(len(points) - 1):
        name = f"spine_{index:02d}"
        bones.append((name, points[index], points[index + 1], parent))
        parent = name
    rig = make_armature(col, "PEL_ECO_EEL_RIG", origin, bones, aid)
    rig["rig_policy"] = "anguilliform axial chain"
    rig["skin_weights"] = "NOT_AUTHORED"
    if len(points) >= 8:
        for index, (start, end) in enumerate(((points[0], points[3]), (points[3], points[7]), (points[7], points[-1]))):
            hidden_cylinder_between(
                col, f"PEL_ECO_EEL_QUERY_{index}", start, end, 0.34,
                "PEL-ECO-EEL-COL", "overlap_query_segment", "overlap_trigger_proposal", debug_mat,
            )
    meta = bpy.data.objects.get("PEL_EEL_METADATA")
    if meta:
        meta["rig_status"] = f"ARMATURE_FOUNDATION_{len(bones)}_BONES_NO_SKIN_WEIGHTS"
        meta["collision_policy"] = "NON_BLOCKING_COMPOUND_QUERY_PROPOSAL; solid blocking TBD by gameplay"
        meta["locomotion"] = "ANGUILLIFORM_AXIAL_WAVE_PROPOSAL"
    return rig


def build_bovine(col, debug_mat):
    aid = "PEL-ECO-BOV-001"
    origin = Vector((150, -120, 11))
    torso = next(o for o in bpy.data.objects if str(o.get("asset_id", "")) == aid and o.get("role") == "torso_mass")
    head = next(o for o in bpy.data.objects if str(o.get("asset_id", "")) == aid and o.get("role") == "grazing_head")
    torso_center = torso.matrix_world.translation
    head_center = head.matrix_world.translation
    bones = [
        ("root", origin, origin + Vector((0, 0, 0.25)), None),
        ("spine", origin + Vector((0, 0, 0.55)), torso_center + Vector((0.6, 0, 0)), "root"),
        ("neck", torso_center + Vector((1.15, 0, 0.05)), head_center - Vector((0.25, 0, 0)), "spine"),
        ("head", head_center - Vector((0.25, 0, 0)), head_center + Vector((0.35, 0, 0)), "neck"),
    ]
    upper = {o.name.replace("PEL_BOV_UpperLeg_", ""): o for o in bpy.data.objects if str(o.get("asset_id", "")) == aid and o.get("role") == "upper_limb"}
    lower = {o.name.replace("PEL_BOV_LowerLeg_", ""): o for o in bpy.data.objects if str(o.get("asset_id", "")) == aid and o.get("role") == "lower_limb"}
    feet = {o.name.replace("PEL_BOV_FootPad_", ""): o for o in bpy.data.objects if str(o.get("asset_id", "")) == aid and o.get("role") == "broad_reef_contact_pad"}
    for key in sorted(set(upper) & set(lower) & set(feet)):
        upper_center = upper[key].matrix_world.translation
        lower_center = lower[key].matrix_world.translation
        foot_center = feet[key].matrix_world.translation
        hip = Vector((upper_center.x, upper_center.y, torso_center.z - 0.15))
        b1 = "upper_" + key
        b2 = "lower_" + key
        b3 = "foot_" + key
        bones.append((b1, hip, lower_center + Vector((0, 0, 0.25)), "spine"))
        bones.append((b2, lower_center + Vector((0, 0, 0.25)), foot_center + Vector((0, 0, 0.08)), b1))
        bones.append((b3, foot_center + Vector((0, 0, 0.08)), foot_center + Vector((0.28, 0, 0)), b2))
    rig = make_armature(col, "PEL_BOV_RIG", origin, bones, aid)
    rig["rig_policy"] = "six-limb reef-grazing locomotion with torso/head chain"
    rig["skin_weights"] = "NOT_AUTHORED"
    hidden_box(
        col, "PEL_BOV_COLLISION_Torso", torso_center, (4.1, 1.75, 1.65),
        "PEL-ECO-BOV-COL", "blocking_body_proxy_proposal", "compound_blocking_proxy_proposal", debug_mat,
    )
    hidden_sphere(
        col, "PEL_BOV_COLLISION_Head", head_center, (0.72, 0.67, 0.57),
        "PEL-ECO-BOV-COL", "blocking_head_proxy_proposal", "compound_blocking_proxy_proposal", debug_mat,
    )
    meta = bpy.data.objects.get("PEL_BOV_METADATA")
    if meta:
        meta["rig_status"] = f"ARMATURE_FOUNDATION_{len(bones)}_BONES_NO_SKIN_WEIGHTS"
        meta["collision_policy"] = "SIMPLE_BODY_HEAD_COMPOUND_BLOCKING_PROPOSAL; feet/contact behavior engine TBD"
        meta["locomotion"] = "SIX_LIMB_REEF_GRAZER_PROPOSAL"
    return rig


def set_scribe_policy():
    meta = bpy.data.objects.get("PEL_SCRIBE_METADATA")
    if meta:
        meta["rig_status"] = "NO_ARMATURE_BY_DESIGN_STATIC_PROCEDURAL_GROWTH"
        meta["rig_rationale"] = "identity is growth/vibration recording; deformation rig not justified until interaction requires it"
        meta["collision_policy"] = "BACKGROUND_NON_BLOCKING_BY_DEFAULT; hero interaction proxy TBD"
    return meta


def build():
    col = ensure_collection()
    debug = material("PEL_Collision_Debug", "PEL_Hostile_Vermilion", "PEL_MAT_Bronze_Oxidized_Marine")
    jelly = build_jelly(col, debug)
    eel = build_eel(col, debug)
    bovine = build_bovine(col, debug)
    set_scribe_policy()
    return {
        "checkpoint": "PELAGOS-ECOLOGY-RIGS-001",
        "rigs": {
            "jelly": len(jelly.data.bones),
            "glass_eel": len(eel.data.bones),
            "reef_bovine": len(bovine.data.bones),
            "scribe_coral": "NO_ARMATURE_BY_DESIGN",
        },
        "pending": [
            "skin weights/deformation QA", "locomotion clips", "engine behavior/physics",
            "fauna LOD", "engine collision semantics", "performance", "human art review",
        ],
    }


if __name__ == "__main__":
    result = build()
    print(result)
