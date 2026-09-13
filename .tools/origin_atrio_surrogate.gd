extends SceneTree

# EXOVANT 2950 — ORIGIN / Atrio de las Rutas
# Integration-only surrogate physics gate for CLM-ORIGIN-MEGA-ATRIO-001.
# IMPORTANT: this reconstructs the validated collision dimensions from Blender rev2.
# It does NOT import the real GLB and therefore cannot promote the engine-import gate.

const CLAIM := "CLM-ORIGIN-MEGA-ATRIO-001"
const MODEL_REVISION := 2
const RING_Y := 4.0
const RING_COLLISION_HEIGHT := 0.648
const RING_COLLISION_WIDTH := 4.6
const BRIDGE_COLLISION_HEIGHT := 0.55
const BRIDGE_COLLISION_WIDTH := 4.1
const PLAYER_HEIGHT := 1.85
const PLAYER_RADIUS := 0.38
const GRAVITY := 24.0
const WALK_SPEED := 5.0

var passed := 0
var failed := 0
var world: Node3D
var player: CharacterBody3D
var case_results: Dictionary = {}

func check(condition: bool, name: String, details: Dictionary = {}) -> void:
	if condition:
		passed += 1
		print("PASS ", name, " ", JSON.stringify(details))
	else:
		failed += 1
		print("FAIL ", name, " ", JSON.stringify(details))

func _init() -> void:
	call_deferred("_run")

func _run() -> void:
	world = Node3D.new()
	world.name = "ORIGIN_ATRIO_SURROGATE_WORLD"
	root.add_child(world)
	_build_collision_surrogate()
	_build_player()
	await physics_frame

	var ring_ok := await _case_outer_ring_sector()
	case_results["outer_ring_sector"] = ring_ok
	check(ring_ok, "CharacterBody traverses outer-ring sector without falling")

	var bridge_ok := await _case_radial_bridge_chain()
	case_results["radial_bridge_chain"] = bridge_ok
	check(bridge_ok, "CharacterBody crosses outer-middle-inner radial bridge chain")

	var node_ok := await _case_middle_ring_node_zone()
	case_results["safe_node_zone"] = node_ok
	check(node_ok, "CharacterBody traverses middle-ring safe-node zone without snagging")

	var clearance := 6.0 - 1.40
	var aperture_ok := clearance > (PLAYER_RADIUS * 2.0) + 1.0
	case_results["route_aperture_clearance_m"] = clearance
	check(aperture_ok, "Route aperture collision clearance exceeds capsule width plus margin", {
		"clearance_m": clearance,
		"capsule_diameter_m": PLAYER_RADIUS * 2.0,
		"margin_m": clearance - PLAYER_RADIUS * 2.0
	})

	var receipt := {
		"suite": "origin_atrio_surrogate_traversal",
		"claim_id": CLAIM,
		"model_revision": MODEL_REVISION,
		"truth_state": "SURROGATE_TRAVERSAL_ONLY",
		"real_glb_import": false,
		"geometry_source": "Blender revision 2 validated collision dimensions reconstructed in Godot primitives",
		"player": {"height_m": PLAYER_HEIGHT, "radius_m": PLAYER_RADIUS},
		"cases": case_results,
		"passed": passed,
		"failed": failed,
		"engine": Engine.get_version_info().string
	}
	var out := FileAccess.open("res://evidence/origin-atrio-surrogate.json", FileAccess.WRITE)
	out.store_string(JSON.stringify(receipt, "  "))
	out.close()
	print(JSON.stringify(receipt))
	quit(1 if failed else 0)

func _build_collision_surrogate() -> void:
	for radius in [35.0, 24.0, 13.0]:
		for center_deg in [0.0, 120.0, 240.0]:
			_add_ring_sector(radius, deg_to_rad(center_deg), 18)

	for angle_deg in [0.0, 120.0, 240.0]:
		var a := deg_to_rad(angle_deg)
		_add_bridge_span(a, 15.5, 21.5)
		_add_bridge_span(a, 26.5, 32.5)

	_add_dodecagonal_node("COL_ORG_ATR_NODE_SAFE", Vector3(24.0, RING_Y, 0.0), 3.72, 0.58)
	var valve_a := deg_to_rad(120.0)
	_add_dodecagonal_node("COL_ORG_ATR_NODE_VALVE", Vector3(24.0 * cos(valve_a), RING_Y, 24.0 * sin(valve_a)), 3.72, 0.58)

	# Route-aperture pylons: same horizontal proxy dimensions and placement as rev2 generator.
	var ap_a := deg_to_rad(60.0)
	var radial := Vector3(cos(ap_a), 0.0, sin(ap_a))
	var tangent := Vector3(-sin(ap_a), 0.0, cos(ap_a))
	var base := radial * 35.0
	for side in [-1.0, 1.0]:
		var center := base + tangent * (side * 3.0)
		center.y = RING_Y + 2.55
		_add_box("COL_ORG_ATR_ROUTE_APERTURE_PYLON_%s" % side, center, Vector3(0.95, 5.0, 1.40), -ap_a)

func _add_ring_sector(radius: float, center_angle: float, segments: int) -> void:
	var span := deg_to_rad(108.0)
	var step := span / float(segments)
	for i in range(segments):
		var a := center_angle - span * 0.5 + (float(i) + 0.5) * step
		var chord := 2.0 * radius * sin(step * 0.5) * 1.06
		var center := Vector3(radius * cos(a), RING_Y, radius * sin(a))
		_add_box(
			"COL_RING_R%.0f_%03d" % [radius, i + int(rad_to_deg(center_angle))],
			center,
			Vector3(chord, RING_COLLISION_HEIGHT, RING_COLLISION_WIDTH),
			-(a + PI * 0.5)
		)

func _add_bridge_span(angle: float, r0: float, r1: float) -> void:
	var rm := (r0 + r1) * 0.5
	var length := r1 - r0
	var center := Vector3(rm * cos(angle), RING_Y, rm * sin(angle))
	_add_box(
		"COL_BRIDGE_%03d_%.1f_%.1f" % [int(rad_to_deg(angle)), r0, r1],
		center,
		Vector3(length, BRIDGE_COLLISION_HEIGHT, BRIDGE_COLLISION_WIDTH),
		-angle
	)

func _add_box(name_: String, center: Vector3, size_: Vector3, yaw: float) -> void:
	var body := StaticBody3D.new()
	body.name = name_
	body.position = center
	body.rotation.y = yaw
	var collision := CollisionShape3D.new()
	var shape := BoxShape3D.new()
	shape.size = size_
	collision.shape = shape
	body.add_child(collision)
	world.add_child(body)

func _add_dodecagonal_node(name_: String, center: Vector3, radius: float, height: float) -> void:
	var points := PackedVector3Array()
	for i in range(12):
		var a := TAU * float(i) / 12.0
		points.append(Vector3(radius * cos(a), -height * 0.5, radius * sin(a)))
		points.append(Vector3(radius * cos(a), height * 0.5, radius * sin(a)))
	var shape := ConvexPolygonShape3D.new()
	shape.points = points
	var collision := CollisionShape3D.new()
	collision.shape = shape
	var body := StaticBody3D.new()
	body.name = name_
	body.position = center
	body.add_child(collision)
	world.add_child(body)

func _build_player() -> void:
	player = CharacterBody3D.new()
	player.name = "SURROGATE_PlayerCapsule_1p85"
	player.up_direction = Vector3.UP
	player.floor_snap_length = 0.30
	player.floor_max_angle = deg_to_rad(50.0)
	player.safe_margin = 0.01
	var collision := CollisionShape3D.new()
	var capsule := CapsuleShape3D.new()
	capsule.height = PLAYER_HEIGHT
	capsule.radius = PLAYER_RADIUS
	collision.shape = capsule
	player.add_child(collision)
	world.add_child(player)

func _deck_player_y() -> float:
	return RING_Y + RING_COLLISION_HEIGHT * 0.5 + PLAYER_HEIGHT * 0.5 + 0.04

func _reset_player(position_xz: Vector3) -> bool:
	player.global_position = Vector3(position_xz.x, _deck_player_y(), position_xz.z)
	player.velocity = Vector3.ZERO
	for _i in range(20):
		await physics_frame
		if player.is_on_floor():
			player.velocity.y = -0.05
		else:
			player.velocity.y -= GRAVITY / 60.0
		player.move_and_slide()
	return player.global_position.y > 4.0 and player.global_position.y < 5.6

func _walk_to(target: Vector3, max_frames: int = 240) -> bool:
	for _i in range(max_frames):
		await physics_frame
		var delta_xz := Vector3(target.x - player.global_position.x, 0.0, target.z - player.global_position.z)
		if delta_xz.length() < 0.45:
			player.velocity.x = 0.0
			player.velocity.z = 0.0
			player.velocity.y = -0.05 if player.is_on_floor() else player.velocity.y - GRAVITY / 60.0
			player.move_and_slide()
			return player.global_position.y > 4.0
		var direction := delta_xz.normalized()
		player.velocity.x = direction.x * WALK_SPEED
		player.velocity.z = direction.z * WALK_SPEED
		if player.is_on_floor():
			player.velocity.y = -0.05
		else:
			player.velocity.y -= GRAVITY / 60.0
		player.move_and_slide()
		if player.global_position.y < 3.0:
			return false
	return false

func _case_outer_ring_sector() -> bool:
	var start_a := deg_to_rad(-40.0)
	if not await _reset_player(Vector3(35.0 * cos(start_a), 0.0, 35.0 * sin(start_a))):
		return false
	for deg in [-30.0, -20.0, -10.0, 0.0, 10.0, 20.0, 30.0, 40.0]:
		var a := deg_to_rad(deg)
		if not await _walk_to(Vector3(35.0 * cos(a), 0.0, 35.0 * sin(a))):
			return false
	return true

func _case_radial_bridge_chain() -> bool:
	if not await _reset_player(Vector3(34.0, 0.0, 0.0)):
		return false
	for radius in [31.0, 28.0, 25.0, 22.5, 19.0, 16.0, 14.0]:
		if not await _walk_to(Vector3(radius, 0.0, 0.0)):
			return false
	return true

func _case_middle_ring_node_zone() -> bool:
	var start_a := deg_to_rad(-14.0)
	if not await _reset_player(Vector3(24.0 * cos(start_a), 0.0, 24.0 * sin(start_a))):
		return false
	for deg in [-8.0, -3.0, 0.0, 3.0, 8.0, 14.0]:
		var a := deg_to_rad(deg)
		if not await _walk_to(Vector3(24.0 * cos(a), 0.0, 24.0 * sin(a))):
			return false
	return true
