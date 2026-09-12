import bpy, math
from mathutils import Vector
scene=bpy.context.scene
terrain=bpy.data.objects.get('ENV_TERRAIN_TWILIGHT_BAND_BLOCKOUT')
root=bpy.data.collections.get('W04_UMBRA')
assert terrain and root

def ensure_coll(name):
    c=bpy.data.collections.get(name)
    if c is None:
        c=bpy.data.collections.new(name); root.children.link(c)
    return c
C_REF=ensure_coll('21_REFLECTOR_WAVE1'); C_CAR=ensure_coll('31_CARAVAN_WAVE1'); C_ARCH=ensure_coll('32_REFUGE_WAVE1'); C_CAM=bpy.data.collections.get('60_CAMERAS') or ensure_coll('60_CAMERAS')
mats={'metal':bpy.data.materials.get('MAT_SINSOL_DARK_METAL'),'mirror':bpy.data.materials.get('MAT_REFLECTOR_MIRROR'),'ivory':bpy.data.materials.get('MAT_COLONIAL_IVORY_REPAIR'),'fabric':bpy.data.materials.get('MAT_SINSOL_TENSION_FABRIC'),'amber':bpy.data.materials.get('MAT_REFUGE_AMBER'),'guide':bpy.data.materials.get('MAT_GUIDE')}
assert all(mats.values())
def link_only(o,coll):
    for c in list(o.users_collection): c.objects.unlink(o)
    coll.objects.link(o); return o
def cube(name,loc,dims,mat,coll,rot=(0,0,0),bevel=0.0):
    bpy.ops.mesh.primitive_cube_add(location=loc,rotation=rot); o=bpy.context.object; o.name=name; o.dimensions=dims; bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    if bevel:
        md=o.modifiers.new('BEVEL_PHYSICAL','BEVEL'); md.width=bevel; md.segments=2
    o.data.materials.append(mat); return link_only(o,coll)
def cyl(name,loc,radius,depth,mat,coll,rot=(0,0,0),verts=20):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts,radius=radius,depth=depth,location=loc,rotation=rot); o=bpy.context.object; o.name=name; o.data.materials.append(mat); return link_only(o,coll)
def torus(name,loc,major,minor,mat,coll,rot=(0,0,0)):
    bpy.ops.mesh.primitive_torus_add(major_radius=major,minor_radius=minor,major_segments=32,minor_segments=8,location=loc,rotation=rot); o=bpy.context.object; o.name=name; o.data.materials.append(mat); return link_only(o,coll)
def rod(name,a,b,r,mat,coll,verts=12):
    a,b=Vector(a),Vector(b); v=b-a; L=v.length
    if L<1e-5: return None
    mid=(a+b)*0.5; bpy.ops.mesh.primitive_cylinder_add(vertices=verts,radius=r,depth=L,location=mid); o=bpy.context.object; o.name=name; o.rotation_euler=v.to_track_quat('Z','Y').to_euler(); o.data.materials.append(mat); return link_only(o,coll)
def terrain_z(x,y):
    inv=terrain.matrix_world.inverted(); origin=inv @ Vector((x,y,200.0)); direction=(inv.to_3x3() @ Vector((0,0,-1))).normalized(); hit,loc,n,idx=terrain.ray_cast(origin,direction,distance=500.0)
    if not hit: raise RuntimeError(f'No terrain hit at {x},{y}')
    return (terrain.matrix_world @ loc).z
def bbox_bottom(o): return min((o.matrix_world @ Vector(c)).z for c in o.bound_box)
def local(origin,yaw,lx,ly,lz):
    c,s=math.cos(yaw),math.sin(yaw); return Vector((origin.x + lx*c-ly*s, origin.y + lx*s+ly*c, origin.z+lz))
def look_at(o,target): o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
refuge=bpy.data.objects.get('ARCH_REFUGE_HUB_BASE'); rg=terrain_z(refuge.location.x,refuge.location.y); ref_delta=rg-bbox_bottom(refuge)+0.08
for o in bpy.data.objects:
    if o.name.startswith('ARCH_REFUGE_HUB_'): o.location.z += ref_delta
refuge['wave1_contact_corrected']=True; refuge['contact_target_clearance_m']=0.08
for i,(dx,dy) in enumerate([(-18,-11),(18,-11),(-18,11),(18,11),(-6,-13),(6,-13)]):
    p=Vector((refuge.location.x+dx,refuge.location.y+dy,rg+0.45)); cyl(f'ARCH_REFUGE_W1_FOOT_{i:02d}',p,0.7,0.9,mats['metal'],C_ARCH,verts=12)
for idx in range(4):
    prefix=f'INFRA_REFLECTOR_{idx:02d}_'; mast=bpy.data.objects[prefix+'MAST']; panel=bpy.data.objects[prefix+'MIRROR']; x,y=mast.location.x,mast.location.y; ground=terrain_z(x,y); delta=ground-bbox_bottom(mast)+0.06
    for o in bpy.data.objects:
        if o.name.startswith(prefix): o.location.z += delta
    mast=bpy.data.objects[prefix+'MAST']; panel=bpy.data.objects[prefix+'MIRROR']; h=mast.dimensions.z; top=ground+h+0.06
    foundation=cyl(prefix+'W1_FOUNDATION',(x,y,ground+0.46),5.4,0.92,mats['metal'],C_REF,verts=16); foundation['manufacturing']='bolted steel/ceramic baseplate on ice anchor field'; foundation['asset_id']='W04-INF-001'
    for a,(dx,dy) in enumerate([(8,0),(-8,0),(0,8),(0,-8)]):
        az=terrain_z(x+dx,y+dy); cyl(prefix+f'W1_ANCHOR_{a:02d}',(x+dx,y+dy,az+0.3),1.4,0.6,mats['metal'],C_REF,verts=12); rod(prefix+f'W1_GUY_{a:02d}',(x,y,ground+6.5),(x+dx,y+dy,az+0.6),0.16,mats['metal'],C_REF,10)
    cab=cube(prefix+'W1_POWER_THERMAL',(x+5.9,y-3.4,ground+2.0),(3.4,2.2,4.0),mats['ivory'],C_REF,bevel=0.18); cab['function']='power conditioning + actuator thermal service'; rod(prefix+'W1_CABLE_TRUNK',(x+4.5,y-2.6,ground+1.0),(x+1.8,y-0.8,ground+7.5),0.18,mats['metal'],C_REF,10)
    platform_z=top-9.0; cyl(prefix+'W1_SERVICE_PLATFORM',(x,y,platform_z),4.4,0.28,mats['metal'],C_REF,verts=24); torus(prefix+'W1_SERVICE_RAIL',(x,y,platform_z+1.05),4.05,0.12,mats['ivory'],C_REF)
    z0=top-19.0; z1=top-9.4
    for sx in (-0.48,0.48): rod(prefix+f'W1_LADDER_RAIL_{sx:+.2f}',(x+2.5+sx,y,z0),(x+2.5+sx,y,z1),0.075,mats['ivory'],C_REF,8)
    for r_i in range(6):
        z=z0+1.0+r_i*1.55; rod(prefix+f'W1_LADDER_RUNG_{r_i:02d}',(x+2.02,y,z),(x+2.98,y,z),0.055,mats['ivory'],C_REF,8)
    pivot=Vector((x,y,top-2.2)); torus(prefix+'W1_GIMBAL_RING',pivot,3.3,0.28,mats['metal'],C_REF,rot=(math.radians(90),0,0)); rod(prefix+'W1_YOKE_L',(x-2.9,y,top-3.1),(x-2.9,y,top+0.6),0.28,mats['metal'],C_REF,12); rod(prefix+'W1_YOKE_R',(x+2.9,y,top-3.1),(x+2.9,y,top+0.6),0.28,mats['metal'],C_REF,12)
    R=panel.matrix_world.to_3x3(); origin=panel.location.copy(); rot=tuple(panel.rotation_euler)
    for r_i,lx in enumerate((-7.0,-3.5,0.0,3.5,7.0)):
        pos=origin + R @ Vector((lx,-0.82,0.0)); cube(prefix+f'W1_MIRROR_RIB_V_{r_i:02d}',pos,(0.28,0.28,11.5),mats['metal'],C_REF,rot=rot,bevel=0.05)
    for r_i,lz in enumerate((-4.6,0.0,4.6)):
        pos=origin + R @ Vector((0.0,-0.84,lz)); cube(prefix+f'W1_MIRROR_RIB_H_{r_i:02d}',pos,(18.0,0.28,0.28),mats['metal'],C_REF,rot=rot,bevel=0.05)
    p1=Vector((x-2.0,y,top-5.2)); p2=origin + R @ Vector((-6.0,-1.25,-4.0)); p3=Vector((x+2.0,y,top-5.2)); p4=origin + R @ Vector((6.0,-1.25,-4.0)); rod(prefix+'W1_ACTUATOR_L',p1,p2,0.22,mats['ivory'],C_REF,14); rod(prefix+'W1_ACTUATOR_R',p3,p4,0.22,mats['ivory'],C_REF,14); rod(prefix+'W1_SENSOR_STEM',(x-3.1,y,platform_z+0.3),(x-3.1,y,platform_z+3.4),0.09,mats['metal'],C_REF,10); cyl(prefix+'W1_SENSOR_HEAD',(x-3.1,y,platform_z+3.6),0.28,0.42,mats['amber'],C_REF,verts=12)
    mast['wave1_contact_corrected']=True; mast['ground_z_m']=round(ground,4); mast['access_logic']='sealed lower mast + exposed upper service ladder/platform'; panel['manufacturing']='reflective panel on ribbed backing frame + twin gimbal actuators'
for idx in range(5):
    prefix=f'CARAVAN_{idx:02d}_'; chassis=bpy.data.objects[prefix+'CHASSIS']; tracks=[bpy.data.objects[prefix+'TRACK_-1'],bpy.data.objects[prefix+'TRACK_+1']]; grounds=[terrain_z(t.location.x,t.location.y) for t in tracks]; avg_ground=sum(grounds)/2; avg_bottom=sum(bbox_bottom(t) for t in tracks)/2; delta=avg_ground+0.10-avg_bottom
    for o in bpy.data.objects:
        if o.name.startswith(prefix): o.location.z += delta
    chassis=bpy.data.objects[prefix+'CHASSIS']; yaw=chassis.rotation_euler.z; origin=chassis.location.copy()
    for side in (-1,1):
        p=local(origin,yaw,0,side*2.25,-1.55); cube(prefix+f'W1_FRAME_RAIL_{side:+d}',p,(13.8,0.42,0.52),mats['metal'],C_CAR,rot=(0,0,yaw),bevel=0.08)
    for side in (-1,1):
        for wi,lx in enumerate((-4.8,0.0,4.8)):
            p=local(origin,yaw,lx,side*3.72,-2.0); wheel=cyl(prefix+f'W1_BOGIE_{side:+d}_{wi:02d}',p,0.74,0.68,mats['metal'],C_CAR,rot=(math.radians(90),0,yaw),verts=16); wheel['function']='low-temperature bogie / track load transfer'; a=local(origin,yaw,lx,side*2.25,-1.2); b=local(origin,yaw,lx,side*3.35,-1.9); rod(prefix+f'W1_SUSPENSION_{side:+d}_{wi:02d}',a,b,0.10,mats['ivory'],C_CAR,10)
    cowl=local(origin,yaw,-0.8,0,3.85); cube(prefix+'W1_WIND_COWL',cowl,(9.8,5.9,0.75),mats['metal'],C_CAR,rot=(0,math.radians(-5),yaw),bevel=0.28)
    for side in (-1,1):
        p=local(origin,yaw,1.5,side*3.42,0.65); bay=cube(prefix+f'W1_SERVICE_BAY_{side:+d}',p,(3.2,0.5,1.55),mats['ivory'],C_CAR,rot=(0,0,yaw),bevel=0.15); bay['function']='field service / thermal access'; p2=local(origin,yaw,5.0,side*3.25,0.95); cargo=cube(prefix+f'W1_CARGO_POD_{side:+d}',p2,(2.4,1.1,1.8),mats['metal'],C_CAR,rot=(0,0,yaw),bevel=0.22); cargo['interface']='quick-release cargo/refuge supply socket'
    for fi in range(5):
        p=local(origin,yaw,5.9,-2.85+fi*1.4,2.2); cube(prefix+f'W1_HEAT_FIN_{fi:02d}',p,(0.18,0.9,2.1),mats['metal'],C_CAR,rot=(0,0,yaw),bevel=0.03)
    canopy_z=4.9
    for si,ly in enumerate((-2.85,2.85)):
        a=local(origin,yaw,0.0,ly,2.7); b=local(origin,yaw,2.4,ly,canopy_z); rod(prefix+f'W1_CANOPY_STRUT_F_{si}',a,b,0.075,mats['ivory'],C_CAR,8); a2=local(origin,yaw,4.8,ly,2.8); b2=local(origin,yaw,2.4,ly,canopy_z); rod(prefix+f'W1_CANOPY_STRUT_R_{si}',a2,b2,0.075,mats['ivory'],C_CAR,8)
    rod(prefix+'W1_CANOPY_RIDGE_L',local(origin,yaw,-0.6,-2.85,4.2),local(origin,yaw,5.4,-2.85,4.2),0.065,mats['ivory'],C_CAR,8); rod(prefix+'W1_CANOPY_RIDGE_R',local(origin,yaw,-0.6,2.85,4.2),local(origin,yaw,5.4,2.85,4.2),0.065,mats['ivory'],C_CAR,8); beacon_pos=local(origin,yaw,-5.4,0,4.2); rod(prefix+'W1_BEACON_GUARD',beacon_pos,beacon_pos+Vector((0,0,1.9)),0.09,mats['metal'],C_CAR,8); cyl(prefix+'W1_BEACON_HEAD',beacon_pos+Vector((0,0,2.15)),0.32,0.45,mats['amber'],C_CAR,verts=12)
    chassis['wave1_contact_corrected']=True; chassis['ground_clearance_reference_m']=0.10; chassis['manufacturing']='modular welded torsion box / serviceable bogies / tension canopy / quick-release cargo interfaces'; chassis['asset_id']='W04-CAR-001'
cam=bpy.data.objects.get('CAM_DELIVERY_UMBRA_WAVE0'); cam.location=(80.0,-1150.0,250.0); cam.data.lens=38; cam.data.clip_end=4000; look_at(cam,(0.0,55.0,28.0)); cam['wave1_framing_goal']='include left caravan + all four reflector masts + NOCTIL destination interface'
cam_data=bpy.data.cameras.get('CAM_QA_PLAYER_READABILITY_DATA') or bpy.data.cameras.new('CAM_QA_PLAYER_READABILITY_DATA'); qa=bpy.data.objects.get('CAM_QA_PLAYER_READABILITY')
if qa is None: qa=bpy.data.objects.new('CAM_QA_PLAYER_READABILITY',cam_data); C_CAM.objects.link(qa)
qa.location=(-145.0,-240.0,2.2); qa.data.lens=34; qa.data.sensor_width=36; qa.data.clip_start=0.1; qa.data.clip_end=2500; look_at(qa,(20.0,-85.0,7.0)); qa['epistemic']='QA_PROPOSAL_NOT_RUNTIME_CAMERA'
scene['checkpoint']='WAVE1_CONTACT_REFLECTOR_CARAVAN_001'; scene['wave1_scope']='contact correction + reflector functional kit + caravan modular kit + delivery framing'; scene['quality_claim']='WAVE1 PRODUCTION FOUNDATION / NOT FINAL AAAA'
bpy.context.view_layer.update()
result={'checkpoint':scene['checkpoint'],'collections':[C_REF.name,C_CAR.name,C_ARCH.name],'delivery_camera':[list(cam.location),cam.data.lens]}
