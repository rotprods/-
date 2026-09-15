extends RefCounted
## Authoritative persistent campaign state. Presentation never grants rewards.
## v2 preserves the Terra campaign fields and adds a bounded per-world state namespace.
const VERSION := 2
const LEGACY_VERSION := 1
const VALID_FLAGS := ["met_ines", "water", "archive", "atlas", "resolved"]
const MAX_WORLDS := 64
const MAX_WORLD_ID := 64
const MAX_WORLD_SCHEMA := 160
const MAX_TREE_DEPTH := 8
const MAX_CONTAINER_ITEMS := 4096
const MAX_STRING := 4096
const WORLD_ID_CHARS := "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-"

var flags: Dictionary = {}
var rewards: Array = []
var memories: int = 0
var choice: String = ""
var valves: Array = [0, 0, 0]
var checkpoint: Array = [0.0, 1.0, 18.0]
var echo: Array = []
var echo_value: int = 0
var worlds: Dictionary = {}

func grant(id: String, value: int) -> bool:
	if id in rewards or value < 0:
		return false
	rewards.append(id)
	memories += value
	return true

func advance(id: String) -> bool:
	var prereqs := {"water":"met_ines", "archive":"water", "atlas":"archive", "resolved":"atlas"}
	if id not in VALID_FLAGS or flags.get(id, false):
		return false
	if prereqs.has(id) and not flags.get(prereqs[id], false):
		return false
	flags[id] = true
	grant("quest:" + id, 100)
	return true

func turn_valve(index: int) -> bool:
	if index < 0 or index > 2 or not flags.get("met_ines", false) or flags.get("water", false):
		return false
	valves[index] = (int(valves[index]) + 1) % 4
	if valves == [1, 2, 3]:
		advance("water")
	return true

func resolve(outcome: String) -> bool:
	if outcome not in ["cogobierno", "industria"] or not flags.get("atlas", false) or choice != "":
		return false
	choice = outcome
	return advance("resolved")

func die(at: Vector3) -> void:
	echo = [at.x, maxf(at.y, 0.5), at.z]
	echo_value = memories
	memories = 0

func recover_echo() -> int:
	var value := echo_value
	memories += value
	echo_value = 0
	echo = []
	return value

func set_world_state(world_id: String, state: Dictionary) -> bool:
	if not world_state_valid(world_id, state):
		return false
	worlds[world_id] = state.duplicate(true)
	return true

func get_world_state(world_id: String) -> Dictionary:
	if not worlds.has(world_id):
		return {}
	return (worlds[world_id] as Dictionary).duplicate(true)

func clear_world_state(world_id: String) -> bool:
	if not worlds.has(world_id):
		return false
	worlds.erase(world_id)
	return true

func snapshot() -> Dictionary:
	return {"version":VERSION, "flags":flags.duplicate(), "rewards":rewards.duplicate(),
		"memories":memories, "choice":choice, "valves":valves.duplicate(),
		"checkpoint":checkpoint.duplicate(), "echo":echo.duplicate(), "echo_value":echo_value,
		"worlds":worlds.duplicate(true)}

static func position_valid(v: Variant, empty_allowed: bool = false) -> bool:
	if not v is Array:
		return false
	if v.is_empty() and empty_allowed:
		return true
	if v.size() != 3:
		return false
	for n in v:
		if not (n is float or n is int) or not is_finite(float(n)) or absf(float(n)) > 10000.0:
			return false
	return true

static func _world_id_valid(world_id: String) -> bool:
	if world_id.is_empty() or world_id.length() > MAX_WORLD_ID:
		return false
	for i in range(world_id.length()):
		if WORLD_ID_CHARS.find(world_id.substr(i, 1)) < 0:
			return false
	return true

static func _json_tree_valid(value: Variant, depth: int = 0) -> bool:
	if depth > MAX_TREE_DEPTH:
		return false
	if value == null or value is bool:
		return true
	if value is int:
		return absf(float(value)) <= 9000000000000000.0
	if value is float:
		return is_finite(value) and absf(value) <= 1000000000000.0
	if value is String:
		return value.length() <= MAX_STRING
	if value is Array:
		if value.size() > MAX_CONTAINER_ITEMS:
			return false
		for item in value:
			if not _json_tree_valid(item, depth + 1):
				return false
		return true
	if value is Dictionary:
		if value.size() > MAX_CONTAINER_ITEMS:
			return false
		for key in value:
			if not key is String or key.is_empty() or key.length() > 160:
				return false
			if not _json_tree_valid(value[key], depth + 1):
				return false
		return true
	return false

static func world_state_valid(world_id: String, state: Variant) -> bool:
	if not _world_id_valid(world_id) or not state is Dictionary:
		return false
	if state.get("world_id") != world_id:
		return false
	if not state.get("schema") is String or state.schema.is_empty() or state.schema.length() > MAX_WORLD_SCHEMA:
		return false
	for key in ["version", "source_revision"]:
		var n: Variant = state.get(key)
		if not (n is int or n is float) or not is_finite(float(n)) or float(n) != floorf(float(n)):
			return false
		if n < 0 or n > 1000000000:
			return false
	if int(state.version) < 1:
		return false
	return _json_tree_valid(state)

static func _base_valid(d: Dictionary) -> bool:
	if not d.get("flags") is Dictionary or not d.get("rewards") is Array:
		return false
	if not d.get("choice") is String or d.choice not in ["", "cogobierno", "industria"]:
		return false
	for k in d.flags:
		if k not in VALID_FLAGS or not d.flags[k] is bool:
			return false
	for pair in [["water","met_ines"],["archive","water"],["atlas","archive"],["resolved","atlas"]]:
		if d.flags.get(pair[0],false) and not d.flags.get(pair[1],false):
			return false
	if d.flags.get("resolved", false) != (d.choice != ""):
		return false
	for k in ["memories", "echo_value"]:
		var n: Variant = d.get(k)
		if not (n is float or n is int) or not is_finite(float(n)) or n < 0 or n > 100000000 or float(n) != floorf(float(n)):
			return false
	if not d.get("valves") is Array or d.valves.size() != 3:
		return false
	for v in d.valves:
		if not (v is int or v is float) or v < 0 or v > 3 or float(v) != floorf(float(v)):
			return false
	if d.rewards.size() > 10000:
		return false
	var seen := {}
	for r in d.rewards:
		if not r is String or r.length() > 100 or seen.has(r):
			return false
		seen[r] = true
	return position_valid(d.get("checkpoint")) and position_valid(d.get("echo"), true)

static func _legacy_v1_valid(d: Variant) -> bool:
	return d is Dictionary and d.get("version") == LEGACY_VERSION and _base_valid(d)

static func validate(d: Variant) -> bool:
	if not d is Dictionary or d.get("version") != VERSION or not _base_valid(d):
		return false
	if not d.get("worlds") is Dictionary or d.worlds.size() > MAX_WORLDS:
		return false
	for world_id in d.worlds:
		if not world_id is String or not world_state_valid(world_id, d.worlds[world_id]):
			return false
	return true

static func migrate(d: Variant) -> Dictionary:
	if validate(d):
		return (d as Dictionary).duplicate(true)
	if not _legacy_v1_valid(d):
		return {}
	var old: Dictionary = d
	return {
		"version":VERSION,
		"flags":old.flags.duplicate(),
		"rewards":old.rewards.duplicate(),
		"memories":int(old.memories),
		"choice":old.choice,
		"valves":old.valves.duplicate(),
		"checkpoint":old.checkpoint.duplicate(),
		"echo":old.echo.duplicate(),
		"echo_value":int(old.echo_value),
		"worlds":{},
	}

func restore(d: Dictionary) -> bool:
	var normalized := migrate(d)
	if normalized.is_empty():
		return false
	flags = normalized.flags.duplicate()
	rewards = normalized.rewards.duplicate()
	memories = int(normalized.memories)
	choice = normalized.choice
	valves = normalized.valves.duplicate()
	checkpoint = normalized.checkpoint.duplicate()
	echo = normalized.echo.duplicate()
	echo_value = int(normalized.echo_value)
	worlds = normalized.worlds.duplicate(true)
	return true

func objective() -> String:
	if not flags.get("met_ines", false): return "LA ÚLTIMA COSTA · Habla con Inés junto al refugio"
	if not flags.get("water", false): return "UN JARDÍN SIN HUMANOS · Restablece el riego [1 · 2 · 3]"
	if not flags.get("archive", false): return "EL ARCHIVO SUMERGIDO · Recupera el acta del depósito"
	if not flags.get("atlas", false): return "DESPERTAR A ATLAS · Aísla el protocolo del custodio"
	if choice == "": return "EL DERECHO A REGRESAR · Decide el futuro de la costa"
	return "TERRA · " + choice.to_upper() + " · Regresa al portal del Reliquario"
