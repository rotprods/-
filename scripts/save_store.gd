extends RefCounted
const Progress = preload("res://scripts/progress.gd")
var path: String
var last_error: String = ""

func _init(file_path: String = "user://exovant-save.json") -> void:
	path = file_path

func read_valid(file_path: String) -> Dictionary:
	if not FileAccess.file_exists(file_path): return {}
	var f := FileAccess.open(file_path, FileAccess.READ)
	if f == null or f.get_length() > 2097152: return {}
	var parser := JSON.new()
	if parser.parse(f.get_as_text()) != OK: return {}
	var envelope: Variant = parser.data
	if not envelope is Dictionary or not envelope.get("payload") is String or not envelope.get("sha256") is String: return {}
	if envelope.payload.sha256_text() != envelope.sha256: return {}
	if parser.parse(envelope.payload) != OK: return {}
	var d: Variant = parser.data
	return d if Progress.validate(d) else {}

func load_game() -> Dictionary:
	var d := read_valid(path)
	if d.is_empty(): d = read_valid(path + ".bak")
	return d

func save_game(d: Dictionary) -> bool:
	last_error = ""
	if not Progress.validate(d):
		last_error = "Estado no válido; guardado conservado"
		return false
	var payload := JSON.stringify(d)
	var f := FileAccess.open(path + ".tmp", FileAccess.WRITE)
	if f == null:
		last_error = "No se puede escribir el guardado"
		return false
	f.store_string(JSON.stringify({"payload":payload,"sha256":payload.sha256_text()}))
	f.flush()
	f.close()
	if read_valid(path + ".tmp").is_empty():
		last_error = "Falló la verificación del guardado temporal"
		return false
	# Never replace a healthy backup with a corrupt main file.
	if not read_valid(path).is_empty():
		var copy_error := DirAccess.copy_absolute(path, path + ".bak")
		if copy_error != OK:
			last_error = "No se pudo conservar la copia anterior"
			return false
	var error := DirAccess.rename_absolute(path + ".tmp", path)
	if error != OK:
		last_error = "No se pudo confirmar el guardado"
		return false
	return true
