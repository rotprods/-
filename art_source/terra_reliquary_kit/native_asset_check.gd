extends SceneTree
## Isolated offline import check; never loads or alters the game runtime.
var failed: Array[String] = []
var mesh_count := 0
var materials_checked := 0
var textured_materials := {}
var roots_found: Array[String] = []
var collision_shapes := 0

func inspect(node: Node) -> void:
    if node is CollisionShape3D:
        collision_shapes += 1
        if node.shape == null: failed.append("Empty collision shape")
    if node is MeshInstance3D:
        if str(node.name).begins_with("COL_"): failed.append("Collision source remained visible")
        mesh_count += 1
        if node.mesh == null:
            failed.append("Null mesh: " + str(node.name))
        else:
            for s in range(node.mesh.get_surface_count()):
                var a = node.mesh.surface_get_arrays(s)
                if a[Mesh.ARRAY_VERTEX].is_empty(): failed.append("Empty mesh surface")
                if a[Mesh.ARRAY_TEX_UV] == null or a[Mesh.ARRAY_TEX_UV].is_empty(): failed.append("Missing UV")
                var m = node.get_active_material(s)
                if m is BaseMaterial3D:
                    materials_checked += 1
                    if m.albedo_texture != null:
                        textured_materials[m.resource_name] = true
                        if m.normal_texture == null: failed.append("Lost normal texture: " + m.resource_name)
                        if m.roughness_texture == null: failed.append("Lost roughness texture: " + m.resource_name)
                        if m.albedo_texture.get_width() != 512: failed.append("Unexpected map size")
                else: failed.append("Material not imported as portable PBR")
    elif node.name.begins_with("ENV_") or node.name.begins_with("PR_") or node.name.begins_with("KIT_") or node.name.begins_with("BIO_"):
        roots_found.append(str(node.name))
    for child in node.get_children(): inspect(child)

func _initialize() -> void:
    call_deferred("run_check")

func run_check() -> void:
    var packed = load("res://candidate.glb") as PackedScene
    if packed == null:
        printerr("GLB did not import"); quit(1); return
    var model = packed.instantiate()
    root.add_child(model)
    inspect(model)
    await physics_frame
    await physics_frame
    if collision_shapes != 11: failed.append("Expected 11 collision shapes, found " + str(collision_shapes))
    var query = PhysicsRayQueryParameters3D.create(Vector3(0, 2, 2), Vector3(0, -2, 2))
    var hit = model.get_world_3d().direct_space_state.intersect_ray(query)
    if hit.is_empty(): failed.append("No floor collision at walkable approach")
    elif absf(hit.position.y - 0.02) > 0.02: failed.append("Floor collision height differs from rendered floor")
    if roots_found.size() < 10: failed.append("Missing asset assembly roots")
    if textured_materials.size() != 4: failed.append("Material family count differs")
    var report = {"passed": failed.is_empty(), "failed": failed, "mesh_instances": mesh_count,
        "material_surfaces_checked": materials_checked, "textured_material_families": textured_materials.keys(),
        "roots": roots_found, "collision_shapes": collision_shapes, "approach_floor_ray_hit": not hit.is_empty(), "engine": Engine.get_version_info().string,
        "scope": "Actual headless Godot import/instantiation and PBR/UV preservation. No artistic approval, playtest or GPU benchmark."}
    var file = FileAccess.open("res://native-asset-check.json", FileAccess.WRITE)
    file.store_string(JSON.stringify(report, "  ") + "\n"); file.close()
    print(JSON.stringify(report)); quit(0 if failed.is_empty() else 1)
