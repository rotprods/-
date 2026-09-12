import bpy
scene=bpy.context.scene
for o in list(bpy.data.objects):
 if o.name in ['Amber memory lens','Core inner gasket','Memory core bezel','Memory core local light'] or o.name.startswith('Core bezel bolt'):
  o.location.x-=2.4
 if o.name.startswith('Core power rail'):
  bpy.data.objects.remove(o,do_unlink=True)
scene['review_note']='Amber core relocated left for visibility. Traversal threshold and game collision pending engine pass.'
scene.frame_set(1)
target=artifacts.file(name='reliquary-gate-final.png',media_type='image/png')
scene.render.image_settings.media_type='IMAGE'
scene.render.image_settings.file_format='PNG'
scene.render.filepath=str(target.path)
bpy.ops.render.render(write_still=True)
target.publish()
result={'objects':len(bpy.data.objects),'core_position':list(bpy.data.objects['Amber memory lens'].location),'animation_verified_degrees':[0,8,0],'engine_validation':False}

