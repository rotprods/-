extends Node3D
const Progress = preload("res://scripts/progress.gd")
const SaveStore = preload("res://scripts/save_store.gd")
const Player = preload("res://scripts/player.gd")
const Enemy = preload("res://scripts/enemy.gd")
const Controls = preload("res://scripts/controls.gd")
var controls = Controls.new()
var controls_footer: Label
var rebind_action := ""
var controls_return: Callable
var progress = Progress.new()
var storage = SaveStore.new()
var player: CharacterBody3D
var enemies: Array = []
var interactables: Array = []
var modal_open := true
var ui: CanvasLayer
var modal: PanelContainer
var modal_content: VBoxContainer
var hud: Label
var quest_label: Label
var notice: Label
var hint: Label
var title: Label
var notice_time := 0.0
var damage_flash := 0.0
var tint: ColorRect
var rover: Node3D
var garden_nodes: Array = []
var echoes: MeshInstance3D
var pulses: Array = []
var elapsed := 0.0
var checkpoint_id := "coast"
var capture_mode := false
var health_bar: ColorRect
var stamina_bar: ColorRect

func material(color: Color, metal: float = 0, emission: float = 0) -> StandardMaterial3D:
	var m := StandardMaterial3D.new()
	m.albedo_color = color
	m.metallic = metal
	m.roughness = .65
	if color.a < 1:
		m.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
	if emission > 0:
		m.emission_enabled = true
		m.emission = Color(color.r,color.g,color.b)
		m.emission_energy_multiplier = emission
	return m

func box(parent: Node3D, pos: Vector3, size: Vector3, mat: Material, solid: bool = false) -> MeshInstance3D:
	var o := MeshInstance3D.new()
	var mesh := BoxMesh.new()
	mesh.size = size
	o.mesh = mesh
	o.material_override = mat
	parent.add_child(o)
	o.position = pos
	if solid:
		var body := StaticBody3D.new()
		var shape := CollisionShape3D.new()
		var geo := BoxShape3D.new()
		geo.size = size
		shape.shape = geo
		body.add_child(shape)
		o.add_child(body)
	return o

func cylinder(parent: Node3D, pos: Vector3, radius: float, height: float, mat: Material) -> MeshInstance3D:
	var o := MeshInstance3D.new()
	var mesh := CylinderMesh.new()
	mesh.top_radius = radius
	mesh.bottom_radius = radius
	mesh.height = height
	mesh.radial_segments = 16
	o.mesh = mesh
	o.material_override = mat
	parent.add_child(o)
	o.position = pos
	return o

func sphere(parent: Node3D, pos: Vector3, radius: float, mat: Material) -> MeshInstance3D:
	var o := MeshInstance3D.new()
	var mesh := SphereMesh.new()
	mesh.radius = radius
	mesh.height = radius*2
	mesh.radial_segments = 16
	mesh.rings = 8
	o.mesh = mesh
	o.material_override = mat
	parent.add_child(o)
	o.position = pos
	return o

func limb(parent: Node3D, pos: Vector3, radius: float, height: float, mat: Material) -> MeshInstance3D:
	var o := MeshInstance3D.new()
	var mesh := CapsuleMesh.new()
	mesh.radius = radius
	mesh.height = height
	mesh.radial_segments = 12
	mesh.rings = 4
	o.mesh = mesh
	o.material_override = mat
	parent.add_child(o)
	o.position = pos
	return o

func make_humanoid(parent: Node3D, color: Color, is_boss: bool) -> Node3D:
	var root := Node3D.new()
	parent.add_child(root)
	var shell := material(color,.45)
	var black := material(Color("1b2b31"),.25)
	var glow := material(Color("ff8055") if is_boss else Color("82ddd8"),.2,1.4)
	var torso := sphere(root,Vector3(0,1.03,0),.38,shell)
	torso.scale = Vector3(1,.98,.65)
	var helmet := sphere(root,Vector3(0,1.61,0),.24,shell)
	helmet.scale = Vector3(.9,1,1)
	box(root,Vector3(0,1.62,-.22),Vector3(.32,.07,.05),glow)
	box(root,Vector3(0,1.04,-.23),Vector3(.20,.25,.07),glow)
	box(root,Vector3(0,1.13,.27),Vector3(.33,.46,.18),black)
	box(root,Vector3(0,1.19,.37),Vector3(.08,.26,.03),glow)
	for side in [-1,1]:
		var leg := Node3D.new()
		root.add_child(leg)
		leg.name = "LegL" if side<0 else "LegR"
		leg.position = Vector3(side*.20,.75,0)
		limb(leg,Vector3(0,-.3,0),.12,.67,black)
		limb(leg,Vector3(0,-.44,-.055),.13,.32,shell)
		var arm := Node3D.new()
		root.add_child(arm)
		arm.name = "ArmL" if side<0 else "ArmR"
		arm.position = Vector3(side*.40,1.27,0)
		limb(arm,Vector3(side*.04,-.24,0),.11,.61,shell)
		sphere(root,Vector3(side*.38,1.27,0),.19,shell)
		box(root,Vector3(side*.22,.1,-.12),Vector3(.28,.19,.45),shell)
	if is_boss:
		root.scale = Vector3.ONE*3
		box(root,Vector3(.72,1.0,-.7),Vector3(.13,.14,1.8),glow)
		for i in range(6):
			var branch := box(root,Vector3((i-2.5)*.22,1.96,.1),Vector3(.09,.7,.13),shell)
			branch.rotation.z = (i-2.5)*.16
	return root

func caption(text: String, pos: Vector3, color: Color = Color("b4d2c9")) -> Label3D:
	var l := Label3D.new()
	l.text = text
	l.position = pos
	l.font_size = 38
	l.pixel_size = .015
	l.modulate = color
	l.billboard = BaseMaterial3D.BILLBOARD_ENABLED
	add_child(l)
	return l

func register(id: String, label: String, pos: Vector3, radius: float = 3.0) -> void:
	interactables.append({"id":id,"label":label,"position":pos,"radius":radius})

func configure_input() -> void:
	if "--test-input" in OS.get_cmdline_user_args():
		controls = Controls.new("user://exovant-test-input-controls.json")
	elif "--test-world" in OS.get_cmdline_user_args():
		controls = Controls.new("user://exovant-test-world-controls.json")
	controls.load_bindings()

func _ready() -> void:
	configure_input()
	capture_mode = "--capture" in OS.get_cmdline_user_args()
	if "--test-world" in OS.get_cmdline_user_args(): storage = SaveStore.new("user://exovant-test-world.json")
	if "--test-input" in OS.get_cmdline_user_args(): storage = SaveStore.new("user://exovant-test-input.json")
	var saved := storage.load_game()
	if not saved.is_empty(): progress.restore(saved)
	build_environment()
	player = Player.new()
	player.world = self
	player.position = Vector3(progress.checkpoint[0],progress.checkpoint[1],progress.checkpoint[2])
	add_child(player)
	for i in range(4):
		spawn_enemy("custodian_%d" % i,Vector3((-1 if i%2==0 else 1)*(6+i),.2,-8-i*10),false)
	spawn_enemy("atlas",Vector3(0,.2,-54),true)
	build_ui()
	refresh_world()
	show_title()
	if capture_mode:
		close_modal()
		player.input_enabled = false
		capture_frame.call_deferred()
	if "--test-world" in OS.get_cmdline_user_args():
		close_modal()
		player.input_enabled = false
		get_node_or_null("WorldTests")

func build_environment() -> void:
	var envnode := WorldEnvironment.new()
	var env := Environment.new()
	env.background_mode = Environment.BG_SKY
	var sky := Sky.new()
	var skymat := ProceduralSkyMaterial.new()
	skymat.sky_top_color = Color("102b41")
	skymat.sky_horizon_color = Color("749e9e")
	skymat.ground_bottom_color = Color("172d32")
	skymat.ground_horizon_color = Color("749e9e")
	sky.sky_material = skymat
	env.sky = sky
	env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
	env.ambient_light_color = Color("a3c2bf")
	env.ambient_light_energy = .36
	env.tonemap_mode = Environment.TONE_MAPPER_FILMIC
	env.fog_enabled = true
	env.fog_light_color = Color("4b797f")
	env.fog_density = .002
	envnode.environment = env
	add_child(envnode)
	var sun := DirectionalLight3D.new()
	sun.rotation_degrees = Vector3(-34,-28,0)
	sun.light_color = Color("ffdbac")
	sun.light_energy = .82
	sun.shadow_enabled = true
	add_child(sun)
	var stone := material(Color("37484a"),.2)
	var paving := material(Color("687675"),.15)
	var bronze := material(Color("96805b"),.65)
	var amber := material(Color("efb25d"),.3,1.2)
	var cyan := material(Color("7dcac4"),.2,1.5)
	box(self,Vector3(0,-.6,-25),Vector3(90,1.2,190),stone,true)
	box(self,Vector3(0,-1.1,-10),Vector3(500,.1,500),material(Color("286478"),.65))
	for side in [-1,1]:
		box(self,Vector3(side*43,2,-25),Vector3(2,5,190),stone,true)
	for z in [69,-119]: box(self,Vector3(0,2,z),Vector3(90,5,2),stone,true)
	for i in range(25):
		box(self,Vector3(0,.03,24-i*4),Vector3(7,.12,3.85),paving)
		for side in [-1,1]:
			box(self,Vector3(side*3.7,.10,24-i*4),Vector3(.07,.08,2.8),amber if i < 8 else cyan)
	# Readable arena and architectural landmarks.
	cylinder(self,Vector3(0,.06,-54),21,.12,material(Color("6e7669"),.2))
	for i in range(24):
		var angle := i*TAU/24
		var p := Vector3(sin(angle)*22,2,-54+cos(angle)*22)
		if absf(p.x)<5: continue
		box(self,p,Vector3(.9,4,.9),bronze,true)
		box(self,p+Vector3(0,2.2,0),Vector3(.7,.2,.7),cyan)
	for side in [-1,1]:
		for i in range(4):
			var pos := Vector3(side*(25+i*3),12+i*3,-55-i*15)
			box(self,pos,Vector3(3,24+i*6,4),stone)
			box(self,pos+Vector3(0,8,0),Vector3(5,.25,5),bronze)
	var rng := RandomNumberGenerator.new()
	rng.seed = 2950
	for i in range(100):
		var side := -1 if i%2==0 else 1
		var pos := Vector3(side*rng.randf_range(12,39),0,rng.randf_range(-90,42))
		var h := rng.randf_range(3,8)
		cylinder(self,pos+Vector3(0,h/2,0),.13,h,bronze)
		var crown := sphere(self,pos+Vector3(0,h,0),rng.randf_range(1,2.5),material(Color("355e53")))
		crown.scale = Vector3(1,.35,1)
		garden_nodes.append(crown)
		if i%5==0: box(self,pos+Vector3(0,.7,0),Vector3(1.5,1.4,1),stone,true)
	# Original GLB geometry, remove studio camera/lights/floor on import.
	var gate = load("res://assets/reliquary_gate.glb").instantiate()
	clean_presentation(gate)
	add_child(gate)
	gate.position = Vector3(0,0,-84)
	# Accessible ramp/landing over the original asset's step lip.
	box(self,Vector3(0,1.43,-83.6),Vector3(3.05,.15,4.7),stone,true)
	var ramp := box(self,Vector3(0,.70,-78.8),Vector3(3.15,.18,5.3),stone,true)
	ramp.rotation.x = .30
	for side in [-1,1]: box(self,Vector3(side*3.2,.8,-84),Vector3(2.2,1.6,3.8),stone,true)
	caption("PRIMER RELIQUARIO",Vector3(0,9,-85))
	register("gate","Examinar el tránsito",Vector3(0,1.5,-83),5)
	# Refuge, archive and three narrative actors.
	cylinder(self,Vector3(-5,.5,16),.65,1,bronze)
	sphere(self,Vector3(-5,1.4,16),.24,amber)
	register("camp","Descansar / guardar",Vector3(-5,0,16),3.5)
	caption("REFUGIO DEL RETORNO",Vector3(-5,3,16),Color("efb25d"))
	var names := ["INÉS VALE", "BRUNO ARCE", "SAJA LIN"]
	var ids := ["ines","bruno","saja"]
	var positions := [Vector3(5,0,15),Vector3(-7,0,6),Vector3(8,0,-17)]
	for i in range(3):
		var npc := Node3D.new()
		add_child(npc)
		npc.position = positions[i]
		make_humanoid(npc,Color("c5bca1"),false)
		caption(names[i],positions[i]+Vector3(0,2.7,0))
		register(ids[i],"Hablar · "+names[i],positions[i],3)
	box(self,Vector3(7,1,-5),Vector3(2.6,2,1.2),bronze,true)
	for i in range(3):
		cylinder(self,Vector3(6.25+i*.75,2.1,-5),.22,.18,cyan)
	caption("RIEGO RESONANTE",Vector3(7,3.7,-5))
	register("valves","Ajustar válvulas",Vector3(7,0,-3.5),3)
	box(self,Vector3(-9,.65,-30),Vector3(4,1.3,3),bronze,true)
	box(self,Vector3(-9,1.4,-30),Vector3(2,.15,1.6),cyan)
	caption("ARCHIVO ABISAL",Vector3(-9,3.2,-30))
	register("archive","Extraer el acta",Vector3(-9,0,-27.7),3)
	register("choice","Decidir la custodia",Vector3(0,0,-54),23)
	# A compact playable maintenance rover; no claim of vehicle suspension physics.
	rover = Node3D.new()
	add_child(rover)
	rover.position = Vector3(-12,0,17)
	box(rover,Vector3(0,.8,0),Vector3(1.9,.65,3),bronze)
	box(rover,Vector3(0,1.4,.1),Vector3(1.4,.7,1.25),material(Color("a7b8b0"),.5))
	for side in [-1,1]:
		for z in [-.9,.9]:
			var wheel := cylinder(rover,Vector3(side, .5,z),.5,.32,stone)
			wheel.rotation.z = PI/2
	caption("PEREGRINO-6",Vector3(-12,3,17))
	register("rover","Pilotar Peregrino-6",Vector3(-12,0,17),3.5)
	echoes = sphere(self,Vector3.ZERO,.3,cyan)
	echoes.visible = false
	# Distant moon and orbital fragments are real meshes, no sky photograph.
	sphere(self,Vector3(-90,110,-240),34,material(Color("aabcb5")))
	for i in range(9):
		var shard := box(self,Vector3(60+i*8,70+i*5,-220),Vector3(2,10+i*2,3),bronze)
		shard.rotation.z = -.3

func clean_presentation(node: Node) -> void:
	for child in node.get_children():
		if child is Camera3D or child is Light3D or "Presentation_floor" in child.name or "Presentation floor" in child.name:
			node.remove_child(child)
			child.free()
		else: clean_presentation(child)

func spawn_enemy(id: String, pos: Vector3, is_boss: bool) -> void:
	var enemy = Enemy.new()
	enemy.world = self
	enemy.boss = is_boss
	enemy.enemy_id = id
	enemy.position = pos
	add_child(enemy)
	enemies.append(enemy)

func build_ui() -> void:
	ui = CanvasLayer.new()
	add_child(ui)
	var shade := ColorRect.new()
	shade.color = Color(0.018,.035,.045,.72)
	shade.size = Vector2(1280,94)
	shade.mouse_filter = Control.MOUSE_FILTER_IGNORE
	ui.add_child(shade)
	title = label("E X O V A N T   /   2 9 5 0",Vector2(30,18),22,Color("f0d6ae"))
	hud = label("",Vector2(30,56),17)
	health_bar = status_bar(Vector2(30,88),Color("b56045"))
	stamina_bar = status_bar(Vector2(30,98),Color("75bda6"))
	quest_label = label("",Vector2(470,24),18)
	quest_label.size.x = 780
	notice = label("",Vector2(30,610),20,Color("efbf79"))
	hint = label("",Vector2(30,650),17)
	var foot := ColorRect.new()
	foot.color = Color(.015,.035,.045,.88)
	foot.position = Vector2(0,665)
	foot.size = Vector2(1280,55)
	foot.mouse_filter = Control.MOUSE_FILTER_IGNORE
	ui.add_child(foot)
	controls_footer = label(controls.footer(),Vector2(30,676),12,Color("b7c9c8"))
	tint = ColorRect.new()
	tint.size = Vector2(1280,720)
	tint.mouse_filter = Control.MOUSE_FILTER_IGNORE
	tint.color = Color(1,.13,.04,0)
	ui.add_child(tint)
	modal = PanelContainer.new()
	modal.position = Vector2(330,140)
	modal.custom_minimum_size = Vector2(620,360)
	var style := StyleBoxFlat.new()
	style.bg_color = Color(.025,.055,.068,.97)
	style.border_color = Color("b29767")
	style.set_border_width_all(1)
	style.content_margin_left = 28
	style.content_margin_right = 28
	style.content_margin_top = 24
	style.content_margin_bottom = 24
	modal.add_theme_stylebox_override("panel",style)
	modal_content = VBoxContainer.new()
	modal_content.add_theme_constant_override("separation",14)
	modal.add_child(modal_content)
	ui.add_child(modal)

func status_bar(pos: Vector2, color: Color) -> ColorRect:
	var bg := ColorRect.new()
	bg.position = pos
	bg.size = Vector2(330,6)
	bg.color = Color("152a30")
	bg.mouse_filter = Control.MOUSE_FILTER_IGNORE
	ui.add_child(bg)
	var b := ColorRect.new()
	b.position = pos
	b.size = Vector2(330,6)
	b.color = color
	b.mouse_filter = Control.MOUSE_FILTER_IGNORE
	ui.add_child(b)
	return b

func label(text: String, pos: Vector2, font_size: int, color: Color = Color("d5e4df")) -> Label:
	var l := Label.new()
	l.text = text
	l.position = pos
	l.add_theme_font_size_override("font_size",font_size)
	l.modulate = color
	ui.add_child(l)
	return l

func open_modal(heading: String, body: String) -> void:
	rebind_action = ""
	modal_open = true
	modal.visible = true
	Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
	for c in modal_content.get_children():
		modal_content.remove_child(c)
		c.queue_free()
	var h := Label.new()
	h.text = heading
	h.add_theme_font_size_override("font_size",28)
	h.modulate = Color("edc68c")
	modal_content.add_child(h)
	var text := Label.new()
	text.text = body
	text.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	text.custom_minimum_size.x = 560
	text.add_theme_font_size_override("font_size",18)
	modal_content.add_child(text)

func button(text: String, callback: Callable) -> void:
	var b := Button.new()
	b.text = text
	b.custom_minimum_size.y = 42
	b.pressed.connect(callback)
	modal_content.add_child(b)
	if get_viewport().gui_get_focus_owner() == null: b.grab_focus()

func close_modal() -> void:
	rebind_action = ""
	modal_open = false
	modal.visible = false
	if not capture_mode: Input.mouse_mode = Input.MOUSE_MODE_CAPTURED

func show_title() -> void:
	open_modal("EXOVANT 2950", "EL DERECHO A REGRESAR\n\nTerra se ha recuperado. Sus custodios ya no nos reconocen como habitantes.\n\nUna sección experimental en 3D: costa, riego, archivo y ATLAS.\nConstrucción 0.1 · Personajes y combate en prototipo.")
	button("Continuar en la costa" if progress.flags.size()>0 else "Despertar en Terra",close_modal)
	button("Controles",func(): controls_return = show_title; show_controls())

func show_controls() -> void:
	open_modal("CONTROLES DEL RETORNADO", "Selecciona una acción y pulsa una tecla o botón.\nEsc cancela · Start pausa · Sticks: movimiento y cámara")
	var scroll := ScrollContainer.new()
	scroll.custom_minimum_size.y = 215
	scroll.horizontal_scroll_mode = ScrollContainer.SCROLL_MODE_DISABLED
	scroll.follow_focus = true
	modal_content.add_child(scroll)
	var rows := VBoxContainer.new()
	rows.size_flags_horizontal = Control.SIZE_EXPAND_FILL
	scroll.add_child(rows)
	for action in Controls.LABELS:
		var b := Button.new()
		b.text = "%s · %s / %s" % [Controls.LABELS[action],controls.binding_text(action),controls.binding_text(action,true)]
		b.custom_minimum_size.y = 36
		b.pressed.connect(func(): begin_rebind(action))
		rows.add_child(b)
		if get_viewport().gui_get_focus_owner() == null: b.grab_focus()
	button("Restaurar controles iniciales",func():
		if not controls.commit(Controls.defaults()): notify(controls.last_error)
		show_controls())
	button("Volver",func():
		if controls_return.is_valid(): controls_return.call()
		else: show_pause())

func begin_rebind(action: String) -> void:
	open_modal("ASIGNAR · " + str(Controls.LABELS[action]).to_upper(), "Pulsa la nueva entrada. Tecla ocupada: se rechaza.\nBotón de mando ocupado: intercambia las dos acciones.\nEsc cancela. Start y navegación de menús se conservan.")
	rebind_action = action

func show_pause() -> void:
	open_modal("RETORNO EN PAUSA","El mundo está detenido. El refugio fija el punto de regreso.\nLas zonas bermellón anuncian golpes: sal del área o esquiva.")
	button("Continuar",close_modal)
	button("Guardar",func(): save_progress(); close_modal())
	button("Controles",func(): controls_return = show_pause; show_controls())

func _input(event: InputEvent) -> void:
	controls.observe(event)
	if not is_instance_valid(modal): return
	if rebind_action != "":
		if event.is_action_pressed("pause_game"):
			show_controls()
		elif event.is_pressed() and not event.is_echo() and (event is InputEventKey or event is InputEventMouseButton or event is InputEventJoypadButton):
			if controls.rebind(rebind_action,event):
				notify("Controles guardados")
				show_controls()
			else: notify(controls.last_error)
		get_viewport().set_input_as_handled()
		return
	if event.is_action_pressed("pause_game") or (modal_open and event.is_action_pressed("ui_cancel")):
		if modal_open: close_modal()
		else: show_pause()
		get_viewport().set_input_as_handled()

func notify(text: String) -> void:
	notice.text = text
	notice_time = 6

func save_progress() -> bool:
	var ok: bool = storage.save_game(progress.snapshot())
	if not ok: notify(storage.last_error)
	return ok

func nearest_enemy(pos: Vector3, distance: float) -> Node3D:
	var found: Node3D = null
	for e in enemies:
		if e.health <= 0: continue
		var d := pos.distance_to(e.global_position)
		if d < distance:
			distance = d
			found = e
	return found

func player_strike(heavy: bool) -> void:
	var forward: Vector3 = -player.body_visual.global_basis.z
	for e in enemies:
		if e.health <= 0: continue
		var delta: Vector3 = e.global_position-player.global_position
		delta.y = 0
		if delta.length() > (4.6 if e.boss else 2.9) or forward.dot(delta.normalized()) < .25: continue
		var ray := PhysicsRayQueryParameters3D.create(player.global_position+Vector3.UP,e.global_position+Vector3.UP,1)
		if not get_world_3d().direct_space_state.intersect_ray(ray).is_empty(): continue
		e.receive_damage(58.0 if heavy else 29.0)
		pulse_at(e.global_position,.6)

func enemy_defeated(enemy: Node3D) -> void:
	progress.grant("enemy:"+enemy.enemy_id,80 if enemy.boss else 25)
	if enemy.boss:
		progress.advance("atlas")
		notify("PROTOCOLO AISLADO · La custodia de Terra está en tus manos")
	else: notify("Custodio neutralizado")
	save_progress()

func player_died() -> void:
	progress.die(player.global_position)
	player.health = 100
	player.stamina = 100
	player.flasks = 3
	player.in_vehicle = false
	player.dodge_time = 0
	player.attack_time = 0
	player.locked = null
	player.velocity = Vector3.ZERO
	player.position = Vector3(progress.checkpoint[0],progress.checkpoint[1],progress.checkpoint[2])
	for e in enemies:
		if not e.boss or not progress.flags.get("atlas",false): e.reset_encounter()
	refresh_world()
	save_progress()
	notify("HAS RETORNADO · Recupera tu eco cian. La misión permanece.")

func current_interaction() -> Dictionary:
	var best := {}
	var distance := 1000.0
	for item in interactables:
		if item.id == "choice" and (not progress.flags.get("atlas",false) or progress.choice != ""): continue
		if item.id == "rover": item.position = rover.position
		var d: float = player.position.distance_to(item.position)
		if d < item.radius and d < distance:
			best = item
			distance = d
	return best

func interact() -> void:
	if player.in_vehicle:
		player.in_vehicle = false
		player.position += Vector3(2,0,0)
		notify("Has abandonado el Peregrino-6")
		return
	if not progress.echo.is_empty() and player.position.distance_to(echoes.position) < 2:
		notify("Eco recuperado · %d memorias" % progress.recover_echo())
		refresh_world()
		save_progress()
		return
	var item := current_interaction()
	if item.is_empty(): return
	match item.id:
		"camp":
			progress.checkpoint = [-5.0,1.0,18.0]
			player.health = 100
			player.stamina = 100
			player.flasks = 3
			for e in enemies:
				if not e.boss: e.reset_encounter()
			if save_progress(): notify("Refugio sincronizado · Guardado · Cargas restauradas")
		"ines":
			progress.advance("met_ines")
			save_progress()
			open_modal("INÉS VALE · ARCHIVISTA", "El agua sigue llegando a las torres vacías. Aquí somos ocho familias.\n\nRestablece el riego: primera válvula a UNO, segunda a DOS, tercera a TRES. Luego busca el acta en el depósito.\n\nMi firma está en ese documento. No te pido que me absuelvas. Te pido que lo leas.")
			button("Iré al distribuidor de riego",close_modal)
		"bruno":
			open_modal("BRUNO ARCE · REFUGIADO", "Por fin vuelve el agua. Ahora que las torres esperen." if progress.flags.get("water",false) else "Nos llaman invasores. Llevamos cinco generaciones aquí. Tráenos agua antes de hablarme del equilibrio del planeta.")
			button("Continuar",close_modal)
		"saja":
			open_modal("SAJA LIN · TÉCNICA DE SEMILLAS", "ATLAS protege lo que queda del vivero. Cuando deje de luchar, no confundas el silencio con permiso para destruirlo. Podemos compartir su trabajo.")
			button("Continuar",close_modal)
		"valves": show_valves()
		"archive":
			if not progress.flags.get("water",false): notify("Depósito sellado · Restablece primero el riego")
			else:
				progress.advance("archive")
				save_progress()
				open_modal("ACTA ORIGINAL · 2941", "Las supuestas extinciones justificaron concesiones de suelo. El Concordato falsificó el informe de inhabitabilidad.\n\nFirma de integridad: INÉS VALE.\n\nEl acta se conserva tras morir. ATLAS acaba de reconocer su señal: entra en la plataforma circular y aísla su protocolo hostil.")
				button("Conservar el acta y avanzar",close_modal)
		"choice": show_choice()
		"gate":
			open_modal("RED MNÉMICA", "TERRA · " + progress.choice.to_upper() + "\n\nHas completado esta sección experimental. El siguiente destino previsto es Ares IX. Su región todavía no está construida en esta versión." if progress.choice != "" else "El tránsito permanece suspendido hasta resolver la custodia del agua, las semillas y el retorno.")
			button("Volver a Terra",close_modal)
		"rover":
			player.in_vehicle = true
			notify("PEREGRINO-6 · Movimiento para pilotar · " + controls.hint_for("interact") + " para bajar")

func show_valves() -> void:
	if not progress.flags.get("met_ines",false):
		notify("Distribución sin orden de servicio · Habla con Inés")
		return
	open_modal("RIEGO RESONANTE", "Presión objetivo: 1 · 2 · 3\nCada válvula recorre 0 → 1 → 2 → 3 → 0.\nSin temporizador; la configuración se conserva.")
	for i in range(3):
		button("Válvula %d: %d" % [i+1,progress.valves[i]],func():
			progress.turn_valve(i)
			save_progress()
			refresh_world()
			if progress.flags.get("water",false):
				close_modal()
				notify("RIEGO RESTAURADO · El depósito del archivo es accesible")
			else: show_valves())
	button("Cerrar",close_modal)

func show_choice() -> void:
	open_modal("EL DERECHO A REGRESAR", "ATLAS sigue vivo; su protocolo hostil está aislado. El acta prueba el fraude.\n\nCOGOBIERNO: técnicos y biosfera comparten el agua.\nINDUSTRIA: el Concordato recupera la infraestructura.\n\nLa decisión se guarda y cambia el jardín de esta región.")
	for outcome in ["cogobierno","industria"]:
		button(outcome.to_upper(),func():
			progress.resolve(outcome)
			save_progress()
			refresh_world()
			close_modal()
			notify("TERRA RECUERDA · " + outcome.to_upper()))
	button("Decidir más tarde",close_modal)

func refresh_world() -> void:
	for n in garden_nodes:
		var m: StandardMaterial3D = n.material_override
		m.albedo_color = Color("6b5842") if progress.choice == "industria" else (Color("509775") if progress.flags.get("water",false) else Color("355e53"))
	echoes.visible = not progress.echo.is_empty()
	if echoes.visible: echoes.position = Vector3(progress.echo[0],progress.echo[1]+.6,progress.echo[2])
	for e in enemies:
		if e.boss and progress.flags.get("atlas",false):
			e.health = 0
			e.visible = false
			e.warning.visible = false

func pulse_at(pos: Vector3, radius: float) -> void:
	var p := cylinder(self,pos+Vector3(0,.12,0),radius,.05,material(Color(1,.53,.25,.5),0,1))
	pulses.append({"mesh":p,"life":.25})

func _process(dt: float) -> void:
	if not is_instance_valid(player) or not is_instance_valid(hud): return
	hud.text = "SALUD %03d   /   RESISTENCIA %03d   /   CARGAS %d   /   MEMORIAS %d" % [player.health,player.stamina,player.flasks,progress.memories]
	health_bar.size.x = clampf(player.health,0,100)*3.3
	stamina_bar.size.x = clampf(player.stamina,0,100)*3.3
	quest_label.text = progress.objective()
	controls_footer.text = controls.footer()
	if modal_open: return
	elapsed += dt
	notice_time -= dt
	if notice_time <= 0: notice.text = ""
	damage_flash = maxf(0,damage_flash-dt)
	tint.color.a = damage_flash*.65
	var item := current_interaction()
	hint.text = controls.hint_for("interact") + " · " + item.label if not item.is_empty() else ""
	if player.in_vehicle:
		rover.position = player.position
		rover.rotation.y = player.yaw
		hint.text = "PEREGRINO-6 · " + controls.hint_for("interact") + " para bajar"
	if not progress.echo.is_empty() and player.position.distance_to(echoes.position)<2: hint.text = controls.hint_for("interact") + " · Recuperar eco"
	for i in range(pulses.size()-1,-1,-1):
		pulses[i].life -= dt
		if pulses[i].life <= 0:
			pulses[i].mesh.queue_free()
			pulses.remove_at(i)

func capture_frame() -> void:
	await get_tree().create_timer(1).timeout
	player.position = Vector3(0,1,-34)
	player.yaw = 0
	await get_tree().create_timer(2).timeout
	await RenderingServer.frame_post_draw
	get_viewport().get_texture().get_image().save_png("res://evidence/runtime.png")
	print("CAPTURE_SAVED")
	get_tree().quit()
