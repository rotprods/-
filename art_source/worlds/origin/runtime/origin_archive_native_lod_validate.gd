extends SceneTree

const ASSEMBLY_IDS: Array[String] = [
    "ORG_ARC_ASM_WITNESS_GALLERY_A",
    "ORG_ARC_ASM_VAULT_JUNCTION_A",
    "ORG_ARC_ASM_MEMORY_NAVE_A",
    "ORG_ARC_ASM_SCAR_THRESHOLD_A",
]
const CAPSULE_RADIUS: float = 0.38
const CAPSULE_HEIGHT: float = 1.85
const GRAVITY: float = 18.0
const MOVE_SPEED: float = 2.5
const MAX_EDGE_M: float = 4.25
const MAX_STEP_Y_M: float = 0.40

var failures: Array[String] = []
var root_scene: Node3D
var physics_root: Node3D

func _initialize() -> void:
    call_deferred("_run")

func _walk(node: Node, out: Array[Node]) -> void:
    out.append(node)
    for child in node.get_children():
        _walk(child, out)

func _all_nodes(node: Node) -> Array[Node]:
    var out: Array[Node] = []
    _walk(node, out)
    return out

func _find_exact(node: Node, wanted: String) -> Node:
    for candidate in _all_nodes(node):
        if String(candidate.name) == wanted:
            return candidate
    return null

func _mesh_tris(mesh: Mesh) -> int:
    var total: int = 0
    for surface: int in range(mesh.get_surface_count()):
        var arrays: Array = mesh.surface_get_arrays(surface)
        var indices = arrays[Mesh.ARRAY_INDEX]
        if indices != null and indices.size() > 0:
            total += int(indices.size() / 3)
        else:
            var vertices = arrays[Mesh.ARRAY_VERTEX]
            if vertices != null:
                total += int(vertices.size() / 3)
    return total

func _world_aabb_center(mesh_node: MeshInstance3D) -> Vector3:
    return mesh_node.global_transform * mesh_node.mesh.get_aabb().get_center()

func _build_static_collision(nodes: Array[MeshInstance3D], namespace: String) -> int:
    var count: int = 0
    for mesh_node: MeshInstance3D in nodes:
        if mesh_node.mesh == null:
            continue
        var shape: ConcavePolygonShape3D = mesh_node.mesh.create_trimesh_shape()
        if shape == null:
            continue
        var body := StaticBody3D.new()
        body.name = namespace + "__BODY__" + String(mesh_node.name)
        var collision := CollisionShape3D.new()
        collision.shape = shape
        body.add_child(collision)
        physics_root.add_child(body)
        body.global_transform = mesh_node.global_transform
        count += 1
    return count

func _support_at(xz: Vector2) -> Dictionary:
    var space := physics_root.get_world_3d().direct_space_state
    var query := PhysicsRayQueryParameters3D.create(
        Vector3(xz.x, 12.0, xz.y),
        Vector3(xz.x, -4.0, xz.y)
    )
    query.collide_with_bodies = true
    query.collide_with_areas = false
    return space.intersect_ray(query)

func _capsule_clear_at(point: Vector3, floor_rid: RID) -> bool:
    var capsule := CapsuleShape3D.new()
    capsule.radius = CAPSULE_RADIUS
    capsule.height = CAPSULE_HEIGHT
    var q := PhysicsShapeQueryParameters3D.new()
    q.shape = capsule
    q.transform = Transform3D(Basis.IDENTITY, point + Vector3(0.0, CAPSULE_HEIGHT * 0.5 + 0.035, 0.0))
    q.collide_with_bodies = true
    q.collide_with_areas = false
    q.margin = 0.015
    if floor_rid.is_valid():
        q.exclude = [floor_rid]
    var hits: Array[Dictionary] = physics_root.get_world_3d().direct_space_state.intersect_shape(q, 4)
    return hits.is_empty()

func _sample_walkable(center: Vector3) -> Dictionary:
    var hit: Dictionary = _support_at(Vector2(center.x, center.z))
    if hit.is_empty():
        return {"ok": false}
    var normal: Vector3 = hit.get("normal", Vector3.ZERO)
    if normal.y < 0.65:
        return {"ok": false}
    var pos: Vector3 = hit.get("position", center)
    var rid: RID = hit.get("rid", RID())
    if not _capsule_clear_at(pos, rid):
        return {"ok": false}
    return {"ok": true, "position": pos, "normal": normal, "rid": rid}

func _edge_clear(a: Vector3, b: Vector3) -> bool:
    for step: int in range(1, 5):
        var t: float = float(step) / 5.0
        var p: Vector3 = a.lerp(b, t)
        if not bool(_sample_walkable(p).get("ok", false)):
            return false
    return true

func _largest_component(adjacency: Array[Array]) -> Array[int]:
    var seen: Dictionary = {}
    var best: Array[int] = []
    for start: int in range(adjacency.size()):
        if seen.has(start):
            continue
        var queue: Array[int] = [start]
        var component: Array[int] = []
        seen[start] = true
        while not queue.is_empty():
            var cur: int = queue.pop_front()
            component.append(cur)
            for nxt_value in adjacency[cur]:
                var nxt: int = int(nxt_value)
                if not seen.has(nxt):
                    seen[nxt] = true
                    queue.append(nxt)
        if component.size() > best.size():
            best = component
    return best

func _bfs_path(adjacency: Array[Array], start: int, goal: int) -> Array[int]:
    var queue: Array[int] = [start]
    var parent: Dictionary = {start: -1}
    while not queue.is_empty():
        var cur: int = queue.pop_front()
        if cur == goal:
            break
        for nxt_value in adjacency[cur]:
            var nxt: int = int(nxt_value)
            if not parent.has(nxt):
                parent[nxt] = cur
                queue.append(nxt)
    if not parent.has(goal):
        return []
    var path: Array[int] = []
    var cur: int = goal
    while cur != -1:
        path.push_front(cur)
        cur = int(parent[cur])
    return path

func _settle_body(body: CharacterBody3D, floor_point: Vector3) -> bool:
    body.global_position = floor_point + Vector3(0.0, 3.0, 0.0)
    body.velocity = Vector3.ZERO
    for _frame: int in range(240):
        if body.is_on_floor():
            body.velocity.y = -0.05
        else:
            body.velocity.y -= GRAVITY / 60.0
        body.move_and_slide()
        await physics_frame
        if body.is_on_floor() and abs(body.global_position.y - (floor_point.y + CAPSULE_HEIGHT * 0.5)) < 0.35:
            return true
        if body.global_position.y < floor_point.y - 3.0:
            return false
    return body.is_on_floor()

func _traverse_path(points: Array[Vector3], path: Array[int]) -> Dictionary:
    var body := CharacterBody3D.new()
    body.name = "ARCHIVE_NATIVE_CHARACTER"
    body.up_direction = Vector3.UP
    body.floor_snap_length = 0.35
    body.floor_max_angle = deg_to_rad(52.0)
    var cs := CollisionShape3D.new()
    var capsule := CapsuleShape3D.new()
    capsule.radius = CAPSULE_RADIUS
    capsule.height = CAPSULE_HEIGHT
    cs.shape = capsule
    body.add_child(cs)
    physics_root.add_child(body)
    var landed: bool = await _settle_body(body, points[path[0]])
    if not landed:
        body.queue_free()
        await physics_frame
        return {"passed": false, "reason": "initial landing failed"}
    var floor_frames: int = 0
    var min_y: float = body.global_position.y
    var max_error: float = 0.0
    var visited: int = 1
    for pi: int in range(1, path.size()):
        var target_floor: Vector3 = points[path[pi]]
        var target_xz := Vector2(target_floor.x, target_floor.z)
        var last_dist: float = INF
        var stagnant: int = 0
        var reached: bool = false
        for _frame: int in range(300):
            var now_xz := Vector2(body.global_position.x, body.global_position.z)
            var delta2: Vector2 = target_xz - now_xz
            var dist: float = delta2.length()
            if dist < 0.28:
                reached = true
                break
            if dist > last_dist - 0.002:
                stagnant += 1
            else:
                stagnant = 0
            last_dist = dist
            if stagnant > 90:
                break
            var dir2: Vector2 = delta2.normalized()
            body.velocity.x = dir2.x * MOVE_SPEED
            body.velocity.z = dir2.y * MOVE_SPEED
            if body.is_on_floor():
                body.velocity.y = -0.05
                floor_frames += 1
            else:
                body.velocity.y -= GRAVITY / 60.0
            body.move_and_slide()
            min_y = min(min_y, body.global_position.y)
            max_error = max(max_error, abs(body.global_position.y - (target_floor.y + CAPSULE_HEIGHT * 0.5)))
            await physics_frame
            if body.global_position.y < target_floor.y - 3.0:
                break
        if not reached:
            var failed_at: int = pi
            var final_pos: Vector3 = body.global_position
            body.queue_free()
            await physics_frame
            return {"passed": false, "reason": "waypoint blocked", "failed_waypoint": failed_at, "position": [final_pos.x, final_pos.y, final_pos.z], "floor_frames": floor_frames}
        visited += 1
    var final_floor: Vector3 = points[path[-1]]
    var final_error: float = Vector2(body.global_position.x - final_floor.x, body.global_position.z - final_floor.z).length()
    var final_pos: Vector3 = body.global_position
    body.queue_free()
    await physics_frame
    return {
        "passed": final_error < 0.55 and min_y > -2.0,
        "visited_waypoints": visited,
        "floor_frames": floor_frames,
        "min_y": min_y,
        "max_vertical_target_error": max_error,
        "final_horizontal_error": final_error,
        "final_position": [final_pos.x, final_pos.y, final_pos.z],
    }

func _qualify_assembly(assembly: Node3D) -> Dictionary:
    var descendants: Array[Node] = _all_nodes(assembly)
    var colliders: Array[MeshInstance3D] = []
    var walkable_meshes: Array[MeshInstance3D] = []
    for node in descendants:
        if node is MeshInstance3D and node.mesh != null and "__COL_" in String(node.name):
            colliders.append(node)
            if "FLOOR_SPINE" in String(node.name) or "THRESHOLD" in String(node.name):
                walkable_meshes.append(node)
    var static_count: int = _build_static_collision(colliders, String(assembly.name))
    await physics_frame
    await physics_frame
    var points: Array[Vector3] = []
    for mesh_node: MeshInstance3D in walkable_meshes:
        var center: Vector3 = _world_aabb_center(mesh_node)
        var sample: Dictionary = _sample_walkable(center)
        if bool(sample.get("ok", false)):
            points.append(sample["position"])
    var adjacency: Array[Array] = []
    adjacency.resize(points.size())
    for i: int in range(points.size()):
        adjacency[i] = []
    for i: int in range(points.size()):
        for j: int in range(i + 1, points.size()):
            var a: Vector3 = points[i]
            var b: Vector3 = points[j]
            var horizontal: float = Vector2(a.x - b.x, a.z - b.z).length()
            if horizontal <= MAX_EDGE_M and abs(a.y - b.y) <= MAX_STEP_Y_M and _edge_clear(a, b):
                adjacency[i].append(j)
                adjacency[j].append(i)
    var component: Array[int] = _largest_component(adjacency)
    if component.size() < 2:
        return {"passed": false, "reason": "no connected walkable component", "colliders": static_count, "walkable_points": points.size()}
    var min_x: float = INF
    var max_x: float = -INF
    var min_z: float = INF
    var max_z: float = -INF
    for p: Vector3 in points:
        min_x = min(min_x, p.x); max_x = max(max_x, p.x)
        min_z = min(min_z, p.z); max_z = max(max_z, p.z)
    var x_span: float = max_x - min_x
    var z_span: float = max_z - min_z
    var use_x: bool = x_span >= z_span
    var all_span: float = max(x_span, z_span)
    var start: int = component[0]
    var goal: int = component[0]
    var comp_min: float = INF
    var comp_max: float = -INF
    for idx: int in component:
        var value: float = points[idx].x if use_x else points[idx].z
        if value < comp_min:
            comp_min = value; start = idx
        if value > comp_max:
            comp_max = value; goal = idx
    var component_span: float = comp_max - comp_min
    var span_ratio: float = component_span / max(all_span, 0.001)
    var path: Array[int] = _bfs_path(adjacency, start, goal)
    if path.is_empty():
        return {"passed": false, "reason": "component endpoints disconnected", "span_ratio": span_ratio}
    var traversal: Dictionary = await _traverse_path(points, path)
    var passed: bool = span_ratio >= 0.70 and bool(traversal.get("passed", false))
    return {
        "passed": passed,
        "colliders_built": static_count,
        "walkable_meshes": walkable_meshes.size(),
        "valid_walkable_points": points.size(),
        "largest_component": component.size(),
        "dominant_axis": "x" if use_x else "z",
        "all_span_m": all_span,
        "component_span_m": component_span,
        "span_ratio": span_ratio,
        "path_waypoints": path.size(),
        "traversal": traversal,
    }

func _collect_lod_groups(scene: Node) -> Dictionary:
    var nodes: Array[Node] = _all_nodes(scene)
    var exact: Dictionary = {}
    for node in nodes:
        if node is MeshInstance3D:
            exact[String(node.name)] = node
    var groups: Dictionary = {}
    for node in nodes:
        if not (node is MeshInstance3D):
            continue
        var n: String = String(node.name)
        if not n.begins_with("LOD1__"):
            continue
        var base_name: String = n.trim_prefix("LOD1__")
        var lod2_name: String = "LOD2__" + base_name
        if exact.has(base_name) and exact.has(lod2_name):
            groups[base_name] = [exact[base_name], node, exact[lod2_name]]
    return groups

func _set_lod_tier(groups: Dictionary, tier: int) -> Dictionary:
    var visible_counts: Array[int] = [0, 0, 0]
    var violations: int = 0
    for base_name in groups:
        var trio: Array = groups[base_name]
        for i: int in range(3):
            var mesh_node: MeshInstance3D = trio[i]
            mesh_node.visible = i == tier
            if mesh_node.visible:
                visible_counts[i] += 1
        var count: int = 0
        for mesh_node in trio:
            if mesh_node.visible:
                count += 1
        if count != 1:
            violations += 1
    return {"tier": tier, "visible_counts": visible_counts, "one_visible_violations": violations}

func _qualify_lod(scene: Node, collision_count_before: int) -> Dictionary:
    var groups: Dictionary = _collect_lod_groups(scene)
    var tris: Array[int] = [0, 0, 0]
    var missing_meshes: int = 0
    for base_name in groups:
        var trio: Array = groups[base_name]
        for tier: int in range(3):
            var mi: MeshInstance3D = trio[tier]
            if mi.mesh == null:
                missing_meshes += 1
            else:
                tris[tier] += _mesh_tris(mi.mesh)
    var near_state: Dictionary = _set_lod_tier(groups, 0)
    await process_frame
    var mid_state: Dictionary = _set_lod_tier(groups, 1)
    await process_frame
    var far_state: Dictionary = _set_lod_tier(groups, 2)
    await process_frame
    var collision_count_after: int = 0
    for node in _all_nodes(scene):
        if node is MeshInstance3D and "COL_ORG_ARC_" in String(node.name) and "__COL_" not in String(node.name):
            collision_count_after += 1
    var lod1_ratio: float = float(tris[1]) / max(float(tris[0]), 1.0)
    var lod2_ratio: float = float(tris[2]) / max(float(tris[0]), 1.0)
    var pass: bool = groups.size() == 94 and missing_meshes == 0 and int(near_state["one_visible_violations"]) == 0 and int(mid_state["one_visible_violations"]) == 0 and int(far_state["one_visible_violations"]) == 0 and lod1_ratio < 0.65 and lod2_ratio < 0.40 and collision_count_after == collision_count_before
    return {
        "passed": pass,
        "group_count": groups.size(),
        "triangles": {"lod0": tris[0], "lod1": tris[1], "lod2": tris[2]},
        "ratios": {"lod1_over_lod0": lod1_ratio, "lod2_over_lod0": lod2_ratio},
        "near_state": near_state,
        "mid_state": mid_state,
        "far_state": far_state,
        "collision_mesh_count_before": collision_count_before,
        "collision_mesh_count_after": collision_count_after,
        "missing_meshes": missing_meshes,
        "resident_tiers_note": "visibility switching proven; residency/packing/HLOD not proven",
    }

func _run() -> void:
    var packed = ResourceLoader.load("res://origin_archive_rev7.glb", "PackedScene")
    if packed == null or not (packed is PackedScene):
        print("ORIGIN_ARCHIVE_WAVE4_RESULT=" + JSON.stringify({"failures": ["PackedScene import failed"]}))
        quit(2)
        return
    root_scene = packed.instantiate()
    get_root().add_child(root_scene)
    physics_root = Node3D.new()
    physics_root.name = "ARCHIVE_NATIVE_PHYSICS"
    get_root().add_child(physics_root)

    var source_collision_count: int = 0
    for node in _all_nodes(root_scene):
        if node is MeshInstance3D and "COL_ORG_ARC_" in String(node.name) and "__COL_" not in String(node.name):
            source_collision_count += 1

    var assembly_results: Dictionary = {}
    var archive_pass: bool = true
    for assembly_id: String in ASSEMBLY_IDS:
        var found: Node = _find_exact(root_scene, assembly_id)
        if found == null or not (found is Node3D):
            assembly_results[assembly_id] = {"passed": false, "reason": "assembly ID missing"}
            archive_pass = false
            continue
        var result: Dictionary = await _qualify_assembly(found)
        assembly_results[assembly_id] = result
        if not bool(result.get("passed", false)):
            archive_pass = false

    var lod_result: Dictionary = await _qualify_lod(root_scene, source_collision_count)
    if not bool(lod_result.get("passed", false)):
        failures.append("runtime LOD qualification failed")
    if not archive_pass:
        failures.append("Archive assembly native traversal failed")
    var report := {
        "godot": Engine.get_version_info(),
        "archive_claim": "CLM-ORIGIN-ARCH-ARCHIVE-NATIVE-001",
        "lod_claim": "CLM-ORIGIN-TECH-RUNTIME-LOD-001",
        "glb_revision": 7,
        "assemblies": assembly_results,
        "archive_native_pass": archive_pass,
        "runtime_lod": lod_result,
        "runtime_lod_pass": bool(lod_result.get("passed", false)),
        "failures": failures,
    }
    print("ORIGIN_ARCHIVE_WAVE4_RESULT=" + JSON.stringify(report))
    quit(0 if failures.is_empty() else 2)
