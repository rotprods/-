extends Node3D
class_name ElysiumRuntimeAdapter

signal contract_ready(contract: Dictionary)
signal contract_error(message: String)
signal asset_import_status(status: String, detail: String)
signal world_state_changed(previous: String, current: String, cause_event: String)
signal adapter_state_requested(adapter_id: String, target_meta: String, state: String)
signal cell_activation_requested(cell_id: String, region: String, seed31: int)
signal cell_deactivation_requested(cell_id: String, region: String)

const MANIFEST_PATH := "res://runtime/elysium/runtime_manifest.json"
const WORLD_ASSET_PATH := "res://runtime/elysium/assets/elysium_world.glb"
const EXPECTED_SCHEMA := "EXOVANT.ELYSIUM.GODOT_RUNTIME_EXPORT.v1"
const EXPECTED_ENGINE := "Godot 4.7.2"
const VALID_STATES := ["CONTROLLED", "ANOMALY", "EMERGENCY"]

@export var auto_import_world_asset := true
@export var strict_native_asset_gate := false

var contract: Dictionary = {}
var current_state := "CONTROLLED"
var state_entered_s := 0.0
var last_transition_s := -INF
var event_times: Dictionary = {}
var event_sequence: Array[String] = []
var active_cells: Dictionary = {}
var imported_world: Node = null
var contract_valid := false

@onready var asset_root: Node3D = get_node_or_null("AssetRoot") as Node3D

func _ready() -> void:
	state_entered_s = _now_s()
	contract_valid = load_contract()
	if not contract_valid:
		set_process(false)
		return
	contract_ready.emit(contract)
	if auto_import_world_asset:
		try_import_world_asset()

func _process(_delta: float) -> void:
	if contract_valid and not event_times.is_empty():
		_evaluate_transitions(_now_s())

func load_contract() -> bool:
	if not FileAccess.file_exists(MANIFEST_PATH):
		return _contract_fail("manifest missing: %s" % MANIFEST_PATH)
	var file := FileAccess.open(MANIFEST_PATH, FileAccess.READ)
	if file == null:
		return _contract_fail("manifest unreadable: %s" % MANIFEST_PATH)
	var parsed: Variant = JSON.parse_string(file.get_as_text())
	if typeof(parsed) != TYPE_DICTIONARY:
		return _contract_fail("manifest is not a JSON object")
	contract = parsed as Dictionary
	var error := validate_contract(contract)
	if error != "":
		return _contract_fail(error)
	current_state = str(contract.get("world_state", {}).get("initial_state", "CONTROLLED"))
	state_entered_s = _now_s()
	return true

func validate_contract(data: Dictionary) -> String:
	if str(data.get("schema", "")) != EXPECTED_SCHEMA:
		return "schema mismatch"
	if str(data.get("claim_id", "")) != "CLM-ELYSIUM-RUNTIME-GODOT-001":
		return "claim id mismatch"
	if str(data.get("truth_state", "")) == "":
		return "truth_state missing"
	var source: Dictionary = data.get("source", {})
	if str(source.get("engine", "")) != EXPECTED_ENGINE:
		return "engine contract mismatch"
	if int(source.get("runtime_export_contract_revision", -1)) != 47:
		return "runtime export revision mismatch"
	if not bool(source.get("offline_runtime_required", false)):
		return "offline runtime contract missing"
	var streaming: Dictionary = data.get("streaming", {})
	if int(streaming.get("cell_size_m", 0)) != 256:
		return "streaming cell-size drift"
	if str(streaming.get("placement_policy", "")) != "REGISTER_ONLY_UNTIL_ORIGIN_REBASING_AND_MACRO_TO_LOCAL_MAPPING_QUALIFIED":
		return "unsafe macro placement policy"
	var cells: Array = streaming.get("cells", [])
	if cells.size() != 17:
		return "expected 17 streaming cells, got %d" % cells.size()
	var cell_ids := {}
	var seeds := {}
	for cell_variant in cells:
		if typeof(cell_variant) != TYPE_DICTIONARY:
			return "invalid streaming cell"
		var cell: Dictionary = cell_variant
		var cell_id := str(cell.get("id", ""))
		var seed := int(cell.get("seed31", -1))
		if cell_id == "" or cell_ids.has(cell_id):
			return "missing/duplicate streaming cell id: %s" % cell_id
		if seed < 0 or seeds.has(seed):
			return "missing/duplicate streaming seed for %s" % cell_id
		var macro_location: Variant = cell.get("macro_location_m", null)
		if typeof(macro_location) != TYPE_ARRAY or (macro_location as Array).size() != 3:
			return "invalid macro location for %s" % cell_id
		cell_ids[cell_id] = true
		seeds[seed] = true
	var world_state: Dictionary = data.get("world_state", {})
	var states: Dictionary = world_state.get("states", {})
	for state in VALID_STATES:
		if not states.has(state):
			return "world state missing: %s" % state
	var priorities := {}
	for state_variant in states.keys():
		var priority := int((states[state_variant] as Dictionary).get("priority", -1))
		if priority < 0 or priorities.has(priority):
			return "missing/duplicate state priority"
		priorities[priority] = true
	var transitions: Array = world_state.get("transitions", [])
	if transitions.size() != 5:
		return "expected 5 world-state transitions"
	for transition_variant in transitions:
		if typeof(transition_variant) != TYPE_DICTIONARY:
			return "invalid transition"
		var transition: Dictionary = transition_variant
		if not VALID_STATES.has(str(transition.get("from", ""))) or not VALID_STATES.has(str(transition.get("to", ""))):
			return "transition references invalid state"
		if not ["ANY", "ALL"].has(str(transition.get("mode", ""))):
			return "transition mode invalid"
		if float(transition.get("debounce_s", -1.0)) < 0.0 or float(transition.get("min_dwell_s", -1.0)) < 0.0 or float(transition.get("cooldown_s", -1.0)) < 0.0:
			return "transition timing invalid"
	if (world_state.get("events", {}) as Dictionary).size() != 11:
		return "expected 11 world-state events"
	if (world_state.get("adapter_targets", {}) as Dictionary).size() != 19:
		return "expected 19 state adapters"
	var population: Dictionary = data.get("population", {})
	if int(population.get("route_count", -1)) != 19:
		return "population route count mismatch"
	if int(population.get("socket_count", -1)) != 118:
		return "population socket count mismatch"
	var socket_sum := 0
	for route_variant in population.get("routes", []):
		if typeof(route_variant) != TYPE_DICTIONARY:
			return "invalid population route"
		socket_sum += int((route_variant as Dictionary).get("socket_count", 0))
	if socket_sum != 118:
		return "population route socket sum mismatch"
	var eden: Dictionary = data.get("eden", {})
	if not is_equal_approx(float(eden.get("canonical_arena_diameter_m", 0.0)), 48.0):
		return "EDEN canonical arena diameter drift"
	if float(eden.get("max_damage_radius_m", 999.0)) > 24.0:
		return "EDEN damage radius exceeds arena contract"
	if float(eden.get("max_population_socket_radius_m", 999.0)) > 24.0:
		return "EDEN population radius exceeds arena contract"
	if not is_equal_approx(float(eden.get("relocation_warning_s", 0.0)), 1.5):
		return "EDEN relocation warning drift"
	return ""

func try_import_world_asset() -> bool:
	if imported_world != null:
		return true
	if not ResourceLoader.exists(WORLD_ASSET_PATH):
		var detail := "world GLB not present at owned runtime path"
		asset_import_status.emit("BLOCKED_ASSET_MISSING", detail)
		if strict_native_asset_gate:
			_contract_fail(detail)
		return false
	var resource: Resource = load(WORLD_ASSET_PATH)
	if not (resource is PackedScene):
		asset_import_status.emit("FAILED_NOT_PACKED_SCENE", WORLD_ASSET_PATH)
		return false
	var instance := (resource as PackedScene).instantiate()
	if instance == null:
		asset_import_status.emit("FAILED_INSTANTIATION", WORLD_ASSET_PATH)
		return false
	if asset_root == null:
		asset_root = Node3D.new()
		asset_root.name = "AssetRoot"
		add_child(asset_root)
	asset_root.add_child(instance)
	imported_world = instance
	asset_import_status.emit("IMPORTED", WORLD_ASSET_PATH)
	return true

func push_event(event_id: String) -> bool:
	if not contract_valid:
		return false
	var events: Dictionary = contract.get("world_state", {}).get("events", {})
	if not events.has(event_id):
		return false
	var now := _now_s()
	event_times[event_id] = now
	event_sequence.append(event_id)
	_evaluate_transitions(now)
	return true

func _evaluate_transitions(now: float) -> bool:
	var candidates: Array[Dictionary] = []
	for transition_variant in contract.get("world_state", {}).get("transitions", []):
		var transition: Dictionary = transition_variant
		if str(transition.get("from", "")) != current_state:
			continue
		if _transition_ready(transition, now):
			candidates.append(transition)
	if candidates.is_empty():
		return false
	candidates.sort_custom(func(a: Dictionary, b: Dictionary) -> bool: return int(a.get("priority", 0)) > int(b.get("priority", 0)))
	var cause_event := event_sequence[-1] if not event_sequence.is_empty() else "TIMER_EVALUATION"
	return _apply_transition(candidates[0], cause_event, now)

func _transition_ready(transition: Dictionary, now: float) -> bool:
	var min_dwell := float(transition.get("min_dwell_s", 0.0))
	if now - state_entered_s < min_dwell:
		return false
	var cooldown := float(transition.get("cooldown_s", 0.0))
	if now - last_transition_s < cooldown:
		return false
	var required_events: Array = transition.get("events", [])
	var debounce := float(transition.get("debounce_s", 0.0))
	var mode := str(transition.get("mode", "ANY"))
	if mode == "ANY":
		for required_variant in required_events:
			var required := str(required_variant)
			if event_times.has(required):
				var occurred := float(event_times[required])
				if occurred >= state_entered_s and now - occurred >= debounce:
					return true
		return false
	for required_variant in required_events:
		var required := str(required_variant)
		if not event_times.has(required):
			return false
		var occurred := float(event_times[required])
		if occurred < state_entered_s or now - occurred < debounce:
			return false
	return true

func _apply_transition(transition: Dictionary, cause_event: String, now: float) -> bool:
	var next_state := str(transition.get("to", ""))
	if not VALID_STATES.has(next_state) or next_state == current_state:
		return false
	var previous := current_state
	current_state = next_state
	state_entered_s = now
	last_transition_s = now
	event_times.clear()
	event_sequence.clear()
	world_state_changed.emit(previous, current_state, cause_event)
	var adapters: Dictionary = contract.get("world_state", {}).get("adapter_targets", {})
	for adapter_id_variant in adapters.keys():
		var adapter_id := str(adapter_id_variant)
		adapter_state_requested.emit(adapter_id, str(adapters[adapter_id_variant]), current_state)
	return true

func get_cells(region: String = "") -> Array:
	if not contract_valid:
		return []
	var matches: Array = []
	for cell_variant in contract.get("streaming", {}).get("cells", []):
		var cell: Dictionary = cell_variant
		if region == "" or str(cell.get("region", "")) == region:
			matches.append(cell.duplicate(true))
	return matches

func request_cell_activation(cell_id: String) -> bool:
	var cell := _find_cell(cell_id)
	if cell.is_empty():
		return false
	if active_cells.has(cell_id):
		return true
	active_cells[cell_id] = true
	cell_activation_requested.emit(cell_id, str(cell.get("region", "")), int(cell.get("seed31", 0)))
	return true

func request_cell_deactivation(cell_id: String) -> bool:
	var cell := _find_cell(cell_id)
	if cell.is_empty() or not active_cells.has(cell_id):
		return false
	active_cells.erase(cell_id)
	cell_deactivation_requested.emit(cell_id, str(cell.get("region", "")))
	return true

func _find_cell(cell_id: String) -> Dictionary:
	for cell_variant in contract.get("streaming", {}).get("cells", []):
		var cell: Dictionary = cell_variant
		if str(cell.get("id", "")) == cell_id:
			return cell
	return {}

func get_macro_location_metadata(cell_id: String) -> Array:
	# Deliberately metadata only. The macro->local transform/origin-rebasing
	# decision remains an explicit gate and must never be guessed here.
	return _find_cell(cell_id).get("macro_location_m", []) as Array

func _contract_fail(message: String) -> bool:
	contract_valid = false
	contract_error.emit(message)
	push_error("ELYSIUM_RUNTIME_CONTRACT: %s" % message)
	return false

func _now_s() -> float:
	return Time.get_ticks_msec() / 1000.0
