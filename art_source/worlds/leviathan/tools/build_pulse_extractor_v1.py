"""EXOVANT 2950 — LEVIATHAN / LEV-ENM-002 Extractor de pulso representative interface v1.

Function-driven hostile extraction apparatus built inside the existing silhouette proxy envelope.
The canon only names "Extractor de pulso"; this generator therefore does NOT claim faction,
origin, mobility, AI, damage, attack cadence or narrative ownership. It expresses the minimum
physical logic required for a pulse/pressure extraction interface:
- three-point wet-tissue anchoring frame;
- central pressure reservoir / collection chamber;
- ventral vascular intake needle and flexible feed;
- upper pressure regulator rings;
- radial siphon conduits;
- hostile vermilion extraction telegraph and cyan diagnostic hijack interface;
- explicit sockets for future gameplay/rig/effects binding.

The original 2.8 x 2.8 x 6 m proxy is a reference envelope only, not canon.
Claim: CLM-W10-WORLD-LEVIATHAN-001
Asset ID: LEV-ENM-002
"""
import bpy
import math
from mathutils import Vector

STAGE = "PULSE_EXTRACTOR_REPRESENTATIVE_V1"
ASSET_ID = "LEV-ENM-002"
COLLECTION = "30_COMBAT_PULSE_EXTRACTOR_MICROSET"
ROOT_NAME = "EXTRACTOR_PULSO_ROOT"
ORIGIN = Vector((80.0, 70.0, 7.0))
REFERENCE_PROXY_DIMS = (2.8, 2.8, 6.0)


def _mat(name):
    m = bpy.data.materials.get(name)
    if m is None:
        raise RuntimeError(f"Required material missing: {name}")
    return m


def _link_only(o, col):
    for c in list(o.users_collection):
        c.objects.unlink(o)
    col.objects.link(o)


def _apply_scale(o):
    bpy.context.view_layer.objects.active = o
    o.select_set(True)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    o.select_set(False)


def _sphere(name, loc, dims, mat, col, seg=24, rings=12):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=rings, radius=1.0, location=loc)
    o = bpy.context.object
    o.name = name
    o.scale = (dims[0]/2, dims[1]/2, dims[2]/2)
    _apply_scale(o)
    _link_only(o, col)
    o.data.materials.append(mat)
    return o


def _cylinder(name, loc, radius, depth, mat, col, vertices=20):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=loc)
    o = bpy.context.object
    o.name = name
    _link_only(o, col)
    o.data.materials.append(mat)
    return o


def _cylinder_between(name, p0, p1, radius, mat, col, vertices=16):
    p0, p1 = Vector(p0), Vector(p1)
    d = p1 - p0
    if d.length <= 1e-6:
        raise RuntimeError(f"Degenerate segment: {name}")
    o = _cylinder(name, (p0+p1)*0.5, radius, d.length, mat, col, vertices)
    o.rotation_mode = 'QUATERNION'
    o.rotation_quaternion = Vector((0,0,1)).rotation_difference(d.normalized())
    o.rotation_mode = 'XYZ'
    return o


def _torus(name, loc, major, minor, mat, col, major_segments=32, minor_segments=10):
    bpy.ops.mesh.primitive_torus_add(major_radius=major, minor_radius=minor, major_segments=major_segments, minor_segments=minor_segments, location=loc)
    o = bpy.context.object
    o.name = name
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
    sp.bezier_points.add(len(pts)-1)
    for bp,p in zip(sp.bezier_points,pts):
        bp.co = p
        bp.handle_left_type = "AUTO"
        bp.handle_right_type = "AUTO"
    o = bpy.data.objects.new(name, cu)
    col.objects.link(o)
    cu.materials.append(mat)
    return o


def _socket(name, loc, col, role):
    o = bpy.data.objects.new(name, None)
    o.empty_display_type = 'SPHERE'
    o.empty_display_size = 0.09
    o.location = loc
    col.objects.link(o)
    o["asset_id"] = ASSET_ID
    o["socket_role"] = role
    o["binding_status"] = "INTERFACE_ONLY_NO_GAMEPLAY_BINDING"
    return o


def _look_at(cam, target):
    cam.rotation_euler = (Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler()


def build():
    scene = bpy.context.scene
    root_col = bpy.data.collections.get("LEV_W10_MASTER")
    if root_col is None:
        raise RuntimeError("LEV_W10_MASTER missing")

    old_proxy = bpy.data.objects.get("EXTRACTOR_PULSO_PROXY")
    proxy_receipt = None
    if old_proxy:
        proxy_receipt = {
            "location": [float(x) for x in old_proxy.location],
            "dimensions": [float(x) for x in old_proxy.dimensions],
            "collections": [c.name for c in old_proxy.users_collection],
        }
        bpy.data.objects.remove(old_proxy, do_unlink=True)

    old = bpy.data.collections.get(COLLECTION)
    if old:
        for o in list(old.all_objects):
            bpy.data.objects.remove(o, do_unlink=True)
        bpy.data.collections.remove(old)
    col = bpy.data.collections.new(COLLECTION)
    root_col.children.link(col)

    mats = {
        "dark": _mat("HUM_MAT_DARK_TECH"),
        "metal": _mat("HUM_MAT_BRUSHED_METAL"),
        "cart": _mat("LEV_MAT_CARTILAGE"),
        "vascular": _mat("LEV_MAT_VASCULAR"),
        "lumen": _mat("LEV_MAT_PRESSURE_LUMEN"),
        "hostile": _mat("SIGNAL_VERMILION_HOSTILE"),
        "cyan": _mat("SIGNAL_CYAN_MEMORY"),
    }

    root = bpy.data.objects.new(ROOT_NAME, None)
    root.location = ORIGIN
    root.empty_display_type = 'CUBE'
    root.empty_display_size = 0.28
    col.objects.link(root)
    root["asset_id"] = ASSET_ID
    root["production_state"] = "REPRESENTATIVE_FUNCTIONAL_INTERFACE_NOT_FINAL"
    root["reference_proxy_dims_m"] = REFERENCE_PROXY_DIMS
    root["reference_proxy_status"] = "BLOCKOUT_ENVELOPE_NOT_CANON"
    root["functional_role"] = "PULSE_PRESSURE_EXTRACTION_INTERFACE"
    root["origin_or_faction"] = "UNSPECIFIED_BY_CURRENT_CANON"
    root["mobility_status"] = "UNKNOWN_NOT_AUTHORED"
    root["collision_authority"] = "NONE"
    root["hit_hurt_volume_status"] = "NOT_AUTHORED"
    root["gameplay_binding"] = "NOT_AUTHORED"
    root["generator_stage"] = STAGE

    # Central column: intentionally kept close to the prior 6 m height envelope.
    base = _cylinder("EX_BASE_COLUMN", ORIGIN + Vector((0,0,-0.25)), 0.72, 4.3, mats["dark"], col, 24)
    chamber = _sphere("EX_PRESSURE_RESERVOIR", ORIGIN + Vector((0,0,0.60)), (1.72,1.72,2.05), mats["lumen"], col, 28, 14)
    upper = _cylinder("EX_UPPER_REGULATOR_CORE", ORIGIN + Vector((0,0,2.30)), 0.44, 1.45, mats["metal"], col, 20)
    for o in (base,chamber,upper):
        o["asset_id"] = ASSET_ID
        o["collision_authority"] = "NONE"

    # Three anchor legs fit within a ~2.8 m reference width.
    for i in range(3):
        a = math.radians(90 + i*120)
        radial = Vector((math.cos(a),math.sin(a),0))
        hip = ORIGIN + radial*0.55 + Vector((0,0,-1.45))
        foot = ORIGIN + radial*1.22 + Vector((0,0,-2.75))
        _cylinder_between(f"EX_ANCHOR_STRUT_{i}", hip, foot, 0.10, mats["metal"], col, 12)
        pad = _sphere(f"EX_ANCHOR_PAD_{i}", foot, (0.48,0.58,0.17), mats["cart"], col, 16, 8)
        pad["functional_role"] = "WET_TISSUE_ANCHOR_PAD"
        pad["collision_authority"] = "NONE"
        _socket(f"EX_SOCKET_ANCHOR_{i}", foot, col, f"ANCHOR_{i}_CONTACT")

    # Ventral intake needle stays inside old vertical extent and is explicitly visual/gameplay interface only.
    intake_top = ORIGIN + Vector((0,0,-1.65))
    intake_tip = ORIGIN + Vector((0,0,-2.95))
    needle = _cylinder_between("EX_VASCULAR_INTAKE_NEEDLE", intake_top, intake_tip, 0.105, mats["vascular"], col, 16)
    needle["functional_role"] = "PULSE_EXTRACTION_INTAKE_INTERFACE"
    needle["penetration_gameplay"] = "NOT_AUTHORED"
    _socket("EX_SOCKET_INTAKE_TIP", intake_tip, col, "INTAKE_TIP")

    # Lower flexible feed bends away from direct straight-line stabbing read; still inside the reference footprint.
    feed = _curve("EX_VASCULAR_FEED", [
        ORIGIN + Vector((0.0,0.0,-1.20)),
        ORIGIN + Vector((0.32,0.18,-0.55)),
        ORIGIN + Vector((0.40,-0.08,0.25)),
        ORIGIN + Vector((0.16,0.0,0.92)),
    ], 0.085, mats["vascular"], col)
    feed["functional_role"] = "EXTRACTED_PULSE_TRANSFER_CONDUIT"
    feed["collision_authority"] = "NONE"

    # Regulator rings + hostile telegraph ring.
    for i,(z,r) in enumerate(((1.65,0.78),(2.25,0.66),(2.78,0.54))):
        ring = _torus(f"EX_PRESSURE_RING_{i}", ORIGIN + Vector((0,0,z)), r, 0.075, mats["cart"], col, 32, 8)
        ring["functional_role"] = "PRESSURE_REGULATOR_RING"
        ring["collision_authority"] = "NONE"
    tele = _torus("EX_EXTRACTION_TELEGRAPH_RING", ORIGIN + Vector((0,0,0.72)), 0.98, 0.065, mats["hostile"], col, 36, 8)
    tele["functional_role"] = "EXTRACTION_TELEGRAPH_INTERFACE"
    tele["timing_status"] = "NOT_AUTHORED"
    _socket("EX_SOCKET_TELEGRAPH_CENTER", ORIGIN + Vector((0,0,0.72)), col, "EXTRACTION_TELEGRAPH_CENTER")

    # Four radial siphon hoses terminate near the central chamber, not in collision.
    for i,a_deg in enumerate((45,135,225,315)):
        a=math.radians(a_deg)
        start=ORIGIN + Vector((math.cos(a)*0.52,math.sin(a)*0.52,0.75))
        mid=ORIGIN + Vector((math.cos(a)*0.92,math.sin(a)*0.92,0.25))
        end=ORIGIN + Vector((math.cos(a)*1.14,math.sin(a)*1.14,-0.58))
        hose=_curve(f"EX_SIPHON_HOSE_{i}",[start,mid,end],0.055,mats["vascular"],col)
        hose["functional_role"]="RADIAL_PULSE_SIPHON"
        hose["collision_authority"]="NONE"
        _socket(f"EX_SOCKET_SIPHON_{i}",end,col,f"SIPHON_{i}_END")

    # Cyan diagnostic hijack rail: semantic signal, not faction proof.
    rail = _curve("EX_DIAGNOSTIC_HIJACK_RAIL", [
        ORIGIN + Vector((0.46,0.0,1.25)),
        ORIGIN + Vector((0.58,0.0,1.90)),
        ORIGIN + Vector((0.38,0.0,2.75)),
    ], 0.035, mats["cyan"], col)
    rail["functional_role"] = "DIAGNOSTIC_SIGNAL_HIJACK_INTERFACE"
    rail["narrative_origin"] = "UNSPECIFIED"
    _socket("EX_SOCKET_DIAGNOSTIC_TOP", ORIGIN + Vector((0.38,0,2.75)), col, "DIAGNOSTIC_INTERFACE")

    # Six small pressure sensors around the reservoir.
    for i in range(6):
        a=math.radians(i*60)
        p=ORIGIN + Vector((math.cos(a)*0.88,math.sin(a)*0.88,0.65))
        s=_sphere(f"EX_PRESSURE_SENSOR_{i}",p,(0.16,0.16,0.16),mats["hostile"],col,12,6)
        s["functional_role"]="PRESSURE_STATUS_SENSOR"
        s["collision_authority"]="NONE"

    _socket("EX_SOCKET_ROOT", ORIGIN, col, "ROOT")
    _socket("EX_SOCKET_RESERVOIR", ORIGIN + Vector((0,0,0.60)), col, "RESERVOIR_CENTER")

    for o in list(col.objects):
        if o != root:
            mw=o.matrix_world.copy(); o.parent=root; o.matrix_world=mw
            o["asset_id"] = ASSET_ID
            if "collision_authority" not in o:
                o["collision_authority"] = "NONE"

    cam_data=bpy.data.cameras.new("CAM_EXTRACTOR_CLOSE_DATA")
    cam=bpy.data.objects.new("CAM_EXTRACTOR_CLOSE",cam_data)
    col.objects.link(cam)
    cam.location=ORIGIN + Vector((-6.8,-7.2,2.7))
    cam_data.lens=68
    _look_at(cam,ORIGIN + Vector((0,0,0.25)))
    cam["qa_only"] = True

    scene["pulse_extractor_stage"] = STAGE
    scene["pulse_extractor_asset_id"] = ASSET_ID
    scene["pulse_extractor_final_design_claimed"] = False

    meshes=[o for o in col.all_objects if o.type=='MESH']
    curves=[o for o in col.all_objects if o.type=='CURVE']
    sockets=[o for o in col.all_objects if o.type=='EMPTY' and o.name.startswith('EX_SOCKET_')]
    tris=0
    for o in meshes:
        o.data.calc_loop_triangles(); tris += len(o.data.loop_triangles)
    return {
        "stage": STAGE,
        "asset_id": ASSET_ID,
        "replaced_proxy": proxy_receipt,
        "mesh_objects": len(meshes),
        "curve_objects": len(curves),
        "interface_sockets": len(sockets),
        "native_mesh_triangles": tris,
        "collision_authority": "NONE",
        "status": "REPRESENTATIVE_FUNCTIONAL_INTERFACE_NOT_FINAL",
    }

if __name__ == '__main__':
    print(build())
