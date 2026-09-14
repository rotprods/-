"""SYLVA R18: promote self-contained structural cross sections to all six primary macro roots.

R01/R03 are retained from accepted R17 A/B and normalized to the R18 contract.
R02/R04/R05/R06 are converted from accepted R16 Curve+taper sources into closed meshes.
"""
from __future__ import annotations
import bpy, json
from mathutils import Vector

CONTRACT='SYLVA_MACRO_ROOT_XSEC_R18_ALL'
PROFILE=[(1.00,0.00),(0.88,0.32),(0.62,0.55),(0.28,0.68),(0.00,0.72),(-0.28,0.68),(-0.62,0.55),(-0.88,0.32),(-1.00,0.00),(-0.92,-0.30),(-0.68,-0.53),(-0.30,-0.65),(0.00,-0.68),(0.30,-0.65),(0.68,-0.53),(0.92,-0.30)]
STEPS=16
TARGETS={
 'SYLVA_ROOT_PRIMARY_R02':{'depth':62.0,'width':1.12,'height':0.70,'region':'BOSQUE'},
 'SYLVA_ROOT_PRIMARY_R04':{'depth':36.0,'width':1.08,'height':0.72,'region':'NETWORK_CROSS'},
 'SYLVA_ROOT_PRIMARY_R05':{'depth':30.0,'width':1.06,'height':0.74,'region':'NETWORK_CROSS'},
 'SYLVA_ROOT_PRIMARY_R06':{'depth':40.0,'width':1.12,'height':0.68,'region':'VESPER_APPROACH'},
}

def bez(a,b,c,d,t):
 u=1-t; return a*(u*u*u)+b*(3*u*u*t)+c*(3*u*t*t)+d*(t*t*t)

def serialize_curve(o):
 sp=o.data.splines[0]
 return json.dumps({'object_name':o.name,'bevel_depth':float(o.data.bevel_depth),'twist_mode':o.data.twist_mode,'resolution_u':int(o.data.resolution_u),'bevel_resolution':int(o.data.bevel_resolution),'points':[{'co':list(p.co),'handle_left':list(p.handle_left),'handle_right':list(p.handle_right),'handle_left_type':p.handle_left_type,'handle_right_type':p.handle_right_type,'radius':float(p.radius),'tilt':float(p.tilt)} for p in sp.bezier_points]},separators=(',',':'))

def sample_curve(o):
 bp=o.data.splines[0].bezier_points; pts=[]; rs=[]
 for i in range(len(bp)-1):
  a,b=bp[i],bp[i+1]
  for j in range(STEPS):
   t=j/STEPS; pts.append(bez(a.co,a.handle_right,b.handle_left,b.co,t)); rs.append(float(a.radius)*(1-t)+float(b.radius)*t)
 pts.append(bp[-1].co.copy()); rs.append(float(bp[-1].radius)); return pts,rs

def build_mesh(name,path,rs,d,w,h):
 n=len(PROFILE); vs=[]; fs=[]; prev_lat=None
 for i,p in enumerate(path):
  prev=path[max(0,i-1)]; nxt=path[min(len(path)-1,i+1)]; tan=nxt-prev
  if tan.length<1e-9: tan=Vector((1,0,0))
  tan.normalize()
  if prev_lat is None:
   lat=tan.cross(Vector((0,0,1))); lat=lat if lat.length>=1e-6 else tan.cross(Vector((1,0,0)))
  else:
   lat=prev_lat-tan*prev_lat.dot(tan); lat=lat if lat.length>=1e-6 else tan.cross(Vector((0,0,1)))
  lat.normalize(); vert=lat.cross(tan).normalized(); prev_lat=lat
  for x,y in PROFILE: vs.append(tuple(p+lat*(x*d*w*rs[i])+vert*(y*d*h*rs[i])))
 rings=len(path)
 for r in range(rings-1):
  for k in range(n): fs.append((r*n+k,r*n+(k+1)%n,(r+1)*n+(k+1)%n,(r+1)*n+k))
 fs.append(tuple(range(n-1,-1,-1))); off=(rings-1)*n; fs.append(tuple(off+k for k in range(n)))
 me=bpy.data.meshes.new(name+'_R18_MESH'); me.from_pydata(vs,[],fs); me.update(); return me

def replace_curve(name,s):
 src=bpy.data.objects.get(name)
 if src is None or src.type!='CURVE' or src.data.bevel_mode!='ROUND': raise RuntimeError('Expected R16 curve '+name)
 source=serialize_curve(src); path,rs=sample_curve(src); me=build_mesh(name,path,rs,s['depth'],s['width'],s['height']); cols=list(src.users_collection); matrix=src.matrix_world.copy(); parent=src.parent; props={k:src[k] for k in src.keys()}; mats=[m for m in src.data.materials]; hr=src.hide_render; hv=src.hide_viewport
 new=bpy.data.objects.new(name+'__R18_TMP',me)
 for c in cols: c.objects.link(new)
 new.parent=parent; new.matrix_world=matrix; new.hide_render=hr; new.hide_viewport=hv
 for k,v in props.items(): new[k]=v
 for m in mats: me.materials.append(m)
 for p in me.polygons: p.use_smooth=True
 new['macro_root_xsec_contract']=CONTRACT; new['macro_root_profile_family']='BILATERAL_FLATTENED_LOAD_SECTION_V1'; new['macro_root_profile_region']=s['region']; new['macro_root_cross_section_status']='R18_SELF_CONTAINED_STRUCTURAL_MESH'; new['r17_source_curve_json']=source; new['r18_mesh_rings']=len(path); new['r18_profile_vertices']=len(PROFILE); new['r18_centerline_sample_steps_per_segment']=STEPS; new['r18_width_factor']=s['width']; new['r18_height_factor']=s['height']; new['r18_base_depth_m']=s['depth']; new['r18_source_taper_preserved']=True; new['macro_root_xsec_source_wave']='R18_PROMOTION'
 old=src.data; bpy.data.objects.remove(src,do_unlink=True); new.name=name
 if old.users==0: bpy.data.curves.remove(old)
 return {'name':name,'verts':len(me.vertices),'faces':len(me.polygons),'stream_cells':new.get('stream_cells')}

root=bpy.data.objects.get('SYLVA_WORLD_ROOT')
if not root or root.get('build_status')!='WAVE1O_R17_SELF_CONTAINED_ROOT_XSEC_AB': raise RuntimeError('Expected accepted R17 AB input')
for n in ['SYLVA_ROOT_PRIMARY_R01','SYLVA_ROOT_PRIMARY_R03']:
 o=bpy.data.objects.get(n)
 if not o or o.type!='MESH' or o.get('macro_root_xsec_contract')!='SYLVA_MACRO_ROOT_XSEC_R17_MESH_AB': raise RuntimeError('Missing R17 accepted mesh '+n)
 o['macro_root_xsec_contract']=CONTRACT; o['macro_root_xsec_source_wave']='R17_AB_VALIDATED'; o['macro_root_cross_section_status']='R18_SELF_CONTAINED_STRUCTURAL_MESH'
changed=[replace_curve(n,s) for n,s in TARGETS.items()]
root['macro_root_xsec_contract']=CONTRACT; root['macro_root_xsec_experiment_targets']=''; root['macro_root_xsec_all_primary_roots']=True; root['build_status']='WAVE1P_R18_ALL_PRIMARY_ROOT_XSEC_MESH'; bpy.context.view_layer.update(); bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
result={'status':'R18_ALL_PRIMARY_ROOT_XSEC_MESH','contract':CONTRACT,'promoted':changed,'all_roots':['SYLVA_ROOT_PRIMARY_R01','SYLVA_ROOT_PRIMARY_R02','SYLVA_ROOT_PRIMARY_R03','SYLVA_ROOT_PRIMARY_R04','SYLVA_ROOT_PRIMARY_R05','SYLVA_ROOT_PRIMARY_R06'],'helper_objects_required':False}
