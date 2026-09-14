"""PELAGOS deterministic coral-growth generator v1.

Authority status:
- This file is the VERSIONED NEXT-REGEN generator for PEL/BIOME/007.
- Current committed Blender rev. 8 retains the first procedural meshes in the .blend.
- Determinism can be validated independently from visual/mesh equivalence.
- Do not claim rev. 8 mesh-equivalence until this generator is replayed into the
  production collection and the before/after silhouette/metric gate passes.

Design mechanism:
- branch hierarchy encodes age and load taper;
- a world-local flow vector biases growth without replacing structural support;
- damage prunes topology, not just texture;
- recovery grows new subordinate branches around damage sites;
- acoustic history controls the density of physical memory nodes;
- LOD reduces branch depth/sides while retaining trunk + primary silhouette;
- no random displacement/surface-noise shortcut is used.

Blender 5.2+, metric scene, 1 BU = 1 m in this Pelagos scope.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import Iterable

import bpy
from mathutils import Matrix, Vector

WORLD = "pelagos"
ASSET_ID = "PEL-BIOME-CORAL-GROWTH"
COLLECTION = "21_CORAL_GROWTH_V1"
FLOW = Vector((0.78, 0.38, 0.0)).normalized()


@dataclass(frozen=True)
class CoralState:
    name: str
    seed: int
    max_depth: int
    trunk_length: float
    branch_factor: int
    damage_probability: float
    recovery_bias: float
    memory_density: float


STATES = {
    "young": CoralState("young", 29500307, 2, 12.0, 2, 0.0, 0.0, 0.12),
    "mature": CoralState("mature", 29500504, 4, 24.0, 3, 0.0, 0.0, 0.34),
    "damaged": CoralState("damaged", 29500701, 4, 22.0, 3, 0.38, 0.0, 0.20),
    "recovering": CoralState("recovering", 29500898, 4, 23.0, 3, 0.20, 0.55, 0.30),
}

# Captured from the accepted rev. 8 Pelagos layout. Uniform scale variation is
# intentional and is the only transform variation allowed on linked instances.
PLACEMENTS = [
    ("young", (210.93219, 24.10415, 1.87864), 0.165671, 1.071380),
    ("mature", (169.30254, 118.69415, 4.28970), 0.229881, 1.097431),
    ("mature", (161.50616, 175.61954, 2.66142), 0.838423, 1.065871),
    ("damaged", (105.13949, 229.98247, 2.18030), 0.947653, 0.981267),
    ("recovering", (17.88988, 263.88208, 3.76604), 1.606147, 0.826366),
    ("young", (-16.47723, 185.38499, 1.72598), 1.679058, 0.803436),
    ("mature", (-85.23928, 207.06038, 3.83399), 2.189733, 1.096009),
    ("mature", (-125.58783, 147.67595, 4.46850), 2.395383, 0.808290),
    ("damaged", (-171.49342, 89.36480, 2.52746), 3.079927, 1.026626),
    ("recovering", (-147.63693, 30.20460, 3.39526), 3.302346, 0.724559),
    ("young", (-144.08221, -4.00890, 2.20716), 3.690984, 0.781514),
    ("mature", (-186.78209, -89.37744, 4.34994), 4.041975, 0.972083),
    ("mature", (-79.90434, -73.58661, 1.81317), 4.171824, 0.985076),
    ("damaged", (-14.14451, -122.08607, 4.05094), 4.635614, 0.909123),
    ("recovering", (22.78278, -154.54675, 2.58885), 4.907516, 0.890718),
    ("young", (113.20190, -132.48729, 2.40498), 5.110956, 0.838832),
    ("mature", (138.70889, -62.57585, 3.30331), 5.574274, 0.845207),
    ("mature", (220.95085, -25.37426, 3.22580), 6.265869, 1.008874),
]

SPECIMEN_POSITIONS = {
    "young": Vector((-115.0, 80.0, 3.0)),
    "mature": Vector((-30.0, 35.0, 3.0)),
    "damaged": Vector((70.0, 20.0, 3.0)),
    "recovering": Vector((135.0, 95.0, 3.0)),
}

LOD_CONFIG = {
    0: {"depth_drop": 0, "radial_sides": 8, "child_scale": 1.00},
    1: {"depth_drop": 1, "radial_sides": 5, "child_scale": 0.94},
    2: {"depth_drop": 2, "radial_sides": 4, "child_scale": 0.88},
}


def _safe_basis(direction: Vector) -> tuple[Vector, Vector]:
    d = direction.normalized()
    helper = Vector((0, 0, 1)) if abs(d.z) < 0.92 else Vector((1, 0, 0))
    x = d.cross(helper).normalized()
    y = d.cross(x).normalized()
    return x, y


def _biased_direction(parent_dir: Vector, angle: float, lift: float, flow_weight: float) -> Vector:
    x, y = _safe_basis(parent_dir)
    lateral = math.cos(angle) * x + math.sin(angle) * y
    d = parent_dir.normalized() * 0.42 + lateral * 0.58 + Vector((0, 0, lift)) + FLOW * flow_weight
    return d.normalized()


def branch_graph(state: CoralState, lod: int) -> tuple[list[tuple[Vector, Vector, float, float]], list[Vector]]:
    """Return deterministic tapered segments and memory-node positions."""
    cfg = LOD_CONFIG[lod]
    rng = random.Random(state.seed + lod * 100_003)
    effective_depth = max(1, state.max_depth - cfg["depth_drop"])
    segments: list[tuple[Vector, Vector, float, float]] = []
    memory_nodes: list[Vector] = []

    def grow(start: Vector, direction: Vector, length: float, radius: float, depth: int, lineage: int):
        if depth > effective_depth:
            return
        # Damage is causal topology loss. Primary trunk cannot disappear.
        if depth > 1 and state.damage_probability > 0 and rng.random() < state.damage_probability:
            if state.name == "recovering" and rng.random() < state.recovery_bias:
                # Scar produces smaller new branch rather than restoring the original exactly.
                direction2 = _biased_direction(direction, rng.uniform(0, math.tau), 0.35, 0.28)
                end2 = start + direction2 * (length * 0.48)
                segments.append((start.copy(), end2.copy(), radius * 0.48, radius * 0.18))
                if rng.random() < state.memory_density:
                    memory_nodes.append(end2.copy())
            return

        flow_weight = 0.08 + depth * 0.03
        end = start + direction.normalized() * length + FLOW * (length * flow_weight)
        end.z = max(end.z, start.z + length * 0.28)
        segments.append((start.copy(), end.copy(), radius, max(radius * 0.55, 0.08)))
        if depth > 1 and rng.random() < state.memory_density:
            memory_nodes.append(end.copy())

        if depth >= effective_depth:
            return
        children = max(1, state.branch_factor - (1 if lod >= 1 and depth > 1 else 0))
        for child in range(children):
            phase = (math.tau * child / children) + rng.uniform(-0.30, 0.30) + lineage * 0.19
            child_dir = _biased_direction(direction, phase, rng.uniform(0.18, 0.42), flow_weight)
            child_len = length * rng.uniform(0.52, 0.69) * cfg["child_scale"]
            grow(end, child_dir, child_len, radius * rng.uniform(0.50, 0.64), depth + 1, lineage * 7 + child + 1)

    grow(Vector((0, 0, 0)), Vector((0, 0, 1)), state.trunk_length, max(0.9, state.trunk_length * 0.085), 1, 1)
    return segments, memory_nodes


def _append_frustum(vertices: list[tuple[float, float, float]], faces: list[tuple[int, ...]], a: Vector, b: Vector, r0: float, r1: float, sides: int):
    direction = (b - a).normalized()
    x, y = _safe_basis(direction)
    base = len(vertices)
    for ring_origin, radius in ((a, r0), (b, r1)):
        for i in range(sides):
            t = math.tau * i / sides
            p = ring_origin + x * (math.cos(t) * radius) + y * (math.sin(t) * radius)
            vertices.append((p.x, p.y, p.z))
    for i in range(sides):
        j = (i + 1) % sides
        faces.append((base + i, base + j, base + sides + j, base + sides + i))
    # Root/end caps make baked standalone meshes manifold; intersections between
    # segments are intentional organic unions to be remeshed only for hero variants.
    faces.append(tuple(base + i for i in reversed(range(sides))))
    faces.append(tuple(base + sides + i for i in range(sides)))


def build_mesh(state: CoralState, lod: int, name: str) -> tuple[bpy.types.Mesh, list[Vector]]:
    segments, nodes = branch_graph(state, lod)
    vertices: list[tuple[float, float, float]] = []
    faces: list[tuple[int, ...]] = []
    sides = LOD_CONFIG[lod]["radial_sides"]
    for a, b, r0, r1 in segments:
        _append_frustum(vertices, faces, a, b, r0, r1, sides)
    mesh = bpy.data.meshes.new(name + "_MESH")
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    return mesh, nodes


def _tag(obj, state: str, lod: int | None, source_mesh: bool):
    obj["asset_id"] = ASSET_ID
    obj["world"] = WORLD
    obj["growth_state"] = state
    obj["lod_level"] = -1 if lod is None else lod
    obj["source_mesh"] = source_mesh
    obj["flow_vector"] = list(FLOW)
    obj["production_state"] = "DETERMINISTIC_FOUNDATION_V1"


def build(collection_name: str = COLLECTION, clear_existing: bool = True):
    root = bpy.data.collections.get("PELAGOS_WORLD")
    if root is None:
        raise RuntimeError("PELAGOS_WORLD foundation is required")
    if clear_existing and (old := bpy.data.collections.get(collection_name)):
        for obj in list(old.objects):
            bpy.data.objects.remove(obj, do_unlink=True)
        bpy.data.collections.remove(old)
    col = bpy.data.collections.new(collection_name)
    root.children.link(col)

    coral_mat = bpy.data.materials.get("PEL_LivingCoral")
    cyan_mat = bpy.data.materials.get("PEL_Memory_Cyan")
    if coral_mat is None or cyan_mat is None:
        raise RuntimeError("Pelagos foundation materials missing")

    sources: dict[tuple[str, int], bpy.types.Object] = {}
    memory_node_mesh = None
    memory_node_radius = 0.55

    for state_name, state in STATES.items():
        for lod in (0, 1, 2):
            obj_name = f"PEL_CORAL_{state_name.upper()}_LOD{lod}"
            mesh, node_positions = build_mesh(state, lod, obj_name)
            obj = bpy.data.objects.new(obj_name, mesh)
            col.objects.link(obj)
            obj.location = SPECIMEN_POSITIONS[state_name]
            obj.data.materials.append(coral_mat)
            obj["seed"] = state.seed
            obj["transform_policy"] = "SOURCE_UNIT_SCALE_REQUIRED"
            _tag(obj, state_name, lod, True)
            sources[(state_name, lod)] = obj

            if lod == 0:
                if memory_node_mesh is None:
                    # Create one shared memory-node mesh and remove its temporary object.
                    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=memory_node_radius)
                    tmp = bpy.context.object
                    memory_node_mesh = tmp.data.copy()
                    bpy.data.objects.remove(tmp, do_unlink=True)
                    memory_node_mesh.name = "PEL_CORAL_MEMORY_NODE_MESH"
                for idx, p in enumerate(node_positions):
                    node = bpy.data.objects.new(f"PEL_CORAL_{state_name.upper()}_MemoryNode_{idx:02d}", memory_node_mesh)
                    col.objects.link(node)
                    node.location = SPECIMEN_POSITIONS[state_name] + p
                    node.data.materials.clear()
                    node.data.materials.append(cyan_mat)
                    node["role"] = "acoustic_memory_node"
                    node["node_function"] = "acoustic_memory_history_marker"
                    _tag(node, state_name, 0, False)

    # Linked LOD0 placements.
    for idx, (state, loc, yaw, uniform_scale) in enumerate(PLACEMENTS):
        source = sources[(state, 0)]
        obj = bpy.data.objects.new(f"PEL_CORAL_INSTANCE_{idx:02d}_{state}", source.data)
        col.objects.link(obj)
        obj.location = Vector(loc)
        obj.rotation_euler = (0, 0, yaw)
        obj.scale = (uniform_scale,) * 3
        obj["role"] = "reef_coral_instance"
        obj["instance_policy"] = "LINKED_MESH_UNIFORM_SCALE_VARIATION"
        obj["uniform_scale_intent"] = True
        obj["uniform_scale_factor"] = uniform_scale
        _tag(obj, state, 0, False)

    # Metadata root.
    meta = bpy.data.objects.new("PEL_CORAL_SYSTEM_METADATA", None)
    col.objects.link(meta)
    meta["asset_id"] = ASSET_ID
    meta["world"] = WORLD
    meta["role"] = "procedural_coral_system"
    meta["production_state"] = "DETERMINISTIC_FOUNDATION_V1"
    meta["seed"] = STATES["young"].seed
    meta["flow_vector"] = list(FLOW)
    meta["flow_vector_status"] = "PROPOSAL_LOCAL_ART_DIRECTION"
    meta["mechanism"] = "age/load taper + flow bias + topology damage/recovery + acoustic-history memory nodes"
    meta["anti_noise"] = "no random displacement; topology parameters only"
    meta["lod_policy"] = "LOD0 full; LOD1 reduced branch depth/sides; LOD2 trunk/primary silhouette"
    meta["cold_replay_status"] = "GENERATOR_VERSIONED_REPLAY_REQUIRED"

    # Legacy foundation curves remain as historical geometry but not visible/rendered.
    for i in range(34):
        old = bpy.data.objects.get(f"PEL_REEF_Spire_{i:02d}")
        if old:
            old.hide_render = True
            old.hide_viewport = True
            old["superseded_by"] = ASSET_ID

    return col


if __name__ == "__main__":
    build()
