extends Node3D
class_name PelagosRuntimeAdapter

signal contract_ready(contract: Dictionary)
signal contract_error(message: String)
signal asset_import_status(status: String, detail: String)
signal family_state_changed(asset_id: String, previous: String, current: String)
signal collision_binding_requested(asset_id: String, policy: String)
signal interaction_requested(asset_id: String)

const MANIFEST_PATH := "res://runtime/pelagos/runtime_manifest.json"
const WORLD_ASSET_PATH := "res://runtime/pelagos/assets/pelagos_world_rev44.glb"
const EXPECTED_SCHEMA := "EXOVANT.PELAGOS.GODOT_RUNTIME_EXPORT.v1"
const EXPECTED_CLAIM := "CLM-PELAGOS-RUNTIME-GODOT-001"
const EXPECTED_ENGINE := "Godot 4.7.2"
const EXPECTED_REVISION := 44
const STATE_SCHEMA := "EXOVANT.PELAGOS.STATE.v1"
const STATE_VERSION := 1
const VALID_COLLISION := [
	"unbound",
	"query_only_until_gameplay_binding",
	"none_or_soft_query",
	"none_or_query_until_runtime_damage_binding",
]

@export var auto_import_world_asset := true
@export var strict_native_asset_gate := false

var contract: Dictionary = {}
var contract_valid := false
var native_scene_valid := false
var imported_world: Node = null
var stateful_index: Dictionary = {}
var machinery_index: Dictionary = {}
var runtime_states: Dictionary = {}
var node_index: Dictionary = {}
var duplicate_node_names: Dictionary = {}
var required_node_names: Array[String] = []

@onready var asset_root: Node3D = get_node_or_null("AssetRoot") as Node3D

func _ready() -> void:
	contract_valid = load_contract()
	if not contract_valid:
		return
	contract_ready.emit(contract)
	if auto_import_world_asset:
		try_import_world_asset()

func load_contract() -> bool:
	if not FileAccess.file_exists(MANIFEST_PATH):
		return _contract_fail("manifest missing")
	var file := FileAccess.open(MANIFEST_PATH, FileAccess.READ)
	if file == null:
		return _contract_fail("manifest unreadable")
	var parsed: Variant = JSON.parse_string(file.get_as_text())
	if typeof(parsed) != TYPE_DICTIONARY:
		return _contract_fail("manifest is not a JSON object")
	contract = parsed as Dictionary
	var error := validate_contract(contract)
	if error != "":
		return _contract_fail(error)
	_build_runtime_indexes()
	return true

func validate_contract(data: Dictionary) -> String:
	if str(data.get("schema", "")) != EXPECTED_SCHEMA:
		return "schema mismatch"
	if str(data.get("claim", "")) != EXPECTED_CLAIM:
		return "claim mismatch"
	if str(data.get("truth", "")) == "":
		return "truth missing"
	var source: Dictionary = data.get("source", {})
	if str(source.get("engine", "")) != EXPECTED_ENGINE:
		return "engine mismatch"
	if int(source.get("revision", -1)) != EXPECTED_REVISION:
		return "revision mismatch"
	if not bool(source.get("offline", false)):
		return "offline contract missing"
	if str(source.get("glb", "")) != WORLD_ASSET_PATH:
		return "GLB path mismatch"

	var counts: Dictionary = data.get("counts", {})
	var expected := {
		"cultural":30, "machinery":9, "socket_groups":9, "sessile":9,
		"damage":8, "stateful":47, "families":56, "required_nodes":224
	}
	for key_variant in expected.keys():
		var key := str(key_variant)
		if int(counts.get(key, -1)) != int(expected[key]):
			return "count mismatch: %s" % key

	var domains: Dictionary = data.get("domains", {})
	for name in ["cultural", "machinery", "sessile", "damage"]:
		if not domains.get(name, null) is Array:
			return "domain missing/not array: %s" % name
	if (domains.cultural as Array).size() != 30 or (domains.machinery as Array).size() != 9:
		return "cultural/machinery count mismatch"
	if (domains.sessile as Array).size() != 9 or (domains.damage as Array).size() != 8:
		return "sessile/damage count mismatch"

	var asset_ids := {}
	var node_keys := {}
	var stateful_count := 0
	for domain_name in ["cultural", "sessile", "damage"]:
		for record_variant in domains[domain_name]:
			if typeof(record_variant) != TYPE_DICTIONARY:
				return "invalid record in %s" % domain_name
			stateful_count += 1
			var error := _validate_stateful_record(record_variant as Dictionary, domain_name, asset_ids, node_keys)
			if error != "":
				return error
	for record_variant in domains.machinery:
		if typeof(record_variant) != TYPE_DICTIONARY:
			return "invalid machinery record"
		var error := _validate_machinery_record(record_variant as Dictionary, asset_ids, node_keys)
		if error != "":
			return error

	if stateful_count != 47 or asset_ids.size() != 56 or node_keys.size() != 224:
		return "normalized registry invariant mismatch"
	if data.get("approved_interactions", []) != []:
		return "interaction allowlist must remain empty"
	var authority: Dictionary = data.get("authority", {})
	if not authority.get("manifest_patterns_are_explicit") is bool or not authority.manifest_patterns_are_explicit:
		return "manifest pattern authority missing"
	if not authority.get("prefix_inference_forbidden") is bool or not authority.prefix_inference_forbidden:
		return "prefix inference prohibition missing"
	if not authority.get("visible_mesh_collision_inference_forbidden") is bool or not authority.visible_mesh_collision_inference_forbidden:
		return "collision inference prohibition missing"
	return ""

func _validate_stateful_record(record: Dictionary, domain_name: String, asset_ids: Dictionary, node_keys: Dictionary) -> String:
	var asset_id := str(record.get("id", ""))
	if asset_id == "" or asset_ids.has(asset_id):
		return "missing/duplicate asset id: %s" % asset_id
	asset_ids[asset_id] = domain_name
	var states: Variant = record.get("states", null)
	if not states is Array or (states as Array).is_empty():
		return "states missing: %s" % asset_id
	var current := str(record.get("current", ""))
	if not (states as Array).has(current):
		return "current state invalid: %s" % asset_id
	for state_variant in states:
		var state := str(state_variant)
		var node_name := _node_name_for_state(record, state)
		if node_name == "" or node_keys.has(node_name):
			return "missing/duplicate state node: %s" % node_name
		node_keys[node_name] = asset_id
	if domain_name == "damage":
		var target := str(record.get("target", ""))
		if target == "" or node_keys.has(target):
			return "missing/duplicate damage target: %s" % target
		node_keys[target] = asset_id + ":target"
	if not VALID_COLLISION.has(str(record.get("collision", ""))):
		return "invalid collision policy: %s" % asset_id
	return ""

func _validate_machinery_record(record: Dictionary, asset_ids: Dictionary, node_keys: Dictionary) -> String:
	var asset_id := str(record.get("id", ""))
	if asset_id == "" or asset_ids.has(asset_id):
		return "missing/duplicate machinery id: %s" % asset_id
	asset_ids[asset_id] = "machinery"
	var node_name := str(record.get("node", ""))
	if node_name == "" or node_keys.has(node_name):
		return "missing/duplicate machinery node: %s" % node_name
	node_keys[node_name] = asset_id
	var sockets: Variant = record.get("sockets", null)
	if not sockets is Array or (sockets as Array).is_empty():
		return "machinery sockets missing: %s" % asset_id
	for socket_variant in sockets:
		var socket_name := str(socket_variant)
		if socket_name == "" or node_keys.has(socket_name):
			return "missing/duplicate socket: %s" % socket_name
		node_keys[socket_name] = asset_id + ":socket"
	if str(record.get("socket_id", "")) == "":
		return "socket id missing: %s" % asset_id
	if not VALID_COLLISION.has(str(record.get("collision", ""))):
		return "invalid machinery collision policy: %s" % asset_id
	return ""

func _node_name_for_state(record: Dictionary, state: String) -> String:
	var nodes: Variant = record.get("nodes", null)
	if nodes is Dictionary:
		return str((nodes as Dictionary).get(state, ""))
	var pattern := str(record.get("node_pattern", ""))
	if pattern == "" or "{STATE}" not in pattern:
		return ""
	return pattern.replace("{STATE}", state.to_upper())

func _build_runtime_indexes() -> void:
	stateful_index.clear()
	machinery_index.clear()
	runtime_states.clear()
	required_node_names.clear()
	var domains: Dictionary = contract.domains
	for domain_name in ["cultural", "sessile", "damage"]:
		for record_variant in domains[domain_name]:
			var record: Dictionary = (record_variant as Dictionary).duplicate(true)
			record["domain"] = domain_name
			var asset_id := str(record.id)
			stateful_index[asset_id] = record
			runtime_states[asset_id] = str(record.current)
			for state_variant in record.states:
				required_node_names.append(_node_name_for_state(record, str(state_variant)))
			if domain_name == "damage":
				required_node_names.append(str(record.target))
	for record_variant in domains.machinery:
		var record: Dictionary = (record_variant as Dictionary).duplicate(true)
		machinery_index[str(record.id)] = record
		required_node_names.append(str(record.node))
		for socket_variant in record.sockets:
			required_node_names.append(str(socket_variant))

func try_import_world_asset() -> bool:
	if imported_world != null and native_scene_valid:
		return true
	if not ResourceLoader.exists(WORLD_ASSET_PATH):
		var detail := "exact rev44 GLB missing from owned runtime path"
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
	_clean_presentation(instance)
	imported_world = instance
	if not _index_and_validate_imported_scene():
		asset_import_status.emit("FAILED_NODE_CONTRACT", "required-node exactness failed")
		return false
	if not apply_all_runtime_states():
		asset_import_status.emit("FAILED_STATE_APPLICATION", "manifest state set failed")
		return false
	native_scene_valid = true
	asset_import_status.emit("IMPORTED_REV44", WORLD_ASSET_PATH)
	return true

func _clean_presentation(node: Node) -> void:
	for child in node.get_children():
		var name_text := str(child.name)
		if child is Camera3D or child is Light3D or "Presentation_floor" in name_text or "Presentation floor" in name_text:
			node.remove_child(child)
			child.free()
		else:
			_clean_presentation(child)

func _index_and_validate_imported_scene() -> bool:
	node_index.clear()
	duplicate_node_names.clear()
	if imported_world == null:
		return false
	_index_scene(imported_world)
	for required_name in required_node_names:
		if required_name == "" or duplicate_node_names.has(required_name) or not node_index.has(required_name):
			push_error("PELAGOS_RUNTIME required-node failure: %s" % required_name)
			return false
	return true

func _index_scene(node: Node) -> void:
	var key := str(node.name)
	if node_index.has(key):
		duplicate_node_names[key] = int(duplicate_node_names.get(key, 1)) + 1
	else:
		node_index[key] = node
	for child in node.get_children():
		_index_scene(child)

func set_family_state(asset_id: String, next_state: String) -> bool:
	if not contract_valid or not stateful_index.has(asset_id):
		return false
	var record: Dictionary = stateful_index[asset_id]
	var states: Array = record.states
	if not states.has(next_state):
		return false
	var previous := str(runtime_states.get(asset_id, record.current))
	if imported_world != null and not _apply_family_state_visual(record, next_state):
		return false
	runtime_states[asset_id] = next_state
	if previous != next_state:
		family_state_changed.emit(asset_id, previous, next_state)
	return true

func _apply_family_state_visual(record: Dictionary, active_state: String) -> bool:
	for state_variant in record.states:
		var state := str(state_variant)
		var node_name := _node_name_for_state(record, state)
		if not node_index.has(node_name):
			return false
		_set_node_active(node_index[node_name] as Node, state == active_state)
	return true

func _set_node_active(node: Node, active: bool) -> void:
	if node is Node3D:
		(node as Node3D).visible = active
	node.process_mode = Node.PROCESS_MODE_INHERIT if active else Node.PROCESS_MODE_DISABLED

func apply_all_runtime_states() -> bool:
	if imported_world == null:
		return false
	for asset_id_variant in stateful_index.keys():
		var asset_id := str(asset_id_variant)
		var record: Dictionary = stateful_index[asset_id]
		var state := str(runtime_states.get(asset_id, record.current))
		if not _apply_family_state_visual(record, state):
			return false
	return true

func get_family_state(asset_id: String) -> String:
	return str(runtime_states.get(asset_id, ""))

func get_family_record(asset_id: String) -> Dictionary:
	if stateful_index.has(asset_id):
		return (stateful_index[asset_id] as Dictionary).duplicate(true)
	if machinery_index.has(asset_id):
		return (machinery_index[asset_id] as Dictionary).duplicate(true)
	return {}

func get_machine_socket_nodes(asset_id: String) -> Array:
	if not machinery_index.has(asset_id):
		return []
	return (machinery_index[asset_id] as Dictionary).sockets.duplicate()

func request_collision_binding(asset_id: String) -> bool:
	var record := get_family_record(asset_id)
	if record.is_empty():
		return false
	collision_binding_requested.emit(asset_id, str(record.get("collision", "unbound")))
	return true

func request_interaction_for_asset(asset_id: String) -> bool:
	var approved: Array = contract.get("approved_interactions", [])
	if not approved.has(asset_id):
		return false
	interaction_requested.emit(asset_id)
	return true

func snapshot_world_state() -> Dictionary:
	return {
		"schema": STATE_SCHEMA,
		"version": STATE_VERSION,
		"world_id": "PELAGOS",
		"source_revision": EXPECTED_REVISION,
		"families": runtime_states.duplicate(true),
	}

func validate_world_state(payload: Variant) -> bool:
	if not payload is Dictionary:
		return false
	var data: Dictionary = payload
	if str(data.get("schema", "")) != STATE_SCHEMA or int(data.get("version", -1)) != STATE_VERSION:
		return false
	if str(data.get("world_id", "")) != "PELAGOS" or int(data.get("source_revision", -1)) != EXPECTED_REVISION:
		return false
	var families: Variant = data.get("families", null)
	if not families is Dictionary or (families as Dictionary).size() != stateful_index.size():
		return false
	for asset_id_variant in stateful_index.keys():
		var asset_id := str(asset_id_variant)
		if not (families as Dictionary).has(asset_id):
			return false
		var state := str((families as Dictionary)[asset_id])
		if not ((stateful_index[asset_id] as Dictionary).states as Array).has(state):
			return false
	for asset_id_variant in (families as Dictionary).keys():
		if not stateful_index.has(str(asset_id_variant)):
			return false
	return true

func restore_world_state(payload: Variant) -> bool:
	if not validate_world_state(payload):
		return false
	var previous := runtime_states.duplicate(true)
	var families: Dictionary = (payload as Dictionary).families
	for asset_id_variant in stateful_index.keys():
		var asset_id := str(asset_id_variant)
		if not set_family_state(asset_id, str(families[asset_id])):
			runtime_states = previous
			if imported_world != null:
				apply_all_runtime_states()
			return false
	return true

func campaign_v2_world_patch() -> Dictionary:
	# Projection only; this world adapter does not own Progress/SaveStore.
	return {"worlds": {"PELAGOS": snapshot_world_state()}}

func is_state_visually_active(asset_id: String, state: String) -> bool:
	if imported_world == null or not stateful_index.has(asset_id):
		return false
	var record: Dictionary = stateful_index[asset_id]
	var node_name := _node_name_for_state(record, state)
	if not node_index.has(node_name):
		return false
	var node: Node = node_index[node_name]
	return (node as Node3D).visible if node is Node3D else node.process_mode != Node.PROCESS_MODE_DISABLED

func _contract_fail(message: String) -> bool:
	contract_valid = false
	native_scene_valid = false
	contract_error.emit(message)
	push_error("PELAGOS_RUNTIME_CONTRACT: %s" % message)
	return false
