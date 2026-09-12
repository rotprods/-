"""EXOVANT Terra: original editable asset study. Run in Blender 5.2.

Metres, Z up. Deterministic geometry and packed PBR maps; no network/assets.
This is a production candidate, not a human-approved shipping asset.
"""
import bpy, math, random
import numpy as np
from mathutils import Vector

random.seed(2950)
S=bpy.context.scene
S.unit_settings.system='METRIC'; S.unit_settings.scale_length=1.0
S.render.engine='BLENDER_EEVEE'
S.render.resolution_x=1200; S.render.resolution_y=850; S.render.resolution_percentage=100
S.render.fps=24; S.frame_start=1; S.frame_end=1
S.world=bpy.data.worlds.new('Terra_overcast_ambient') if not S.world else S.world
S.world.use_nodes=True
S.world.node_tree.nodes['Background'].inputs['Color'].default_value=(0.11,0.16,0.19,1)
S.world.node_tree.nodes['Background'].inputs['Strength'].default_value=0.38
S.view_settings.view_transform='Khronos PBR Neutral'
S['project']='EXOVANT 2950'; S['run_id']='EXO-006-ART-001'
S['quality_status']='ART_CANDIDATE_REQUIRES_HUMAN_AND_TARGET_GPU_REVIEW'
S['scale']='metres; each asset root is an assembly pivot; detail is not a quality gate'

def collection(name):
 c=bpy.data.collections.new(name); S.collection.children.link(c); return c
C=collection('EXO_TERRA_KIT_EDITABLE'); P=collection('PRESENTATION'); COLL=collection('COLLISION_PROXIES')
COLL.hide_render=True; COLL.hide_viewport=True
def root(name,loc=(0,0,0)):
 o=bpy.data.objects.new(name,None); C.objects.link(o); o.location=loc
 o['asset_id']=name; o['status']='candidate'; return o

# Packed tileable texture maps are the same inputs in Blender and glTF.
# Directional abrasion, mineral pitting and broad oxidation are material families,
# not generated-image replacements for geometry. Per-edge wear remains a later bake.
def pbr(name,color,metal,rough,kind,seed):
 m=bpy.data.materials.new(name); m.use_nodes=True
 m.diffuse_color=(*color,1); m.metallic=metal; m.roughness=rough
 nt=m.node_tree; bs=nt.nodes.get('Principled BSDF')
 bs.inputs['Metallic'].default_value=metal
 bs.inputs['Roughness'].default_value=rough
 n=512; rng=np.random.default_rng(seed)
 y,x=np.mgrid[0:n,0:n]/n
 coarse=(np.sin(x*math.tau*3+np.sin(y*math.tau*2)) + np.cos(y*math.tau*5+x*math.tau))/2
 micro=rng.normal(0,1,(n,n)); pits=(rng.random((n,n))>0.985).astype(float)
 stripes=np.sin(y*math.tau*93)*0.05
 height=coarse*0.12+micro*0.045-pits*0.28
 if kind=='bronze':
  patina=np.clip(coarse*0.7-0.05,0,0.65)
  rgb=np.asarray(color)[None,None,:]*(0.78+0.22*coarse[:,:,None])+micro[:,:,None]*0.012
  rgb=rgb*(1-patina[:,:,None])+np.array([0.07,0.19,0.16])*patina[:,:,None]
  roughmap=np.clip(rough+patina*.45+micro*.025,.12,.94)
 elif kind=='stone':
  rgb=np.asarray(color)[None,None,:]*(0.88+coarse[:,:,None]*.22)+micro[:,:,None]*.018
  rgb-=pits[:,:,None]*.06; roughmap=np.clip(rough+coarse*.06,.35,.98)
 elif kind=='ceramic':
  rgb=np.asarray(color)[None,None,:]*(.95+coarse[:,:,None]*.07)+micro[:,:,None]*.008
  roughmap=np.clip(rough+coarse*.08+stripes,.16,.75)
 else:
  rgb=np.asarray(color)[None,None,:]*(.90+coarse[:,:,None]*.1)+stripes[:,:,None]*.03
  roughmap=np.clip(rough+micro*.02,.12,.94)
 dx=(np.roll(height,-1,1)-np.roll(height,1,1))*.7
 dy=(np.roll(height,-1,0)-np.roll(height,1,0))*.7
 normal=np.stack([-dx,-dy,np.ones_like(dx)],-1);normal/=np.linalg.norm(normal,axis=-1,keepdims=True)
 def tex(suffix,arr,noncolor=False):
  im=bpy.data.images.new(name+'_'+suffix,width=n,height=n,alpha=True)
  im.colorspace_settings.name='Non-Color' if noncolor else 'sRGB'
  rgba=np.ones((n,n,4),np.float32);rgba[:,:,:3]=np.clip(arr,0,1)
  im.pixels.foreach_set(rgba.ravel());im.pack()
  node=nt.nodes.new('ShaderNodeTexImage');node.image=im;node.label=suffix;return node
 base=tex('BaseColor',rgb);nt.links.new(base.outputs['Color'],bs.inputs['Base Color'])
 r=tex('Roughness',np.repeat(roughmap[:,:,None],3,axis=2),True);nt.links.new(r.outputs['Color'],bs.inputs['Roughness'])
 norm=tex('Normal',(normal+1)/2,True);nm=nt.nodes.new('ShaderNodeNormalMap');nm.inputs['Strength'].default_value=.30
 nt.links.new(norm.outputs['Color'],nm.inputs['Color']);nt.links.new(nm.outputs['Normal'],bs.inputs['Normal'])
 return m

M={
 'stone':pbr('MAT_MarineBasalt',(0.19,0.22,0.22),0,.78,'stone',1),
 'ceramic':pbr('MAT_IvorySaltCeramic',(0.66,0.69,0.58),0,.30,'ceramic',2),
 'bronze':pbr('MAT_RepairedBronze',(0.38,0.23,0.095),.82,.36,'bronze',3),
 'dark':pbr('MAT_GraphiteSteel',(0.055,0.07,0.073),.72,.34,'steel',4),
}
def flat(name,color,metal=0,rough=.5,emission=0):
 m=bpy.data.materials.new(name);m.use_nodes=True;m.diffuse_color=(*color,1)
 bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(*color,1)
 bs.inputs['Metallic'].default_value=metal;bs.inputs['Roughness'].default_value=rough
 if emission:bs.inputs['Emission Color'].default_value=(*color,1);bs.inputs['Emission Strength'].default_value=emission
 return m
M['jade']=flat('MAT_BioelectricJade',(.09,.65,.39),.12,.25,2.0)
M['amber']=flat('MAT_ServiceAmber',(.9,.26,.025),.1,.28,1.5)
M['moss']=flat('MAT_SaltMoss',(.10,.17,.057),0,.92)
M['root']=flat('MAT_RootBark',(.115,.13,.065),0,.95)

# Accumulate disconnected editable components per asset/material to bound draw calls.
G={}
def geom(parent,mat,verts,faces):
 key=(parent.name,mat)
 if key not in G:G[key]=[parent,[],[]]
 g=G[key];i=len(g[1]);g[1].extend(verts);g[2].extend([tuple(i+k for k in f) for f in faces])
def box(parent,mat,center,dim,rot=0):
 x,y,z=center; a,b,c=[v/2 for v in dim];co=math.cos(rot);si=math.sin(rot)
 vv=[(x+u*co-v*si,y+u*si+v*co,z+w) for u,v,w in [(-a,-b,-c),(a,-b,-c),(a,b,-c),(-a,b,-c),(-a,-b,c),(a,-b,c),(a,b,c),(-a,b,c)]]
 geom(parent,mat,vv,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)])
def lathe(parent,mat,center,profile,n=48):
 x,y,z=center;v=[]
 for r,h in profile:
  v.extend([(x+r*math.cos(i*math.tau/n),y+r*math.sin(i*math.tau/n),z+h) for i in range(n)])
 f=[]
 for j in range(len(profile)-1):
  for i in range(n):k=j*n+i; q=j*n+(i+1)%n; f.append((k,q,q+n,k+n))
 f.extend([tuple(range(n-1,-1,-1)),tuple((len(profile)-1)*n+i for i in range(n))]);geom(parent,mat,v,f)
def tube(parent,mat,points,r=.04,sides=10):
 v=[]
 for j,p in enumerate(points):
  tang=Vector(points[min(j+1,len(points)-1)])-Vector(points[max(j-1,0)])
  tang.normalize();ref=Vector((0,0,1)) if abs(tang.z)<.9 else Vector((1,0,0))
  a=tang.cross(ref).normalized();b=tang.cross(a).normalized()
  for i in range(sides):v.append(tuple(Vector(p)+r*(math.cos(i*math.tau/sides)*a+math.sin(i*math.tau/sides)*b)))
 f=[]
 for j in range(len(points)-1):
  for i in range(sides):f.append((j*sides+i,j*sides+(i+1)%sides,(j+1)*sides+(i+1)%sides,(j+1)*sides+i))
 f.extend([tuple(range(sides-1,-1,-1)),tuple((len(points)-1)*sides+i for i in range(sides))]);geom(parent,mat,v,f)
def ring(parent,mat,center,r,t=.035,plane='XY',a0=0,a1=math.tau,n=64):
 x,y,z=center
 if plane=='XZ':pts=[(x+r*math.cos(a),y,z+r*math.sin(a)) for a in np.linspace(a0,a1,n)]
 else:pts=[(x+r*math.cos(a),y+r*math.sin(a),z) for a in np.linspace(a0,a1,n)]
 tube(parent,mat,pts,t,10)

floor=root('ENV_TERRA_Foundation_10x8')
box(floor,'dark',(0,0,-.26),(10,8,.4))
for i in range(10):
 for j in range(8):
  mat='ceramic' if (i in (0,9) or j==7) else 'stone'
  box(floor,mat,(i-4.5,j-3.5,-.065),(.975,.975,.17))
for x in (-2.0,2.0):
 box(floor,'bronze',(x,-.1,.035),(.035,7.3,.018))
for j in range(3):box(floor,'stone',(0,-4.2-j*.28,-.18-j*.16),(4.2,.38,.30))
for x in (-4.7,4.7):
 for j in range(22):box(floor,'dark',(x,-3.5+j*.32,.035),(.22,.11,.03))

back=root('ENV_TERRA_SluiceWall_8x4',(0,2.9,0))
for x in (-3,-1,1,3):
 box(back,'stone',(x,0,1.9),(1.97,.38,3.8))
 box(back,'ceramic',(x,-.235,2.2),(1.72,.12,2.9))
 for k in range(5):box(back,'bronze',(x-.65+k*.32,-.32,2.5),(.018,.035,2.1))
box(back,'dark',(0,-.24,.42),(8,.2,.48))
for x in np.linspace(-3.8,3.8,32):box(back,'bronze',(float(x),-.36,.42),(.08,.06,.30))
box(back,'bronze',(0,0,3.88),(8.4,.65,.16))

for side in (-1,1):
 col=root('ENV_TERRA_RibPilaster_'+('L' if side<0 else 'R'),(side*3.4,1.05,0))
 box(col,'stone',(0,0,.23),(1.18,1.15,.46));box(col,'bronze',(0,0,.48),(1.07,1.02,.08))
 box(col,'dark',(0,0,2.03),(.64,.65,3.0))
 for k in (-1,0,1):
  box(col,'ceramic',(k*.25,-.34,2.04),(.22,.30,2.98))
  box(col,'bronze',(k*.25,-.515,2.07),(.032,.04,2.92))
 for z in (.69,1.9,3.48):box(col,'bronze',(0,0,z),(.97,.99,.10))
 box(col,'ceramic',(0,0,3.69),(1.14,1.13,.29))
 # load-bearing curved ribs from pilaster toward upper central keystone
 pts=[(side*(-.0-2.45*t),.20,3.72+1.05*math.sin(t*math.pi/2)) for t in np.linspace(0,1,28)]
 tube(col,'ceramic',pts,.19,12)
 tube(col,'bronze',[(x,y-.205,z+.04) for x,y,z in pts],.035,8)
 for z in (.67,3.46):
  for x in (-.36,.36):lathe(col,'dark',(x,-.34,z),[(.054,0),(.054,.07)],8)

header=root('ENV_TERRA_CrownSpine',(0,1.35,4.73))
box(header,'dark',(0,0,0),(2.4,.65,.23));box(header,'bronze',(0,-.15,.1),(2.5,.64,.055))
for x in np.linspace(-1.08,1.08,13):box(header,'ceramic',(float(x),-.39,0),(.13,.16,.34))
ring(header,'bronze',(0,-.50,.12),.32,.035,'XZ')

pump=root('PR_TERRA_ResonanceRegulator',(0,0,0))
pump['interaction']='valve socket local (0,-0.75,1.08); no behavior embedded'
pump['catalog_refs']='MINI_terra; KIT_terra; PROPS_terra'
lathe(pump,'stone',(0,0,0),[(1.12,0),(1.12,.12),(.97,.22),(.97,.32)],64)
lathe(pump,'bronze',(0,0,0),[(.83,.3),(.83,.4),(.64,.47),(.60,.53)],64)
lathe(pump,'dark',(0,0,0),[(.51,.43),(.51,2.7),(.46,2.78)],64)
for z in (.52,.64,1.36,2.12,2.68):
 lathe(pump,'bronze',(0,0,0),[(.61,z),(.63,z+.025),(.63,z+.10),(.61,z+.125)],64)
for i in range(12):
 a=i*math.tau/12
 x,y=.52*math.cos(a),.52*math.sin(a)
 lathe(pump,'ceramic',(x,y,0),[(.105,.77),(.14,.84),(.14,1.21),(.105,1.3)],16)
 tube(pump,'bronze',[(x*1.10,y*1.10,.72),(x*1.13,y*1.13,2.48)],.022,8)
 if i%2==0:lathe(pump,'jade',(x,y,0),[(.04,1.6),(.055,1.65),(.055,1.97),(.04,2.02)],12)
lathe(pump,'ceramic',(0,0,0),[(.38,2.76),(.47,2.83),(.45,2.98),(.3,3.10),(.19,3.16)],64)
lathe(pump,'bronze',(0,0,0),[(.23,3.13),(.23,3.19),(.10,3.22)],48)
# Isolated valve wheel: full ring, spokes, visible stop and grip.
ring(pump,'bronze',(0,-.77,1.08),.29,.032,'XZ')
for a in np.linspace(0,math.tau,6,endpoint=False):
 tube(pump,'dark',[(0,-.77,1.08),(.27*math.cos(a),-.77,1.08+.27*math.sin(a))],.021,8)
tube(pump,'bronze',[(0,-.45,1.08),(0,-.86,1.08)],.055,16)
tube(pump,'amber',[(.20,-.77,.875),(.20,-.9,.875)],.037,12)
for side in (-1,1):
 pts=[(side*.45,.18,2.36),(side*.88,.18,2.36),(side*1.02,.18,2.15),(side*1.02,.18,.50),(side*1.26,.18,.22),(side*1.62,.18,.22)]
 tube(pump,'bronze',pts,.11,16)
 for z in (.72,1.95):
  lathe(pump,'dark',(side*1.02,.18,z),[(.15,0),(.15,.12)],16)

console=root('PR_TERRA_ServiceConsole',(2.45,-1.6,0))
box(console,'stone',(0,0,.12),(1.0,.85,.24))
box(console,'dark',(0,0,.58),(.55,.55,.75))
box(console,'ceramic',(0,0,1.04),(1.0,.7,.24))
box(console,'bronze',(0,-.37,1.02),(.92,.055,.18))
box(console,'dark',(0,0,1.175),(.73,.48,.035))
for i in range(3):
 box(console,'jade',(-.22+i*.22,-.04,1.2),(.11,.21,.012))
 lathe(console,'bronze',(-.26+i*.26,-.24,1.175),[(.045,0),(.045,.032)],12)
for x in (-.38,.38):box(console,'bronze',(x,0,.67),(.033,.63,.5))

archive=root('PR_TERRA_ArchiveCradle',(-2.6,-1.55,0))
box(archive,'dark',(0,0,.14),(1.5,.8,.28));box(archive,'bronze',(0,0,.3),(1.48,.78,.065))
for i in (-1,0,1):
 x=i*.43
 lathe(archive,'dark',(x,0,0),[(.18,.34),(.18,1.26)],32)
 lathe(archive,'ceramic',(x,0,0),[(.16,.45),(.185,.5),(.185,1.05),(.16,1.10)],32)
 for z in (.39,1.15):lathe(archive,'bronze',(x,0,z),[(.20,0),(.20,.08)],32)
 box(archive,'jade',(x,-.18,.76),(.045,.032,.43))
 for y in (-.12,.12):tube(archive,'bronze',[(x,y,1.23),(x,y,1.36)],.023,8)
 tube(archive,'bronze',[(x,-.12,1.36),(x,.12,1.36)],.023,8)

pipe=root('KIT_TERRA_SupplyPipe_3m',(-3.4,1.6,0))
tube(pipe,'dark',[(0,0,.3),(0,1,.3),(0,1.1,.45),(0,1.1,2.9)],.115,16)
for z in (.65,1.4,2.5):lathe(pipe,'bronze',(0,1.1,z),[(.18,0),(.18,.10)],24)

bio=root('BIO_TERRA_WitnessRoots')
for side in (-1,1):
 for k in range(4):
  pts=[]
  for t in np.linspace(0,1,18):pts.append((side*(3.25-.26*math.sin(t*8+k)),1.30-.9*t+.1*math.sin(t*17+k),3.7*(1-t)**1.5+.08))
  tube(bio,'root',pts,.022+k*.009,8)
 for k in range(12):
  x=side*(3.2+random.uniform(-.5,.4));y=random.uniform(.5,1.9)
  lathe(bio,'moss',(x,y,.025),[(.08,0),(.11,.025),(.06,.05)],7)

def build_meshes():
 for (name,mat),(parent,v,f) in G.items():
  me=bpy.data.meshes.new(name+'_'+mat+'_mesh');me.from_pydata(v,[],f);me.update()
  o=bpy.data.objects.new(name+'__'+mat,me);C.objects.link(o);o.parent=parent
  me.materials.append(M[mat]);o['material_role']=mat
  # Box-projected metre UVs on dominant face axes, preserving tiled physical scale.
  uv=me.uv_layers.new(name='UV_MetreTile')
  for poly in me.polygons:
   n=poly.normal;axis=max(range(3),key=lambda a:abs(n[a]))
   axes=((1,2),(0,2),(0,1))[axis]
   for li in poly.loop_indices:
    co=me.vertices[me.loops[li].vertex_index].co;uv.data[li].uv=(co[axes[0]],co[axes[1]])
   poly.use_smooth=False
  if mat not in ('root','moss','jade','amber'):
   bevel=o.modifiers.new('Machined_edges_editable','BEVEL');bevel.width=.009 if mat in ('bronze','dark') else .015;bevel.segments=2;bevel.limit_method='ANGLE'
   normal=o.modifiers.new('Weighted_corner_normals','WEIGHTED_NORMAL');normal.keep_sharp=True;normal.weight=30
  o['uv_note']='1 texture repeat/metre, 512 px/metre nominal; per-asset bake/UV2 pending'
build_meshes()

def camera(name,pos,target,lens):
 d=bpy.data.cameras.new(name);o=bpy.data.objects.new(name,d);P.objects.link(o);o.location=pos
 o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();d.lens=lens;d.clip_end=200;return o
S.camera=camera('CAM_Delivery',(10,-14,9),(0,.0,1.85),47)
camera('CAM_Player',(0,-5.8,1.7),(0,.4,1.5),32)
camera('CAM_Closeup',(3.4,-4.6,2.8),(0,0,1.6),60)
def light(name,pos,power,color,size=1):
 d=bpy.data.lights.new(name,'SPOT');o=bpy.data.objects.new(name,d);P.objects.link(o);o.location=pos;d.energy=power;d.color=color;d.spot_size=math.radians(120);d.spot_blend=.7;d.shadow_soft_size=size*.3
 o.rotation_euler=(Vector((0,0,1.5))-o.location).to_track_quat('-Z','Y').to_euler()
 # Blender lighting rig remains editable. Runtime lights supplied by target scene.
light('KEY_Overcast',(-4,-4,9),1800,(.77,.89,1.0),7)
light('FILL_Bounce',(5,-2,4),1000,(1,.75,.44),5)
light('RIM_Skylight',(1,4,7),2200,(.53,.80,.75),4)
# Ground/collision kept separate from exported render geometry; neutral gray studio.
me=bpy.data.meshes.new('Studio_ground');me.from_pydata([(-200,-200,-.85),(200,-200,-.85),(200,200,-.85),(-200,200,-.85)],[],[(0,1,2,3)]);me.update()
o=bpy.data.objects.new('PRESENTATION_Ground',me);P.objects.link(o);me.materials.append(flat('MAT_StudioGround',(.035,.052,.057),0,.92))
S['kit_assets']=[o.name for o in C.objects if o.type=='EMPTY']
result={'objects':len(bpy.data.objects),'asset_roots':S['kit_assets'][:], 'materials':len(bpy.data.materials),'packed_maps':len(bpy.data.images),'editable_meshes':len(bpy.data.meshes),'scope':'Terra asset candidate; runtime integration and human art approval pending'}
