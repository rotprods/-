extends SceneTree

const Adapter = preload("res://runtime/pelagos/pelagos_runtime_adapter.gd")

var failures: Array[String] = []

func _initialize() -> void:
	call_deferred("_run")

func check(condition: bool, label: String) -> void:
	if condition:
		print("PASS · " + label)
	else:
		failures.append(label)
		push_error("FAIL · " + label)

func _run() -> void:
	var holder := Node3D.new()
	holder.name = "PelagosSmokeRoot"
	root.add_child(holder)

	var adapter := Adapter.new()
	adapter.name = "PelagosRuntimeAdapter"
	adapter.auto_import_world_asset = false
	holder.add_child(adapter)
	await process_frame

	check(adapter.contract_valid, "manifest contract loads")
	check(adapter.stateful_index.size() == 47, "47 stateful family records")
	check(adapter.machinery_index.size() == 9, "9 machinery families")
	check(adapter.required_node_names.size() == 224, "224 required native node keys")
	check(adapter.runtime_states.size() == 47, "47 initialized runtime states")
	check(not adapter.request_interaction_for_asset("PEL-PROP-WET-WORK-STATION-002"), "interaction denied by empty allowlist")
	check(adapter.request_collision_binding("PEL-PROP-WET-WORK-STATION-002"), "collision request emits policy only")

	var sample := "PEL-PROP-WET-WORK-STATION-002"
	var original := adapter.get_family_state(sample)
	check(original == "used", "sample state starts at manifest current")
	check(adapter.set_family_state(sample, "pristine"), "valid in-memory state transition accepted")
	check(adapter.get_family_state(sample) == "pristine", "state transition stored")
	check(not adapter.set_family_state(sample, "not_a_state"), "unknown state rejected")
	check(adapter.get_family_state(sample) == "pristine", "unknown state preserves last valid state")

	var snapshot := adapter.snapshot_world_state()
	check(adapter.validate_world_state(snapshot), "world-state snapshot validates")
	var corrupt := snapshot.duplicate(true)
	corrupt.families[sample] = "invalid"
	check(not adapter.validate_world_state(corrupt), "corrupt world-state payload rejected")
	check(adapter.restore_world_state(snapshot), "world-state snapshot roundtrip restores")
	check(adapter.get_family_state(sample) == "pristine", "roundtrip restores exact state")
	check(adapter.set_family_state(sample, original), "sample restored to manifest default")

	var patch := adapter.campaign_v2_world_patch()
	check(patch.has("worlds") and (patch.worlds as Dictionary).has("PELAGOS"), "campaign v2 projection is namespaced")
	check(not patch.has("version"), "adapter does not mutate global campaign schema")

	var contract_only := "--contract-only" in OS.get_cmdline_user_args()
	if not contract_only:
		adapter.strict_native_asset_gate = true
		check(adapter.try_import_world_asset(), "native rev44 GLB imports and instantiates")
		check(adapter.native_scene_valid, "native scene exactness gate passes")
		if adapter.native_scene_valid:
			check(adapter.node_index.size() >= 224, "native node index covers required contract")
			check(adapter.is_state_visually_active(sample, original), "manifest current state visible")
			check(adapter.set_family_state(sample, "pristine"), "native state swap applies")
			check(adapter.is_state_visually_active(sample, "pristine"), "native target state visible")
			check(not adapter.is_state_visually_active(sample, original), "native previous state hidden")
			check(adapter.set_family_state(sample, original), "native sample state restored")

	if failures.is_empty():
		print(
			"PELAGOS_RUNTIME_SMOKE_PASS mode=%s families=56 stateful=47 required_nodes=224 revision=44"
			% ("contract-only" if contract_only else "native")
		)
		quit(0)
	else:
		print("PELAGOS_RUNTIME_SMOKE_FAIL count=%d" % failures.size())
		for failure in failures:
			print(" - " + failure)
		quit(1)
