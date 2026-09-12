"""Aurora Veil bounded temporal visual/collision contract.

Validated against Blender 5.2 remote revision 12.
This creates only Aurora local temporal proof geometry and hidden collision proxies.
It does NOT implement runtime time manipulation, save-state rewinds or engine logic.
"""
import bpy
import math

STATE_ORDER = ['IDLE','PRE_CUE','REPEAT_ARMED','REPEAT_ACTIVE','COOLDOWN']
FIELDS = [
    {'id':'AUR-TMP-FIELD-A','center':(-430,-230),'delay':1.0,'cue_lead':0.80,'active_window':0.55},
    {'id':'AUR-TMP-FIELD-B','center':(50,60),'delay':1.4,'cue_lead':1.05,'active_window':0.65},
    {'id':'AUR-TMP-FIELD-C','center':(460,-170),'delay':1.8,'cue_lead':1.25,'active_window':0.75},
]
ARENA_SECTORS = [(1,0,0.9),(2,120,1.2),(3,240,1.5)]


def ensure_collection(root,name):
    c=bpy.data.collections.get(name)
    if not c:
        c=bpy.data.collections.new(name); root.children.link(c)
    return c


def material(name,base,metallic=0.0,roughness=0.5,emission=None):
    m=bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes=True
    p=m.node_tree.nodes.get('Principled BSDF')
    p.inputs['Base Color'].default_value=(*base,1)
    p.inputs['Metallic'].default_value=metallic
    p.inputs['Roughness'].default_value=roughness
    if emission:
        p.inputs['Emission Color'].default_value=(*emission[0],1)
        p.inputs['Emission Strength'].default_value=emission[1]
    return m


def move(obj,col):
    for c in list(obj.users_collection): c.objects.unlink(obj)
    col.objects.link(obj); return obj


def cube(name,loc,dims,mat,col,rot=(0,0,0)):
    bpy.ops.mesh.primitive_cube_add(location=loc,rotation=rot)
    o=bpy.context.object; o.name=name; o.dimensions=dims
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    o.data.materials.append(mat); return move(o,col)


def cylinder(name,loc,radius,depth,mat,col,verts=20):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts,radius=radius,depth=depth,location=loc)
    o=bpy.context.object; o.name=name; o.data.materials.append(mat); return move(o,col)


def torus(name,loc,major,minor,mat,col):
    bpy.ops.mesh.primitive_torus_add(major_radius=major,minor_radius=minor,major_segments=48,minor_segments=8,location=loc)
    o=bpy.context.object; o.name=name; o.data.materials.append(mat); return move(o,col)


def path(name,pts,bevel,mat,col):
    cu=bpy.data.curves.new(name,'CURVE'); cu.dimensions='3D'; cu.bevel_depth=bevel; cu.bevel_resolution=2
    sp=cu.splines.new('POLY'); sp.points.add(len(pts)-1)
    for i,p in enumerate(pts): sp.points[i].co=(*p,1)
    o=bpy.data.objects.new(name,cu); col.objects.link(o); cu.materials.append(mat); return o


def build():
    scene=bpy.context.scene
    root=bpy.data.collections.get('AURORA_VEIL_ROOT') or scene.collection
    legacy=bpy.data.collections.get('05_TEMPORAL')
    if legacy:
        legacy.hide_render=True
        legacy['status']='LEGACY_BLOCKOUT_SUPERSEDED_BY_18_TEMPORAL_PRODUCTION'
    prod=ensure_collection(root,'18_TEMPORAL_PRODUCTION')
    coll=ensure_collection(root,'19_TEMPORAL_COLLISION_PROXIES')
    qa=ensure_collection(root,'20_TEMPORAL_QA')
    for c in (prod,coll,qa):
        for o in list(c.objects): bpy.data.objects.remove(o,do_unlink=True)
    coll.hide_render=True; qa.hide_render=True

    idle=material('AUR_TMP_MAT_IDLE',(0.12,0.15,0.16),0.55,0.45)
    cue=material('AUR_TMP_MAT_PRE_CUE',(0.12,0.22,0.20),0.22,0.30,((0.02,0.90,0.72),3.0))
    active=material('AUR_TMP_MAT_ACTIVE',(0.19,0.08,0.22),0.16,0.28,((0.62,0.08,1.0),4.2))
    cooldown=material('AUR_TMP_MAT_COOLDOWN',(0.18,0.13,0.07),0.45,0.52)
    collmat=material('AUR_TMP_MAT_COLLISION_DEBUG',(0.04,0.35,0.08),0.0,0.82)

    for f in FIELDS:
        fid=f['id']; x,y=f['center']; z=0.35; radius=26.0
        r=bpy.data.objects.new(fid+'_ROOT',None); prod.objects.link(r); r.location=(x,y,0)
        r['asset_id']='AUR-TMP-001'; r['field_id']=fid; r['delay_s']=f['delay']; r['cue_lead_s']=f['cue_lead']; r['active_window_s']=f['active_window']
        r['rule']='REPEAT_LAST_AUTHORED_ACTION_ONCE'; r['state_order']='>'.join(STATE_ORDER)
        r['persistence']='ENCOUNTER_LOCAL_RESET_ON_EXIT_OR_RELOAD'; r['save_state_mutation']='FORBIDDEN'; r['global_rewind']='FORBIDDEN'
        r['collision_owner']='19_TEMPORAL_COLLISION_PROXIES'; r['accessibility']='shape+motion+audio required; color supplemental'

        ring=torus(fid+'_IDLE_RING',(x,y,z),radius,0.32,idle,prod); ring['state_id']='IDLE'; ring['field_id']=fid; ring['collision_policy']='NONE_VISUAL_BOUNDARY_ONLY'
        for s in range(8):
            a=2*math.pi*s/8; px=x+(radius-2)*math.cos(a); py=y+(radius-2)*math.sin(a)
            o=cube(f'{fid}_PRECUE_TICK_{s:02d}',(px,py,z+0.9),(0.55,4.8,1.4),cue,prod,(0,0,a)); o['state_id']='PRE_CUE'; o['field_id']=fid; o['non_color_cue']='RADIAL_INWARD_TICK'
        for s in range(4):
            a=2*math.pi*s/4+math.pi/4; px=x+(radius-5)*math.cos(a); py=y+(radius-5)*math.sin(a)
            o=cube(f'{fid}_ARMED_GATE_{s:02d}',(px,py,z+2.3),(1.0,5.6,4.4),cue,prod,(0,0,a)); o['state_id']='REPEAT_ARMED'; o['field_id']=fid; o['collision_policy']='NONE_VISUAL_ONLY'
        src_loc=(x-7,y-2,z+2.1); rep_loc=(x+7,y+2,z+2.1)
        src=cylinder(fid+'_SOURCE_ACTION',src_loc,2.2,4.0,idle,prod); src['state_id']='REPEAT_ACTIVE'; src['field_id']=fid; src['role']='SOURCE_ACTION_REFERENCE'
        rep=cylinder(fid+'_REPEAT_ACTION',rep_loc,2.2,4.0,active,prod); rep['state_id']='REPEAT_ACTIVE'; rep['field_id']=fid; rep['role']='DELAYED_REPEAT_VISUAL'; rep['delay_s']=f['delay']
        p=path(fid+'_ACTIVE_TRAJECTORY',[(src_loc[0],src_loc[1],z+4.7),(x,y,z+5.7),(rep_loc[0],rep_loc[1],z+4.7)],0.26,active,prod); p['state_id']='REPEAT_ACTIVE'; p['field_id']=fid
        for s in range(6):
            a=2*math.pi*s/6+math.pi/6; px=x+(radius-8)*math.cos(a); py=y+(radius-8)*math.sin(a)
            o=cylinder(f'{fid}_COOLDOWN_POST_{s:02d}',(px,py,z+0.7),0.55,1.4,cooldown,prod,12); o['state_id']='COOLDOWN'; o['field_id']=fid
        cp=cube(fid+'_COL_REPEAT_ACTIVE',rep_loc,(5,5,4.4),collmat,coll); cp.hide_render=True; cp.display_type='WIRE'; cp['field_id']=fid; cp['collision_state']='REPEAT_ACTIVE'; cp['collision_policy']='ENABLE_LOCAL_REPEAT_PROXY_ONLY'; cp['runtime_default']='DISABLED'
        g=torus(fid+'_QA_RADIUS',(x,y,z-0.2),radius,0.12,collmat,qa); g.hide_render=True; g.display_type='WIRE'; g['expected_radius_m']=radius

    center=(1650,250,6.0)
    for index,angle,delay in ARENA_SECTORS:
        a=math.radians(angle); loc=(center[0]+18*math.cos(a),center[1]+18*math.sin(a),center[2])
        r=bpy.data.objects.new(f'AUR-AEON-TMP-SECTOR-{index}_ROOT',None); prod.objects.link(r); r.location=loc
        r['asset_id']='AUR-TMP-002'; r['sector_index']=index; r['delay_s_proposal']=delay; r['rule']='ONE_VISIBLE_DELAY_PER_SECTOR'; r['persistence']='ARENA_LOCAL_ONLY'; r['global_save_mutation']='FORBIDDEN'; r['collision_policy']='RUNTIME_STATE_TOGGLE_REQUIRED'
        for fin in range(index):
            off=(fin-((index-1)/2))*1.4
            cube(f'AUR_AEON_SECTOR_{index}_FIN_{fin+1}',(loc[0]+off*math.cos(a+math.pi/2),loc[1]+off*math.sin(a+math.pi/2),loc[2]+2),(0.55,3.6,4.0),cue,prod,(0,0,a))
        cp=cube(f'AUR_AEON_SECTOR_{index}_COL_ACTIVE',loc,(6,6,4),collmat,coll); cp.hide_render=True; cp.display_type='WIRE'; cp['field_id']=f'AUR-AEON-TMP-SECTOR-{index}'; cp['collision_state']='REPEAT_ACTIVE'; cp['collision_policy']='ENABLE_LOCAL_REPEAT_PROXY_ONLY'; cp['runtime_default']='DISABLED'

    scene['temporal_contract_version']='AUR-TEMPORAL-v1-r12'; scene['temporal_state_order']='>'.join(STATE_ORDER); scene['temporal_global_rewind']='FORBIDDEN'; scene['temporal_save_mutation']='FORBIDDEN'; scene['temporal_collision_strategy']='separate hidden proxies; runtime enables only ACTIVE state'; scene['temporal_field_count']=3; scene['temporal_arena_sector_count']=3; scene['status']='WAVE2_TEMPORAL_CONTRACT_R12_METADATA_QA'
    return {'status':scene['status'],'fields':3,'arena_sectors':3,'collision_proxies':len(coll.objects),'state_order':STATE_ORDER}

if __name__ == '__main__':
    print(build())
