"""EXOVANT 2950 — LEVIATHAN / LEV-ENM-001 Fagocito guardián representative anatomy v1.

Replaces the master-scene capsule silhouette proxy with an editable, function-driven immune-cell
combat interface while preserving the proxy's approximate gameplay envelope as a REFERENCE only.
No final anatomy, rig, hit/hurt volumes, animation, AI, damage values or attack timing are claimed.

Functional logic:
- central pressure/nuclear body;
- six amoeboid pseudopod lobes for wet locomotion / engulfment;
- forward phagocytosis cup as an explicit gameplay socket;
- dorsal chemo-pressure receptor cilia;
- cartilage armor nodules protecting the central body;
- vermilion pulse-expulsor telegraph ring as a readable attack interface;
- explicit sockets for future rig/gameplay binding.

Claim: CLM-W10-WORLD-LEVIATHAN-001
Asset ID: LEV-ENM-001
"""
import bpy
import math
from mathutils import Vector

STAGE = "FAGOCITO_GUARDIAN_REPRESENTATIVE_V1"
ASSET_ID = "LEV-ENM-001"
COLLECTION = "29_COMBAT_FAGOCYTE_GUARDIAN_MICROSET"
ROOT_NAME = "FAGOCITO_GUARDIAN_ROOT"
ORIGIN = Vector((145.0, 10.0, 7.0))
REFERENCE_PROXY_DIMS = (4.2, 4.2, 7.6)


def _mat(name):
    m = bpy.data.materials.get(name)
    if m is None:
        raise RuntimeError(f"Missing material {name}")
    return m


def _link_only(obj, col):
    for c in list(obj.users_collection):
        c.objects.unlink(obj)
    col.objects.link(obj)


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


def _torus(name, loc, major, minor, mat, col, rot=(0,0,0), major_segments=32, minor_segments=10):
    bpy.ops.mesh.primitive_torus_add(major_radius=major, minor_radius=minor, major_segments=major_segments, minor_segments=minor_segments, location=loc, rotation=rot)
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
    o.empty_display_size = 0.12
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

    # Replace the coarse capsule proxy deterministically; cold replay starts from the same master proxy.
    old_proxy = bpy.data.objects.get("FAGOCITO_GUARDIAN_PROXY")
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
        "warm": _mat("LEV_MAT_TISSUE_WARM"),
        "dark": _mat("LEV_MAT_TISSUE_DARK"),
        "mem": _mat("LEV_MAT_MEMBRANE"),
        "cart": _mat("LEV_MAT_CARTILAGE"),
        "lumen": _mat("LEV_MAT_PRESSURE_LUMEN"),
        "hostile": _mat("SIGNAL_VERMILION_HOSTILE"),
        "cyan": _mat("SIGNAL_CYAN_MEMORY"),
    }

    root = bpy.data.objects.new(ROOT_NAME, None)
    root.location = ORIGIN
    root.empty_display_type = 'CUBE'
    root.empty_display_size = 0.35
    col.objects.link(root)
    root["asset_id"] = ASSET_ID
    root["production_state"] = "REPRESENTATIVE_FUNCTIONAL_ANATOMY_NOT_FINAL"
    root["reference_proxy_dims_m"] = REFERENCE_PROXY_DIMS
    root["reference_proxy_status"] = "BLOCKOUT_ENVELOPE_NOT_CANON"
    root["combat_role"] = "IMMUNE_GUARDIAN_PHAGOCYTOSIS_AND_PRESSURE_EXPULSION"
    root["collision_authority"] = "NONE"
    root["hit_hurt_volume_status"] = "NOT_AUTHORED"
    root["rig_status"] = "SOCKETS_ONLY_NO_ARMATURE"
    root["animation_status"] = "NOT_AUTHORED"
    root["gameplay_attack_binding"] = "NOT_AUTHORED"
    root["generator_stage"] = STAGE

    # Core cell body and internal pressure/nuclear read.
    core = _sphere("FG_CORE_BODY", ORIGIN, (4.0,4.0,2.65), mats["warm"], col, 32, 16)
    nucleus = _sphere("FG_PRESSURE_NUCLEUS", ORIGIN + Vector((0,-0.15,0.25)), (1.65,1.65,1.35), mats["lumen"], col, 24, 12)
    dorsal = _sphere("FG_DORSAL_IMMUNE_MANTLE", ORIGIN + Vector((0,0,1.05)), (3.1,3.1,0.9), mats["mem"], col, 28, 14)
    for o in (core,nucleus,dorsal):
        o["asset_id"] = ASSET_ID
        o["collision_authority"] = "NONE"

    # Six radial pseudopod lobes: locomotion and engulfment surfaces.
    pseudopod_centers=[]
    for i in range(6):
        a = math.radians(i*60.0)
        radial = Vector((math.cos(a), math.sin(a), 0))
        center = ORIGIN + radial*1.72 + Vector((0,0,-0.48))
        pseudopod_centers.append(center)
        o = _sphere(f"FG_PSEUDOPOD_{i}", center, (1.55,1.25,0.72), mats["mem"], col, 20, 10)
        o.rotation_euler.z = a
        o["functional_role"] = "AMOEBOID_LOCOMOTION_AND_ENGULFMENT_LOBE"
        o["collision_authority"] = "NONE"
        _socket(f"FG_SOCKET_PSEUDOPOD_{i}", ORIGIN + radial*1.15 + Vector((0,0,-0.20)), col, f"PSEUDOPOD_{i}_BASE")
        pad = _sphere(f"FG_WET_CONTACT_PAD_{i}", center + radial*0.28 + Vector((0,0,-0.42)), (0.62,0.52,0.16), mats["dark"], col, 16, 8)
        pad["functional_role"] = "WET_TISSUE_TRACTION_PAD"
        pad["collision_authority"] = "NONE"

    # Forward phagocytosis cup (+Y): visual mouth ring and inner lumen.
    mouth_center = ORIGIN + Vector((0,2.02,0.05))
    mouth = _torus("FG_PHAGOCYTOSIS_CUP_RING", mouth_center, 0.92, 0.17, mats["cart"], col, rot=(math.radians(90),0,0), major_segments=36, minor_segments=10)
    lumen = _sphere("FG_PHAGOCYTOSIS_LUMEN", ORIGIN + Vector((0,1.88,0.05)), (1.45,0.42,1.25), mats["dark"], col, 24, 12)
    mouth["functional_role"] = "ENGULFMENT_MOUTH_INTERFACE"; lumen["functional_role"] = "ENGULFMENT_LUMEN_VISUAL"
    _socket("FG_SOCKET_ENGULFMENT", mouth_center + Vector((0,0.20,0)), col, "ENGULFMENT_ATTACK_ORIGIN")

    # Expulsor pulse visual telegraph — interface only, no timing/damage claim.
    pulse = _torus("FG_PULSE_EXPULSOR_TELEGRAPH", ORIGIN + Vector((0,0,0.55)), 2.18, 0.075, mats["hostile"], col, major_segments=40, minor_segments=8)
    pulse["functional_role"] = "PULSE_EXPULSOR_TELEGRAPH_INTERFACE"
    pulse["timing_status"] = "NOT_BOUND_TO_CANON_TELL"
    _socket("FG_SOCKET_PULSE_CENTER", ORIGIN + Vector((0,0,0.55)), col, "PULSE_EXPULSOR_ORIGIN")

    # Cartilage armor nodules around dorsal body.
    for i in range(8):
        a = math.radians(i*45.0 + 22.5)
        p = ORIGIN + Vector((math.cos(a)*1.45, math.sin(a)*1.45, 1.16))
        n = _sphere(f"FG_ARMOR_NODULE_{i}", p, (0.46,0.46,0.34), mats["cart"], col, 16, 8)
        n["functional_role"] = "DORSAL_CARTILAGE_ARMOR_NODULE"
        n["collision_authority"] = "NONE"

    # Four receptor cilia rise toward the original 7.6 m proxy-height envelope.
    receptor_tips=[]
    for i,a_deg in enumerate((30,120,210,300)):
        a=math.radians(a_deg)
        base=ORIGIN + Vector((math.cos(a)*0.85,math.sin(a)*0.85,1.25))
        mid=ORIGIN + Vector((math.cos(a)*1.15,math.sin(a)*1.15,2.25))
        tip=ORIGIN + Vector((math.cos(a)*1.32,math.sin(a)*1.32,3.45))
        receptor_tips.append(tip)
        c=_curve(f"FG_RECEPTOR_CILIUM_{i}",[base,mid,tip],0.045,mats["cyan"],col)
        c["functional_role"]="CHEMO_PRESSURE_RECEPTOR"
        c["collision_authority"]="NONE"
        sensor=_sphere(f"FG_RECEPTOR_NODE_{i}",tip,(0.18,0.18,0.18),mats["cyan"],col,12,6)
        sensor["collision_authority"]="NONE"
        _socket(f"FG_SOCKET_RECEPTOR_{i}",base,col,f"RECEPTOR_{i}_BASE")

    _socket("FG_SOCKET_CORE", ORIGIN, col, "CORE_ROOT")
    _socket("FG_SOCKET_NUCLEUS", ORIGIN + Vector((0,-0.15,0.25)), col, "NUCLEUS_CENTER")

    # Parent art pieces to root while preserving world transforms.
    for o in list(col.objects):
        if o != root:
            mw=o.matrix_world.copy(); o.parent=root; o.matrix_world=mw
            o["asset_id"] = ASSET_ID
            if "collision_authority" not in o:
                o["collision_authority"] = "NONE"

    # Dedicated QA camera; stays in same collection but outside gameplay semantics.
    cam_data=bpy.data.cameras.new("CAM_FAGOCITO_CLOSE_DATA")
    cam=bpy.data.objects.new("CAM_FAGOCITO_CLOSE",cam_data)
    col.objects.link(cam)
    cam.location=ORIGIN + Vector((-8.2,-7.4,4.4))
    cam_data.lens=60
    _look_at(cam,ORIGIN + Vector((0,0,0.65)))
    cam["qa_only"] = True

    scene["fagocito_guardian_stage"] = STAGE
    scene["fagocito_guardian_asset_id"] = ASSET_ID
    scene["fagocito_guardian_final_anatomy_claimed"] = False

    mesh_objs=[o for o in col.all_objects if o.type=='MESH']
    curve_objs=[o for o in col.all_objects if o.type=='CURVE']
    sockets=[o for o in col.all_objects if o.type=='EMPTY' and o.name.startswith('FG_SOCKET_')]
    tris=0
    for o in mesh_objs:
        o.data.calc_loop_triangles(); tris += len(o.data.loop_triangles)
    return {
        "stage": STAGE,
        "asset_id": ASSET_ID,
        "replaced_proxy": proxy_receipt,
        "mesh_objects": len(mesh_objs),
        "curve_objects": len(curve_objs),
        "interface_sockets": len(sockets),
        "native_mesh_triangles": tris,
        "collision_authority": "NONE",
        "status": "REPRESENTATIVE_FUNCTIONAL_ANATOMY_NOT_FINAL",
    }

if __name__ == '__main__':
    print(build())
