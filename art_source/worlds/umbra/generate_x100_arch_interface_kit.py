"""Generate the UMBRA X100 architectural-interface catalog.

Input checkpoint: X100_DAMAGE_STATES_FOUNDATION_001.
Output checkpoint: X100_ARCH_INTERFACE_KIT_QA_FIXED_001.

The kit is a reversible production proposal: 10 families × S/M/L ×
STANDARD/WIND_SHIELDED/FIELD_MODIFIED on a 0.2 m interface grid. It does not
implement runtime traversal, collision, LOD budgets, final UV/PBR or hidden
underground infrastructure.
"""
import bpy, bmesh, math
from mathutils import Vector, Matrix

scene=bpy.context.scene
terrain=bpy.data.objects['ENV_TERRAIN_TWILIGHT_BAND_BLOCKOUT']
world=bpy.data.collections['W04_UMBRA']
FAMILIES=['ACCESS_DOOR','SERVICE_HATCH','LADDER','PLATFORM','HANDRAIL','GANTRY_FRAME','BRIDGE_DECK','CABLE_GLAND','CONDUIT_JUNCTION','ACCESS_CANOPY']


def ensure(parent,name):
    c=bpy.data.collections.get(name) or bpy.data.collections.new(name)
    if c.name not in [x.name for x in parent.children]: parent.children.link(c)
    return c

C=ensure(world,'86_X100_ARCH_INTERFACE_KIT')
sub={f:ensure(C,'87_X100_ARCH_'+f) for f in FAMILIES}
mats={'metal':bpy.data.materials['MAT_SINSOL_DARK_METAL'],'ivory':bpy.data.materials['MAT_COLONIAL_IVORY_REPAIR'],'fabric':bpy.data.materials['MAT_SINSOL_TENSION_FABRIC'],'gasket':bpy.data.materials['MAT_SINSOL_GASKET'],'amber':bpy.data.materials['MAT_REFUGE_AMBER']}
box_cache={};cyl_cache={}

def box_mesh(dims,mat):
    k=(tuple(round(float(x),4) for x in dims),mat.name)
    if k in box_cache:return box_cache[k]
    me=bpy.data.meshes.new('MESH_X100A_BOX_'+str(len(box_cache)).zfill(3));bm=bmesh.new();bmesh.ops.create_cube(bm,size=1);bm.transform(Matrix.Diagonal((dims[0],dims[1],dims[2],1)));bm.to_mesh(me);bm.free();me.materials.append(mat);box_cache[k]=me;return me

def cyl_mesh(r,d,mat,v=10):
    k=(round(r,4),round(d,4),mat.name,v)
    if k in cyl_cache:return cyl_cache[k]
    me=bpy.data.meshes.new('MESH_X100A_CYL_'+str(len(cyl_cache)).zfill(3));bm=bmesh.new();bmesh.ops.create_cone(bm,cap_ends=True,segments=v,radius1=r,radius2=r,depth=d);bm.to_mesh(me);bm.free();me.materials.append(mat);cyl_cache[k]=me;return me

def add(name,me,col,parent,loc=(0,0,0),rot=(0,0,0)):
    o=bpy.data.objects.new(name,me);col.objects.link(o);o.parent=parent;o.location=loc;o.rotation_euler=rot;return o

def box(name,dims,mat,col,parent,loc=(0,0,0),rot=(0,0,0)):return add(name,box_mesh(dims,mat),col,parent,loc,rot)
def cyl(name,r,d,mat,col,parent,loc=(0,0,0),rot=(0,0,0),v=10):return add(name,cyl_mesh(r,d,mat,v),col,parent,loc,rot)
def rod(name,a,b,r,mat,col,parent,v=8):
    a,b=Vector(a),Vector(b);vec=b-a;o=cyl(name,r,vec.length,mat,col,parent,(a+b)*.5,v=v);o.rotation_euler=vec.to_track_quat('Z','Y').to_euler();return o

def tz(x,y):
    inv=terrain.matrix_world.inverted();origin=inv@Vector((x,y,220));direction=(inv.to_3x3()@Vector((0,0,-1))).normalized();hit,loc,_n,_i=terrain.ray_cast(origin,direction,distance=600)
    if not hit:raise RuntimeError((x,y))
    return (terrain.matrix_world@loc).z

def make_root(fam,size,variant,idx,x,y):
    e=bpy.data.objects.new(f'X100A_{fam}_{size}_{variant}_{idx:02d}',None);sub[fam].objects.link(e);e.location=(x,y,tz(x,y)+.03)
    e['stable_id']=f'W04-X100A-{fam}-{size}-{variant}-{idx:02d}';e['family']=fam;e['size_variant']=size;e['fabrication_variant']=variant;e['snap_grid_m']=.2;e['epistemic']='PRODUCTION_PROPOSAL_WITHIN_WORLD_OWNER';e['lod_strategy']='LOD0 authored; LOD1/2 pending target contract';e['collision_strategy']='simple primitives/convex pending integration';e['interface_schema']='0.2m grid; protected service interfaces';return e

def variant(r,var,col,w,h):
    if var=='WIND_SHIELDED':
        box(r.name+'_WIND_SHIELD',(w,.10,h),mats['fabric'],col,r,(0,.30,max(.55,h*.5)),(math.radians(-5),0,0));r['variation_cause']='persistent lateral wind / exposed access'
    elif var=='FIELD_MODIFIED':
        box(r.name+'_REPAIR_PLATE',(.7*w,.10,.28*h),mats['ivory'],col,r,(.12*w,-.30,max(.35,h*.45)),(0,0,math.radians(6)));rod(r.name+'_FIELD_BRACE',(-.4*w,-.26,.10),(.4*w,-.26,.55*h),.045,mats['ivory'],col,r,8);r['variation_cause']='field reinforcement / replacement structure'
    else:r['variation_cause']='standardized fabrication'

def door(r,s,var,c):
    w,h={.78:(1.2,2.2),1.0:(1.6,2.4),1.28:(2.2,2.8)}[s];t=.16
    box(r.name+'_JAMB_L',(t,.22,h+.18),mats['metal'],c,r,(-(w+t)/2,0,(h+.18)/2));box(r.name+'_JAMB_R',(t,.22,h+.18),mats['metal'],c,r,((w+t)/2,0,(h+.18)/2));box(r.name+'_HEADER',(w+2*t,.22,t),mats['metal'],c,r,(0,0,h+.10));box(r.name+'_SILL',(w+2*t,.30,.08),mats['ivory'],c,r,(0,0,.04));box(r.name+'_LEAF',(w-.08,.12,h-.10),mats['metal'],c,r,(0,.06,h/2+.04));cyl(r.name+'_HANDLE',.055,.16,mats['ivory'],c,r,(w*.32,-.08,h*.48),(math.radians(90),0,0),10);variant(r,var,c,w,h*.55);r['semantic_purpose']='human-scale protected access door';r['clearance_width_m']=w;r['clearance_height_m']=h

def hatch(r,s,var,c):
    w,h={.78:(.9,1.0),1.0:(1.2,1.3),1.28:(1.6,1.6)}[s];t=.12
    for x in (-(w+t)/2,(w+t)/2):box(r.name+f'_SIDE_{x:+}',(t,.20,h+.12),mats['metal'],c,r,(x,0,(h+.12)/2))
    for z in (.06,h+.06):box(r.name+f'_RAIL_{z:.2f}',(w+2*t,.20,t),mats['metal'],c,r,(0,0,z))
    box(r.name+'_PANEL',(w-.08,.10,h-.08),mats['ivory'],c,r,(0,.05,h/2+.06));variant(r,var,c,w,h*.45);r['semantic_purpose']='service/crawl hatch';r['clearance_width_m']=w;r['clearance_height_m']=h

def ladder(r,s,var,c):
    h={.78:2.4,1.0:3.6,1.28:5.0}[s];w=.68
    for x in (-w/2,w/2):rod(r.name+f'_RAIL_{x:+}',(x,0,.05),(x,0,h),.045,mats['metal'],c,r,8)
    for i in range(int(h/.30)+1):z=min(h,.20+i*.30);rod(r.name+f'_RUNG_{i:02d}',(-w/2,0,z),(w/2,0,z),.035,mats['ivory'],c,r,8)
    for x in (-w/2,w/2):rod(r.name+f'_GRAB_{x:+}',(x,0,h),(x,-.22,h+.55),.045,mats['metal'],c,r,8)
    variant(r,var,c,w*1.6,min(1.4,h*.35));r['semantic_purpose']='fixed maintenance ladder';r['ladder_height_m']=h;r['rung_pitch_m']=.30

def platform(r,s,var,c):
    w={.78:2.4,1.0:3.6,1.28:5.0}[s];d=1.8;box(r.name+'_DECK',(w,d,.16),mats['metal'],c,r,(0,0,.08))
    for y in (-.7,.7):box(r.name+f'_STRINGER_{y:+}',(w,.14,.28),mats['ivory'],c,r,(0,y,.22))
    for x in (-w/2+.15,w/2-.15):cyl(r.name+f'_FOOT_{x:+}',.12,.45,mats['metal'],c,r,(x,0,.225),v=10)
    variant(r,var,c,min(w,2.5),1.0);r['semantic_purpose']='service landing / modular platform';r['platform_width_m']=w;r['platform_depth_m']=d

def handrail(r,s,var,c):
    L={.78:2.4,1.0:3.6,1.28:5.0}[s];h=1.05;rod(r.name+'_TOP',(-L/2,0,h),(L/2,0,h),.045,mats['ivory'],c,r,8);rod(r.name+'_MID',(-L/2,0,.55),(L/2,0,.55),.035,mats['metal'],c,r,8)
    n=max(2,int(L/1.2)+1)
    for i in range(n):x=-L/2+L*i/(n-1);rod(r.name+f'_POST_{i:02d}',(x,0,.03),(x,0,h),.04,mats['metal'],c,r,8)
    box(r.name+'_TOE',(L,.08,.15),mats['metal'],c,r,(0,0,.075));variant(r,var,c,min(L,2.2),.8);r['semantic_purpose']='fall-protection handrail/toe-board module';r['rail_height_m']=h;r['module_length_m']=L

def gantry(r,s,var,c):
    span={.78:2.4,1.0:3.6,1.28:5.0}[s];h=3.2
    for x in (-span/2,span/2):box(r.name+f'_COLUMN_{x:+}',(.22,.22,h),mats['metal'],c,r,(x,0,h/2));box(r.name+f'_FOOT_{x:+}',(.55,.55,.12),mats['ivory'],c,r,(x,0,.06))
    box(r.name+'_BEAM',(span+.22,.24,.28),mats['metal'],c,r,(0,0,h-.14));rod(r.name+'_KNEE_L',(-span/2,0,h-.8),(-span/2+.65,0,h-.28),.055,mats['ivory'],c,r,8);rod(r.name+'_KNEE_R',(span/2,0,h-.8),(span/2-.65,0,h-.28),.055,mats['ivory'],c,r,8);variant(r,var,c,min(span,2.2),1.2);r['semantic_purpose']='service gantry load frame';r['clear_span_m']=span;r['clear_height_m']=h-.30

def bridge(r,s,var,c):
    L={.78:3.0,1.0:4.8,1.28:7.2}[s];w=2.2;box(r.name+'_DECK',(L,w,.18),mats['metal'],c,r,(0,0,.12))
    for y in (-.82,.82):box(r.name+f'_STRINGER_{y:+}',(L,.18,.36),mats['ivory'],c,r,(0,y,.28));rod(r.name+f'_RAIL_{y:+}',(-L/2,y,1.1),(L/2,y,1.1),.045,mats['ivory'],c,r,8)
    n=max(2,int(L/1.6)+1)
    for i in range(n):
        x=-L/2+L*i/(n-1);rod(r.name+f'_POST_L_{i}',(x,-.82,.25),(x,-.82,1.1),.04,mats['metal'],c,r,8);rod(r.name+f'_POST_R_{i}',(x,.82,.25),(x,.82,1.1),.04,mats['metal'],c,r,8)
    variant(r,var,c,min(L,2.2),.75);r['semantic_purpose']='modular service bridge';r['bridge_length_m']=L;r['clear_width_m']=w

def gland(r,s,var,c):
    w,h={.78:(1.2,.9),1.0:(1.8,1.1),1.28:(2.4,1.3)}[s];ports={.78:2,1.0:4,1.28:6}[s];box(r.name+'_PANEL',(w,.16,h),mats['ivory'],c,r,(0,0,h/2));spacing=w/(ports+1)
    for i in range(ports):x=-w/2+spacing*(i+1);cyl(r.name+f'_GLAND_{i:02d}',.10,.24,mats['gasket'],c,r,(x,-.18,h*.52),(math.radians(90),0,0),12)
    variant(r,var,c,w*.8,h*.45);r['semantic_purpose']='sealed cable/service penetration panel';r['port_count']=ports

def junction(r,s,var,c):
    w={.78:1.0,1.0:1.4,1.28:1.8}[s];h=1.2*s+.5;box(r.name+'_BOX',(w,.75,h),mats['metal'],c,r,(0,0,h/2));box(r.name+'_COVER',(w-.14,.08,h-.18),mats['ivory'],c,r,(0,-.415,h/2))
    for side in (-1,1):cyl(r.name+f'_CONDUIT_{side:+}',.10*s,.7,mats['gasket'],c,r,(side*(w/2+.35),0,h*.35),(0,math.radians(90),0),10)
    down=cyl(r.name+'_DOWN',.11*s,.55,mats['gasket'],c,r,(0,0,.30),v=10);down['function']='surface-accessible downward conduit stub; underground continuation not authored';variant(r,var,c,w*.75,h*.4);r['semantic_purpose']='protected conduit/cable junction'

def canopy(r,s,var,c):
    w,d,h={.78:(2.4,1.8,2.4),1.0:(3.6,2.2,2.7),1.28:(5.0,2.6,3.0)}[s];box(r.name+'_ROOF',(w,d,.16),mats['fabric'],c,r,(0,0,h))
    for x in (-w/2+.15,w/2-.15):
        for y in (-d/2+.15,d/2-.15):rod(r.name+f'_POST_{x:+.1f}_{y:+.1f}',(x,y,.03),(x,y,h-.05),.055,mats['metal'],c,r,8)
    for y in (-d/2+.1,d/2-.1):rod(r.name+f'_EDGE_{y:+}',(-w/2+.15,y,h-.1),(w/2-.15,y,h-.1),.06,mats['ivory'],c,r,8)
    variant(r,var,c,min(w,2.5),min(h*.55,1.5));r['semantic_purpose']='protected service/access canopy';r['clear_width_m']=w;r['clear_depth_m']=d;r['clear_height_m']=h-.2

BUILD={'ACCESS_DOOR':door,'SERVICE_HATCH':hatch,'LADDER':ladder,'PLATFORM':platform,'HANDRAIL':handrail,'GANTRY_FRAME':gantry,'BRIDGE_DECK':bridge,'CABLE_GLAND':gland,'CONDUIT_JUNCTION':junction,'ACCESS_CANOPY':canopy}
sizes={'S':.78,'M':1.0,'L':1.28};variants=['STANDARD','WIND_SHIELDED','FIELD_MODIFIED']
centers={fam:((-550+70*(i%5)),(-335 if i<5 else -285)) for i,fam in enumerate(FAMILIES)}
roots=[];idx=0
for fam in FAMILIES:
    bx,by=centers[fam]
    for si,(size,s) in enumerate(sizes.items()):
        for vi,var in enumerate(variants):
            r=make_root(fam,size,var,idx,bx+(si-1)*16,by+(vi-1)*8);BUILD[fam](r,s,var,sub[fam]);roots.append(r);idx+=1

scene['checkpoint']='X100_ARCH_INTERFACE_KIT_QA_FIXED_001';scene['x100_arch_family_count']=10;scene['x100_arch_prefab_roots']=90;scene['x100_arch_snap_grid_m']=.2;scene['x100_arch_fabrication_variants']='STANDARD|WIND_SHIELDED|FIELD_MODIFIED';scene['x100_arch_config_capacity']='>100 credible cross-family configurations';scene['x100_arch_conduit_contract']='surface-mounted stub; no undeclared underground geometry';scene['x100_arch_status']='KIT_FOUNDATION_NOT_FAMILY_COMPLETE'
assert len(roots)==90 and len({r['stable_id'] for r in roots})==90
