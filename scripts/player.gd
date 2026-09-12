extends CharacterBody3D
var world: Node3D
var health := 100.0
var stamina := 100.0
var flasks := 3
var yaw := 0.0
var pitch := -0.26
var dodge_time := 0.0
var attack_time := 0.0
var attack_heavy := false
var attack_fired := false
var guarding := false
var in_vehicle := false
var locked: Node3D
var dodge_direction := Vector3.ZERO
var camera: Camera3D
var body_visual: Node3D
var blade: Node3D
var gait := 0.0
var input_enabled := true

func _ready() -> void:
	collision_layer = 2
	collision_mask = 1
	var shape := CollisionShape3D.new()
	var capsule := CapsuleShape3D.new()
	capsule.radius = 0.38
	capsule.height = 1.85
	shape.shape = capsule
	shape.position.y = 0.95
	add_child(shape)
	body_visual = world.make_humanoid(self, Color("c4c8bb"), false)
	blade = world.box(body_visual, Vector3(.56,1.0,-.5), Vector3(.08,.09,1.25), world.material(Color("9dddd9"),.7,1.0))
	camera = Camera3D.new()
	get_parent().add_child(camera)
	camera.fov = 67
	camera.current = true
	camera.position = position + Vector3(0,4,7)

func _unhandled_input(event: InputEvent) -> void:
	if not input_enabled or world.modal_open or event.is_echo(): return
	if event is InputEventMouseMotion and Input.mouse_mode == Input.MOUSE_MODE_CAPTURED:
		yaw -= event.relative.x * .0025
		pitch = clampf(pitch - event.relative.y * .0025, -.8, .2)
	if event.is_action_pressed("light_attack"): begin_attack(false)
	if event.is_action_pressed("heavy_attack"): begin_attack(true)
	if event.is_action_pressed("dodge"): begin_dodge()
	if event.is_action_pressed("heal") and flasks > 0 and health < 100 and attack_time <= 0 and dodge_time <= 0:
		flasks -= 1
		health = minf(100, health + 50)
		world.notify("Memoria restaurada · %d cargas" % flasks)
	if event.is_action_pressed("lock"):
		locked = null if is_instance_valid(locked) else world.nearest_enemy(global_position,28)
	if event.is_action_pressed("interact"): world.interact()

func begin_attack(heavy: bool) -> bool:
	var cost := 34.0 if heavy else 19.0
	if health <= 0 or in_vehicle or world.modal_open or attack_time > 0 or dodge_time > 0 or stamina < cost: return false
	stamina -= cost
	attack_heavy = heavy
	attack_time = 1.0 if heavy else .58
	attack_fired = false
	return true

func begin_dodge() -> bool:
	if health <= 0 or in_vehicle or world.modal_open or attack_time > 0 or dodge_time > 0 or stamina < 27: return false
	stamina -= 27
	dodge_time = .52
	dodge_direction = movement_direction()
	if dodge_direction.length() < .1: dodge_direction = -body_visual.global_basis.z
	return true

func movement_direction() -> Vector3:
	if not input_enabled: return Vector3.ZERO
	var input := Input.get_vector("left", "right", "forward", "back")
	return Vector3(input.x, 0, input.y).rotated(Vector3.UP, yaw)

func receive_damage(amount: float, source: Vector3) -> bool:
	if health <= 0 or (dodge_time > .14 and dodge_time < .50): return false
	if guarding and stamina >= amount * .8:
		var towards := (source - global_position).normalized()
		if (-body_visual.global_basis.z).dot(towards) > .25:
			stamina -= amount * .8
			amount *= .15
	health = maxf(0, health - amount)
	world.damage_flash = .28
	if health <= 0: world.player_died()
	return true

func _physics_process(dt: float) -> void:
	if world.modal_open: return
	if input_enabled and not is_instance_valid(locked):
		var look := Input.get_vector("look_left","look_right","look_up","look_down",.22)
		yaw -= look.x * 2.8 * dt
		pitch = clampf(pitch - look.y * 1.8 * dt,-.8,.2)
	guarding = input_enabled and Input.is_action_pressed("guard") and attack_time <= 0 and dodge_time <= 0
	if is_instance_valid(locked) and (locked.health <= 0 or global_position.distance_to(locked.global_position) > 35): locked = null
	if is_instance_valid(locked):
		var v: Vector3 = locked.global_position - global_position
		yaw = lerp_angle(yaw, atan2(-v.x,-v.z), dt*8)
	var direction := movement_direction()
	var speed := 20.0 if in_vehicle else (3.0 if guarding else 6.0)
	if dodge_time > 0:
		dodge_time = maxf(0,dodge_time-dt)
		direction = dodge_direction
		speed = 13
	if attack_time > 0:
		attack_time = maxf(0,attack_time-dt)
		speed *= .25
		var hit_at := .48 if attack_heavy else .28
		if attack_time <= hit_at and not attack_fired:
			attack_fired = true
			world.player_strike(attack_heavy)
	else:
		stamina = minf(100,stamina + dt * (13 if guarding else 25))
	velocity.x = direction.x*speed
	velocity.z = direction.z*speed
	if not is_on_floor(): velocity.y -= 24*dt
	else:
		velocity.y = 0
		if input_enabled and Input.is_action_just_pressed("jump") and not in_vehicle: velocity.y = 8
	move_and_slide()
	if global_position.y < -15: world.player_died()
	if direction.length() > .1 and not is_instance_valid(locked): body_visual.rotation.y = lerp_angle(body_visual.rotation.y, atan2(-direction.x,-direction.z), dt*12)
	elif is_instance_valid(locked): body_visual.rotation.y = yaw
	gait += dt*velocity.length()*1.4
	body_visual.position.y = sin(gait)*.045 if is_on_floor() else 0
	var walk_amount := minf(velocity.length()/6.0,1.0)
	body_visual.get_node("LegL").rotation.x = sin(gait)*.45*walk_amount
	body_visual.get_node("LegR").rotation.x = -sin(gait)*.45*walk_amount
	body_visual.get_node("ArmL").rotation.x = -sin(gait)*.28*walk_amount
	body_visual.get_node("ArmR").rotation.x = -1.1 if attack_time>0 else sin(gait)*.28*walk_amount
	body_visual.visible = not in_vehicle
	blade.rotation.y = sin(attack_time*9)*1.8 if attack_time > 0 else -.12
	var focus := global_position + Vector3(0,1.7,0)
	var offset := Vector3(0,1.2-pitch*2.8,6.5).rotated(Vector3.UP,yaw)
	var desired := focus + offset
	var ray := PhysicsRayQueryParameters3D.create(focus,desired,1)
	var hit := get_world_3d().direct_space_state.intersect_ray(ray)
	if not hit.is_empty(): desired = hit.position + hit.normal*.3
	camera.global_position = camera.global_position.lerp(desired,1-exp(-8*dt))
	camera.look_at(focus)
