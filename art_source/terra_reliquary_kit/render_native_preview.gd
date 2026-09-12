extends SceneTree
## Isolated Godot visual comparison. Needs a display; no game runtime loaded.
func _initialize() -> void:
    call_deferred("capture")

func capture() -> void:
    var packed = load("res://candidate.glb") as PackedScene
    if packed == null: quit(1); return
    var model = packed.instantiate()
    root.add_child(model)
    var camera = model.find_child("CAM_Delivery", true, false) as Camera3D
    if camera == null: printerr("Missing delivery camera"); quit(1); return
    camera.current = true
    var env_node := WorldEnvironment.new()
    var env := Environment.new()
    env.background_mode = Environment.BG_COLOR
    env.background_color = Color(0.015, 0.025, 0.03)
    env.ambient_light_source = Environment.AMBIENT_SOURCE_COLOR
    env.ambient_light_color = Color(0.35, 0.43, 0.45)
    env.ambient_light_energy = 0.7
    env.tonemap_mode = Environment.TONE_MAPPER_FILMIC
    env_node.environment = env
    root.add_child(env_node)
    for i in range(12): await process_frame
    await RenderingServer.frame_post_draw
    var image = root.get_texture().get_image()
    var error = image.save_png("res://godot-kit-preview.png")
    print(JSON.stringify({"saved": error == OK, "width": image.get_width(), "height": image.get_height(),
        "renderer": RenderingServer.get_video_adapter_name(), "scope": "Isolated GLB comparison under Godot lights and ambient; no target performance qualification"}))
    quit(0 if error == OK else 1)
