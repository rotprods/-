"""EXOVANT 2950 — ORIGIN / Archivo X100 Wave 02 assembly grammar.

Run inside Blender 5.2+ after `origin_archive_x100_wave1.py`.
Builds four stable Archive assemblies by linked instancing existing ORG_ARC source meshes.
No source mesh ownership is duplicated. Assembly dimensions remain proposal until native Godot traversal.
"""

import math
import bpy
from mathutils import Matrix, Vector

CLAIM_ID = "CLM-ORIGIN-ARCH-ARCHIVE-GRAMMAR-001"
ASSEMBLY_COLLECTION = "80_ORIGIN_ARCHIVE_ASSEMBLIES"

RECIPES = {
    "ORG_ARC_ASM_WITNESS_GALLERY_A": {
        "seed": 4101,
        "modules": [
            ("ORG_ARC_FLOOR_SPINE_B", (-15.0, 34.0, 0.0), 0.0),
            ("ORG_ARC_RIB_WALL_B", (-19.2, 34.0, 0.0), 0.0),
            ("ORG_ARC_RIB_WALL_B", (-10.8, 34.0, 0.0), math.pi),
            ("ORG_ARC_CEILING_RIB_B", (-15.0, 34.0, 4.8), 0.0),
            ("ORG_ARC_MEMORY_CELL_A", (-18.0, 34.0, 0.0), 0.0),
            ("ORG_ARC_MEMORY_CELL_A", (-12.0, 34.0, 0.0), 0.0),
            ("ORG_ARC_THRESHOLD_A", (-15.0, 30.5, 0.0), 0.0),
            ("ORG_ARC_THRESHOLD_A", (-15.0, 37.5, 0.0), math.pi),
            ("ORG_ARC_VAULT_FRAME_B", (-15.0, 34.0, 0.0), math.pi / 2),
            ("ORG_ARC_BRIDGE_SOCKET_B", (-20.5, 34.0, 1.0), math.pi / 2),
            ("ORG_ARC_BRIDGE_SOCKET_B", (-9.5, 34.0, 1.0), -math.pi / 2),
            ("ORG_ARC_MEMORY_CELL_B", (-15.0, 31.5, 0.0), 0.0),
            ("ORG_ARC_MEMORY_CELL_B", (-15.0, 36.5, 0.0), math.pi),
            ("ORG_ARC_RIB_WALL_A", (-15.0, 39.0, 0.0), math.pi / 2),
            ("ORG_ARC_RIB_WALL_A", (-15.0, 29.0, 0.0), -math.pi / 2),
            ("ORG_ARC_CEILING_RIB_A", (-15.0, 34.0, 5.6), math.pi / 2),
        ],
    },
    "ORG_ARC_ASM_VAULT_JUNCTION_A": {
        "seed": 4201,
        "modules": [
            ("ORG_ARC_ARCHIVE_CORE_SHELL_A", (15.0, 34.0, 0.0), 0.0),
            ("ORG_ARC_VAULT_FRAME_C", (15.0, 34.0, 0.0), 0.0),
            ("ORG_ARC_FLOOR_SPINE_A", (15.0, 27.5, 0.0), 0.0),
            ("ORG_ARC_FLOOR_SPINE_A", (15.0, 40.5, 0.0), math.pi),
            ("ORG_ARC_RIB_WALL_C", (8.6, 34.0, 0.0), math.pi / 2),
            ("ORG_ARC_RIB_WALL_C", (21.4, 34.0, 0.0), -math.pi / 2),
            ("ORG_ARC_BRIDGE_SOCKET_C", (15.0, 26.0, 1.2), 0.0),
            ("ORG_ARC_BRIDGE_SOCKET_C", (15.0, 42.0, 1.2), math.pi),
            ("ORG_ARC_BRIDGE_SOCKET_B", (7.5, 34.0, 1.0), math.pi / 2),
            ("ORG_ARC_BRIDGE_SOCKET_B", (22.5, 34.0, 1.0), -math.pi / 2),
            ("ORG_ARC_CEILING_RIB_C", (15.0, 34.0, 6.0), 0.0),
            ("ORG_ARC_MEMORY_CELL_C", (11.5, 34.0, 0.0), 0.0),
            ("ORG_ARC_MEMORY_CELL_C", (18.5, 34.0, 0.0), math.pi),
            ("ORG_ARC_THRESHOLD_B", (15.0, 25.0, 0.0), 0.0),
            ("ORG_ARC_THRESHOLD_B", (15.0, 43.0, 0.0), math.pi),
            ("ORG_ARC_CEILING_RIB_B", (15.0, 34.0, 7.0), math.pi / 2),
            ("ORG_ARC_ARCHIVE_CORE_SHELL_B", (15.0, 34.0, 0.0), 0.0),
        ],
    },
    "ORG_ARC_ASM_MEMORY_NAVE_A": {
        "seed": 4301,
        "modules": [
            ("ORG_ARC_FLOOR_SPINE_B", (-15.0, 76.0, 0.0), 0.0),
            ("ORG_ARC_RIB_WALL_C", (-21.0, 76.0, 0.0), 0.0),
            ("ORG_ARC_RIB_WALL_C", (-9.0, 76.0, 0.0), math.pi),
            ("ORG_ARC_CEILING_RIB_C", (-15.0, 76.0, 6.2), 0.0),
            ("ORG_ARC_MEMORY_CELL_A", (-19.0, 72.0, 0.0), 0.0),
            ("ORG_ARC_MEMORY_CELL_B", (-15.0, 72.0, 0.0), 0.0),
            ("ORG_ARC_MEMORY_CELL_C", (-11.0, 72.0, 0.0), 0.0),
            ("ORG_ARC_MEMORY_CELL_A", (-19.0, 80.0, 0.0), math.pi),
            ("ORG_ARC_MEMORY_CELL_B", (-15.0, 80.0, 0.0), math.pi),
            ("ORG_ARC_MEMORY_CELL_C", (-11.0, 80.0, 0.0), math.pi),
            ("ORG_ARC_VAULT_FRAME_C", (-15.0, 68.5, 0.0), 0.0),
            ("ORG_ARC_VAULT_FRAME_C", (-15.0, 83.5, 0.0), math.pi),
            ("ORG_ARC_THRESHOLD_B", (-15.0, 67.0, 0.0), 0.0),
            ("ORG_ARC_THRESHOLD_B", (-15.0, 85.0, 0.0), math.pi),
            ("ORG_ARC_BRIDGE_SOCKET_C", (-22.8, 76.0, 1.2), math.pi / 2),
            ("ORG_ARC_BRIDGE_SOCKET_C", (-7.2, 76.0, 1.2), -math.pi / 2),
            ("ORG_ARC_CEILING_RIB_B", (-15.0, 72.0, 7.0), math.pi / 2),
            ("ORG_ARC_CEILING_RIB_B", (-15.0, 80.0, 7.0), math.pi / 2),
            ("ORG_ARC_ARCHIVE_CORE_SHELL_A", (-15.0, 76.0, 0.0), 0.0),
            ("ORG_ARC_RIB_WALL_B", (-15.0, 76.0, 0.0), math.pi / 2),
        ],
    },
    "ORG_ARC_ASM_SCAR_THRESHOLD_A": {
        "seed": 4401,
        "modules": [
            ("ORG_ARC_THRESHOLD_B", (20.0, 76.0, 0.0), 0.0),
            ("ORG_ARC_VAULT_FRAME_B", (20.0, 76.0, 0.0), 0.0),
            ("ORG_ARC_RIB_WALL_B", (14.5, 76.0, 0.0), math.pi / 2),
            ("ORG_ARC_RIB_WALL_B", (25.5, 76.0, 0.0), -math.pi / 2),
            ("ORG_ARC_CEILING_RIB_B", (20.0, 76.0, 5.2), 0.0),
            ("ORG_ARC_MEMORY_CELL_A", (17.0, 73.0, 0.0), 0.0),
            ("ORG_ARC_MEMORY_CELL_A", (23.0, 73.0, 0.0), 0.0),
            ("ORG_ARC_MEMORY_CELL_B", (17.0, 79.0, 0.0), math.pi),
            ("ORG_ARC_MEMORY_CELL_B", (23.0, 79.0, 0.0), math.pi),
            ("ORG_ARC_BRIDGE_SOCKET_B", (13.0, 76.0, 1.0), math.pi / 2),
            ("ORG_ARC_BRIDGE_SOCKET_B", (27.0, 76.0, 1.0), -math.pi / 2),
            ("ORG_ARC_FLOOR_SPINE_A", (20.0, 72.0, 0.0), 0.0),
            ("ORG_ARC_FLOOR_SPINE_A", (20.0, 80.0, 0.0), math.pi),
            ("ORG_ARC_CEILING_RIB_A", (20.0, 76.0, 6.2), math.pi / 2),
        ],
    },
}


def ensure_collection(name):
    coll = bpy.data.collections.get(name)
    if coll is None:
        coll = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(coll)
    return coll


def purge_generated():
    for obj in list(bpy.data.objects):
        if obj.get("origin_archive_assembly_generated"):
            bpy.data.objects.remove(obj, do_unlink=True)


def source_parent(asset_id):
    obj = bpy.data.objects.get(asset_id)
    if obj is None:
        matches = [o for o in bpy.data.objects if o.get("origin_asset_id") == asset_id and o.type == "EMPTY"]
        obj = matches[0] if matches else None
    if obj is None:
        raise RuntimeError(f"Missing source asset parent: {asset_id}")
    return obj


def source_mesh_children(parent):
    return sorted((o for o in parent.children_recursive if o.type == "MESH" and not o.name.upper().startswith("COL_")), key=lambda o: o.name)


def instantiate_module(asset_id, assembly_root, module_index, location, rot_z):
    parent = source_parent(asset_id)
    module_root = bpy.data.objects.new(f"{assembly_root.name}__M{module_index:02d}__{asset_id}", None)
    module_root["origin_archive_assembly_generated"] = True
    module_root["origin_source_asset_id"] = asset_id
    module_root["origin_claim_id"] = CLAIM_ID
    module_root.location = Vector(location)
    module_root.rotation_euler[2] = rot_z
    assembly_root.users_collection[0].objects.link(module_root)
    module_root.parent = assembly_root

    parent_world_inv = parent.matrix_world.inverted_safe()
    for child_index, src in enumerate(source_mesh_children(parent), 1):
        inst = bpy.data.objects.new(f"{module_root.name}__{child_index:02d}__{src.name}", src.data)
        inst["origin_archive_assembly_generated"] = True
        inst["origin_source_asset_id"] = asset_id
        inst["origin_claim_id"] = CLAIM_ID
        assembly_root.users_collection[0].objects.link(inst)
        inst.parent = module_root
        inst.matrix_parent_inverse = Matrix.Identity(4)
        inst.matrix_local = parent_world_inv @ src.matrix_world
    return module_root


def build():
    purge_generated()
    coll = ensure_collection(ASSEMBLY_COLLECTION)
    report = []
    for assembly_id, recipe in RECIPES.items():
        root = bpy.data.objects.new(assembly_id, None)
        coll.objects.link(root)
        root["origin_archive_assembly_generated"] = True
        root["origin_assembly_id"] = assembly_id
        root["origin_claim_id"] = CLAIM_ID
        root["origin_recipe_seed"] = int(recipe["seed"])
        root["origin_dimension_status"] = "PROPOSAL_UNTIL_GODOT"
        root["origin_boss_or_heart_included"] = False
        root["origin_player_capsule_radius_m"] = 0.38
        root["origin_player_height_m"] = 1.85
        for index, (asset_id, location, rot_z) in enumerate(recipe["modules"]):
            instantiate_module(asset_id, root, index, location, rot_z)
        report.append((assembly_id, len(recipe["modules"]), recipe["seed"]))
    bpy.context.scene["origin_archive_grammar_claim"] = CLAIM_ID
    return report


if __name__ == "__main__":
    print(build())
