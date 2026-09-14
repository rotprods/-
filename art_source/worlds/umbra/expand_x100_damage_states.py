"""Add causal DAMAGED/ABANDONED states to the UMBRA X100 service ecosystem.

Input checkpoint: X100_SERVICE_YARDS_QA_FIXED_001.
Output checkpoint: X100_DAMAGE_STATES_FOUNDATION_001.

No random destruction or material noise is generated. Each family has a named,
physically legible failure mode; roots are reseated after deformations so the
lowest authored mesh contact remains at local terrain +0.03 m.
"""
import bpy, math
from mathutils import Vector

scene=bpy.context.scene
terrain=bpy.data.objects['ENV_TERRAIN_TWILIGHT_BAND_BLOCKOUT']
world=bpy.data.collections['W04_UMBRA']
FAMILIES=['TOOLCASE','CABLE_REEL','STORAGE','POWERBOX','HEATEX','WINCH','LAMP','TEXTILE','SERVICE_STAND','WAYFIND']


def ensure(parent,name):
    c=bpy.data.collections.get(name) or bpy.data.collections.new(name)
    if c.name not in [x.name for x in parent.children]: parent.children.link(c)
    return c

C=ensure(world,'84_X100_DAMAGE_STATES')
sub={f:ensure(C,'85_X100_DAMAGE_'+f) for f in FAMILIES}


def tz(x,y):
    inv=terrain.matrix_world.inverted(); origin=inv@Vector((x,y,220)); d=(inv.to_3x3()@Vector((0,0,-1))).normalized()
    hit,loc,_n,_i=terrain.ray_cast(origin,d,distance=600)
    if not hit: raise RuntimeError((x,y))
    return (terrain.matrix_world@loc).z


def source(family,size):
    m=[o for o in bpy.data.objects if o.type=='EMPTY' and o.get('family')==family and o.get('size_variant')==size and o.get('state_variant')=='USED' and o.name.startswith('X100_')]
    if not m: raise RuntimeError((family,size))
    return sorted(m,key=lambda o:o.name)[0]


def clone(src_root,name,x,y,state,col):
    r=bpy.data.objects.new(name,None); col.objects.link(r); r.location=(x,y,tz(x,y)+0.03)
    for k in src_root.keys(): r[k]=src_root[k]
    r['stable_id']=name.replace('X100D_','W04-X100D-'); r['source_prefab']=src_root['stable_id']; r['state_variant']=state
    r['temporal_layer']='ERA_2_FAILURE_OR_POST_USE'; r['damage_causality']='FAMILY_SPECIFIC_NO_RANDOM_DESTRUCTION'; r['x100_status']='STATE_FOUNDATION_NOT_FAMILY_COMPLETE'
    for ch in src_root.children:
        nc=ch.copy(); nc.data=ch.data; col.objects.link(nc); tail=ch.name[len(src_root.name):] if ch.name.startswith(src_root.name) else '__'+ch.name
        nc.name=name+tail; nc.parent=r; nc.location=ch.location.copy(); nc.rotation_euler=ch.rotation_euler.copy(); nc.scale=ch.scale.copy()
    return r


def pick(r,token): return [o for o in r.children if token in o.name]
def remove(objs):
    for o in list(objs): bpy.data.objects.remove(o,do_unlink=True)
def move(o,dx=0,dy=0,dz=0,rx=0,ry=0,rz=0):
    o.location.x+=dx; o.location.y+=dy; o.location.z+=dz; o.rotation_euler.x+=math.radians(rx); o.rotation_euler.y+=math.radians(ry); o.rotation_euler.z+=math.radians(rz)
def seat(r):
    bpy.context.view_layer.update(); pts=[]
    for ch in r.children:
        if ch.type=='MESH': pts.extend(ch.matrix_world@Vector(c) for c in ch.bound_box)
    if pts:
        bottom=min(p.z for p in pts); p=r.matrix_world.translation; r.location.z+=tz(p.x,p.y)+0.03-bottom
    bpy.context.view_layer.update()


def fail(r,fam,state):
    if fam=='TOOLCASE':
        lid=pick(r,'_LID')[0]
        if state=='DAMAGED': move(lid,dy=.06,dz=.08,rx=14); move(pick(r,'_LATCH_')[-1],dy=-.08,rz=22); mode='impact distorts lid alignment and one latch'
        else: move(lid,dy=.18,dz=.22,rx=58); remove(pick(r,'_LATCH_')[1:]); move(pick(r,'_HANDLE')[0],dz=-.10,ry=55); mode='abandoned open case with failed latch and collapsed handle'
    elif fam=='CABLE_REEL':
        frames=pick(r,'_FRAME_'); hubs=pick(r,'_HUB_')
        if state=='DAMAGED': move(frames[-1],dx=.13,rz=9); move(hubs[-1],dy=.08,rx=8); mode='side-frame impact misaligns one cheek/hub'
        else: remove(hubs[-1:]); move(frames[-1],dx=.28,rz=24); move(pick(r,'_DRUM')[0],dz=-.10,rz=12); mode='abandoned reel with missing hub and collapsed side frame'
    elif fam=='STORAGE':
        lid=pick(r,'_LID')[0]; corners=pick(r,'_CORNER_')
        if state=='DAMAGED': move(lid,dx=.07,dz=.05,ry=9); remove(corners[-1:]); mode='corner impact removes protector and racks lid'
        else: move(lid,dy=-.22,dz=.20,rx=42); remove(corners[-2:]); mode='abandoned container left open after corner failures'
    elif fam=='POWERBOX':
        door=pick(r,'_DOOR')[0]; fins=pick(r,'_FIN_'); ports=pick(r,'_PORT_')
        if state=='DAMAGED': move(door,dy=-.06,rz=11); remove(fins[-1:]); move(ports[-1],dy=-.08,rx=12); mode='service-door strike plus lost heat fin and stressed port'
        else: move(door,dy=-.34,dz=-.38,rx=72); remove(fins[-2:]+ports[-1:]); mode='abandoned disconnected cabinet with open/fallen door and missing cooling parts'
    elif fam=='HEATEX':
        fins=pick(r,'_FIN_')
        if state=='DAMAGED': remove(fins[-2:]); move(fins[-3],rz=16); mode='windborne impact bends/removes radiator fins'
        else: remove(fins[-4:]); move(pick(r,'_CORE')[0],ry=7); mode='abandoned exchanger isolated with major fin loss and settled core'
    elif fam=='WINCH':
        guide=pick(r,'_GUIDE')[0]; cheeks=pick(r,'_CHEEK_'); motor=pick(r,'_MOTOR')[0]
        if state=='DAMAGED': move(guide,dx=-.12,rz=17); move(cheeks[-1],dy=.05,rx=8); mode='overload deforms cable guide and one drum cheek'
        else: remove([guide]); move(cheeks[-1],dy=.20,rx=32); move(motor,dx=.35,dy=.35,dz=-.25,rz=20); mode='abandoned winch with lost guide, displaced motor and collapsed cheek'
    elif fam=='LAMP':
        shield=pick(r,'_SHIELD')[0]; cages=pick(r,'_CAGE_')
        if state=='DAMAGED': move(shield,dx=.10,rz=13); remove(cages[-1:]); move(pick(r,'_EMITTER')[0],dx=.06,rz=7); mode='wind/impact twists shield and breaks one protective cage bar'
        else: remove(pick(r,'_EMITTER')+cages[-1:]); move(shield,dz=-.18,rz=28); move(pick(r,'_MAST')[0],rx=12); mode='abandoned unpowered lamp with missing emitter and bent mast/shield'
    elif fam=='TEXTILE':
        straps=pick(r,'_STRAP_'); roll=pick(r,'_ROLL')[0]
        if state=='DAMAGED': remove(straps[-1:]); move(roll,dy=.08,rz=8); mode='strap failure lets insulated roll deform/shift under wind load'
        else: remove(straps); move(roll,dx=.18,dy=.22,rz=18); mode='abandoned unstrapped roll displaced by persistent lateral wind'
    elif fam=='SERVICE_STAND':
        legs=pick(r,'_LEG_'); feet=pick(r,'_FOOT_'); saddle=pick(r,'_SADDLE')[0]
        if state=='DAMAGED': move(legs[-1],dx=.10,ry=13); move(feet[-1],dx=.12,rz=8); mode='overload bends one leg/foot while saddle remains usable'
        else: move(legs[-1],dx=.30,ry=42); move(legs[-2],dx=.16,ry=25); move(saddle,dz=-.32,rz=11); mode='abandoned trestle partially collapsed after load-path failure'
    elif fam=='WAYFIND':
        post=pick(r,'_POST')[0]; bar=pick(r,'_HORIZON_BAR')[0]; back=pick(r,'_ECLIPSE_BACK')[0]; cut=pick(r,'_ECLIPSE_CUT')[0]
        if state=='DAMAGED': move(bar,dx=.08,rz=18); move(back,dx=.08,rz=14); move(cut,dx=.10,rz=14); mode='wind/impact racks upper horizon/eclipsing marker while anchor remains intact'
        else:
            move(post,dx=.62,dz=-.45,ry=58); move(bar,dx=.80,dz=-.62,ry=58); move(back,dx=.92,dz=-.70,ry=58); move(cut,dx=.95,dz=-.72,ry=58); mode='upper marker fails at anchor interface; base stump remains seated'
    r['failure_mode']=mode; r['state_semantics']=state; seat(r)

sizes={'S':0.78,'M':1.0,'L':1.28}
centers={fam:((330+50*(i%5)),(-320 if i<5 else -250)) for i,fam in enumerate(FAMILIES)}
roots=[]; idx=0
for fam in FAMILIES:
    bx,by=centers[fam]
    for si,(size,_scale) in enumerate(sizes.items()):
        for state,dy in [('DAMAGED',-5),('ABANDONED',5)]:
            r=clone(source(fam,size),f'X100D_{fam}_{size}_{state}_{idx:02d}',bx+(si-1)*12,by+dy,state,sub[fam]); fail(r,fam,state); roots.append(r); idx+=1

scene['checkpoint']='X100_DAMAGE_STATES_FOUNDATION_001'
scene['x100_damage_state_roots']=len(roots)
scene['x100_temporal_states']='SERVICED|USED|FIELD_REPAIRED|DAMAGED|ABANDONED'
scene['x100_damage_contract']='family-specific failure modes only; no random destruction/grunge'
scene['x100_damage_status']='STATE_FOUNDATION_NOT_FAMILY_COMPLETE'
assert len(roots)==60
assert len({r['stable_id'] for r in roots})==60
