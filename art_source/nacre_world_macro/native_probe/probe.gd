extends SceneTree

const ASSET_PATH := "res://nacre_r5.glb"
const COLLISION_PREFIX := "NACRE_COLL_"
const EXPECTED_COLLISION_PROXIES := 12

var errors: Array[String] = []
var visible_meshes := 0
var collision_named_visible_meshes := 0
var static_bodies := 0
var collision_shapes := 0
var mesh_instances := 0
var material_names := {}
var bounds_initialized := false
var bounds_min := Vector3.ZERO
var bounds_max := Vector3.ZERO

func _initialize() -> void:
    if not ResourceLoader.exists(ASSET_PATH):
        _fail("missing imported asset: %s" % ASSET_PATH)
        _finish()
        return

    var resource := load(ASSET_PATH)
    if resource == null or not (resource is PackedScene):
        _fail("asset did not import as PackedScene")
        _finish()
        return

    var instance := (resource as PackedScene).instantiate()
    if instance == null:
        _fail("PackedScene instantiate returned null")
        _finish()
        return

    get_root().add_child(instance)
    _walk(instance)

    if collision_named_visible_meshes != 0:
        _fail("collision-only proxies survived as visible MeshInstance3D nodes: %d" % collision_named_visible_meshes)
    if static_bodies < EXPECTED_COLLISION_PROXIES:
        _fail("expected at least %d StaticBody3D nodes, got %d" % [EXPECTED_COLLISION_PROXIES, static_bodies])
    if collision_shapes < EXPECTED_COLLISION_PROXIES:
        _fail("expected at least %d CollisionShape3D nodes, got %d" % [EXPECTED_COLLISION_PROXIES, collision_shapes])
    if not bounds_initialized:
        _fail("no visible mesh bounds were produced")
    else:
        var span := bounds_max - bounds_min
        var maximum_span := max(span.x, max(span.y, span.z))
        if maximum_span < 1200.0 or maximum_span > 1600.0:
            _fail("unexpected macro scale: max span %.3f m" % maximum_span)
    if material_names.size() < 5:
        _fail("too few imported material roles: %d" % material_names.size())

    _finish()

func _walk(node: Node) -> void:
    if node is MeshInstance3D:
        var mesh_instance := node as MeshInstance3D
        mesh_instances += 1
        if mesh_instance.visible:
            visible_meshes += 1
        if String(mesh_instance.name).begins_with(COLLISION_PREFIX):
            collision_named_visible_meshes += 1
        _accumulate_mesh(mesh_instance)
    elif node is StaticBody3D:
        static_bodies += 1
    elif node is CollisionShape3D:
        collision_shapes += 1

    for child in node.get_children():
        _walk(child)

func _accumulate_mesh(mesh_instance: MeshInstance3D) -> void:
    var mesh := mesh_instance.mesh
    if mesh == null:
        return

    for surface in range(mesh.get_surface_count()):
        var material := mesh.surface_get_material(surface)
        if material != null:
            var role := material.resource_name
            if role.is_empty():
                role = "<unnamed>"
            material_names[role] = true

    var aabb := mesh.get_aabb()
    var p := aabb.position
    var s := aabb.size
    var corners := [
        Vector3(p.x, p.y, p.z),
        Vector3(p.x + s.x, p.y, p.z),
        Vector3(p.x, p.y + s.y, p.z),
        Vector3(p.x, p.y, p.z + s.z),
        Vector3(p.x + s.x, p.y + s.y, p.z),
        Vector3(p.x + s.x, p.y, p.z + s.z),
        Vector3(p.x, p.y + s.y, p.z + s.z),
        Vector3(p.x + s.x, p.y + s.y, p.z + s.z),
    ]
    for corner in corners:
        var world_point := mesh_instance.global_transform * corner
        if not bounds_initialized:
            bounds_min = world_point
            bounds_max = world_point
            bounds_initialized = true
        else:
            bounds_min = Vector3(min(bounds_min.x, world_point.x), min(bounds_min.y, world_point.y), min(bounds_min.z, world_point.z))
            bounds_max = Vector3(max(bounds_max.x, world_point.x), max(bounds_max.y, world_point.y), max(bounds_max.z, world_point.z))

func _fail(message: String) -> void:
    errors.append(message)
    push_error(message)

func _finish() -> void:
    var span := Vector3.ZERO
    if bounds_initialized:
        span = bounds_max - bounds_min

    var receipt := {
        "passed": errors.is_empty(),
        "asset_path": ASSET_PATH,
        "mesh_instances": mesh_instances,
        "visible_meshes": visible_meshes,
        "collision_named_visible_meshes": collision_named_visible_meshes,
        "static_bodies": static_bodies,
        "collision_shapes": collision_shapes,
        "material_roles": material_names.keys(),
        "bounds_span_m": [span.x, span.y, span.z],
        "errors": errors,
    }
    print("NACRE_NATIVE_RECEIPT=" + JSON.stringify(receipt))
    quit(0 if errors.is_empty() else 2)
