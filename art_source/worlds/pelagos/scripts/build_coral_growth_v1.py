"""Deterministic coral-growth foundation for PELAGOS / Coro del Arrecife.

Task: PEL/BIOME/007
Blender: 5.2+
Units: 1 BU = 1 metre

This script builds exportable source meshes for four causal states (young, mature,
damaged, recovering) and LOD0/1/2. It deliberately avoids geometry-noise and
surface-randomness shortcuts: topology is driven by age, load taper, current bias,
damage and acoustic-history parameters.

The local flow vector is a PROPOSAL for art-direction/blockout only, not world canon.
"""
import bpy
import bmesh
import math
import random
from mathutils import Vector, Matrix

WORLD = "pelagos"
ASSET_ID = "PEL-BIOME-CORAL-GROWTH"
COLLECTION = "21_CORAL_GROWTH_V1"
SEED = 29500307
FLOW = Vector((0.78, 0.38, 0.0)).normalized()  # PROPOSAL_LOCAL_ART_DIRECTION
UP = Vector((0, 0, 1))

STATE_DEFS = {
    "young": {"age": 0.28, "depth": 2, "height": 16.0, "base_r": 1.15, "branching": 2, "acoustic": 0.25, "damage": 0.0, "recovery": 0.0, "material": "PEL_LivingCoral_Pale"},
    "mature": {"age": 1.0, "depth": 4, "height": 42.0, "base_r": 2.4, "branching": 3, "acoustic": 0.85, "damage": 0.0, "recovery": 0.0, "material": "PEL_LivingCoral"},
    "damaged": {"age": 0.9, "depth": 3, "height": 34.0, "base_r": 2.2, "branching": 3, "acoustic": 0.48, "damage": 0.42, "recovery": 0.0, "material": "PEL_Coral_Damaged_Mineralized"},
    "recovering": {"age": 0.95, "depth": 4, "height": 38.0, "base_r": 2.25, "branching": 3, "acoustic": 0.72, "damage": 0.18, "recovery": 0.55, "material": "PEL_Coral_Recovering_Tissue"},
}

HERO_POSITIONS = {
    "young": Vector((-115, 80, 3)),
    "mature": Vector((-30, 35, 3)),
    "damaged": Vector((70, 20, 3)),
    "recovering": Vector((135, 95, 3)),
}


def ensure_material(name, fallback_rgba, roughness=0.62):
    m = bpy.data.materials.get(name)
    if m:
        return m
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes.get("Principled BSDF")
    b.inputs["Base Color"].default_value = fallback_rgba
    b.inputs["Roughness"].default_value = roughness
    return m


def ensure_collection():
    root = bpy.data.collections.get("PELAGOS_WORLD")
    if root is None:
        raise RuntimeError("Build Pelagos world foundation first")
    old = bpy.data.collections.get(COLLECTION)
    if old:
        for o in list(old.objects):
            bpy.data.objects.remove(o, do_unlink=True)
        bpy.data.collections.remove(old)
    c = bpy.data.collections.new(COLLECTION)
    root.children.link(c)
    return c


def topology(seed, cfg, lod):
    """Return causal branch segments and terminal acoustic-memory nodes."""
    rng = random.Random(seed + lod * 10007)
    max_depth = max(1, cfg["depth"] - lod)
    segments = []
    nodes = []

    def recurse(p, direction, radius, length, depth, path_id):
        if depth > max_depth or radius < 0.16 or length < 1.2:
            return
        flow_bias = 0.12 + 0.08 * depth
        d = (direction * (1.0 - flow_bias) + FLOW * flow_bias + UP * (0.12 if depth == 1 else 0.0)).normalized()
        yaw = (rng.random() - 0.5) * math.radians(22 if depth > 1 else 10)
        pitch = (rng.random() - 0.5) * math.radians(16)
        rot = Matrix.Rotation(yaw, 4, UP) @ Matrix.Rotation(pitch, 4, Vector((1, 0, 0)))
        d = (rot @ d).normalized()
        q = p + d * length

        damaged = cfg["damage"] > 0 and depth > 1 and rng.random() < cfg["damage"] * 0.34
        if damaged:
            stump = p + d * (length * 0.28)
            segments.append((p.copy(), stump.copy(), radius, max(radius * 0.72, 0.14), depth, path_id + "D"))
            return

        segments.append((p.copy(), q.copy(), radius, max(radius * 0.58, 0.12), depth, path_id))
        if depth == max_depth and rng.random() < cfg["acoustic"]:
            nodes.append(q.copy())
        if depth == max_depth:
            return

        child_count = max(1, cfg["branching"] - (1 if lod > 0 else 0) - (1 if depth >= 3 else 0))
        for i in range(child_count):
            az = 2 * math.pi * (i / child_count) + rng.uniform(-0.25, 0.25)
            lateral = Vector((math.cos(az), math.sin(az), rng.uniform(0.35, 0.72))).normalized()
            child = (d * 0.52 + lateral * 0.48 + FLOW * 0.14).normalized()
            recurse(q, child, radius * (0.57 + rng.uniform(-0.04, 0.04)), length * (0.64 + rng.uniform(-0.05, 0.05)), depth + 1, path_id + str(i))

        if cfg["recovery"] > 0 and depth >= 2 and rng.random() < cfg["recovery"] * 0.5:
            recovery_dir = (d * 0.35 + Vector((-FLOW.y, FLOW.x, 0.72)) * 0.65).normalized()
            recurse(q, recovery_dir, radius * 0.36, length * 0.44, depth + 1, path_id + "R")

    recurse(Vector((0, 0, 0)), Vector((0.08, 0.02, 1)).normalized(), cfg["base_r"], cfg["height"] * 0.34, 1, "0")
    return segments, nodes


def build_segment_mesh(name, segments, material, location, state, lod, collection, visible=True):
    mesh = bpy.data.meshes.new(name + "_MESH")
    bm = bmesh.new()
    for p, q, r0, r1, _depth, _path in segments:
        direction = q - p
        length = direction.length
        if length <= 1e-4:
            continue
        midpoint = (p + q) * 0.5
        quat = direction.to_track_quat("Z", "Y")
        transform = Matrix.Translation(midpoint) @ quat.to_matrix().to_4x4()
        bmesh.ops.create_cone(
            bm,
            cap_ends=True,
            cap_tris=False,
            segments=max(6, 10 - lod * 2),
            radius1=r0,
            radius2=r1,
            depth=length,
            matrix=transform,
        )
    bm.to_mesh(mesh)
    bm.free()
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    collection.objects.link(obj)
    obj.location = location
    obj.data.materials.append(material)
    obj["asset_id"] = ASSET_ID
    obj["world"] = WORLD
    obj["role"] = "coral_specimen"
    obj["state"] = state
    obj["lod"] = lod
    obj["production_state"] = "PROCEDURAL_FOUNDATION_V1"
    obj["collision_intent"] = "none"
    obj["segment_count"] = len(segments)
    obj.hide_render = not visible
    obj.hide_set(not visible)
    return obj


def ensure_memory_mesh(material):
    mesh = bpy.data.meshes.get("PEL_CORAL_MEMORY_NODE_MESH")
    if mesh is None:
        bm = bmesh.new()
        bmesh.ops.create_icosphere(bm, subdivisions=2, radius=0.55)
        mesh = bpy.data.meshes.new("PEL_CORAL_MEMORY_NODE_MESH")
        bm.to_mesh(mesh)
        bm.free()
        mesh.update()
        mesh["physical_radius_applied"] = True
        mesh["physical_radius_m"] = 0.55
    if len(mesh.materials) == 0:
        mesh.materials.append(material)
    return mesh


def build():
    c = ensure_collection()
    coral = ensure_material("PEL_LivingCoral", (0.22, 0.40, 0.36, 1))
    pale = ensure_material("PEL_LivingCoral_Pale", (0.43, 0.58, 0.48, 1))
    damaged = ensure_material("PEL_Coral_Damaged_Mineralized", (0.12, 0.17, 0.15, 1), 0.78)
    recovering = ensure_material("PEL_Coral_Recovering_Tissue", (0.31, 0.52, 0.42, 1), 0.58)
    memory = ensure_material("PEL_Memory_Cyan", (0.03, 0.30, 0.40, 1), 0.28)
    mats = {"young": pale, "mature": coral, "damaged": damaged, "recovering": recovering}

    # Hide only superseded Coro silhouette proxies; never delete recovery history.
    for o in bpy.data.objects:
        if o.name.startswith("PEL_REEF_Spire_"):
            o.hide_render = True
            o.hide_set(True)
            o["production_state"] = "SUPERSEDED_REGION_PROXY"
            o["superseded_by"] = COLLECTION

    meta = bpy.data.objects.new("PEL_CORAL_SYSTEM_METADATA", None)
    c.objects.link(meta)
    meta["asset_id"] = ASSET_ID
    meta["world"] = WORLD
    meta["role"] = "procedural_coral_system"
    meta["seed"] = SEED
    meta["production_state"] = "DETERMINISTIC_FOUNDATION_V1"
    meta["flow_vector_status"] = "PROPOSAL_LOCAL_ART_DIRECTION"
    meta["flow_vector"] = [0.78, 0.38, 0.0]
    meta["mechanism"] = "age/load taper + current bias + damage + acoustic-history memory nodes"
    meta["lod_policy"] = "LOD0 full branch depth; LOD1 reduced branching; LOD2 trunk/primary silhouette"
    meta["engine_state"] = "NOT_IMPORTED"
    meta["memory_node_radius_m"] = 0.55

    memory_mesh = ensure_memory_mesh(memory)
    source_meshes = {}
    node_counts = {}
    for idx, (state, cfg) in enumerate(STATE_DEFS.items()):
        for lod in (0, 1, 2):
            segs, nodes = topology(SEED + idx * 197, cfg, lod)
            obj = build_segment_mesh(
                f"PEL_CORAL_{state.upper()}_LOD{lod}",
                segs,
                mats[state],
                HERO_POSITIONS[state],
                state,
                lod,
                c,
                visible=(lod == 0),
            )
            obj["seed"] = SEED + idx * 197
            obj["age_parameter"] = cfg["age"]
            obj["acoustic_history_parameter"] = cfg["acoustic"]
            obj["damage_parameter"] = cfg["damage"]
            obj["recovery_parameter"] = cfg["recovery"]
            obj["memory_node_count"] = len(nodes)
            source_meshes[(state, lod)] = obj.data
            if lod == 0:
                node_counts[state] = len(nodes)
                for ni, p in enumerate(nodes):
                    n = bpy.data.objects.new(f"PEL_CORAL_{state.upper()}_MemoryNode_{ni:02d}", memory_mesh)
                    c.objects.link(n)
                    n.location = HERO_POSITIONS[state] + p
                    n["asset_id"] = ASSET_ID
                    n["world"] = WORLD
                    n["role"] = "acoustic_memory_node"
                    n["state"] = state
                    n["production_state"] = "PROCEDURAL_FOUNDATION_V1"

    # Linked mesh instances only inside the authored Coro radius.
    rng = random.Random(44017)
    states = ["young", "mature", "mature", "damaged", "recovering"]
    for i in range(18):
        angle = 2 * math.pi * i / 18 + rng.uniform(-0.10, 0.10)
        radius = rng.uniform(120, 240)
        state = states[i % len(states)]
        obj = bpy.data.objects.new(f"PEL_CORAL_INSTANCE_{i:02d}_{state}", source_meshes[(state, 0)])
        c.objects.link(obj)
        obj.location = (math.cos(angle) * radius, 40 + math.sin(angle) * radius, 2.5 + rng.uniform(-1, 2))
        s = rng.uniform(0.72, 1.12)
        obj.scale = (s, s, s)
        obj.rotation_euler.z = angle + rng.uniform(-0.35, 0.35)
        obj["asset_id"] = ASSET_ID
        obj["world"] = WORLD
        obj["role"] = "coral_linked_instance"
        obj["state"] = state
        obj["lod"] = 0
        obj["instance_source"] = f"PEL_CORAL_{state.upper()}_LOD0"
        obj["production_state"] = "PROCEDURAL_FOUNDATION_V1"

    return {
        "collection": COLLECTION,
        "states": list(STATE_DEFS),
        "lods": [0, 1, 2],
        "source_mesh_count": len(source_meshes),
        "linked_instance_count": 18,
        "memory_node_counts": node_counts,
        "seed": SEED,
        "flow_vector_status": "PROPOSAL_LOCAL_ART_DIRECTION",
        "pending": ["UV/bake", "final PBR", "engine LOD switching", "hero collision", "performance", "human art review"],
    }


if __name__ == "__main__":
    print(build())
