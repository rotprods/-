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
	check(Progress.validate(p.snapshot()),"Snapshot satisfies schema")
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
	check(not Progress.validate(bad),"Unknown save version rejected")
	var store = SaveStore.new("user://gauntlet-state-test.json")
	for suffix in ["", ".bak", ".tmp"]:
		if FileAccess.file_exists(store.path+suffix): DirAccess.remove_absolute(store.path+suffix)
	check(store.save_game(p.snapshot()),"Write verified save")
	var fresh = Progress.new()
	check(fresh.restore(store.load_game()) and fresh.choice=="cogobierno" and fresh.memories==p.memories,"Cold restore preserves choices and rewards")
	p.grant("second",10)
	check(store.save_game(p.snapshot()),"Second write preserves backup")
	var f := FileAccess.open(store.path,FileAccess.WRITE)
	f.store_string("{partial_write")
	f.close()
	check(not store.load_game().is_empty() and not store.load_game().rewards.has("second"),"Corrupt main restores previous healthy generation")
	check(store.save_game(p.snapshot()) and not store.read_valid(store.path+".bak").is_empty(),"Repair never overwrites healthy backup with corruption")
	check(not store.save_game(bad),"Invalid save never replaces healthy save")
	# Atomic contract: an abandoned temporary file must not be promoted on load.
	f = FileAccess.open(store.path+".tmp",FileAccess.WRITE)
	f.store_string("interrupted")
	f.close()
	check(store.load_game().memories==p.memories,"Interrupted temporary write ignored")
	var receipt := {"suite":"state_and_recovery","passed":passed,"failed":failed,"engine":Engine.get_version_info().string}
	var out := FileAccess.open("res://evidence/state-tests.json",FileAccess.WRITE)
	out.store_string(JSON.stringify(receipt,"  "))
	out.close()
	print(JSON.stringify(receipt))
	quit(1 if failed else 0)
