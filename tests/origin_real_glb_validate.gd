extends SceneTree

var failures: Array[String] = []
var report: Dictionary = {}

func _initialize() -> void:
    call_deferred("_run")

func _walk(node: Node, out: Array[Node]) -> void:
    out.append(node)
    for child in node.get_children():
        _walk(child, out)

func _inspect_scene(path: String, label: String, world: Node3D) -> Dictionary:
    var packed: Resource = ResourceLoader.load(path, "PackedScene")
    if packed == null or not (packed is PackedScene):
        failures.append(label + ": PackedScene load failed")
        return {"loaded": false}
    var instance: Node = (packed as PackedScene).instantiate()
    if instance == null:
        failures.append(label + ": instantiate failed")
        return {"loaded": false}
    world.add_child(instance)
    var nodes: Array[Node] = []
    _walk(instance, nodes)
    var mesh_count: int = 0
    var material_slots: int = 0
    var names: Array[String] = []
    var collision_meshes: Array[Node] = []
    var lod1: int = 0
    var lod2: int = 0
    for node in nodes:
        var n: String = String(node.name)
        names.append(n)
        if n.begins_with("LOD1__"):
            lod1 += 1
        if n.begins_with("LOD2__"):
            lod2 += 1
        if node is MeshInstance3D and (node as MeshInstance3D).mesh != null:
            var mesh_node := node as MeshInstance3D
            mesh_count += 1
            for surface in range(mesh_node.mesh.get_surface_count()):
                if mesh_node.mesh.surface_get_material(surface) != null:
                    material_slots += 1
            if n.begins_with("COL_") or n.contains("__COL_"):
                collision_meshes.append(node)
    var service_count: int = 0
    var culture_count: int = 0
    var arc_count: int = 0
    var assemblies: int = 0
    var expected_assemblies: Dictionary = {
        "ORG_ARC_ASM_WITNESS_GALLERY_A": true,
        "ORG_ARC_ASM_VAULT_JUNCTION_A": true,
        "ORG_ARC_ASM_MEMORY_NAVE_A": true,
        "ORG_ARC_ASM_SCAR_THRESHOLD_A": true,
    }
    for n in names:
        if n.begins_with("ORG_ATR_SVC_"):
            service_count += 1
        if n.begins_with("ORG_CULT_"):
            culture_count += 1
        if n.begins_with("ORG_ARC_"):
            arc_count += 1
        if expected_assemblies.has(n):
            assemblies += 1
    return {
        "loaded": true,
        "node_count": nodes.size(),
        "mesh_count": mesh_count,
        "material_slots": material_slots,
        "collision_mesh_count": collision_meshes.size(),
        "lod1_nodes": lod1,
        "lod2_nodes": lod2,
        "service_named_nodes": service_count,
        "culture_named_nodes": culture_count,
        "archive_named_nodes": arc_count,
        "assembly_ids_found": assemblies,
        "collision_meshes": collision_meshes,
    }

func _build_static_collision(world: Node3D, mesh_nodes: Array[Node]) -> int:
    var count: int = 0
    for node in mesh_nodes:
        if not (node is MeshInstance3D):
            continue
        var mesh_node := node as MeshInstance3D
        if mesh_node.mesh == null:
            continue
        var shape: Shape3D = mesh_node.mesh.create_trimesh_shape()
        if shape == null:
            continue
        var body := StaticBody3D.new()
        var collision := CollisionShape3D.new()
        collision.shape = shape
        body.add_child(collision)
        world.add_child(body)
        body.global_transform = mesh_node.global_transform
        body.name = "STATIC_FROM_" + String(mesh_node.name)
        count += 1
    return count

func _ray_support(world: Node3D, xz: Vector2) -> Dictionary:
    var space: PhysicsDirectSpaceState3D = world.get_world_3d().direct_space_state
    var query := PhysicsRayQueryParameters3D.create(Vector3(xz.x, 20.0, xz.y), Vector3(xz.x, -10.0, xz.y))
    query.collide_with_bodies = true
    query.collide_with_areas = false
    return space.intersect_ray(query)

func _supported_radii(world: Node3D, angle: float) -> Array[float]:
    var out: Array[float] = []
    for r in range(10, 39):
        var rf := float(r)
        var p := Vector2(cos(angle) * rf, sin(angle) * rf)
        if not _ray_support(world, p).is_empty():
            out.append(rf)
    return out

func _settle_character(world: Node3D, position: Vector3) -> Dictionary:
    var body := CharacterBody3D.new()
    var collision := CollisionShape3D.new()
    var capsule := CapsuleShape3D.new()
    capsule.radius = 0.38
    capsule.height = 1.85
    collision.shape = capsule
    body.add_child(collision)
    world.add_child(body)
    body.global_position = position
    var floor_frames: int = 0
    for _i in range(180):
        if not body.is_on_floor():
            body.velocity.y -= 18.0 / 60.0
        else:
            body.velocity.y = -0.05
            floor_frames += 1
        body.move_and_slide()
        await physics_frame
    var result: Dictionary = {
        "on_floor": body.is_on_floor(),
        "floor_frames": floor_frames,
        "position": [body.global_position.x, body.global_position.y, body.global_position.z],
    }
    body.queue_free()
    await physics_frame
    return result

func _radial_traverse(world: Node3D, angle: float, start_radius: float, target_radius: float) -> Dictionary:
    var direction := Vector3(cos(angle), 0.0, sin(angle)).normalized()
    var body := CharacterBody3D.new()
    var collision := CollisionShape3D.new()
    var capsule := CapsuleShape3D.new()
    capsule.radius = 0.38
    capsule.height = 1.85
    collision.shape = capsule
    body.add_child(collision)
    world.add_child(body)
    body.global_position = direction * start_radius + Vector3(0.0, 10.0, 0.0)
    for _i in range(180):
        body.velocity.y -= 18.0 / 60.0
        body.move_and_slide()
        await physics_frame
        if body.is_on_floor():
            break
    var floor_frames: int = 0
    var min_y: float = body.global_position.y
    var max_radius: float = Vector2(body.global_position.x, body.global_position.z).length()
    for _i in range(480):
        body.velocity.x = direction.x * 4.0
        body.velocity.z = direction.z * 4.0
        if body.is_on_floor():
            body.velocity.y = -0.05
            floor_frames += 1
        else:
            body.velocity.y -= 18.0 / 60.0
        body.move_and_slide()
        min_y = minf(min_y, body.global_position.y)
        max_radius = maxf(max_radius, Vector2(body.global_position.x, body.global_position.z).length())
        await physics_frame
        if max_radius >= target_radius + 1.0:
            break
    var radial: float = Vector2(body.global_position.x, body.global_position.z).length()
    var result: Dictionary = {
        "start_radius": start_radius,
        "target_radius": target_radius,
        "final_radius": radial,
        "max_radius": max_radius,
        "final_y": body.global_position.y,
        "min_y": min_y,
        "floor_frames": floor_frames,
    }
    body.queue_free()
    await physics_frame
    return result

func _compact_scene_result(data: Dictionary) -> Dictionary:
    var out := data.duplicate()
    out.erase("collision_meshes")
    return out

func _run() -> void:
    var world := Node3D.new()
    world.name = "ORIGIN_IMPORT_WORLD"
    get_root().add_child(world)

    var atrio: Dictionary = _inspect_scene("res://origin_atrio_rev6.glb", "atrio", world)
    var archive: Dictionary = _inspect_scene("res://origin_archive_rev6.glb", "archive", world)
    var atrio_loaded: bool = bool(atrio.get("loaded", false))
    var archive_loaded: bool = bool(archive.get("loaded", false))
    if not atrio_loaded or not archive_loaded:
        print("ORIGIN_REAL_IMPORT_RESULT=" + JSON.stringify({"failures": failures, "atrio": _compact_scene_result(atrio), "archive": _compact_scene_result(archive)}))
        quit(2)
        return

    if int(atrio.get("mesh_count", 0)) < 300:
        failures.append("atrio mesh count unexpectedly low")
    if int(atrio.get("lod1_nodes", 0)) < 140 or int(atrio.get("lod2_nodes", 0)) < 140:
        failures.append("atrio LOD nodes missing after import")
    if int(atrio.get("service_named_nodes", 0)) < 19 or int(atrio.get("culture_named_nodes", 0)) < 17:
        failures.append("atrio stable family naming lost")
    if int(archive.get("mesh_count", 0)) < 500:
        failures.append("archive mesh count unexpectedly low")
    if int(archive.get("lod1_nodes", 0)) < 90 or int(archive.get("lod2_nodes", 0)) < 90:
        failures.append("archive LOD nodes missing after import")
    if int(archive.get("assembly_ids_found", 0)) != 4:
        failures.append("archive assembly IDs missing after import")

    var collision_nodes: Array[Node] = atrio.get("collision_meshes", []) as Array[Node]
    var static_count: int = _build_static_collision(world, collision_nodes)
    await physics_frame
    await physics_frame

    var best_angle: float = 0.0
    var best_supported: Array[float] = []
    for deg in range(0, 360, 5):
        var angle := deg_to_rad(float(deg))
        var supported := _supported_radii(world, angle)
        if supported.size() > best_supported.size():
            best_supported = supported
            best_angle = angle

    var support_min_radius: float = best_supported[0] if not best_supported.is_empty() else 0.0
    var support_max_radius: float = best_supported[best_supported.size() - 1] if not best_supported.is_empty() else 0.0
    var direction := Vector3(cos(best_angle), 0.0, sin(best_angle))
    var inner_land: Dictionary = await _settle_character(world, direction * support_min_radius + Vector3(0.0, 10.0, 0.0)) if not best_supported.is_empty() else {"on_floor": false}
    var outer_land: Dictionary = await _settle_character(world, direction * support_max_radius + Vector3(0.0, 10.0, 0.0)) if not best_supported.is_empty() else {"on_floor": false}
    var traverse: Dictionary = await _radial_traverse(world, best_angle, support_min_radius, support_max_radius) if best_supported.size() >= 2 else {"max_radius": 0.0, "min_y": -999.0, "floor_frames": 0}

    var import_pass: bool = failures.is_empty()
    var physics_pass: bool = (
        static_count >= 19
        and best_supported.size() >= 8
        and bool(inner_land.get("on_floor", false))
        and bool(outer_land.get("on_floor", false))
        and float(traverse.get("max_radius", 0.0)) >= support_max_radius - 1.0
        and float(traverse.get("min_y", -999.0)) > -5.0
    )
    if not physics_pass:
        failures.append("real imported collision / CharacterBody traversal gate failed")

    report = {
        "godot": Engine.get_version_info(),
        "atrio": _compact_scene_result(atrio),
        "archive": _compact_scene_result(archive),
        "import_structure_pass_before_physics": import_pass,
        "static_collision_meshes_built": static_count,
        "best_supported_radii": best_supported,
        "best_angle_degrees": rad_to_deg(best_angle),
        "inner_character_landing": inner_land,
        "outer_character_landing": outer_land,
        "radial_character_traversal": traverse,
        "physics_pass": physics_pass,
        "failures": failures,
    }
    print("ORIGIN_REAL_IMPORT_RESULT=" + JSON.stringify(report))
    quit(0 if failures.is_empty() else 2)
