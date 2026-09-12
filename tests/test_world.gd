extends SceneTree
const World = preload("res://scenes/main.tscn")
var passed := 0
var failed := 0
var world: Node3D

func check(condition: bool, name: String) -> void:
	if condition:
		passed += 1
		print("PASS ",name)
	else:
		failed += 1
		print("FAIL ",name)

func frames(count: int) -> void:
	for i in range(count): await physics_frame

func _init() -> void:
	run.call_deferred()

func run() -> void:
	for suffix in ["", ".bak", ".tmp"]:
		DirAccess.remove_absolute("user://exovant-test-world.json"+suffix)
	world = World.instantiate()
	root.add_child(world)
	world.close_modal()
	var p = world.player
	await frames(30)
	check(p.is_on_floor(),"Player stands on a real collider")
	var start_z: float = p.position.z
	p.input_enabled = true
	Input.action_press("forward")
	await frames(60)
	Input.action_release("forward")
	check(p.position.z < start_z-5,"W movement advances character in physics")
	p.position = Vector3(41,.2,30)
	Input.action_press("right")
	await frames(60)
	Input.action_release("right")
	check(p.position.x<42,"Boundary collider blocks traversal")
	p.position = Vector3(5,.2,15)
	world.interact()
	check(world.progress.flags.get("met_ines",false),"Ines interaction starts mission")
	world.close_modal()
	p.position = Vector3(7,.2,-3.5)
	for i in range(3):
		for j in range(i+1):
			world.show_valves()
			var buttons: Array = []
			for child in world.modal_content.get_children():
				if child is Button: buttons.append(child)
			buttons[i].pressed.emit()
	check(world.progress.flags.get("water",false),"Valve UI buttons resolve actual mission")
	world.close_modal()
	p.position = Vector3(-9,.2,-27.7)
	world.interact()
	check(world.progress.flags.get("archive",false),"Archive interaction preserves authentic acta")
	world.close_modal()
	# Isolate the combat pair from other enemies for deterministic mechanics checks.
	for e in world.enemies:
		if not e.boss: e.health = 0; e.visible = false
	var boss = world.enemies[-1]
	p.position = Vector3(0,.2,-50.8)
	p.body_visual.rotation.y = 0
	p.input_enabled = false
	var hp: float = boss.health
	check(p.begin_attack(false) and not p.begin_attack(false),"Attack cannot be duplicated during its commitment")
	await frames(42)
	check(is_equal_approx(boss.health,hp-29),"Attack animation window damages boss exactly once")
	p.dodge_time = .3
	check(not p.receive_damage(30,boss.position),"Dodge invulnerability rejects incoming damage")
	p.dodge_time = 0
	p.guarding = true
	p.stamina = 100
	p.health = 100
	p.receive_damage(20,p.position+Vector3(0,0,-2))
	check(p.health>95 and p.stamina<100,"Frontal guard spends stamina and reduces damage")
	p.guarding = false
	p.health = 100
	var cover: MeshInstance3D = world.box(world,Vector3(0,1.5,-52.7),Vector3(5,3,.5),world.material(Color.GRAY),true)
	await frames(2)
	boss.state = "windup"
	boss.timer = .001
	boss.attack_target = p.position
	boss.attack_radius = 5
	await frames(2)
	check(p.health==100,"Solid cover blocks an enemy strike")
	cover.queue_free()
	await frames(2)
	# Native enemy FSM must wind up, hit and recover, not just expose health fields.
	boss.state = "idle"
	boss.position = Vector3(0,.2,-54)
	p.position = Vector3(0,.2,-51)
	await frames(105)
	check(p.health < 100 and boss.state == "recover","Enemy telegraph leads to damage and punish window")
	boss.receive_damage(500)
	await frames(2)
	check(boss.phase==3,"Atlas changes phase at the health thresholds")
	boss.receive_damage(200)
	check(world.progress.flags.get("atlas",false),"Boss defeat advances the campaign")
	world.show_choice()
	var choice_buttons: Array = []
	for child in world.modal_content.get_children():
		if child is Button: choice_buttons.append(child)
	choice_buttons[0].pressed.emit()
	check(world.progress.choice=="cogobierno","Consequence UI persists chosen outcome")
	var memories: int = world.progress.memories
	p.position = Vector3(0,.2,-42)
	world.player_died()
	check(world.progress.flags.get("resolved",false) and world.progress.echo_value==memories,"Death after ending preserves outcome and creates recoverable echo")
	p.position = world.echoes.position
	world.interact()
	check(world.progress.memories==memories and world.progress.echo.is_empty(),"World interaction recovers echo exactly once")
	# Traverse the installed ramp through the portal in the actual physics scene.
	p.position = Vector3(0,.3,-76)
	p.yaw = 0
	p.input_enabled = true
	Input.action_press("forward")
	await frames(100)
	Input.action_release("forward")
	check(p.position.z < -84 and p.position.y > 1.2,"Portal threshold is physically traversable")
	check(not world.storage.load_game().is_empty(),"World writes a recoverable campaign save")
	var receipt := {"suite":"native_scene_integration","passed":passed,"failed":failed,"portal_final_position":[p.position.x,p.position.y,p.position.z],"note":"Automated integration with controlled setup; not a full human playthrough or GPU benchmark"}
	var out := FileAccess.open("res://evidence/world-tests.json",FileAccess.WRITE)
	out.store_string(JSON.stringify(receipt,"  "))
	out.close()
	print(JSON.stringify(receipt))
	world.queue_free()
	await process_frame
	quit(1 if failed else 0)
