"""SYLVA R17: replace R01/R03 circular Curve render geometry with self-contained structural meshes.

The source Bezier/taper is serialized into each replacement object's custom properties for rollback.
No external bevel helper object is required or exported.
"""
from __future__ import annotations
import bpy, json
from mathutils import Vector

CONTRACT='SYLVA_MACRO_ROOT_XSEC_R17_MESH_AB'
PROFILE=[(1.00,0.00),(0.88,0.32),(0.62,0.55),(0.28,0.68),(0.00,0.72),(-0.28,0.68),(-0.62,0.55),(-0.88,0.32),(-1.00,0.00),(-0.92,-0.30),(-0.68,-0.53),(-0.30,-0.65),(0.00,-0.68),(0.30,-0.65),(0.68,-0.53),(0.92,-0.30)]
TARGETS={
 'SYLVA_ROOT_PRIMARY_R01':{'depth':48.0,'width':1.10,'height':0.70,'region':'PUERTO'},
 'SYLVA_ROOT_PRIMARY_R03':{'depth':72.0,'width':1.18,'height':0.66,'region':'VESPER'},
}
STEPS=16

def bez(a,b,c,d,t):
 u=1.0-t
 return a*(u*u*u)+b*(3*u*u*t)+c*(3*u*t*t)+d*(t*t*t)

def serialize_curve(o):
 sp=o.data.splines[0]
 return json.dumps({
  'object_name':o.name,'bevel_depth':float(o.data.bevel_depth),'twist_mode':o.data.twist_mode,
  'resolution_u':int(o.data.resolution_u),'bevel_resolution':int(o.data.bevel_resolution),
  'points':[{'co':list(p.co),'handle_left':list(p.handle_left),'handle_right':list(p.handle_right),'handle_left_type':p.handle_left_type,'handle_right_type':p.handle_right_type,'radius':float(p.radius),'tilt':float(p.tilt)} for p in sp.bezier_points]
 },separators=(',',':'))

def sample_curve(o):
 bp=o.data.splines[0].bezier_points; pts=[]; radii=[]
 for i in range(len(bp)-1):
  a,b=bp[i],bp[i+1]
  for j in range(STEPS):
   t=j/STEPS
   pts.append(bez(a.co,a.handle_right,b.handle_left,b.co,t))
   radii.append(float(a.radius)*(1-t)+float(b.radius)*t)
 pts.append(bp[-1].co.copy()); radii.append(float(bp[-1].radius))
 return pts,radii

def build_mesh(name,path,radii,depth,w,h):
 n=len(PROFILE); verts=[]; faces=[]; prev_lat=None
 for i,p in enumerate(path):
  prev=path[max(0,i-1)]; nxt=path[min(len(path)-1,i+1)]; tan=nxt-prev
  if tan.length<1e-9: tan=Vector((1,0,0))
  tan.normalize()
  if prev_lat is None:
   lat=tan.cross(Vector((0,0,1)))
   if lat.length<1e-6: lat=tan.cross(Vector((1,0,0)))
  else:
   lat=prev_lat-tan*prev_lat.dot(tan)
   if lat.length<1e-6: lat=tan.cross(Vector((0,0,1)))
  lat.normalize(); vertical=lat.cross(tan).normalized(); prev_lat=lat
  for x,y in PROFILE:
   verts.append(tuple(p + lat*(x*depth*w*radii[i]) + vertical*(y*depth*h*radii[i])))
 rings=len(path)
 for r in range(rings-1):
  for k in range(n): faces.append((r*n+k,r*n+(k+1)%n,(r+1)*n+(k+1)%n,(r+1)*n+k))
 faces.append(tuple(range(n-1,-1,-1)))
 off=(rings-1)*n; faces.append(tuple(off+k for k in range(n)))
 me=bpy.data.meshes.new(name+'_R17_MESH'); me.from_pydata(verts,[],faces); me.update()
 return me

def replace_root(name,spec):
 src=bpy.data.objects.get(name)
 if src is None or src.type!='CURVE' or src.data.bevel_mode!='ROUND': raise RuntimeError('Expected R16 curve '+name)
 if len(src.data.splines)!=1 or src.data.splines[0].type!='BEZIER': raise RuntimeError('Invalid source curve '+name)
 source_json=serialize_curve(src); path,radii=sample_curve(src); me=build_mesh(name,path,radii,spec['depth'],spec['width'],spec['height'])
 cols=list(src.users_collection); matrix=src.matrix_world.copy(); parent=src.parent; props={k:src[k] for k in src.keys()}; mats=[m for m in src.data.materials]; hide_render=src.hide_render; hide_viewport=src.hide_viewport
 new=bpy.data.objects.new(name+'__R17_TMP',me)
 for c in cols: c.objects.link(new)
 new.parent=parent; new.matrix_world=matrix; new.hide_render=hide_render; new.hide_viewport=hide_viewport
 for k,v in props.items(): new[k]=v
 for m in mats: me.materials.append(m)
 for poly in me.polygons: poly.use_smooth=True
 new['macro_root_xsec_contract']=CONTRACT; new['macro_root_profile_family']='BILATERAL_FLATTENED_LOAD_SECTION_V1'; new['macro_root_profile_region']=spec['region']; new['macro_root_cross_section_status']='R17_SELF_CONTAINED_MESH_AB'; new['r17_source_curve_json']=source_json; new['r17_mesh_rings']=len(path); new['r17_profile_vertices']=len(PROFILE); new['r17_centerline_sample_steps_per_segment']=STEPS; new['r17_width_factor']=spec['width']; new['r17_height_factor']=spec['height']; new['r17_base_depth_m']=spec['depth']; new['r17_source_taper_preserved']=True
 old_data=src.data; bpy.data.objects.remove(src,do_unlink=True); new.name=name
 if old_data.users==0: bpy.data.curves.remove(old_data)
 return {'name':name,'verts':len(me.vertices),'faces':len(me.polygons),'stream_cells':new.get('stream_cells')}

root=bpy.data.objects.get('SYLVA_WORLD_ROOT')
if not root or root.get('build_status')!='WAVE1N_R16_ROOT_TAPER_MEMBERSHIP_RECONCILED': raise RuntimeError('Expected safe R16 input')
changed=[replace_root(n,s) for n,s in TARGETS.items()]
root['macro_root_xsec_contract']=CONTRACT; root['macro_root_xsec_experiment_targets']='SYLVA_ROOT_PRIMARY_R01|SYLVA_ROOT_PRIMARY_R03'; root['build_status']='WAVE1O_R17_SELF_CONTAINED_ROOT_XSEC_AB'
bpy.context.view_layer.update(); bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
result={'status':'R17_SELF_CONTAINED_ROOT_XSEC_AB','contract':CONTRACT,'targets':changed,'helper_objects_required':False}
