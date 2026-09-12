extends RefCounted
## Authoritative persistent campaign state. Presentation never grants rewards.
const VERSION := 1
const VALID_FLAGS := ["met_ines", "water", "archive", "atlas", "resolved"]
var flags: Dictionary = {}
var rewards: Array = []
var memories: int = 0
var choice: String = ""
var valves: Array = [0, 0, 0]
var checkpoint: Array = [0.0, 1.0, 18.0]
var echo: Array = []
var echo_value: int = 0

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

func snapshot() -> Dictionary:
	return {"version":VERSION, "flags":flags.duplicate(), "rewards":rewards.duplicate(),
		"memories":memories, "choice":choice, "valves":valves.duplicate(),
		"checkpoint":checkpoint.duplicate(), "echo":echo.duplicate(), "echo_value":echo_value}

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

static func validate(d: Variant) -> bool:
	if not d is Dictionary or d.get("version") != VERSION:
		return false
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

func restore(d: Dictionary) -> bool:
	if not validate(d):
		return false
	flags = d.flags.duplicate()
	rewards = d.rewards.duplicate()
	memories = int(d.memories)
	choice = d.choice
	valves = d.valves.duplicate()
	checkpoint = d.checkpoint.duplicate()
	echo = d.echo.duplicate()
	echo_value = int(d.echo_value)
	return true

func objective() -> String:
	if not flags.get("met_ines", false): return "LA ÚLTIMA COSTA · Habla con Inés junto al refugio"
	if not flags.get("water", false): return "UN JARDÍN SIN HUMANOS · Restablece el riego [1 · 2 · 3]"
	if not flags.get("archive", false): return "EL ARCHIVO SUMERGIDO · Recupera el acta del depósito"
	if not flags.get("atlas", false): return "DESPERTAR A ATLAS · Aísla el protocolo del custodio"
	if choice == "": return "EL DERECHO A REGRESAR · Decide el futuro de la costa"
	return "TERRA · " + choice.to_upper() + " · Regresa al portal del Reliquario"

