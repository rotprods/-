extends CharacterBody3D
var world: Node3D
var boss := false
var enemy_id := ""
var health := 70.0
var max_health := 70.0
var home := Vector3.ZERO
var visual: Node3D
var warning: MeshInstance3D
var phase := 1
var state := "idle"
var timer := 0.0
var attack_index := 0
var attack_target := Vector3.ZERO
var attack_radius := 3.0
var bar: Label3D

func _ready() -> void:
	collision_layer = 4
	collision_mask = 1
	max_health = 650 if boss else 70
	health = max_health
	home = position
	var s := CollisionShape3D.new()
	var c := CapsuleShape3D.new()
	c.radius = 1.1 if boss else .4
	c.height = 5.8 if boss else 1.8
	s.shape = c
	s.position.y = c.height/2
	add_child(s)
	visual = world.make_humanoid(self, Color("758b76") if boss else Color("a69580"), boss)
	bar = Label3D.new()
	bar.position.y = 6.5 if boss else 2.6
	bar.font_size = 28
	bar.pixel_size = .01
	bar.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	add_child(bar)
	warning = MeshInstance3D.new()
	var disc := CylinderMesh.new()
	disc.top_radius = 1
	disc.bottom_radius = 1
	disc.height = .025
	disc.radial_segments = 48
	warning.mesh = disc
	warning.material_override = world.material(Color(1,.18,.08,.4),0,1.0)
	get_parent().add_child(warning)
	warning.visible = false

func reset_encounter() -> void:
	health = max_health
	position = home
	state = "idle"
	phase = 1
	timer = 0
	visible = true
	warning.visible = false

func receive_damage(amount: float) -> void:
	if health <= 0 or (boss and not world.progress.flags.get("archive",false)): return
	health = maxf(0, health-amount)
	if health <= 0:
		state = "dead"
		visible = false
		warning.visible = false
		world.enemy_defeated(self)

func _physics_process(dt: float) -> void:
	if world.modal_open or health <= 0: return
	if boss and (not world.progress.flags.get("archive",false) or world.progress.flags.get("atlas",false)):
		bar.text = "ATLAS · PROTOCOLO DORMIDO" if not world.progress.flags.get("atlas",false) else "ATLAS · AISLADO"
		return
	var player: Node3D = world.player
	var distance := global_position.distance_to(player.global_position)
	phase = (1 if health > max_health*.6 else (2 if health > max_health*.25 else 3)) if boss else 1
	bar.text = ("ATLAS · FASE %d · %d" % [phase,int(health)]) if boss else ("CUSTODIO · %d" % int(health))
	if state == "windup":
		timer -= dt
		warning.visible = true
		warning.position = attack_target + Vector3(0,.05,0)
		warning.scale = Vector3.ONE*attack_radius
		if timer <= 0:
			var sight := PhysicsRayQueryParameters3D.create(global_position+Vector3.UP,player.global_position+Vector3.UP,1)
			var clear_sight := get_world_3d().direct_space_state.intersect_ray(sight).is_empty()
			if clear_sight and Vector2(player.global_position.x-attack_target.x,player.global_position.z-attack_target.z).length() < attack_radius and absf(player.global_position.y-attack_target.y) < 2.8:
				player.receive_damage(34.0 + phase*4 if boss else 22.0,global_position)
			world.pulse_at(attack_target,attack_radius)
			state = "recover"
			timer = 1.3 if boss else 1.05
			warning.visible = false
	elif state == "recover":
		timer -= dt
		if timer <= 0: state = "idle"
	else:
		var leash := 30.0 if boss else 17.0
		if distance < (5.8 if boss else 2.6):
			state = "windup"
			attack_index += 1
			attack_target = player.global_position if boss and attack_index % 2 == 0 else global_position
			attack_target.y = 0
			attack_radius = (3.2 + phase*.5) if boss else 2.5
			timer = (1.25 if attack_index%2==0 else .95) if boss else .85
		elif distance < leash:
			var dir := player.global_position-global_position
			dir.y = 0
			dir = dir.normalized()
			velocity.x = dir.x*(2.0+phase*.25 if boss else 3.3)
			velocity.z = dir.z*(2.0+phase*.25 if boss else 3.3)
			visual.rotation.y = atan2(-dir.x,-dir.z)
		else:
			var dir := home-global_position
			dir.y = 0
			velocity.x = dir.normalized().x*minf(dir.length(),2.0)
			velocity.z = dir.normalized().z*minf(dir.length(),2.0)
	if state in ["windup","recover"]:
		velocity.x = 0
		velocity.z = 0
	if not is_on_floor(): velocity.y -= 24*dt
	else: velocity.y = 0
	move_and_slide()
