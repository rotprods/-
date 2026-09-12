"""Revision 3: contact repair and readable functional wear/detail after render review."""
import bpy, math
from mathutils import Vector
s=bpy.context.scene;c=bpy.data.collections['EXO_TERRA_KIT_EDITABLE']
for o in list(c.objects):
 if o.type=='MESH' and not o.data.vertices:bpy.data.objects.remove(o,do_unlink=True)
for v in bpy.data.objects['ENV_TERRA_Foundation_10x8__dark'].data.vertices:
 if v.co.z<-.4:v.co.z=-.65
ground=bpy.data.objects['PRESENTATION_Ground']
for v in ground.data.vertices:v.co.z=-.65

G={}
def add(parent,material,verts,faces):
 key=(parent.name,material)
 if key not in G:G[key]=[parent,[],[]]
 g=G[key];n=len(g[1]);g[1].extend(verts);g[2].extend([tuple(n+i for i in f) for f in faces])
def box(p,m,loc,d):
 x,y,z=loc;a,b,h=[k/2 for k in d]
 v=[(x+u,y+w,z+t) for u,w,t in [(-a,-b,-h),(a,-b,-h),(a,b,-h),(-a,b,-h),(-a,-b,h),(a,-b,h),(a,b,h),(-a,b,h)]]
 add(p,m,v,[(0,3,2,1),(4,5,6,7),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)])
def disc(p,m,loc,r,depth,n=48):
 x,y,z=loc;v=[]
 for dy in (0,depth):v.extend([(x+r*math.cos(i*math.tau/n),y+dy,z+r*math.sin(i*math.tau/n)) for i in range(n)])
 f=[tuple(range(n)),tuple(n+i for i in range(n-1,-1,-1))]
 for i in range(n):f.append((i,(i+1)%n,(i+1)%n+n,i+n))
 add(p,m,v,f)
def stroke(p,m,start,end,width):
 a=Vector(start);b=Vector(end);d=b-a;side=Vector((-d.z,0,d.x)).normalized()*width/2
 v=[tuple(a-side),tuple(a+side),tuple(b+side),tuple(b-side)]
 add(p,m,v,[(0,1,2,3)])
p=bpy.data.objects['PR_TERRA_ResonanceRegulator']
disc(p,'MAT_RepairedBronze',(0,-.655,1.98),.245,.105)
disc(p,'MAT_GraphiteSteel',(0,-.674,1.98),.220,.025)
disc(p,'MAT_IvorySaltCeramic',(0,-.68,1.98),.202,.008)
for i in range(17):
 a=math.radians(210-i*15)
 stroke(p,'MAT_GraphiteSteel',(.168*math.cos(a),-.691,1.98+.168*math.sin(a)),((.14 if i%4==0 else .154)*math.cos(a),-.691,1.98+(.14 if i%4==0 else .154)*math.sin(a)),.009 if i%4==0 else .005)
stroke(p,'MAT_GraphiteSteel',(-.026,-.70,1.947),(.115,-.70,2.083),.016)
disc(p,'MAT_RepairedBronze',(0,-.709,1.98),.026,.02,16)
for x,z in [(-.30,1.48),(.30,1.48),(-.30,2.51),(.30,2.51)]:disc(p,'MAT_RepairedBronze',(x,-.53,z),.045,.032,6)
box(p,'MAT_RepairedBronze',(0,-.566,1.47),(.43,.045,.14))
# Physical serial marks and functional arrow; not illegible pseudo-text.
for i in range(9):box(p,'MAT_GraphiteSteel',(-.16+i*.038,-.593,1.47),(.012 if i%3 else .024,.008,.075))
stroke(p,'MAT_GraphiteSteel',(-.05,-.598,1.68),(.05,-.598,1.68),.015)
stroke(p,'MAT_GraphiteSteel',(.05,-.598,1.68),(.015,-.598,1.713),.015)
stroke(p,'MAT_GraphiteSteel',(.05,-.598,1.68),(.015,-.598,1.647),.015)

wall=bpy.data.objects['ENV_TERRA_SluiceWall_8x4']
for x,z,w,h in [(-2.45,.93,.48,.22),(1.43,2.94,.29,.36),(3.43,1.26,.42,.20)]:
 box(wall,'MAT_RepairedBronze',(x,-.327,z),(w,.025,h))
 for sx in (-1,1):
  for sz in (-1,1):disc(wall,'MAT_GraphiteSteel',(x+sx*w*.35,-.35,z+sz*h*.27),.018,.02,6)
# Localized ceramic cracks constrained to individual panels, grounded in gravity.
for x,z in [(-2.7,1.3),(1.65,2.5),(3.25,.9)]:
 pts=[(x,-.301,z),(x+.04,-.301,z-.12),(x+.025,-.301,z-.18),(x+.08,-.301,z-.26)]
 for a,b in zip(pts,pts[1:]):stroke(wall,'MAT_GraphiteSteel',a,b,.006)
for (parent,mat),(root,verts,faces) in G.items():
 me=bpy.data.meshes.new(parent+'_Detail_'+mat);me.from_pydata(verts,[],faces);me.update()
 o=bpy.data.objects.new(parent+'__detail_'+mat,me);c.objects.link(o);o.parent=root;me.materials.append(bpy.data.materials[mat])
 uv=me.uv_layers.new(name='UV_MetreTile')
 for f in me.polygons:
  axes=((1,2),(0,2),(0,1))[max(range(3),key=lambda k:abs(f.normal[k]))]
  for li in f.loop_indices:
   v=me.vertices[me.loops[li].vertex_index].co;uv.data[li].uv=(v[axes[0]],v[axes[1]])
 bevel=o.modifiers.new('Service_edge_bevel','BEVEL');bevel.width=.002;bevel.segments=2
 o.modifiers.new('Weighted_normals','WEIGHTED_NORMAL')
s['visual_review']='r2 Eevee inspected: fix podium ground contact, remove empty export node, add localized repairs and readable pressure gauge. Human AAA review remains pending.'
result={'objects':len(bpy.data.objects),'revision_scope':'3','presentation_ground_z':-.65,'functional_details':['pressure gauge','service serial marks','repair plates','local ceramic cracks'],'empty_meshes':[o.name for o in c.objects if o.type=='MESH' and not o.data.vertices]}
