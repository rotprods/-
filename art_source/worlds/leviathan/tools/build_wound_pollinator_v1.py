"""EXOVANT 2950 — LEVIATHAN / LEV-ECO-003 wound pollinator representative anatomy v1.

Functional-anatomy proposal for the canonical "Polinizador de herida" ecology role.
This is NOT final creature art, rig, animation, hit geometry or gameplay AI. New physical
measurements are production proposals. The asset has no collision authority.

Design logic:
- low-speed wound/lymph-channel pollination and cicatrization transfer;
- four broad membrane wings for controllable hover inside organic corridors;
- six articulated landing legs with wet-contact pads;
- ventral extensible proboscis for wound-film feeding / transfer;
- paired hind-leg pollen/healing-material baskets;
- antennae and cyan sensory nodes for pressure/chemical sensing;
- explicit articulation socket empties so a later creature/rig owner can replace the proxy
  without reverse-engineering intended joints.

Claim: CLM-W10-WORLD-LEVIATHAN-001
Asset ID: LEV-ECO-003
"""

import bpy
import math
from mathutils import Vector

STAGE = "WOUND_POLLINATOR_REPRESENTATIVE_V1"
ASSET_ID = "LEV-ECO-003"
COLLECTION = "28_R2_WOUND_POLLINATOR_MICROSET"
ROOT_NAME = "R2_HPOLL_ROOT"
ORIGIN = Vector((18.0, 88.0, 13.0))
BODY_LENGTH_M = 2.4   # PROPOSAL
WINGSPAN_M = 4.8      # PROPOSAL


def _mat(name):
    m = bpy.data.materials.get(name)
    if m is None:
        raise RuntimeError(f"Required LEVIATHAN material missing: {name}")
    return m


def _link_only(obj, col):
    for c in list(obj.users_collection):
        c.objects.unlink(obj)
    col.objects.link(obj)


def _apply_scale(obj):
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.select_set(False)


def _sphere(name, loc, dims, mat, col, segments=24, rings=12):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segments, ring_count=rings, radius=1.0, location=loc)
    o = bpy.context.object
    o.name = name
    o.scale = (dims[0] / 2.0, dims[1] / 2.0, dims[2] / 2.0)
    _apply_scale(o)
    _link_only(o, col)
    o.data.materials.append(mat)
    return o


def _cylinder_between(name, p0, p1, radius, mat, col, vertices=16):
    p0, p1 = Vector(p0), Vector(p1)
    d = p1 - p0
    if d.length <= 1e-6:
        raise RuntimeError(f"Degenerate segment {name}")
    mid = (p0 + p1) * 0.5
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=d.length, location=mid)
    o = bpy.context.object
    o.name = name
    o.rotation_mode = 'QUATERNION'
    o.rotation_quaternion = Vector((0, 0, 1)).rotation_difference(d.normalized())
    o.rotation_mode = 'XYZ'
    _link_only(o, col)
    o.data.materials.append(mat)
    return o


def _curve(name, pts, bevel, mat, col):
    cu = bpy.data.curves.new(name + "_CURVE", "CURVE")
    cu.dimensions = "3D"
    cu.resolution_u = 4
    cu.bevel_depth = bevel
    cu.bevel_resolution = 2
    sp = cu.splines.new("BEZIER")
    sp.bezier_points.add(len(pts) - 1)
    for bp, p in zip(sp.bezier_points, pts):
        bp.co = p
        bp.handle_left_type = "AUTO"
        bp.handle_right_type = "AUTO"
    o = bpy.data.objects.new(name, cu)
    col.objects.link(o)
    cu.materials.append(mat)
    return o


def _wing(name, side, fore, col, membrane, cartilage):
    sx = 1.0 if side == "R" else -1.0
    # Local shape around ORIGIN. Four wings differ in fore/aft sweep while sharing a functional root.
    yroot = 0.20 if fore else -0.35
    tip_y = 0.85 if fore else -1.05
    chord = 0.78 if fore else 0.64
    xroot = 0.34 * sx
    xtip = (WINGSPAN_M * 0.5) * sx
    zroot = 0.18
    ztip = 0.28 if fore else 0.10
    local = [
        (xroot, yroot + chord * 0.5, zroot),
        (xtip * 0.72, tip_y + chord * 0.36, ztip + 0.10),
        (xtip, tip_y, ztip),
        (xtip * 0.70, tip_y - chord * 0.42, ztip - 0.06),
        (xroot, yroot - chord * 0.5, zroot - 0.03),
    ]
    thick = 0.035
    verts = []
    for zoff in (+thick * 0.5, -thick * 0.5):
        for x, y, z in local:
            verts.append(tuple(ORIGIN + Vector((x, y, z + zoff))))
    n = len(local)
    faces = []
    faces.append(tuple(range(n)))
    faces.append(tuple(range(2*n - 1, n - 1, -1)))
    for i in range(n):
        j = (i + 1) % n
        faces.append((i, j, n + j, n + i))
    me = bpy.data.meshes.new(name + "_MESH")
    me.from_pydata(verts, [], faces)
    me.update()
    o = bpy.data.objects.new(name, me)
    col.objects.link(o)
    me.materials.append(membrane)
    o["functional_role"] = "CONTROLLED_HOVER_MEMBRANE"
    o["rig_status"] = "STATIC_PROXY_SOCKET_DEFINED"

    # Structural leading-edge vein follows real wing load path.
    _cylinder_between(name + "_LEADING_VEIN", ORIGIN + Vector((xroot, yroot + chord*0.38, zroot)), ORIGIN + Vector((xtip, tip_y, ztip)), 0.045, cartilage, col, 12)
    return o


def _socket(name, loc, col, role):
    o = bpy.data.objects.new(name, None)
    o.empty_display_type = 'SPHERE'
    o.empty_display_size = 0.08
    o.location = loc
    col.objects.link(o)
    o["asset_id"] = ASSET_ID
    o["socket_role"] = role
    o["rig_status"] = "SOCKET_ONLY_NO_ARMATURE"
    return o


def _look_at(cam, target):
    direction = Vector(target) - cam.location
    cam.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()


def build():
    scene = bpy.context.scene
    root_col = bpy.data.collections.get("LEV_W10_MASTER")
    if root_col is None:
        raise RuntimeError("LEV_W10_MASTER missing")
    # Idempotent collection cleanup.
    old = bpy.data.collections.get(COLLECTION)
    if old:
        for o in list(old.all_objects):
            bpy.data.objects.remove(o, do_unlink=True)
        bpy.data.collections.remove(old)
    col = bpy.data.collections.new(COLLECTION)
    root_col.children.link(col)

    mats = {
        "tissue": _mat("LEV_MAT_TISSUE_WARM"),
        "dark": _mat("LEV_MAT_TISSUE_DARK"),
        "cart": _mat("LEV_MAT_CARTILAGE"),
        "mem": _mat("LEV_MAT_MEMBRANE"),
        "vascular": _mat("LEV_MAT_VASCULAR"),
        "cyan": _mat("SIGNAL_CYAN_MEMORY"),
        "alga": _mat("LEV_MAT_ALGA_PRESSURE"),
    }

    root = bpy.data.objects.new(ROOT_NAME, None)
    root.location = ORIGIN
    root.empty_display_type = 'CUBE'
    root.empty_display_size = 0.25
    col.objects.link(root)
    root["asset_id"] = ASSET_ID
    root["production_state"] = "REPRESENTATIVE_FUNCTIONAL_ANATOMY_NOT_FINAL"
    root["dimension_status"] = "PROPOSAL_NOT_CANON"
    root["body_length_m_proposal"] = BODY_LENGTH_M
    root["wingspan_m_proposal"] = WINGSPAN_M
    root["ecology_role"] = "WOUND_POLLINATION_AND_CICATRIZATION_TRANSFER"
    root["collision_authority"] = "NONE"
    root["rig_status"] = "SOCKETS_ONLY_NO_ARMATURE"
    root["animation_status"] = "NOT_AUTHORED"
    root["generator_stage"] = STAGE

    # Body is oriented +Y forward.
    body_parts = [
        _sphere("R2_HPOLL_HEAD", ORIGIN + Vector((0, 1.02, 0.05)), (0.62, 0.62, 0.54), mats["cart"], col),
        _sphere("R2_HPOLL_THORAX", ORIGIN + Vector((0, 0.25, 0.0)), (0.78, 0.86, 0.76), mats["tissue"], col),
        _sphere("R2_HPOLL_ABDOMEN", ORIGIN + Vector((0, -0.68, -0.04)), (0.72, 1.15, 0.64), mats["tissue"], col),
        _sphere("R2_HPOLL_HEALING_RESERVOIR", ORIGIN + Vector((0, -1.05, 0.05)), (0.48, 0.58, 0.44), mats["alga"], col, 20, 10),
    ]
    for o in body_parts:
        o["asset_id"] = ASSET_ID
        o["collision_authority"] = "NONE"
        o["rig_status"] = "STATIC_PROXY"

    # Eyes / chemical-pressure sensors.
    for sx in (-1, 1):
        eye = _sphere(f"R2_HPOLL_EYE_{'L' if sx < 0 else 'R'}", ORIGIN + Vector((0.23*sx, 1.29, 0.12)), (0.16,0.12,0.18), mats["dark"], col, 16, 8)
        sensor = _sphere(f"R2_HPOLL_SENSOR_{'L' if sx < 0 else 'R'}", ORIGIN + Vector((0.34*sx, 1.18, 0.28)), (0.09,0.09,0.09), mats["cyan"], col, 12, 6)
        for o in (eye, sensor):
            o["asset_id"] = ASSET_ID
            o["collision_authority"] = "NONE"

    # Four wings and root sockets.
    for side in ("L", "R"):
        sx = -1 if side == "L" else 1
        for fore in (True, False):
            tag = "FORE" if fore else "HIND"
            _wing(f"R2_HPOLL_WING_{side}_{tag}", side, fore, col, mats["mem"], mats["cart"])
            _socket(f"R2_HPOLL_SOCKET_WING_{side}_{tag}", ORIGIN + Vector((0.34*sx, 0.20 if fore else -0.35, 0.18)), col, f"WING_{side}_{tag}_HINGE")

    # Six legs: coxa -> knee -> wet pad. Hind pair carries transfer baskets.
    leg_y = [0.55, 0.02, -0.55]
    for pair, y in enumerate(leg_y):
        for sx in (-1, 1):
            side = "L" if sx < 0 else "R"
            hip = ORIGIN + Vector((0.32*sx, y, -0.18))
            knee = ORIGIN + Vector((0.68*sx, y + (0.08 if pair == 0 else -0.03), -0.55))
            pad = ORIGIN + Vector((0.92*sx, y + (-0.12 if pair == 2 else 0.10), -0.78))
            _cylinder_between(f"R2_HPOLL_LEG_{pair}_{side}_PROX", hip, knee, 0.055, mats["cart"], col, 12)
            _cylinder_between(f"R2_HPOLL_LEG_{pair}_{side}_DIST", knee, pad, 0.045, mats["mem"], col, 12)
            po = _sphere(f"R2_HPOLL_PAD_{pair}_{side}", pad, (0.22,0.28,0.09), mats["mem"], col, 16, 8)
            po["contact_role"] = "WET_TISSUE_LANDING_PAD"
            po["collision_authority"] = "NONE"
            _socket(f"R2_HPOLL_SOCKET_LEG_{pair}_{side}", hip, col, f"LEG_{pair}_{side}_COXA")
            if pair == 2:
                basket = _sphere(f"R2_HPOLL_TRANSFER_BASKET_{side}", (knee + pad) * 0.5 + Vector((0,0,0.08)), (0.28,0.38,0.24), mats["alga"], col, 16, 8)
                basket["functional_role"] = "POLLEN_CICATRIZATION_TRANSFER_BASKET"
                basket["collision_authority"] = "NONE"

    # Proboscis and antennae are flexible interfaces, not collision.
    prob_pts = [
        ORIGIN + Vector((0,1.28,-0.10)),
        ORIGIN + Vector((0,1.55,-0.35)),
        ORIGIN + Vector((0,1.72,-0.68)),
        ORIGIN + Vector((0,1.58,-0.94)),
    ]
    prob = _curve("R2_HPOLL_PROBOSCIS", prob_pts, 0.038, mats["vascular"], col)
    prob["functional_role"] = "EXTENSIBLE_WOUND_FILM_PROBOSCIS"
    prob["collision_authority"] = "NONE"
    _socket("R2_HPOLL_SOCKET_PROBOSCIS", ORIGIN + Vector((0,1.28,-0.10)), col, "PROBOSCIS_BASE")
    for sx in (-1,1):
        side = "L" if sx < 0 else "R"
        ant = _curve(f"R2_HPOLL_ANTENNA_{side}", [
            ORIGIN + Vector((0.18*sx,1.27,0.25)),
            ORIGIN + Vector((0.38*sx,1.62,0.42)),
            ORIGIN + Vector((0.52*sx,1.88,0.50)),
        ], 0.025, mats["cyan"], col)
        ant["functional_role"] = "PRESSURE_CHEMICAL_SENSOR"
        ant["collision_authority"] = "NONE"
        _socket(f"R2_HPOLL_SOCKET_ANTENNA_{side}", ORIGIN + Vector((0.18*sx,1.27,0.25)), col, f"ANTENNA_{side}_BASE")

    _socket("R2_HPOLL_SOCKET_ABDOMEN", ORIGIN + Vector((0,-0.18,0.0)), col, "ABDOMEN_HINGE")

    # Parent microset objects to root while preserving world transforms; sockets remain explicit children too.
    for o in list(col.objects):
        if o != root:
            mw = o.matrix_world.copy()
            o.parent = root
            o.matrix_world = mw
            o["asset_id"] = ASSET_ID
            if "collision_authority" not in o:
                o["collision_authority"] = "NONE"

    # Dedicated QA framing, portable and non-gameplay.
    cam_data = bpy.data.cameras.new("CAM_R2_POLLINATOR_CLOSE_DATA")
    cam = bpy.data.objects.new("CAM_R2_POLLINATOR_CLOSE", cam_data)
    col.objects.link(cam)
    cam.location = ORIGIN + Vector((-5.6, -6.2, 2.8))
    cam_data.lens = 68
    _look_at(cam, ORIGIN + Vector((0,0.15,-0.05)))
    cam["qa_only"] = True

    scene["wound_pollinator_stage"] = STAGE
    scene["wound_pollinator_asset_id"] = ASSET_ID
    scene["wound_pollinator_dimensions_final_claimed"] = False

    # Return measured source counts; final QA evaluates modifiers/curve tessellation separately.
    mesh_objs = [o for o in col.all_objects if o.type == 'MESH']
    curve_objs = [o for o in col.all_objects if o.type == 'CURVE']
    sockets = [o for o in col.all_objects if o.type == 'EMPTY' and o.name.startswith("R2_HPOLL_SOCKET_")]
    tris = 0
    for o in mesh_objs:
        o.data.calc_loop_triangles()
        tris += len(o.data.loop_triangles)
    return {
        "stage": STAGE,
        "asset_id": ASSET_ID,
        "collection": COLLECTION,
        "proposal_body_length_m": BODY_LENGTH_M,
        "proposal_wingspan_m": WINGSPAN_M,
        "mesh_objects": len(mesh_objs),
        "curve_objects": len(curve_objs),
        "rig_socket_count": len(sockets),
        "native_mesh_triangles": tris,
        "collision_authority": "NONE",
        "status": "REPRESENTATIVE_FUNCTIONAL_ANATOMY_NOT_FINAL",
    }


if __name__ == "__main__":
    print(build())
