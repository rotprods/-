"""Revision 2: interaction pivot, explicit collision sources, UV audit correction."""
import bpy, math
from mathutils import Vector
S=bpy.context.scene; C=bpy.data.collections['EXO_TERRA_KIT_EDITABLE']
coll=bpy.data.collections['COLLISION_PROXIES']
pump=bpy.data.objects['PR_TERRA_ResonanceRegulator']
valve=bpy.data.objects.new('PR_TERRA_RegulatorValve',None);C.objects.link(valve)
valve.parent=pump;valve.location=(0,-.77,1.08)
valve['rotation_axis']='local Y';valve['rest_angle_degrees']=0
valve['interaction']='rotate local Y; no gameplay or animation states authored here'
parts=0
for obj in list(pump.children):
 if obj.type!='MESH':continue
 me=obj.data; adjacency={i:set() for i in range(len(me.vertices))}
 for e in me.edges:
  a,b=e.vertices;adjacency[a].add(b);adjacency[b].add(a)
 remaining=set(adjacency); move=set()
 while remaining:
  start=remaining.pop();component={start};todo=[start]
  while todo:
   for neighbor in adjacency[todo.pop()]:
    if neighbor in remaining:remaining.remove(neighbor);component.add(neighbor);todo.append(neighbor)
  coords=[me.vertices[i].co for i in component]
  if max(v.y for v in coords)<-.65 and min(v.z for v in coords)>.70 and max(v.z for v in coords)<1.46:move.update(component)
 if not move:continue
 def subset(indices,name,offset):
  ids=sorted(indices);remap={old:new for new,old in enumerate(ids)}
  faces=[tuple(remap[i] for i in f.vertices) for f in me.polygons if all(i in indices for i in f.vertices)]
  data=bpy.data.meshes.new(name);data.from_pydata([me.vertices[i].co-offset for i in ids],[],faces);data.update()
  data.materials.append(me.materials[0]);uv=data.uv_layers.new(name='UV_MetreTile')
  for p in data.polygons:
   axes=((1,2),(0,2),(0,1))[max(range(3),key=lambda a:abs(p.normal[a]))]
   for li in p.loop_indices:
    v=data.vertices[data.loops[li].vertex_index].co+offset;uv.data[li].uv=(v[axes[0]],v[axes[1]])
  return data
 data=subset(move,'Valve_'+obj.name,Vector(valve.location))
 child=bpy.data.objects.new('Valve__'+obj.get('material_role','part'),data);C.objects.link(child);child.parent=valve
 bevel=child.modifiers.new('Editable_valve_edge','BEVEL');bevel.width=.004;bevel.segments=2
 child.modifiers.new('Weighted_normals','WEIGHTED_NORMAL')
 keep=set(range(len(me.vertices)))-move;obj.data=subset(keep,me.name+'_static',Vector((0,0,0)));parts+=1

# Explicit collision source proxies are independent of rendering triangles.
def cube(name,parent,center,dim):
 bpy.ops.mesh.primitive_cube_add(size=1,location=(0,0,0));o=bpy.context.object;o.name=name+'-colonly'
 for c in list(o.users_collection):c.objects.unlink(o)
 coll.objects.link(o);o.parent=parent;o.location=center
 for v in o.data.vertices:v.co.x*=dim[0];v.co.y*=dim[1];v.co.z*=dim[2]
 o.hide_render=True;o.display_type='WIRE';o['purpose']='collision-only; inspect in native import'
def cylinder(name,parent,center,r,h):
 bpy.ops.mesh.primitive_cylinder_add(vertices=16,radius=r,depth=h,location=(0,0,0));o=bpy.context.object;o.name=name+'-colonly'
 for c in list(o.users_collection):c.objects.unlink(o)
 coll.objects.link(o);o.parent=parent;o.location=center;o.hide_render=True;o.display_type='WIRE';o['purpose']='collision-only'
floor=bpy.data.objects['ENV_TERRA_Foundation_10x8']
cube('COL_Foundation',floor,(0,0,-.20),(10,8,.44))
for j in range(3):cube('COL_Step_'+str(j),floor,(0,-4.2-j*.28,-.18-j*.16),(4.2,.38,.30))
cube('COL_SluiceWall',bpy.data.objects['ENV_TERRA_SluiceWall_8x4'],(0,0,1.9),(8,.5,3.8))
for side in ('L','R'):cube('COL_Pilaster_'+side,bpy.data.objects['ENV_TERRA_RibPilaster_'+side],(0,0,1.92),(1.16,1.15,3.84))
cylinder('COL_RegulatorBase',pump,(0,0,.16),1.12,.32)
cylinder('COL_RegulatorBody',pump,(0,0,1.74),.64,2.88)
cube('COL_Console',bpy.data.objects['PR_TERRA_ServiceConsole'],(0,0,.61),(1,.85,1.22))
cube('COL_Archive',bpy.data.objects['PR_TERRA_ArchiveCradle'],(0,0,.69),(1.5,.8,1.38))
# Keep collection included for interchange. Individual proxies remain non-rendering in Blender.
coll.hide_viewport=False
ground=bpy.data.objects['PRESENTATION_Ground'].data
uv=ground.uv_layers.new(name='UV_Studio')
for p in ground.polygons:
 for li in p.loop_indices:
  v=ground.vertices[ground.loops[li].vertex_index].co;uv.data[li].uv=(v.x,v.y)
S.eevee.taa_render_samples=8
S.render.resolution_x=640;S.render.resolution_y=452
S['delivery_revision']='2; valve pivot and collision proxies; presentation separated by collection'
result={'valve_material_parts':parts,'valve_pivot':list(valve.location),'collision_sources':len(coll.objects),'objects':len(bpy.data.objects),'uv_missing':[o.name for o in C.objects if o.type=='MESH' and not o.data.uv_layers],'runtime_integration':False}
