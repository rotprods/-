extends SceneTree

const MANIFEST_PATH := "res://art_source/worlds/elysium_null/runtime/runtime_manifest.json"
const ADAPTER_PATH := "res://art_source/worlds/elysium_null/runtime/elysium_runtime_adapter.gd"
const SCENE_PATH := "res://art_source/worlds/elysium_null/runtime/elysium_runtime.tscn"
const ASSET_PATH := "res://art_source/worlds/elysium_null/runtime/assets/elysium_world.glb"
const EXPECTED_SCHEMA := "EXOVANT.ELYSIUM.GODOT_RUNTIME_EXPORT.v1"

var failures: Array[String] = []

func _initialize() -> void:
	call_deferred("_run")

func _run() -> void:
	var contract_only := OS.get_cmdline_user_args().has("--contract-only")
	var data := _read_manifest()
	if data.is_empty():
		_finish(contract_only)
		return
	_expect(str(data.get("schema", "")) == EXPECTED_SCHEMA, "schema")
	_expect(str(data.get("claim_id", "")) == "CLM-ELYSIUM-RUNTIME-GODOT-001", "claim id")
	_expect(str(data.get("truth_state", "")) == "CONTRACT_READY_NOT_NATIVE_IMPORT_PROVEN", "truth state")
	var source: Dictionary = data.get("source", {})
	_expect(str(source.get("engine", "")) == "Godot 4.7.2", "engine contract")
	_expect(bool(source.get("offline_runtime_required", false)), "offline runtime")
	_expect(int(source.get("runtime_export_contract_revision", -1)) == 47, "R47 export contract")
	var cells: Array = data.get("streaming", {}).get("cells", [])
	_expect(cells.size() == 17, "17 streaming cells")
	var ids := {}
	var seeds := {}
	for cell_variant in cells:
		if typeof(cell_variant) != TYPE_DICTIONARY:
			failures.append("cell is not dictionary")
			continue
		var cell: Dictionary = cell_variant
		var id := str(cell.get("id", ""))
		var seed := int(cell.get("seed31", -1))
		_expect(id != "" and not ids.has(id), "unique cell id %s" % id)
		_expect(seed >= 0 and not seeds.has(seed), "unique seed for %s" % id)
		ids[id] = true
		seeds[seed] = true
	var state: Dictionary = data.get("world_state", {})
	var states: Dictionary = state.get("states", {})
	_expect(states.size() == 3, "3 world states")
	_expect(states.has("CONTROLLED") and states.has("ANOMALY") and states.has("EMERGENCY"), "state names")
	_expect((state.get("transitions", []) as Array).size() == 5, "5 transitions")
	_expect((state.get("events", {}) as Dictionary).size() == 11, "11 events")
	_expect((state.get("adapter_targets", {}) as Dictionary).size() == 19, "19 adapters")
	var population: Dictionary = data.get("population", {})
	_expect(int(population.get("route_count", -1)) == 19, "19 population routes")
	_expect(int(population.get("socket_count", -1)) == 118, "118 population sockets")
	var socket_sum := 0
	for route_variant in population.get("routes", []):
		var route: Dictionary = route_variant
		socket_sum += int(route.get("socket_count", 0))
	_expect(socket_sum == 118, "route socket sum")
	var eden: Dictionary = data.get("eden", {})
	_expect(is_equal_approx(float(eden.get("canonical_arena_diameter_m", 0.0)), 48.0), "EDEN 48m diameter")
	_expect(float(eden.get("max_damage_radius_m", 999.0)) <= 24.0, "EDEN damage radius")
	_expect(float(eden.get("max_population_socket_radius_m", 999.0)) <= 24.0, "EDEN population radius")
	_expect(is_equal_approx(float(eden.get("relocation_warning_s", 0.0)), 1.5), "EDEN 1.5s warning")
	# Loading these resources forces Godot to parse the adapter/scene even in contract-only mode.
	var adapter_resource: Resource = load(ADAPTER_PATH)
	_expect(adapter_resource != null, "adapter parses")
	var runtime_scene: Resource = load(SCENE_PATH)
	_expect(runtime_scene is PackedScene, "runtime scene parses")
	if runtime_scene is PackedScene:
		var instance := (runtime_scene as PackedScene).instantiate()
		_expect(instance != null, "runtime scene instantiates")
		if instance != null:
			instance.free()
	if contract_only:
		if not ResourceLoader.exists(ASSET_PATH):
			print("ELYSIUM_RUNTIME_SMOKE: native asset intentionally unresolved in contract-only mode")
	else:
		_expect(ResourceLoader.exists(ASSET_PATH), "native GLB exists")
		if ResourceLoader.exists(ASSET_PATH):
			var world_resource: Resource = load(ASSET_PATH)
			_expect(world_resource is PackedScene, "native GLB imports as PackedScene")
			if world_resource is PackedScene:
				var world_instance := (world_resource as PackedScene).instantiate()
				_expect(world_instance != null, "native GLB instantiates")
				if world_instance != null:
					world_instance.free()
	_finish(contract_only)

func _read_manifest() -> Dictionary:
	if not FileAccess.file_exists(MANIFEST_PATH):
		failures.append("manifest missing")
		return {}
	var file := FileAccess.open(MANIFEST_PATH, FileAccess.READ)
	if file == null:
		failures.append("manifest unreadable")
		return {}
	var parsed: Variant = JSON.parse_string(file.get_as_text())
	if typeof(parsed) != TYPE_DICTIONARY:
		failures.append("manifest invalid JSON object")
		return {}
	return parsed as Dictionary

func _expect(condition: bool, label: String) -> void:
	if not condition:
		failures.append(label)

func _finish(contract_only: bool) -> void:
	if failures.is_empty():
		print("ELYSIUM_RUNTIME_SMOKE: PASS mode=%s cells=17 states=3 transitions=5 routes=19 sockets=118 adapters=19" % ("contract-only" if contract_only else "native"))
		quit(0)
		return
	for item in failures:
		printerr("ELYSIUM_RUNTIME_SMOKE: FAIL %s" % item)
	quit(1)
