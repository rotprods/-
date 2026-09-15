extends SceneTree
const Progress = preload("res://scripts/progress.gd")
const SaveStore = preload("res://scripts/save_store.gd")
var passed := 0
var failed := 0

func check(condition: bool, name: String) -> void:
	if condition:
		passed += 1
		print("PASS ",name)
	else:
		failed += 1
		print("FAIL ",name)

func remove_store_files(store: SaveStore) -> void:
	for suffix in ["", ".bak", ".tmp"]:
		if FileAccess.file_exists(store.path+suffix):
			DirAccess.remove_absolute(store.path+suffix)

func raw_payload(file_path: String) -> Dictionary:
	if not FileAccess.file_exists(file_path):
		return {}
	var f := FileAccess.open(file_path, FileAccess.READ)
	if f == null:
		return {}
	var parser := JSON.new()
	if parser.parse(f.get_as_text()) != OK or not parser.data is Dictionary:
		return {}
	var envelope: Dictionary = parser.data
	if not envelope.get("payload") is String:
		return {}
	if parser.parse(envelope.payload) != OK or not parser.data is Dictionary:
		return {}
	return parser.data

func _init() -> void:
	var p = Progress.new()
	check(not p.advance("atlas"),"Cannot skip mission dependencies")
	check(not p.advance("unknown"),"Unknown mission rejected")
	check(not p.turn_valve(0),"Valve requires Ines")
	check(p.advance("met_ines"),"Accept Ines mission")
	check(not p.advance("met_ines") and p.memories==100,"Duplicate objective gives no reward")
	check(not p.turn_valve(-1) and not p.turn_valve(3),"Malformed valve indexes rejected")
	for i in range(3):
		for j in range(i+1): p.turn_valve(i)
	check(p.flags.get("water",false),"Puzzle resolves at 1 2 3")
	check(not p.turn_valve(0),"Solved puzzle remains solved")
	check(p.advance("archive"),"Archive unlocked by water")
	p.die(Vector3(4,0,-20))
	check(p.memories==0 and p.echo_value==300 and p.flags.archive,"Death preserves quest and drops memories")
	check(p.recover_echo()==300 and p.recover_echo()==0 and p.memories==300,"Echo can be claimed once")
	check(p.advance("atlas"),"Atlas completion")
	check(p.resolve("cogobierno") and not p.resolve("industria"),"Outcome cannot be overwritten")
	check(Progress.validate(p.snapshot()),"Snapshot satisfies current v2 schema")
	check(p.snapshot().version==2 and p.snapshot().worlds.is_empty(),"Fresh v2 snapshot has empty world namespace")

	# Explicit legacy migration: v1 is not current schema, but a valid v1 payload upgrades losslessly.
	var legacy: Dictionary = p.snapshot()
	legacy.version = 1
	legacy.erase("worlds")
	check(not Progress.validate(legacy),"Legacy v1 is not silently accepted as current schema")
	var migrated := Progress.migrate(legacy)
	check(Progress.validate(migrated) and migrated.version==2 and migrated.worlds.is_empty(),"Legacy v1 migrates to valid v2")
	check(migrated.flags==legacy.flags and migrated.rewards==legacy.rewards and migrated.memories==legacy.memories and migrated.choice==legacy.choice and migrated.valves==legacy.valves and migrated.checkpoint==legacy.checkpoint and migrated.echo==legacy.echo and migrated.echo_value==legacy.echo_value,"Legacy migration preserves every Terra field")
	var legacy_fresh = Progress.new()
	check(legacy_fresh.restore(legacy) and legacy_fresh.snapshot()==migrated,"Progress.restore cold-migrates legacy v1")

	# World state is generic, revision-bound, deep-copied and fail-closed.
	var pelagos := {
		"schema":"EXOVANT.PELAGOS.STATE.v1",
		"version":1,
		"world_id":"PELAGOS",
		"source_revision":44,
		"families":{
			"PEL-PROP-WET-WORK-STATION-002":"used",
			"PEL-DMG-DECK-IMPACT-001":"field_repaired",
		},
	}
	check(Progress.world_state_valid("PELAGOS",pelagos),"Revision-bound Pelagos world envelope validates")
	check(p.set_world_state("PELAGOS",pelagos),"World state accepted into v2 namespace")
	check(p.get_world_state("PELAGOS")==pelagos,"World state roundtrips exactly")
	var caller_copy := p.get_world_state("PELAGOS")
	caller_copy.families["PEL-PROP-WET-WORK-STATION-002"] = "abandoned"
	check(p.get_world_state("PELAGOS").families["PEL-PROP-WET-WORK-STATION-002"]=="used","World state getter returns deep copy")
	pelagos.families["PEL-PROP-WET-WORK-STATION-002"] = "pristine"
	check(p.get_world_state("PELAGOS").families["PEL-PROP-WET-WORK-STATION-002"]=="used","World state setter stores deep copy")
	var wrong_world := p.get_world_state("PELAGOS")
	wrong_world.world_id = "ARES_IX"
	check(not p.set_world_state("PELAGOS",wrong_world),"Mismatched world id rejected")
	var bad_revision := p.get_world_state("PELAGOS")
	bad_revision.source_revision = -1
	check(not p.set_world_state("PELAGOS",bad_revision),"Negative world revision rejected")
	var bad_tree := p.get_world_state("PELAGOS")
	bad_tree.families["bad"] = INF
	check(not p.set_world_state("PELAGOS",bad_tree),"Non-finite nested world data rejected")
	var bad_world_name := p.get_world_state("PELAGOS")
	bad_world_name.world_id = "pelagos unsafe"
	check(not Progress.world_state_valid("pelagos unsafe",bad_world_name),"Unsafe world identifiers rejected")
	check(Progress.validate(p.snapshot()),"Snapshot with world namespace satisfies v2 schema")

	var bad: Dictionary = p.snapshot()
	bad.memories = -1
	check(not Progress.validate(bad),"Negative balance rejected")
	bad = p.snapshot()
	bad.rewards.append(bad.rewards[0])
	check(not Progress.validate(bad),"Duplicated reward ledger rejected")
	bad = p.snapshot()
	bad.checkpoint = [0,INF,0]
	check(not Progress.validate(bad),"Infinite checkpoint rejected")
	bad = p.snapshot()
	bad.flags.erase("water")
	check(not Progress.validate(bad),"Broken dependency graph rejected")
	bad = p.snapshot()
	bad.version = 999
	check(not Progress.validate(bad) and Progress.migrate(bad).is_empty(),"Unknown save version rejected by validation and migration")
	bad = p.snapshot()
	bad.worlds.PELAGOS.world_id = "WRONG"
	check(not Progress.validate(bad),"Corrupt nested world envelope rejects whole save")

	# Storage boundary canonicalizes valid v1 to physical v2 before hashing/writing.
	var legacy_store = SaveStore.new("user://gauntlet-state-legacy-v1.json")
	remove_store_files(legacy_store)
	check(legacy_store.save_game(legacy),"SaveStore accepts valid legacy payload for canonical migration")
	var physical := raw_payload(legacy_store.path)
	check(physical.get("version")==2 and physical.get("worlds") is Dictionary and physical.worlds.is_empty(),"SaveStore physically writes canonical v2, never v1")
	var legacy_loaded := legacy_store.load_game()
	check(Progress.validate(legacy_loaded) and legacy_loaded==migrated,"Legacy storage roundtrip returns canonical v2")
	remove_store_files(legacy_store)

	# Existing atomic save/backup contract must remain unchanged with v2 world data present.
	var store = SaveStore.new("user://gauntlet-state-test.json")
	remove_store_files(store)
	check(store.save_game(p.snapshot()),"Write verified v2 save")
	var fresh = Progress.new()
	check(fresh.restore(store.load_game()) and fresh.choice=="cogobierno" and fresh.memories==p.memories,"Cold restore preserves choices and rewards")
	check(fresh.get_world_state("PELAGOS")==p.get_world_state("PELAGOS"),"Cold restore preserves namespaced world state")
	p.grant("second",10)
	check(store.save_game(p.snapshot()),"Second write preserves backup")
	var f := FileAccess.open(store.path,FileAccess.WRITE)
	f.store_string("{partial_write")
	f.close()
	check(not store.load_game().is_empty() and not store.load_game().rewards.has("second"),"Corrupt main restores previous healthy generation")
	check(store.load_game().get("version")==2 and (store.load_game().worlds as Dictionary).has("PELAGOS"),"Backup recovery remains migrated/current and preserves world namespace")
	check(store.save_game(p.snapshot()) and not store.read_valid(store.path+".bak").is_empty(),"Repair never overwrites healthy backup with corruption")
	check(not store.save_game(bad),"Invalid save never replaces healthy save")
	# Atomic contract: an abandoned temporary file must not be promoted on load.
	f = FileAccess.open(store.path+".tmp",FileAccess.WRITE)
	f.store_string("interrupted")
	f.close()
	check(store.load_game().memories==p.memories,"Interrupted temporary write ignored")
	check(store.load_game().get("version")==2,"Interrupted write leaves current schema intact")

	var receipt := {"suite":"state_and_recovery_v2","passed":passed,"failed":failed,"engine":Engine.get_version_info().string,"schema":Progress.VERSION}
	var out := FileAccess.open("res://evidence/state-tests.json",FileAccess.WRITE)
	out.store_string(JSON.stringify(receipt,"  "))
	out.close()
	print(JSON.stringify(receipt))
	quit(1 if failed else 0)
