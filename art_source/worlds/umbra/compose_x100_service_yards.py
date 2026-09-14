"""Compose three deterministic UMBRA X100 service yards from the authored service prefabs.

Input checkpoint: X100_SERVICE_ECOSYSTEM_FOUNDATION_001.
Output checkpoint: X100_SERVICE_YARDS_QA_FIXED_001.

The composer uses linked mesh data from catalog prefabs and adds no random scatter.
"""
import bpy, math
from mathutils import Vector

scene=bpy.context.scene
terrain=bpy.data.objects['ENV_TERRAIN_TWILIGHT_BAND_BLOCKOUT']
world=bpy.data.collections['W04_UMBRA']


def tz(x,y):
    inv=terrain.matrix_world.inverted(); origin=inv@Vector((x,y,220)); direction=(inv.to_3x3()@Vector((0,0,-1))).normalized()
    hit,loc,_n,_i=terrain.ray_cast(origin,direction,distance=600)
    if not hit: raise RuntimeError((x,y))
    return (terrain.matrix_world@loc).z


def ensure(parent,name):
    c=bpy.data.collections.get(name) or bpy.data.collections.new(name)
    if c.name not in [x.name for x in parent.children]: parent.children.link(c)
    return c


C=ensure(world,'82_X100_SERVICE_YARDS')
yard_cols={n:ensure(C,'83_X100_YARD_'+n) for n in ['REFLECTOR_MAINT','CARAVAN_REPAIR','REFUGE_LOGISTICS']}


def source(fam,size,state):
    matches=[o for o in bpy.data.objects if o.type=='EMPTY' and o.get('family')==fam and o.get('size_variant')==size and o.get('state_variant')==state]
    if not matches: raise RuntimeError((fam,size,state))
    return sorted(matches,key=lambda o:o.name)[0]


def clone_prefab(src,name,x,y,rot_deg,col,era,role):
    r=bpy.data.objects.new(name,None); col.objects.link(r); r.location=(x,y,tz(x,y)+0.03); r.rotation_euler[2]=math.radians(rot_deg)
    for k in src.keys(): r[k]=src[k]
    r['stable_id']=name.replace('X100Y_','W04-X100Y-'); r['source_prefab']=src['stable_id']; r['era_layer']=era; r['yard_role']=role; r['x100_composition']='AUTHORED_SYSTEMIC_COMPOSITION'
    for ch in src.children:
        nc=ch.copy(); nc.data=ch.data; col.objects.link(nc); nc.name=name+'__'+ch.name.split('_',1)[-1]; nc.parent=r; nc.location=ch.location.copy(); nc.rotation_euler=ch.rotation_euler.copy(); nc.scale=ch.scale.copy()
    return r


configs={
 'REFLECTOR_MAINT': {'center':(430,112),'angle':-8,'dims':(44,24),'assets':[
  ('POWERBOX','L','SERVICED',-16,7,0,'ERA_0','installed power distribution'),('CABLE_REEL','L','USED',-7,8,90,'ERA_1','active cable service'),('WINCH','L','FIELD_REPAIRED',5,8,180,'ERA_2','field-repaired anchor tensioning'),('HEATEX','M','USED',16,7,180,'ERA_1','temporary thermal rejection'),('SERVICE_STAND','L','USED',-14,-7,0,'ERA_1','mirror/actuator maintenance stand'),('TOOLCASE','M','FIELD_REPAIRED',-4,-8,15,'ERA_2','field tool cache'),('STORAGE','M','USED',7,-8,0,'ERA_1','service spares'),('LAMP','M','SERVICED',17,-7,0,'ERA_0','safe work light'),('WAYFIND','L','SERVICED',21,9,0,'ERA_0','reflector yard wayfinding')]},
 'CARAVAN_REPAIR': {'center':(20,-145),'angle':12,'dims':(52,26),'assets':[
  ('SERVICE_STAND','M','USED',-20,8,0,'ERA_1','bogie support'),('SERVICE_STAND','M','FIELD_REPAIRED',-10,8,0,'ERA_2','secondary bogie support'),('WINCH','M','USED',2,8,90,'ERA_1','caravan recovery tension'),('CABLE_REEL','M','USED',14,8,90,'ERA_1','mobile power feed'),('TOOLCASE','S','USED',21,7,0,'ERA_1','active hand tools'),('STORAGE','M','USED',-20,-8,0,'ERA_1','spares'),('STORAGE','M','FIELD_REPAIRED',-10,-8,0,'ERA_2','salvaged spares'),('TEXTILE','M','FIELD_REPAIRED',1,-8,0,'ERA_2','canopy repair stock'),('TEXTILE','M','USED',11,-8,0,'ERA_1','insulation stock'),('LAMP','S','SERVICED',21,-7,0,'ERA_0','safe repair light'),('WAYFIND','M','FIELD_REPAIRED',25,10,0,'ERA_2','repair-bay perimeter marker')]},
 'REFUGE_LOGISTICS': {'center':(72,-8),'angle':0,'dims':(46,24),'assets':[
  ('POWERBOX','L','SERVICED',-17,7,0,'ERA_0','refuge power'),('HEATEX','L','SERVICED',-7,8,0,'ERA_0','refuge thermal plant extension'),('STORAGE','L','SERVICED',5,8,0,'ERA_0','sealed provisions'),('STORAGE','L','USED',15,8,0,'ERA_1','active stores'),('TEXTILE','L','SERVICED',-16,-8,0,'ERA_1','insulation reserve'),('TEXTILE','L','FIELD_REPAIRED',-6,-8,0,'ERA_2','repair reserve'),('TOOLCASE','M','SERVICED',5,-8,0,'ERA_1','maintenance station'),('LAMP','M','SERVICED',15,-8,0,'ERA_0','refuge safe light'),('LAMP','M','USED',20,-9,0,'ERA_1','secondary perimeter light'),('WAYFIND','M','SERVICED',22,5,0,'ERA_0','refuge logistics marker')]}
}

roots=[]
for yn,cfg in configs.items():
    col=yard_cols[yn]; cx,cy=cfg['center']; angle=math.radians(cfg['angle']); ca,sa=math.cos(angle),math.sin(angle)
    for i,(fam,size,state,dx,dy,rel_ang,era,role) in enumerate(cfg['assets']):
        x=cx+dx*ca-dy*sa; y=cy+dx*sa+dy*ca
        roots.append(clone_prefab(source(fam,size,state),f'X100Y_{yn}_{i:02d}_{fam}',x,y,cfg['angle']+rel_ang,col,era,role))
    # terrain-conforming hardpack: 12x6 cells, +0.04 m sampled offset
    sx,sy=cfg['dims']; nx,ny=12,6; verts=[]; faces=[]
    for j in range(ny+1):
        ly=-sy/2+sy*j/ny
        for i in range(nx+1):
            lx=-sx/2+sx*i/nx; x=cx+lx*ca-ly*sa; y=cy+lx*sa+ly*ca; verts.append((x,y,tz(x,y)+0.04))
    for j in range(ny):
        for i in range(nx):
            a=j*(nx+1)+i; faces.append((a,a+1,a+nx+2,a+nx+1))
    me=bpy.data.meshes.new('MESH_X100Y_'+yn+'_HARDPACK'); me.from_pydata(verts,[],faces); me.update(); me.materials.append(bpy.data.materials['MAT_UMBRA_ICE_EDGE'])
    hp=bpy.data.objects.new('X100Y_'+yn+'_HARDPACK',me); col.objects.link(hp); hp['function']='terrain-conforming packed service apron'; hp['clear_corridor_m']=5.0
    anchor=bpy.data.objects.new('X100Y_'+yn+'_ANCHOR',None); col.objects.link(anchor); anchor.location=(cx,cy,tz(cx,cy)+.05); anchor['clear_corridor_m']=5.0; anchor['history_contract']='ERA_0 original systems | ERA_1 occupation/service | ERA_2 field repair/adaptation'

scene['checkpoint']='X100_SERVICE_YARDS_QA_FIXED_001'
scene['x100_yards']=3
scene['x100_yard_prefab_instances']=len(roots)
scene['x100_history_geometry']='ERA_0|ERA_1|ERA_2'
scene['x100_corridor_contract']='5m center corridor; no visible QA rails'
scene['x100_yard_apron_contract']='terrain-conforming sampled hardpack +0.04m'

assert len(roots)==30
