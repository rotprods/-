extends SceneTree
const World = preload("res://scenes/main.tscn")
func _init():
	run.call_deferred()
func run():
	var world = World.instantiate()
	root.add_child(world)
	world.show_controls()
	await create_timer(1).timeout
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png("res://evidence/controls-ui.png")
	var rect: Rect2 = world.modal.get_global_rect()
	var size: Vector2 = root.get_visible_rect().size
	var within = rect.position.x>=0 and rect.position.y>=0 and rect.end.x<=size.x and rect.end.y<=size.y
	var out = FileAccess.open("res://evidence/controls-ui.json",FileAccess.WRITE)
	out.store_string(JSON.stringify({"viewport":[size.x,size.y],"modal_rect":[rect.position.x,rect.position.y,rect.size.x,rect.size.y],"within_viewport":within,"renderer":"GL Compatibility on Mesa CPU; no GPU performance claim"},"  "));out.close()
	print("UI_CAPTURE ",within)
	world.queue_free()
	await process_frame
	quit(0 if within else 1)
