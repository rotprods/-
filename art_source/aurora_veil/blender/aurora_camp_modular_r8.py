"""Aurora Veil — Campamento del Segundo Día modular architecture kit.

Reconstruction source for remote Blender revision 8.
Validated on Blender 5.2. This script is intentionally limited to AUR-ARC-001..004
and AUR-INF-001..003 inside the Aurora scene. It assumes the macro world already
exists. Final PBR/UV/hero art is NOT claimed.
"""
import bpy
import math
from mathutils import Vector

GRID = 4.0
RING_DIAMETER = 48.0
RING_SEGMENTS = 24
REFUGE_BAYS = (4, 3)
REFUGE_FOOTPRINT = (16.0, 12.0)


def ensure_collection(name, parent):
    c = bpy.data.collections.get(name)
    if not c:
        c = bpy.data.collections.new(name)
        parent.children.link(c)
    return c


def move_to(obj, col):
    for current in list(obj.users_collection):
        current.objects.unlink(obj)
    col.objects.link(obj)
    return obj


def mat(name, base, metallic, roughness):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    p = m.node_tree.nodes.get("Principled BSDF")
    p.inputs["Base Color"].default_value = (*base, 1.0)
    p.inputs["Metallic"].default_value = metallic
    p.inputs["Roughness"].default_value = roughness
    return m


def cube_mesh(name, dimensions, material=None):
    bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
    o = bpy.context.object
    o.name = name
    o.dimensions = dimensions
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    o.data.name = name + "_MESH"
    if material:
        o.data.materials.append(material)
    return o


def instance(name, source, location, rotation=(0, 0, 0), col=None):
    o = bpy.data.objects.new(name, source.data)
    o.location = location
    o.rotation_euler = rotation
    if col:
        col.objects.link(o)
    return o


def tag(obj, asset_id, manufacturing):
    obj["asset_id"] = asset_id
    obj["manufacturing"] = manufacturing
    obj["grid_m"] = GRID
    return obj


def build():
    scene = bpy.context.scene
    root = bpy.data.collections.get("AURORA_VEIL_ROOT") or scene.collection
    camp = ensure_collection("02_R01_CAMP", root)
    library = ensure_collection("15_CAMP_MODULE_LIBRARY", root)
    proof = ensure_collection("16_CAMP_MODULAR_PROOF", root)
    qa = ensure_collection("17_CAMP_QA_GUIDES", root)

    for col in (library, proof, qa):
        for obj in list(col.objects):
            bpy.data.objects.remove(obj, do_unlink=True)

    library.hide_render = True
    qa.hide_render = True

    steel = mat("AUR_MAT_STRUCTURAL_GALV_STEEL", (0.12, 0.14, 0.16), 0.92, 0.32)
    ceramic = mat("AUR_MAT_CERAMIC_COMPOSITE_PANEL", (0.48, 0.51, 0.50), 0.03, 0.62)
    epdm = mat("AUR_MAT_EPDM_GASKET", (0.02, 0.024, 0.026), 0.0, 0.86)
    glass = mat("AUR_MAT_DARK_TEMPERED_GLASS", (0.03, 0.07, 0.09), 0.0, 0.10)
    bronze = mat("AUR_MAT_CLOCK_BRONZE_CAL", (0.28, 0.16, 0.06), 0.95, 0.38)
    foundation = mat("AUR_MAT_MINERAL_FOUNDATION", (0.18, 0.19, 0.18), 0.0, 0.84)
    service = mat("AUR_MAT_SERVICE_TRAY", (0.16, 0.17, 0.18), 0.72, 0.47)

    sources = {}
    specs = [
        ("LIB_AUR_ARC_001_FRAME_WALL_4M", (4.0, 0.22, 3.2), steel, "AUR-ARC-001",
         "galvanized welded SHS/rolled sections with field-bolted splice plates"),
        ("LIB_AUR_ARC_002_CERAMIC_PANEL_4M", (3.52, 0.14, 2.7), ceramic, "AUR-ARC-002",
         "ceramic-faced composite cassette on secondary rails with EPDM perimeter gasket"),
        ("LIB_AUR_ARC_002_DOOR_PANEL_4M", (3.72, 0.14, 2.85), ceramic, "AUR-ARC-002",
         "cassette wall variant with serviceable sliding pressure-door opening"),
        ("LIB_AUR_ARC_001_FLOOR_CASSETTE_4X4", (4.0, 4.0, 0.46), steel, "AUR-ARC-001",
         "bolted steel floor cassette with replaceable deck and perimeter beams"),
        ("LIB_AUR_ARC_002_ROOF_CASSETTE_4X4", (4.0, 4.0, 0.28), ceramic, "AUR-ARC-002",
         "insulated ceramic composite roof cassette; field shim sets drainage plane"),
        ("LIB_AUR_ARC_001_FOUNDATION_PAD", (0.9, 0.9, 0.55), foundation, "AUR-ARC-001",
         "precast/mineral grout pad with steel base plate"),
        ("LIB_AUR_INF_002_SERVICE_TRAY_4M", (4.0, 0.5, 0.47), service, "AUR-INF-002",
         "perforated folded-metal cable/utility tray with removable cover"),
        ("LIB_AUR_INF_003_ROUTE_BEACON", (1.4, 0.45, 2.51), steel, "AUR-INF-003",
         "field-replaceable mast + sensor bar; route-recorder interface"),
        ("LIB_AUR_INF_001_CLOCK_SYNC_BASE", (2.2, 2.2, 2.4), foundation, "AUR-INF-001",
         "mineral foundation + sealed service pedestal for mechanical clock head"),
        ("LIB_AUR_ARC_004_SERVICE_GANTRY_4M", (4.0, 1.1, 1.5), steel, "AUR-ARC-004",
         "bolted service walkway and grating envelope with safety rails")
    ]
    for name, dims, material, asset_id, manufacturing in specs:
        src = cube_mesh(name, dims, material)
        tag(src, asset_id, manufacturing)
        move_to(src, library)
        sources[name] = src

    # Ring segment source: 15 degree arc cut from a 48 m outer diameter ring.
    outer_r = RING_DIAMETER / 2.0
    inner_r = 20.4
    height = 2.2
    verts = []
    faces = []
    steps = 6
    half = math.radians(7.5)
    for iz, z in enumerate((-height/2, height/2)):
        for ir, r in enumerate((inner_r, outer_r)):
            for i in range(steps + 1):
                a = -half + (2*half) * i / steps
                verts.append((r*math.cos(a), r*math.sin(a), z))
    # surfaces between four strips
    strip = steps + 1
    for iz in range(2):
        base = iz * 2 * strip
        for i in range(steps):
            faces.append((base+i, base+i+1, base+strip+i+1, base+strip+i))
    for ir in range(2):
        lo = ir*strip
        hi = 2*strip + ir*strip
        for i in range(steps):
            faces.append((lo+i, hi+i, hi+i+1, lo+i+1))
    for i in (0, steps):
        faces.append((i, strip+i, 3*strip+i, 2*strip+i))
    mesh = bpy.data.meshes.new("LIB_AUR_ARC_003_RING_SEG_15D_MESH")
    mesh.from_pydata(verts, [], faces); mesh.update()
    seg = bpy.data.objects.new("LIB_AUR_ARC_003_RING_SEG_15D", mesh)
    library.objects.link(seg); mesh.materials.append(steel)
    tag(seg, "AUR-ARC-003", "rolled/formed ring box segment with bolted end flanges and replaceable covers")
    sources[seg.name] = seg

    flange = cube_mesh("LIB_AUR_ARC_003_RING_FLANGE", (2.4, 0.16, 2.2), steel)
    tag(flange, "AUR-ARC-003", "field-bolted ring splice flange")
    move_to(flange, library); sources[flange.name] = flange

    # Proof refuge on a 4 m grid, deliberately simple and serviceable.
    origin = Vector((-1380.0, 600.0, 4.0))
    floor_src = sources["LIB_AUR_ARC_001_FLOOR_CASSETTE_4X4"]
    roof_src = sources["LIB_AUR_ARC_002_ROOF_CASSETTE_4X4"]
    pad_src = sources["LIB_AUR_ARC_001_FOUNDATION_PAD"]
    frame_src = sources["LIB_AUR_ARC_001_FRAME_WALL_4M"]
    panel_src = sources["LIB_AUR_ARC_002_CERAMIC_PANEL_4M"]
    door_src = sources["LIB_AUR_ARC_002_DOOR_PANEL_4M"]
    tray_src = sources["LIB_AUR_INF_002_SERVICE_TRAY_4M"]

    for ix in range(REFUGE_BAYS[0]):
        for iy in range(REFUGE_BAYS[1]):
            x = origin.x + (ix + 0.5) * GRID
            y = origin.y + (iy + 0.5) * GRID
            instance(f"AUR_REFUGE_FLOOR_{ix}_{iy}", floor_src, (x, y, origin.z), col=proof)
            instance(f"AUR_REFUGE_ROOF_{ix}_{iy}", roof_src, (x, y, origin.z + 3.55), col=proof)

    for ix in range(REFUGE_BAYS[0] + 1):
        for iy in range(REFUGE_BAYS[1] + 1):
            x = origin.x + ix * GRID
            y = origin.y + iy * GRID
            instance(f"AUR_REFUGE_PAD_{ix}_{iy}", pad_src, (x, y, origin.z - 0.5), col=proof)

    # Perimeter frames/envelope. One door on south side.
    for ix in range(REFUGE_BAYS[0]):
        x = origin.x + (ix + 0.5) * GRID
        for side, y, rot in (("S", origin.y, 0), ("N", origin.y + REFUGE_BAYS[1]*GRID, 0)):
            instance(f"AUR_REFUGE_FRAME_{side}_{ix}", frame_src, (x, y, origin.z + 1.8), col=proof)
            src = door_src if side == "S" and ix == 1 else panel_src
            instance(f"AUR_REFUGE_PANEL_{side}_{ix}", src, (x, y, origin.z + 1.8), col=proof)
    for iy in range(REFUGE_BAYS[1]):
        y = origin.y + (iy + 0.5) * GRID
        for side, x in (("W", origin.x), ("E", origin.x + REFUGE_BAYS[0]*GRID)):
            rot = (0, 0, math.radians(90))
            instance(f"AUR_REFUGE_FRAME_{side}_{iy}", frame_src, (x, y, origin.z + 1.8), rot, proof)
            instance(f"AUR_REFUGE_PANEL_{side}_{iy}", panel_src, (x, y, origin.z + 1.8), rot, proof)

    for iy in range(REFUGE_BAYS[1] + 1):
        instance(f"AUR_REFUGE_SERVICE_TRAY_{iy}", tray_src,
                 (origin.x + REFUGE_FOOTPRINT[0]/2, origin.y + iy*GRID, origin.z + 3.1), col=proof)

    root_obj = bpy.data.objects.new("AUR_REFUGE_PROOF_ROOT", None)
    proof.objects.link(root_obj)
    root_obj.location = origin
    root_obj["asset_family"] = "AUR-ARC-001/AUR-ARC-002/AUR-ARC-004"
    root_obj["grid_m"] = GRID
    root_obj["bays"] = list(REFUGE_BAYS)
    root_obj["habitable_footprint_m"] = list(REFUGE_FOOTPRINT)
    root_obj["manufacturing_status"] = "BLOCKOUT_CONTRACT"

    # Replace previous monolithic ring representation with instanced segment proof.
    old = bpy.data.objects.get("AUR_OBSERVATORY_RING")
    if old:
        bpy.data.objects.remove(old, do_unlink=True)
    ring_center = Vector((-1520.0, 475.0, 36.953))
    for i in range(RING_SEGMENTS):
        a = 2*math.pi*i/RING_SEGMENTS
        instance(f"AUR_OBS_RING_SEG_{i:02d}", seg, ring_center, (0, 0, a), camp)
        f = instance(f"AUR_OBS_RING_FLANGE_{i:02d}", flange,
                     (ring_center.x + 22.2*math.cos(a), ring_center.y + 22.2*math.sin(a), ring_center.z),
                     (0, 0, a + math.pi/2), camp)
        f["asset_id"] = "AUR-ARC-003"

    ring_root = bpy.data.objects.new("AUR_OBSERVATORY_RING_MODULAR_ROOT", None)
    camp.objects.link(ring_root)
    ring_root.location = ring_center
    ring_root["asset_id"] = "AUR-ARC-003"
    ring_root["segments"] = RING_SEGMENTS
    ring_root["outer_diameter_m"] = RING_DIAMETER
    ring_root["module_angle_deg"] = 360.0/RING_SEGMENTS

    # Clock sync proof and route beacons.
    clock_src = sources["LIB_AUR_INF_001_CLOCK_SYNC_BASE"]
    beacon_src = sources["LIB_AUR_INF_003_ROUTE_BEACON"]
    instance("AUR_INF_001_CLOCK_SYNC_PROOF", clock_src, (-1188, 624, -3.9), col=camp)
    for idx, loc in enumerate(((-1320, 520, 1), (-1260, 560, 1), (-1210, 610, 1), (-1160, 650, 1))):
        instance(f"AUR_INF_003_ROUTE_BEACON_{idx:02d}", beacon_src, loc, col=camp)

    scene["camp_modular_revision"] = 8
    scene["camp_modular_grid_m"] = GRID
    scene["camp_refuge_footprint_m"] = list(REFUGE_FOOTPRINT)
    scene["camp_ring_segments"] = RING_SEGMENTS
    scene["camp_ring_outer_diameter_m"] = RING_DIAMETER
    scene["status"] = "WAVE2_CAMP_MODULAR_R8"

    return {
        "status": scene["status"],
        "grid_m": GRID,
        "refuge_bays": list(REFUGE_BAYS),
        "refuge_footprint_m": list(REFUGE_FOOTPRINT),
        "ring_segments": RING_SEGMENTS,
        "ring_outer_diameter_m": RING_DIAMETER,
        "source_modules": len(sources)
    }


if __name__ == "__main__":
    print(build())
