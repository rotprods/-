extends SceneTree
const Controls = preload("res://scripts/controls.gd")
const World = preload("res://scenes/main.tscn")
const SETTINGS := "user://exovant-test-input-controls.json"
var passed := 0
var failed := 0

func check(condition: bool, name: String) -> void:
	if condition: passed += 1; print("PASS ",name)
	else: failed += 1; print("FAIL ",name)

func frames(count: int) -> void:
	for i in range(count): await physics_frame

func key(code: int, down: bool = true) -> InputEventKey:
	var e := InputEventKey.new()
	e.keycode = code; e.physical_keycode = code; e.pressed = down
	return e

func pad(code: int, down: bool = true) -> InputEventJoypadButton:
	var e := InputEventJoypadButton.new()
	e.device = 0; e.button_index = code; e.pressed = down
	return e

func emit(event: InputEvent) -> void:
	Input.parse_input_event(event.duplicate())
	Input.flush_buffered_events()

func tap(event: InputEvent) -> void:
	emit(event)
	await process_frame
	await frames(2)
	event.pressed = false
	emit(event)
	await frames(2)

func axis(code: int, value: float) -> void:
	var e := InputEventJoypadMotion.new()
	e.device = 0; e.axis = code; e.axis_value = value
	emit(e)

func _init() -> void:
	run.call_deferred()

func run() -> void:
	# Headless CI has no focused native window; only this synthetic-event harness opts in.
	Input.ignore_joypad_on_unfocused_application = false
	for path in [SETTINGS,"user://exovant-test-input.json"]:
		for suffix in ["",".bak",".tmp"]: DirAccess.remove_absolute(path+suffix)
	var settings = Controls.new(SETTINGS)
	check(settings.load_bindings() and Controls.valid(settings.bindings),"Missing preferences load complete defaults")
	var counts := {}
	for action in Controls.LABELS: counts[action] = InputMap.action_get_events(action).size()
	settings.apply()
	check(Controls.LABELS.keys().all(func(a): return InputMap.action_get_events(a).size() == counts[a]),"Reconfiguration does not duplicate input bindings")
	check(settings.rebind("interact",key(KEY_L)),"Free physical keyboard binding saves")
	var reopened = Controls.new(SETTINGS)
	check(reopened.load_bindings() and reopened.binding_text("interact") == "L","Remap survives a new settings instance")
	var saved := FileAccess.get_file_as_string(SETTINGS)
	check(not reopened.rebind("interact",key(KEY_W)) and FileAccess.get_file_as_string(SETTINGS) == saved,"Duplicate keyboard binding preserves saved controls")
	check(not reopened.rebind("interact",key(KEY_ESCAPE)),"Escape cannot be stolen from menus")
	check(reopened.rebind("heal",pad(JOY_BUTTON_Y)) and reopened.bindings.heavy_attack.gamepad.code == JOY_BUTTON_X,"Occupied gamepad button swaps both actions without losing one")
	var bad: Dictionary = reopened.bindings.duplicate(true)
	bad.forward.desktop.code = 4.5
	check(not Controls.valid(bad),"Fractional input codes are rejected")
	bad = reopened.bindings.duplicate(true); bad.interact.desktop.code = KEY_ESCAPE
	check(not Controls.valid(bad),"Persisted reserved keys are rejected too")
	var unavailable = Controls.new("user://does-not-exist/input.json")
	check(not unavailable.rebind("interact",key(KEY_L)) and unavailable.binding_text("interact") == "E","Write failure keeps previous active configuration")
	var broken := FileAccess.open(SETTINGS,FileAccess.WRITE)
	broken.store_string("{ broken"); broken.close()
	check(not reopened.load_bindings() and reopened.binding_text("interact") == "E","Corrupt preferences recover safe defaults")
	check(reopened.commit(Controls.defaults()),"User can persist restored defaults")
	var world = World.instantiate()
	root.add_child(world)
	await frames(3)
	check(world.modal_open and root.gui_get_focus_owner() is Button,"New-game menu has initial keyboard/controller focus")
	var initial_focus := root.gui_get_focus_owner()
	await tap(pad(JOY_BUTTON_DPAD_DOWN))
	check(root.gui_get_focus_owner()!=initial_focus,"Controller D-pad navigates menu choices")
	await tap(pad(JOY_BUTTON_DPAD_UP))
	await tap(pad(JOY_BUTTON_A))
	check(not world.modal_open and world.player.attack_time == 0,"Controller accepts title without leaking an attack into play")
	var p = world.player
	await frames(20)
	var start: Vector3 = p.position
	axis(JOY_AXIS_LEFT_X,.1)
	await frames(20)
	check(absf(p.position.x-start.x)<.01,"Stick drift inside deadzone does not move player")
	axis(JOY_AXIS_LEFT_X,.5)
	await frames(30)
	axis(JOY_AXIS_LEFT_X,0)
	var half_distance: float = p.position.x-start.x
	axis(JOY_AXIS_LEFT_X,1)
	await frames(30)
	axis(JOY_AXIS_LEFT_X,0)
	var full_distance: float = p.position.x-start.x-half_distance
	check(half_distance>.5 and full_distance>half_distance*1.8,"Analog stick preserves partial walking speed")
	# No teleport/state grant: reach the first NPC from the genuine fresh-game spawn.
	axis(JOY_AXIS_LEFT_Y,-1)
	await frames(30)
	axis(JOY_AXIS_LEFT_Y,0)
	await tap(pad(JOY_BUTTON_A))
	check(world.progress.flags.get("met_ines",false),"Fresh-spawn walk and controller interaction start Ines mission")
	check(world.modal_open and root.gui_get_focus_owner() is Button,"Dialogue retains controller focus")
	var before: Vector3 = p.position
	var enemy_before: Vector3 = world.enemies[0].position
	axis(JOY_AXIS_LEFT_Y,-1)
	await tap(pad(JOY_BUTTON_RIGHT_SHOULDER))
	await frames(20)
	axis(JOY_AXIS_LEFT_Y,0)
	check(p.position.is_equal_approx(before) and world.enemies[0].position.is_equal_approx(enemy_before) and p.attack_time==0,"Modal freezes player/enemies and blocks combat input")
	check(not p.begin_dodge(),"Dodge entry point also refuses modal input")
	await tap(pad(JOY_BUTTON_B))
	check(not world.modal_open and p.dodge_time==0,"Controller cancel closes dialogue without leaking a dodge")
	var yaw_before: float = p.yaw
	axis(JOY_AXIS_RIGHT_X,1)
	await frames(20)
	axis(JOY_AXIS_RIGHT_X,0)
	check(p.yaw<yaw_before-.5,"Right stick rotates gameplay camera")
	await tap(pad(JOY_BUTTON_START))
	check(world.modal_open,"Start pauses gameplay")
	world.controls_return = world.show_pause
	world.show_controls()
	await frames(2)
	check(root.gui_get_focus_owner() is Button,"Scrollable remapping menu has focus")
	world.begin_rebind("interact")
	await tap(key(KEY_L))
	check(world.rebind_action=="" and world.controls.binding_text("interact")=="L" and world.modal_open,"Physical key capture persists remap without unpausing")
	check(world.controls.footer().contains("L interactuar"),"HUD uses saved keyboard mapping")
	check(world.controls.binding_text("interact",true)=="A / Cruz","Keyboard remap preserves independent controller binding")
	world.begin_rebind("heal")
	await tap(key(KEY_ESCAPE))
	check(world.rebind_action=="" and world.modal_open,"Escape cancels capture and keeps controls menu open")
	await tap(key(KEY_ESCAPE))
	check(not world.modal_open,"Escape remains a route back to gameplay")
	await tap(key(KEY_L))
	check(world.modal_open,"Remapped physical interaction works in the scene")
	await tap(key(KEY_ESCAPE))
	await tap(pad(JOY_BUTTON_RIGHT_SHOULDER))
	check(p.attack_time>0 and p.stamina<100,"Controller attack executes combat commitment")
	await frames(40)
	await tap(pad(JOY_BUTTON_B))
	check(p.dodge_time>0,"Controller dodge executes outside menus")
	var receipt := {"suite":"native_input_and_preferences","passed":passed,"failed":failed,
		"fresh_route":"spawn to Ines only; no teleports or progression injection",
		"scope":"Synthetic physical InputEvents through engine; no attached-controller hardware or full human playthrough claim"}
	var out := FileAccess.open("res://evidence/input-tests.json",FileAccess.WRITE)
	out.store_string(JSON.stringify(receipt,"  ")); out.close()
	print(JSON.stringify(receipt))
	world.queue_free()
	await process_frame
	for path in [SETTINGS,"user://exovant-test-input.json"]:
		for suffix in ["",".bak",".tmp"]: DirAccess.remove_absolute(path+suffix)
	quit(1 if failed else 0)
