"""AURORA VEIL / EXOVANT-X100 — Campamento systemic settlement generator.

Workunit: AUR-X100-CAMP-SYSTEMIC-001
Validated remote scene: Blender 5.2, revision 23.
Parent claim: CLM-AURORA-WORLD-001.

Purpose
-------
Build a deterministic, manufacturing-aware settlement family for Campamento del
Segundo Dia. The multiplier is the grammar: 24 source modules, 3 footprint
patterns, 4 facade patterns, 3 roof/service patterns and 4 authored history
states = 144 controlled combinations. Only twelve representative configurations
are instantiated as proof.

This script intentionally does NOT:
- modify AEON hero content;
- invent global geography/canon;
- implement engine-specific LOD/HLOD or collision;
- claim final UV/PBR/texture/art/performance quality.

The source/LOD meshes live as fake-user datablocks in the .blend. Beauty/exchange
GLB receives only the proof district, while LOD/collision source contracts remain
metadata until EXO-012 resolves the production engine.
"""
import bpy
import math
from mathutils import Vector

WORKUNIT = "AUR-X100-CAMP-SYSTEMIC-001"
ROOT_COLLECTION = "AURORA_VEIL_ROOT"
COLLECTIONS = {
    "library": "25_X100_CAMP_LIBRARY",
    "states": "26_X100_CAMP_STATES",
    "contracts": "27_X100_CAMP_LOD_COLLISION",
    "proof": "28_X100_CAMP_DISTRICT_PROOF",
    "qa": "29_X100_CAMP_QA",
}
THEORETICAL_CONFIGS = 144

MODULE_SPECS = {
    "wall_solid": ("AUR_X100_ARC_WALL_SOLID_4M", (4.0, 0.22, 3.2), "AUR_MAT_CERAMIC_COMPOSITE_PANEL", "AUR-ARC-003-WALL-SOLID-4M", "envelope", "ceramic-faced composite cassette on galvanized rail frame"),
    "wall_window": ("AUR_X100_ARC_WALL_WINDOW_4M", (4.0, 0.24, 3.2), "AUR_MAT_DARK_TEMPERED_GLASS", "AUR-ARC-003-WALL-WINDOW-4M", "envelope", "laminated tempered glazing cassette with replaceable perimeter gasket"),
    "wall_service": ("AUR_X100_ARC_WALL_SERVICE_4M", (4.0, 0.28, 3.2), "AUR_MAT_SERVICE_TRAY", "AUR-ARC-003-WALL-SERVICE-4M", "envelope", "removable folded-metal service cassette with inspection access"),
    "airlock": ("AUR_X100_ARC_AIRLOCK_4M", (4.0, 1.15, 3.2), "AUR_MAT_STRUCTURAL_GALV_STEEL", "AUR-ARC-003-AIRLOCK-4M", "access", "field-bolted vestibule frame with serviceable sliding pressure-door leaves"),
    "floor4": ("AUR_X100_ARC_FLOOR_4X4", (4.0, 4.0, 0.46), "AUR_MAT_STRUCTURAL_GALV_STEEL", "AUR-ARC-003-FLOOR-4X4", "structure", "bolted steel cassette with replaceable walking deck"),
    "floor2": ("AUR_X100_ARC_FLOOR_4X2", (4.0, 2.0, 0.46), "AUR_MAT_STRUCTURAL_GALV_STEEL", "AUR-ARC-003-FLOOR-4X2", "structure", "half-bay steel floor cassette for transition/service bays"),
    "roof4": ("AUR_X100_ARC_ROOF_FLAT_4X4", (4.0, 4.0, 0.28), "AUR_MAT_CERAMIC_COMPOSITE_PANEL", "AUR-ARC-003-ROOF-FLAT-4X4", "roof", "insulated ceramic composite roof cassette with shim-set drainage fall"),
    "roof_vent": ("AUR_X100_ARC_ROOF_SERVICE_4X4", (4.0, 4.0, 0.38), "AUR_MAT_SERVICE_TRAY", "AUR-ARC-003-ROOF-SERVICE-4X4", "roof", "service roof cassette with removable equipment curb"),
    "corner": ("AUR_X100_ARC_CORNER_POST", (0.32, 0.32, 3.35), "AUR_MAT_STRUCTURAL_GALV_STEEL", "AUR-ARC-003-CORNER-POST", "structure", "galvanized SHS corner post with field-bolted splice plates"),
    "stair": ("AUR_X100_ARC_STAIR_4M", (4.0, 1.3, 1.8), "AUR_MAT_STRUCTURAL_GALV_STEEL", "AUR-ARC-003-STAIR-4M", "traversal", "shop-welded stair stringers with replaceable anti-slip treads"),
    "ladder": ("AUR_X100_ARC_LADDER_3M", (0.65, 0.28, 3.0), "AUR_MAT_STRUCTURAL_GALV_STEEL", "AUR-ARC-003-LADDER-3M", "traversal", "galvanized rung ladder with stand-off brackets"),
    "parapet": ("AUR_X100_ARC_PARAPET_4M", (4.0, 0.12, 1.05), "AUR_MAT_STRUCTURAL_GALV_STEEL", "AUR-ARC-003-PARAPET-4M", "safety", "bolted guard-rail envelope; open production geometry deferred"),
    "bridge": ("AUR_X100_ARC_BRIDGE_8M", (8.0, 1.6, 0.42), "AUR_MAT_STRUCTURAL_GALV_STEEL", "AUR-ARC-003-BRIDGE-8M", "traversal", "bolted twin-stringer service bridge with removable grating deck"),
    "pier": ("AUR_X100_ARC_ADJUSTABLE_PIER", (0.55, 0.55, 1.2), "AUR_MAT_STRUCTURAL_GALV_STEEL", "AUR-ARC-003-ADJUSTABLE-PIER", "foundation", "telescopic galvanized pier over mineral grout pad"),
    "tray": ("AUR_X100_INF_TRAY_STRAIGHT_4M", (4.0, 0.48, 0.32), "AUR_MAT_SERVICE_TRAY", "AUR-INF-003-TRAY-STRAIGHT-4M", "utility", "perforated folded-metal service tray with removable cover"),
    "tray_elbow": ("AUR_X100_INF_TRAY_ELBOW_90", (1.8, 1.8, 0.32), "AUR_MAT_SERVICE_TRAY", "AUR-INF-003-TRAY-ELBOW-90", "utility", "factory elbow tray with bolted splice flanges"),
    "junction": ("AUR_X100_INF_SERVICE_JUNCTION", (1.1, 0.7, 1.35), "AUR_MAT_SERVICE_TRAY", "AUR-INF-003-SERVICE-JUNCTION", "utility", "sealed junction cabinet with segregated power/data gland plates"),
    "power": ("AUR_X100_INF_POWER_CAB", (1.4, 0.65, 1.9), "AUR_MAT_SERVICE_TRAY", "AUR-INF-003-POWER-CAB", "utility", "vented folded-metal power cabinet on replaceable plinth"),
    "data": ("AUR_X100_INF_DATA_CAB", (1.05, 0.58, 1.55), "AUR_MAT_SERVICE_TRAY", "AUR-INF-003-DATA-CAB", "utility", "sealed instrumentation/data cabinet with maintenance door"),
    "scupper": ("AUR_X100_INF_DRAIN_SCUPPER", (0.55, 0.9, 0.35), "AUR_MAT_SERVICE_TRAY", "AUR-INF-003-DRAIN-SCUPPER", "utility", "formed drainage scupper directing roof runoff away from foundations"),
    "crate": ("AUR_X100_PRP_STORAGE_CRATE", (1.2, 0.8, 0.72), "AUR_MAT_STRUCTURAL_GALV_STEEL", "AUR-PRP-001-STORAGE-CRATE", "prop", "stackable folded-metal logistics crate with replaceable latch panel"),
    "bench": ("AUR_X100_PRP_FIELD_BENCH", (2.1, 0.75, 0.85), "AUR_MAT_STRUCTURAL_GALV_STEEL", "AUR-PRP-001-FIELD-BENCH", "prop", "welded maintenance bench with sacrificial work surface"),
    "kiosk": ("AUR_X100_PRP_CLOCK_KIOSK", (1.6, 1.1, 2.4), "AUR_MAT_CLOCK_BRONZE_CAL", "AUR-PRP-002-CLOCK-KIOSK", "cultural", "calibrated clock-market kiosk shell; mechanical face serviced from rear"),
    "trolley": ("AUR_X100_PRP_SERVICE_TROLLEY", (1.5, 0.75, 1.05), "AUR_MAT_SERVICE_TRAY", "AUR-PRP-001-SERVICE-TROLLEY", "prop", "maintenance trolley frame with modular tool/cable drawers"),
}

LOD_KEYS = ("pier", "airlock", "roof4", "wall_solid", "tray", "crate")
FOOTPRINTS = ((2, 2), (3, 2), (3, 3))
FACADE_PATTERNS = (
    ("wall_solid", "wall_window"),
    ("wall_window", "wall_service"),
    ("wall_solid", "wall_service"),
    ("wall_window", "wall_solid", "wall_service"),
)
ROOF_PATTERNS = (("roof4",), ("roof4", "roof_vent"), ("roof_vent",))
STATES = ("PRISTINE", "USED", "DAMAGED", "ABANDONED")
PROOF_X = (-1780.0, -1660.0, -1540.0, -1420.0)
PROOF_Y = (650.0, 760.0, 870.0)


def ensure_collection(name, parent):
    c = bpy.data.collections.get(name)
    if c is None:
        c = bpy.data.collections.new(name)
        parent.children.link(c)
    return c


def clear_collection_objects(collection):
    for obj in list(collection.objects):
        bpy.data.objects.remove(obj, do_unlink=True)


def simple_box_mesh(name, dims, material):
    dx, dy, dz = (d * 0.5 for d in dims)
    verts = [
        (-dx, -dy, -dz), (dx, -dy, -dz), (dx, dy, -dz), (-dx, dy, -dz),
        (-dx, -dy, dz), (dx, -dy, dz), (dx, dy, dz), (-dx, dy, dz),
    ]
    faces = [(0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(2,6,7,3),(4,0,3,7)]
    mesh = bpy.data.meshes.get(name + "_MESH") or bpy.data.meshes.new(name + "_MESH")
    mesh.clear_geometry()
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    if material and len(mesh.materials) == 0:
        mesh.materials.append(material)
    mesh.use_fake_user = True
    return mesh


def resolve_material(name):
    material = bpy.data.materials.get(name)
    if material is None:
        material = bpy.data.materials.new(name)
        material.use_nodes = True
        bsdf = material.node_tree.nodes.get("Principled BSDF")
        bsdf.inputs["Base Color"].default_value = (0.18, 0.19, 0.20, 1.0)
        bsdf.inputs["Roughness"].default_value = 0.55
    return material


def terrain_sampler():
    terrain = bpy.data.objects.get("AURORA_MACRO_TERRAIN")
    if terrain is None:
        raise RuntimeError("AURORA_MACRO_TERRAIN is required")
    vertices = [terrain.matrix_world @ vertex.co for vertex in terrain.data.vertices]
    def sample(x, y):
        point = min(vertices, key=lambda p: (p.x - x) ** 2 + (p.y - y) ** 2)
        return point.z
    return sample


def make_instance(mesh, name, collection, parent, location, rotation_z=0.0, scale=(1,1,1), props=None):
    obj = bpy.data.objects.new(name, mesh)
    collection.objects.link(obj)
    obj.parent = parent
    obj.location = location
    obj.rotation_euler[2] = rotation_z
    obj.scale = scale
    obj["x100_workunit"] = WORKUNIT
    if props:
        for key, value in props.items():
            obj[key] = value
    return obj


def make_collision_contract(collection, name, world_location, dims, policy="SOLID_SIMPLE_PROXY"):
    obj = bpy.data.objects.new("META_COL_" + name, None)
    collection.objects.link(obj)
    obj.location = world_location
    obj.empty_display_type = "CUBE"
    obj.empty_display_size = max(dims) * 0.5
    obj["collision_proxy"] = True
    obj["dimensions_m"] = list(dims)
    obj["policy"] = policy
    obj["engine_status"] = "CONTRACT_ONLY_EXO_012_BLOCKED"
    obj["x100_workunit"] = WORKUNIT
    return obj


def build_source_library(library, contract_collection):
    meshes = {}
    source_meta = {}
    for key, (name, dims, material_name, asset_id, family, manufacturing) in MODULE_SPECS.items():
        mesh = simple_box_mesh(name, dims, resolve_material(material_name))
        meshes[key] = mesh
        source_meta[key] = {
            "mesh": mesh.name,
            "asset_id": asset_id,
            "family": family,
            "dimensions_m": dims,
            "manufacturing": manufacturing,
        }
        meta = bpy.data.objects.new("META_" + name, None)
        library.objects.link(meta)
        meta["asset_id"] = asset_id
        meta["family"] = family
        meta["mesh_datablock"] = mesh.name
        meta["dimensions_m"] = list(dims)
        meta["manufacturing"] = manufacturing
        meta["source_module"] = True
        meta["x100_workunit"] = WORKUNIT

    # LOD contract: current sources are already blockout-low-poly. Preserve identical envelope;
    # future production meshes remove tertiary detail inside that envelope.
    for key in LOD_KEYS:
        name, dims, material_name, asset_id, family, manufacturing = MODULE_SPECS[key]
        for lod in ("LOD0", "LOD1", "LOD2"):
            mesh = simple_box_mesh(name + "_" + lod, dims, resolve_material(material_name))
            meta = bpy.data.objects.new("META_" + name + "_" + lod, None)
            contract_collection.objects.link(meta)
            meta["asset_id"] = asset_id
            meta["lod"] = lod
            meta["mesh_datablock"] = mesh.name
            meta["dimensions_m"] = list(dims)
            meta["lod_policy"] = "preserve silhouette/opening envelope; remove tertiary service detail first"
            meta["lod_geometry_status"] = "ENVELOPE_PRESERVED; production decimation deferred"
            meta["x100_workunit"] = WORKUNIT
    return meshes, source_meta


def build_state_contracts(state_collection):
    causes = {
        "PRISTINE": "new/recently serviced",
        "USED": "contact and maintenance wear concentrated at service access",
        "DAMAGED": "localized impact/overload followed by temporary stabilization",
        "ABANDONED": "maintenance ceased; removable components salvaged or missing",
    }
    for key in ("wall_solid", "airlock", "power", "crate"):
        spec = MODULE_SPECS[key]
        for state in STATES:
            obj = bpy.data.objects.new(f"META_{spec[0]}_STATE_{state}", None)
            state_collection.objects.link(obj)
            obj["asset_id"] = spec[3]
            obj["state"] = state
            obj["state_cause"] = causes[state]
            obj["export_policy"] = "metadata/source recipe in Blend; proof geometry lives in district"
            obj["x100_workunit"] = WORKUNIT


def build_proof_district(meshes, proof_collection, contract_collection, sample_terrain):
    foundation_pad = bpy.data.meshes.get("LIB_AUR_ARC_003_FOUNDATION_PAD_MESH")
    configs = []
    state_detail_counts = {state: 0 for state in STATES}
    collision_contracts = 0
    instance_count = 0

    for row, y in enumerate(PROOF_Y):
        for col, x in enumerate(PROOF_X):
            index = row * 4 + col
            bays_x, bays_y = FOOTPRINTS[index % len(FOOTPRINTS)]
            facade = FACADE_PATTERNS[index % len(FACADE_PATTERNS)]
            roof_pattern = ROOF_PATTERNS[index % len(ROOF_PATTERNS)]
            state = STATES[(index // 3) % len(STATES)]

            terrain_samples = []
            for ix in range(bays_x):
                for iy in range(bays_y):
                    lx = (ix - (bays_x - 1) * 0.5) * 4.0
                    ly = (iy - (bays_y - 1) * 0.5) * 4.0
                    terrain_samples.append(sample_terrain(x + lx, y + ly))
            for sx in (-1, 1):
                for sy in (-1, 1):
                    terrain_samples.append(sample_terrain(x + sx * bays_x * 2.0, y + sy * bays_y * 2.0))
            floor_bottom = max(terrain_samples) + 0.35

            root = bpy.data.objects.new(f"AUR_X100_CAMP_CONFIG_{index:02d}", None)
            proof_collection.objects.link(root)
            root.location = (x, y, floor_bottom)
            root["config_id"] = f"AUR-X100-CFG-{index:02d}"
            root["footprint_bays"] = [bays_x, bays_y]
            root["grid_m"] = 4.0
            root["facade_pattern"] = ",".join(facade)
            root["roof_pattern"] = ",".join(roof_pattern)
            root["history_state"] = state
            root["platform_floor_bottom_z"] = floor_bottom
            root["theoretical_family_space"] = THEORETICAL_CONFIGS
            root["history_geometry_revision"] = 23
            root["era_0"] = "factory-built galvanized frame + ceramic cassette settlement module"
            root["x100_workunit"] = WORKUNIT

            roof_objects = []
            for ix in range(bays_x):
                for iy in range(bays_y):
                    lx = (ix - (bays_x - 1) * 0.5) * 4.0
                    ly = (iy - (bays_y - 1) * 0.5) * 4.0
                    make_instance(meshes["floor4"], f"{root.name}_FLOOR_{ix}_{iy}", proof_collection, root, (lx, ly, 0.23))
                    roof_key = roof_pattern[(ix + iy) % len(roof_pattern)]
                    roof = make_instance(meshes[roof_key], f"{root.name}_ROOF_{ix}_{iy}", proof_collection, root, (lx, ly, 3.80))
                    roof_objects.append(roof)
                    instance_count += 2

            wall_z = 2.06
            for ix in range(bays_x):
                lx = (ix - (bays_x - 1) * 0.5) * 4.0
                south_key = "airlock" if ix == bays_x // 2 else facade[(index + ix) % len(facade)]
                make_instance(meshes[south_key], f"{root.name}_S_{ix}", proof_collection, root, (lx, -bays_y * 2.0, wall_z))
                make_instance(meshes[facade[(index + ix + 1) % len(facade)]], f"{root.name}_N_{ix}", proof_collection, root, (lx, bays_y * 2.0, wall_z))
                instance_count += 2
            for iy in range(bays_y):
                ly = (iy - (bays_y - 1) * 0.5) * 4.0
                make_instance(meshes[facade[(index + iy + 2) % len(facade)]], f"{root.name}_W_{iy}", proof_collection, root, (-bays_x * 2.0, ly, wall_z), math.radians(90))
                make_instance(meshes[facade[(index + iy + 3) % len(facade)]], f"{root.name}_E_{iy}", proof_collection, root, (bays_x * 2.0, ly, wall_z), math.radians(90))
                instance_count += 2

            pier_lengths = []
            for sx in (-1, 1):
                for sy in (-1, 1):
                    lx, ly = sx * bays_x * 2.0, sy * bays_y * 2.0
                    ground = sample_terrain(x + lx, y + ly)
                    pier_bottom = ground + 0.08
                    length = max(0.25, floor_bottom - pier_bottom)
                    pier_lengths.append(length)
                    make_instance(
                        meshes["pier"], f"{root.name}_PIER_{sx}_{sy}", proof_collection, root,
                        (lx, ly, (pier_bottom + floor_bottom) * 0.5 - floor_bottom),
                        scale=(1, 1, length / 1.2),
                        props={"adjusted_length_m": length, "terrain_contact_z": ground},
                    )
                    instance_count += 1
                    if foundation_pad:
                        pad = bpy.data.objects.new(f"{root.name}_PAD_{sx}_{sy}", foundation_pad)
                        proof_collection.objects.link(pad)
                        pad.parent = root
                        pad.location = (lx, ly, ground + 0.275 - floor_bottom)
                        pad["x100_workunit"] = WORKUNIT
                        instance_count += 1
                    make_instance(meshes["corner"], f"{root.name}_CORNER_{sx}_{sy}", proof_collection, root, (lx, ly, wall_z))
                    instance_count += 1
            root["pier_length_min_m"] = min(pier_lengths)
            root["pier_length_max_m"] = max(pier_lengths)

            tray = make_instance(meshes["tray"], f"{root.name}_TRAY", proof_collection, root, (0, bays_y * 2.0 + 0.75, 1.08), scale=(max(1, bays_x),1,1), props={"function":"overhead service spine"})
            make_instance(meshes["power"], f"{root.name}_POWER", proof_collection, root, (-1.3, bays_y * 2.0 + 1.0, 1.41))
            make_instance(meshes["data"], f"{root.name}_DATA", proof_collection, root, (1.3, bays_y * 2.0 + 1.0, 1.24))
            instance_count += 3

            if index % 2 == 0:
                make_instance(meshes["bench"], f"{root.name}_BENCH", proof_collection, root, (-bays_x * 2.0 - 1.4, 0, 0.89), math.radians(90))
                instance_count += 1
            if index % 3 == 0:
                make_instance(meshes["kiosk"], f"{root.name}_KIOSK", proof_collection, root, (bays_x * 2.0 + 1.6, 0, 1.66))
                instance_count += 1
            else:
                for crate_index in range(2):
                    make_instance(meshes["crate"], f"{root.name}_CRATE_{crate_index}", proof_collection, root, (bays_x * 2.0 + 1.2, -0.7 + crate_index, 0.82))
                    instance_count += 1

            if state == "PRISTINE":
                root["era_1"] = "recent service cycle"
                root["era_2"] = "maintained occupancy"
            elif state == "USED":
                root["era_1"] = "maintenance interface added after repeated servicing"
                root["era_2"] = "active use concentrated at service side"
                make_instance(meshes["junction"], root.name + "_USED_SERVICE_PATCH", proof_collection, root, (bays_x * 2.0 + 0.55, 0, 1.56), math.radians(90), (.48,.48,.62), {"x100_state_detail":True,"state":"USED","cause":"frequently handled service retrofit"})
                state_detail_counts[state] += 1; instance_count += 1
            elif state == "DAMAGED":
                root["era_1"] = "localized impact/overload"
                root["era_2"] = "temporary stabilization pending replacement"
                for sign in (-1, 1):
                    brace = make_instance(meshes["parapet"], root.name + f"_DAMAGE_BRACE_{sign}", proof_collection, root, (sign * 3.1, -bays_y * 2.0 - 0.45, 2.11), math.radians(32 * sign), (.82,.75,1), {"x100_state_detail":True,"state":"DAMAGED","cause":"temporary diagonal brace at impact-softened bay"})
                    brace.rotation_euler[1] = math.radians(18 * sign)
                    state_detail_counts[state] += 1; instance_count += 1
                make_instance(meshes["junction"], root.name + "_IMPACT_PATCH", proof_collection, root, (0, -bays_y * 2.0 - 0.5, 1.46), 0, (.72,.45,.62), {"x100_state_detail":True,"state":"DAMAGED","cause":"localized field patch at impact zone"})
                state_detail_counts[state] += 1; instance_count += 1
            else:
                root["era_1"] = "maintenance discontinued; salvage removes serviceable components"
                root["era_2"] = "open roof bay + disconnected utility remnant"
                if roof_objects:
                    bpy.data.objects.remove(roof_objects[-1], do_unlink=True)
                    state_detail_counts[state] += 1; instance_count -= 1
                remnant = make_instance(meshes["tray"], root.name + "_ABANDONED_TRAY_REMNANT", proof_collection, root, (2.8,1.8,.30), math.radians(18), (.65,.8,.65), {"x100_state_detail":True,"state":"ABANDONED","cause":"disconnected service remnant after salvage"})
                remnant.rotation_euler[0] = math.radians(14); remnant.rotation_euler[1] = math.radians(-10)
                make_instance(meshes["crate"], root.name + "_ABANDONED_CRATE", proof_collection, root, (-3,-2,.82), math.radians(17), (1,1,1), {"x100_state_detail":True,"state":"ABANDONED","cause":"left logistics crate after evacuation"})
                state_detail_counts[state] += 1; instance_count += 2

            make_collision_contract(contract_collection, root.name + "_FOOTPRINT", (x,y,floor_bottom+1.7), (bays_x*4+1,bays_y*4+1,3.4))
            make_collision_contract(contract_collection, root.name + "_AIRLOCK_CLEARANCE", (x,y-bays_y*2-1.3,floor_bottom+1.3), (2.2,2.6,2.6), "CLEARANCE_ONLY_NOT_SOLID")
            collision_contracts += 2
            configs.append({"config": index, "state": state, "bays": [bays_x,bays_y], "floor_bottom_z": floor_bottom, "pier_min": min(pier_lengths), "pier_max": max(pier_lengths)})

    return configs, instance_count, collision_contracts, state_detail_counts


def build():
    scene = bpy.context.scene
    root = bpy.data.collections.get(ROOT_COLLECTION) or scene.collection
    collections = {key: ensure_collection(name, root) for key, name in COLLECTIONS.items()}
    for collection in collections.values():
        clear_collection_objects(collection)

    meshes, source_meta = build_source_library(collections["library"], collections["contracts"])
    build_state_contracts(collections["states"])
    sample_terrain = terrain_sampler()
    configs, instance_count, collision_contracts, state_detail_counts = build_proof_district(meshes, collections["proof"], collections["contracts"], sample_terrain)

    human_mesh = simple_box_mesh("AUR_X100_QA_HUMAN_1P8M", (0.36,0.36,1.8), resolve_material("AUR_MAT_ECHO_CYAN"))
    human = bpy.data.objects.new("AUR_X100_QA_HUMAN_1P8M", human_mesh)
    collections["qa"].objects.link(human)
    human.location = (-1840,630,sample_terrain(-1840,630)+0.9)
    human.hide_render = True
    human["qa_role"] = "1.8m player scale guide"
    human["x100_workunit"] = WORKUNIT

    scene["x100_protocol"] = "EXOVANT-X100-v1"
    scene["x100_active_workunit"] = WORKUNIT
    scene["x100_camp_theoretical_configurations"] = THEORETICAL_CONFIGS
    scene["x100_camp_proof_configurations"] = 12
    scene["x100_camp_source_modules"] = len(MODULE_SPECS)
    scene["x100_camp_history_states"] = len(STATES)
    scene["x100_camp_sources_blend_only"] = True
    scene["x100_camp_collision_contract_only"] = True
    scene["x100_camp_lod_envelope_preserved"] = True
    scene["status"] = "X100_CAMP_SYSTEMIC_R23_FOUNDATION_LOD_QA"
    return {
        "status": scene["status"],
        "source_modules": len(MODULE_SPECS),
        "theoretical_configurations": THEORETICAL_CONFIGS,
        "proof_configurations": len(configs),
        "proof_instances": instance_count,
        "collision_contracts": collision_contracts,
        "state_details": state_detail_counts,
        "configs": configs,
    }


if __name__ == "__main__":
    print(build())
