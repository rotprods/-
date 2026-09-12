extends RefCounted
## Offline, validated bindings. Menu escape routes stay available even after remapping.
const KEYS := {"forward":KEY_W,"back":KEY_S,"left":KEY_A,"right":KEY_D,
	"dodge":KEY_SPACE,"jump":KEY_C,"heal":KEY_R,"lock":KEY_Q,
	"interact":KEY_E,"heavy_attack":KEY_F,"guard":KEY_SHIFT}
const PADS := {"dodge":JOY_BUTTON_B,"jump":JOY_BUTTON_LEFT_STICK,
	"heal":JOY_BUTTON_X,"lock":JOY_BUTTON_RIGHT_STICK,"interact":JOY_BUTTON_A,
	"heavy_attack":JOY_BUTTON_Y,"guard":JOY_BUTTON_LEFT_SHOULDER,
	"light_attack":JOY_BUTTON_RIGHT_SHOULDER}
const UI_PADS := {"ui_accept":JOY_BUTTON_A,"ui_cancel":JOY_BUTTON_B,
	"ui_up":JOY_BUTTON_DPAD_UP,"ui_down":JOY_BUTTON_DPAD_DOWN,
	"ui_left":JOY_BUTTON_DPAD_LEFT,"ui_right":JOY_BUTTON_DPAD_RIGHT}
const LABELS := {"forward":"Avanzar","back":"Retroceder","left":"Izquierda","right":"Derecha",
	"light_attack":"Ataque ligero","heavy_attack":"Ataque fuerte","dodge":"Esquiva",
	"guard":"Guardia","heal":"Curación","jump":"Salto","lock":"Fijar enemigo","interact":"Interactuar"}
const AXES := {"left":[JOY_AXIS_LEFT_X,-1.0],"right":[JOY_AXIS_LEFT_X,1.0],
	"forward":[JOY_AXIS_LEFT_Y,-1.0],"back":[JOY_AXIS_LEFT_Y,1.0],
	"look_left":[JOY_AXIS_RIGHT_X,-1.0],"look_right":[JOY_AXIS_RIGHT_X,1.0],
	"look_up":[JOY_AXIS_RIGHT_Y,-1.0],"look_down":[JOY_AXIS_RIGHT_Y,1.0]}
const PAD_NAMES := {JOY_BUTTON_A:"A / Cruz",JOY_BUTTON_B:"B / Círculo",JOY_BUTTON_X:"X / Cuadrado",
	JOY_BUTTON_Y:"Y / Triángulo",JOY_BUTTON_LEFT_SHOULDER:"LB / L1",JOY_BUTTON_RIGHT_SHOULDER:"RB / R1",
	JOY_BUTTON_LEFT_STICK:"L3",JOY_BUTTON_RIGHT_STICK:"R3"}
var path: String
var bindings: Dictionary = {}
var last_error := ""
var using_gamepad := false

func _init(save_path: String = "user://exovant-controls.json") -> void:
	path = save_path
	bindings = defaults()

static func defaults() -> Dictionary:
	var result := {}
	for action in LABELS:
		result[action] = {"desktop":{"kind":"key","code":KEYS[action]} if KEYS.has(action) else {"kind":"mouse","code":MOUSE_BUTTON_LEFT}}
		if PADS.has(action): result[action]["gamepad"] = {"kind":"button","code":PADS[action]}
	return result

static func valid(candidate: Variant) -> bool:
	if not candidate is Dictionary or candidate.size() != LABELS.size(): return false
	var seen := {}
	for action in LABELS:
		var slots: Variant = candidate.get(action)
		if not slots is Dictionary or slots.size() != (2 if PADS.has(action) else 1): return false
		for slot in ["desktop","gamepad"] if PADS.has(action) else ["desktop"]:
			var item: Variant = slots.get(slot)
			if not item is Dictionary or item.size() != 2: return false
			var code: Variant = item.get("code")
			if not (code is int or code is float) or not is_finite(float(code)) or float(code) != floorf(float(code)): return false
			if slot == "gamepad":
				if item.get("kind") != "button" or not PAD_NAMES.has(int(code)): return false
			elif item.get("kind") == "key":
				if code <= 0 or code == KEY_ESCAPE or code >= KEY_CODE_MASK or OS.get_keycode_string(int(code)).is_empty(): return false
			elif item.get("kind") == "mouse":
				if int(code) not in [MOUSE_BUTTON_LEFT,MOUSE_BUTTON_RIGHT,MOUSE_BUTTON_MIDDLE,MOUSE_BUTTON_XBUTTON1,MOUSE_BUTTON_XBUTTON2]: return false
			else: return false
			var signature := str(item.kind)+":"+str(int(code))
			if seen.has(signature): return false
			seen[signature] = true
	return true

func load_bindings() -> bool:
	last_error = ""
	bindings = defaults()
	if not FileAccess.file_exists(path): apply(); return true
	var file := FileAccess.open(path,FileAccess.READ)
	if file == null or file.get_length() > 16384:
		last_error = "No se pudieron leer los controles; se usan los valores iniciales."
		apply(); return false
	var parser := JSON.new()
	var ok := parser.parse(file.get_as_text()) == OK
	var data: Variant = parser.data if ok else null
	if not data is Dictionary or data.get("version") != 1 or not valid(data.get("bindings")):
		last_error = "Archivo de controles inválido; se usan los valores iniciales."
		bindings = defaults(); apply(); return false
	bindings = data.bindings.duplicate(true)
	apply(); return true

func commit(candidate: Dictionary) -> bool:
	last_error = ""
	if not valid(candidate): last_error = "Entrada reservada, duplicada o no compatible."; return false
	var file := FileAccess.open(path+".tmp",FileAccess.WRITE)
	if file == null: last_error = "No se pudieron guardar los controles."; return false
	file.store_string(JSON.stringify({"version":1,"bindings":candidate}))
	file.flush()
	var write_error := file.get_error()
	file.close()
	if write_error != OK or DirAccess.rename_absolute(path+".tmp",path) != OK:
		last_error = "No se pudieron guardar los controles."
		DirAccess.remove_absolute(path+".tmp"); return false
	bindings = candidate.duplicate(true)
	apply(); return true

func rebind(action: String, event: InputEvent) -> bool:
	if not LABELS.has(action) or not event.is_pressed() or event.is_echo(): return false
	var item := {}
	var slot := "desktop"
	if event is InputEventKey:
		if event.ctrl_pressed or event.alt_pressed or event.meta_pressed:
			last_error = "Usa una tecla sin Ctrl, Alt ni Meta."; return false
		item = {"kind":"key","code":event.physical_keycode if event.physical_keycode else event.keycode}
	elif event is InputEventMouseButton: item = {"kind":"mouse","code":event.button_index}
	elif event is InputEventJoypadButton and PADS.has(action):
		slot = "gamepad"; item = {"kind":"button","code":event.button_index}
	else: last_error = "Usa una tecla, botón de ratón o botón de mando compatible."; return false
	var candidate := bindings.duplicate(true)
	if slot == "gamepad":
		for other in candidate:
			if other != action and candidate[other].has("gamepad") and int(candidate[other]["gamepad"].code) == int(item.code):
				candidate[other]["gamepad"] = bindings[action]["gamepad"].duplicate()
	candidate[action][slot] = item
	return commit(candidate)

static func make_event(item: Dictionary) -> InputEvent:
	var event: InputEvent
	match item.kind:
		"key":
			event = InputEventKey.new(); event.physical_keycode = int(item.code)
		"mouse":
			event = InputEventMouseButton.new(); event.button_index = int(item.code)
		"button":
			event = InputEventJoypadButton.new(); event.button_index = int(item.code); event.device = -1
	return event

func apply() -> void:
	var actions: Array = LABELS.keys()+["look_left","look_right","look_up","look_down","pause_game"]
	for action in actions:
		if not InputMap.has_action(action): InputMap.add_action(action,.22)
		Input.action_release(action)
		InputMap.action_erase_events(action)
		InputMap.action_set_deadzone(action,.22)
	for action in bindings:
		for item in bindings[action].values(): InputMap.action_add_event(action,make_event(item))
	for action in AXES:
		var axis := InputEventJoypadMotion.new()
		axis.device = -1; axis.axis = AXES[action][0]; axis.axis_value = AXES[action][1]
		InputMap.action_add_event(action,axis)
	InputMap.action_add_event("pause_game",make_event({"kind":"key","code":KEY_ESCAPE}))
	InputMap.action_add_event("pause_game",make_event({"kind":"button","code":JOY_BUTTON_START}))
	# The runtime-created map does not include controller UI bindings by default.
	for action in UI_PADS:
		if not InputMap.has_action(action): InputMap.add_action(action)
		var event := make_event({"kind":"button","code":UI_PADS[action]})
		if not InputMap.action_has_event(action,event): InputMap.action_add_event(action,event)

func observe(event: InputEvent) -> void:
	if event is InputEventJoypadButton and event.pressed: using_gamepad = true
	elif event is InputEventJoypadMotion and absf(event.axis_value) > .22: using_gamepad = true
	elif (event is InputEventKey or event is InputEventMouseButton) and event.is_pressed(): using_gamepad = false
	elif event is InputEventMouseMotion and event.relative.length() > 2: using_gamepad = false

func binding_text(action: String, gamepad: bool = false) -> String:
	if gamepad and not PADS.has(action): return "Stick izquierdo"
	var item: Dictionary = bindings[action]["gamepad" if gamepad else "desktop"]
	if item.kind == "button": return PAD_NAMES[int(item.code)]
	if item.kind == "mouse": return "Ratón %d" % int(item.code)
	return OS.get_keycode_string(int(item.code))

func hint_for(action: String) -> String:
	return binding_text(action,using_gamepad)

func footer() -> String:
	if using_gamepad:
		return "Stick izq. mover · Stick der. cámara · %s atacar · %s fuerte · %s esquivar\n%s fijar · %s curar · %s interactuar · Start pausa · Opciones en Controles" % [hint_for("light_attack"),hint_for("heavy_attack"),hint_for("dodge"),hint_for("lock"),hint_for("heal"),hint_for("interact")]
	return "%s/%s/%s/%s mover · Ratón cámara · %s atacar · %s fuerte · %s esquivar\n%s guardia · %s fijar · %s curar · %s saltar · %s interactuar · Esc pausa" % [hint_for("forward"),hint_for("left"),hint_for("back"),hint_for("right"),hint_for("light_attack"),hint_for("heavy_attack"),hint_for("dodge"),hint_for("guard"),hint_for("lock"),hint_for("heal"),hint_for("jump"),hint_for("interact")]
