"""EXOVANT 2950 — LEVIATHAN / LEV-ENM-003 Colonia parasitaria representative system v1.

Represents the canonical parasitic-colony adversary as a multicellular / multinode system instead
of collapsing the concept into one creature. Current canon names the adversary but does not define
its species, cognition, locomotion, AI, damage model or lifecycle. Those remain unclaimed.

Functional production logic:
- one maternal nutrient node;
- six satellite buds around the mother node;
- vascular/hyphal feed network joining satellites to the mother;
- tissue adhesion roots that explain attachment to LEVIATHAN without becoming collision authority;
- dorsal dispersal capsules as a future spawn/effects interface, not an authored gameplay ability;
- necrotic digestion patches + vermilion threat lesions;
- explicit sockets for each bud, dispersal capsule, mother core and feed root.

The original 8.4 x 8.4 x 5 m capsule is only a blockout envelope reference.
Claim: CLM-W10-WORLD-LEVIATHAN-001
Asset ID: LEV-ENM-003
"""
import bpy
import math
from mathutils import Vector

STAGE = "PARASITIC_COLONY_REPRESENTATIVE_V1"
ASSET_ID = "LEV-ENM-003"
COLLECTION = "31_COMBAT_PARASITIC_COLONY_MICROSET"
ROOT_NAME = "COLONIA_PARASITARIA_ROOT"
ORIGIN = Vector((10.0, 150.0, 6.0))
REFERENCE_PROXY_DIMS = (8.4, 8.4, 5.0)


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


def _torus(name, loc, major, minor, mat, col, major_segments=28, minor_segments=8):
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
    for bp,p in zip(sp.bezier_points, pts):
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
    o.empty_display_size = 0.11
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

    old_proxy = bpy.data.objects.get("COLONIA_PARASITARIA_PROXY")
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
        "dark": _mat("LEV_MAT_TISSUE_DARK"),
        "necrotic": _mat("LEV_MAT_NECROTIC"),
        "mem": _mat("LEV_MAT_MEMBRANE"),
        "vascular": _mat("LEV_MAT_VASCULAR"),
        "cart": _mat("LEV_MAT_CARTILAGE"),
        "lumen": _mat("LEV_MAT_PRESSURE_LUMEN"),
        "hostile": _mat("SIGNAL_VERMILION_HOSTILE"),
        "cyan": _mat("SIGNAL_CYAN_MEMORY"),
    }

    root = bpy.data.objects.new(ROOT_NAME, None)
    root.location = ORIGIN
    root.empty_display_type = 'CUBE'
    root.empty_display_size = 0.42
    col.objects.link(root)
    root["asset_id"] = ASSET_ID
    root["production_state"] = "REPRESENTATIVE_MULTINODE_SYSTEM_NOT_FINAL"
    root["reference_proxy_dims_m"] = REFERENCE_PROXY_DIMS
    root["reference_proxy_status"] = "BLOCKOUT_ENVELOPE_NOT_CANON"
    root["functional_role"] = "PARASITIC_NUTRIENT_EXTRACTION_AND_COLONY_PROPAGATION_INTERFACE"
    root["species_or_origin"] = "UNSPECIFIED_BY_CURRENT_CANON"
    root["cognition_status"] = "UNSPECIFIED_BY_CURRENT_CANON"
    root["locomotion_status"] = "NOT_AUTHORED"
    root["collision_authority"] = "NONE"
    root["hit_hurt_volume_status"] = "NOT_AUTHORED"
    root["gameplay_binding"] = "NOT_AUTHORED"
    root["generator_stage"] = STAGE

    # Maternal node stays low and broad, emphasizing colony/system rather than boss-creature silhouette.
    mother = _sphere("PC_MOTHER_NODE", ORIGIN + Vector((0,0,-0.25)), (3.55,3.75,2.35), mats["dark"], col, 32, 16)
    core = _sphere("PC_NUTRIENT_CORE", ORIGIN + Vector((0,0,-0.05)), (1.55,1.55,1.35), mats["lumen"], col, 24, 12)
    mantle = _sphere("PC_NECROTIC_MANTLE", ORIGIN + Vector((0,0,0.65)), (2.65,2.85,0.72), mats["necrotic"], col, 28, 12)
    for o in (mother,core,mantle):
        o["asset_id"] = ASSET_ID
        o["collision_authority"] = "NONE"
    _socket("PC_SOCKET_MOTHER_CORE", ORIGIN + Vector((0,0,-0.05)), col, "MOTHER_CORE")

    # Six satellite buds around radius ~3 m, kept inside the 8.4 m historical footprint.
    bud_centers=[]
    for i in range(6):
        a=math.radians(i*60.0 + 30.0)
        radial=Vector((math.cos(a),math.sin(a),0))
        r=2.85 if i%2==0 else 2.65
        z=-0.48 + 0.14*(i%3)
        p=ORIGIN + radial*r + Vector((0,0,z))
        bud_centers.append(p)
        dims=(1.28 + 0.12*(i%2), 1.18 + 0.10*((i+1)%2), 1.10 + 0.08*(i%3))
        bud=_sphere(f"PC_BUD_{i}",p,dims,mats["mem"],col,20,10)
        bud["functional_role"]="SATELLITE_PARASITIC_BUD"
        bud["collision_authority"]="NONE"
        lesion=_sphere(f"PC_BUD_LESION_{i}",p+Vector((0,0,dims[2]*0.38)),(0.34,0.34,0.18),mats["hostile"],col,14,7)
        lesion["functional_role"]="ACTIVE_THREAT_LESION_SIGNAL"
        lesion["gameplay_status"]="NOT_BOUND"
        _socket(f"PC_SOCKET_BUD_{i}",p,col,f"BUD_{i}_CENTER")
        # Feed network bends above substrate to remain visible.
        mid=(ORIGIN+p)*0.5 + Vector((0,0,0.28 + 0.08*(i%2)))
        feed=_curve(f"PC_FEED_VESSEL_{i}",[ORIGIN+radial*0.85+Vector((0,0,-0.05)),mid,p],0.095,mats["vascular"],col)
        feed["functional_role"]="MOTHER_TO_BUD_NUTRIENT_FEED"
        feed["collision_authority"]="NONE"

    # Three dorsal dispersal capsules remain below proxy max Z=8.5m.
    for i,a_deg in enumerate((90,210,330)):
        a=math.radians(a_deg)
        p=ORIGIN+Vector((math.cos(a)*0.88,math.sin(a)*0.88,1.82))
        capsule=_sphere(f"PC_DISPERSAL_CAPSULE_{i}",p,(0.72,0.72,1.05),mats["cart"],col,20,10)
        cap=_sphere(f"PC_DISPERSAL_SIGNAL_{i}",p+Vector((0,0,0.48)),(0.20,0.20,0.20),mats["hostile"],col,12,6)
        capsule["functional_role"]="DISPERSAL_CAPSULE_INTERFACE"
        capsule["spawn_or_release_gameplay"]="NOT_AUTHORED"
        cap["functional_role"]="DISPERSAL_STATE_SIGNAL"
        cap["gameplay_status"]="NOT_BOUND"
        _socket(f"PC_SOCKET_DISPERSAL_{i}",p+Vector((0,0,0.42)),col,f"DISPERSAL_{i}_RELEASE")

    # Four adhesion roots explain attachment. They remain visual interfaces only.
    for i,a_deg in enumerate((0,90,180,270)):
        a=math.radians(a_deg)
        radial=Vector((math.cos(a),math.sin(a),0))
        start=ORIGIN+radial*1.15+Vector((0,0,-0.80))
        mid=ORIGIN+radial*2.05+Vector((0,0,-1.10))
        end=ORIGIN+radial*3.35+Vector((0,0,-1.55))
        root_curve=_curve(f"PC_ADHESION_ROOT_{i}",[start,mid,end],0.12,mats["necrotic"],col)
        root_curve["functional_role"]="TISSUE_ADHESION_ROOT_VISUAL"
        root_curve["collision_authority"]="NONE"
        pad=_sphere(f"PC_ADHESION_PAD_{i}",end,(0.82,0.62,0.18),mats["necrotic"],col,16,8)
        pad["functional_role"]="ADHESION_CONTACT_PAD"
        pad["collision_authority"]="NONE"
        _socket(f"PC_SOCKET_ADHESION_{i}",end,col,f"ADHESION_{i}_CONTACT")

    # Outer warning rim establishes the colony footprint without claiming an attack radius.
    rim=_torus("PC_COLONY_WARNING_RIM",ORIGIN+Vector((0,0,-1.20)),3.72,0.055,mats["hostile"],col,48,8)
    rim["functional_role"]="COLONY_FOOTPRINT_THREAT_SIGNAL"
    rim["attack_radius_claimed"] = False

    # Cyan memory/diagnostic contact is ambiguous by canon; labelled interface, not origin proof.
    diag=_curve("PC_DIAGNOSTIC_INTRUSION",[
        ORIGIN+Vector((-0.40,0.15,0.30)),
        ORIGIN+Vector((-0.75,0.55,0.95)),
        ORIGIN+Vector((-1.05,0.80,1.42)),
    ],0.04,mats["cyan"],col)
    diag["functional_role"]="DIAGNOSTIC_MEMORY_INTRUSION_INTERFACE"
    diag["origin_implication"]="NONE"
    _socket("PC_SOCKET_DIAGNOSTIC",ORIGIN+Vector((-1.05,0.80,1.42)),col,"DIAGNOSTIC_INTERFACE")

    for o in list(col.objects):
        if o != root:
            mw=o.matrix_world.copy(); o.parent=root; o.matrix_world=mw
            o["asset_id"] = ASSET_ID
            if "collision_authority" not in o:
                o["collision_authority"] = "NONE"

    cam_data=bpy.data.cameras.new("CAM_PARASITIC_COLONY_CLOSE_DATA")
    cam=bpy.data.objects.new("CAM_PARASITIC_COLONY_CLOSE",cam_data)
    col.objects.link(cam)
    cam.location=ORIGIN+Vector((-10.0,-10.5,5.2))
    cam_data.lens=58
    _look_at(cam,ORIGIN+Vector((0,0,0.10)))
    cam["qa_only"] = True

    scene["parasitic_colony_stage"] = STAGE
    scene["parasitic_colony_asset_id"] = ASSET_ID
    scene["parasitic_colony_final_design_claimed"] = False

    meshes=[o for o in col.all_objects if o.type=='MESH']
    curves=[o for o in col.all_objects if o.type=='CURVE']
    sockets=[o for o in col.all_objects if o.type=='EMPTY' and o.name.startswith('PC_SOCKET_')]
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
        "status": "REPRESENTATIVE_MULTINODE_SYSTEM_NOT_FINAL",
    }

if __name__ == '__main__':
    print(build())
