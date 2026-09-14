import bpy, math
from mathutils import Vector

WORKUNIT = 'AUR-X100-PLAIN-STORY-SITES-001'
ACCIDENT_CENTER = (-850.0, 520.0)
RESCUE_CENTER = (720.0, 520.0)

FAMILY_SPECS = {
    'MAST_BASE': ('AUR_X100_STORY_MAST_BASE_MESH',(2.4,2.4,0.45),'AUR_MAT_MINERAL_FOUNDATION','AUR-STORY-001','route recorder mast foundation','none'),
    'MAST_SPAR': ('AUR_X100_STORY_MAST_SPAR_MESH',(0.36,0.36,4.2),'AUR_MAT_STRUCTURAL_GALV_STEEL','AUR-STORY-002','instrument mast spar','impact_bend'),
    'RECORDER_CRADLE': ('AUR_X100_STORY_RECORDER_CRADLE_MESH',(1.8,0.9,0.7),'AUR_MAT_SERVICE_TRAY','AUR-STORY-003','route recorder cradle','impact_release'),
    'SERVICE_PANEL': ('AUR_X100_STORY_SERVICE_PANEL_MESH',(1.2,0.16,1.4),'AUR_MAT_CERAMIC_COMPOSITE_PANEL','AUR-STORY-004','field service panel','mount_failure'),
    'EMERGENCY_BEACON': ('AUR_X100_STORY_EMERGENCY_BEACON_MESH',(0.45,0.45,1.5),'AUR_MAT_ECHO_CYAN','AUR-STORY-005','local emergency/temporal beacon','emergency_deploy'),
    'DEBRIS_CASSETTE': ('AUR_X100_STORY_DEBRIS_CASSETTE_MESH',(0.8,0.5,0.24),'AUR_MAT_SERVICE_TRAY','AUR-STORY-006','identifiable failed cassette debris','impact_scatter'),
    'GATE_UPRIGHT': ('AUR_X100_STORY_GATE_UPRIGHT_MESH',(0.34,0.34,3.2),'AUR_MAT_STRUCTURAL_GALV_STEEL','AUR-STORY-007','rescue access frame upright','structural_gate'),
    'BARRIER_PANEL': ('AUR_X100_STORY_BARRIER_PANEL_MESH',(2.8,0.16,2.35),'AUR_MAT_CERAMIC_COMPOSITE_PANEL','AUR-STORY-008','Window A vertical-raise barrier','window_state'),
    'BRIDGE_DECK': ('AUR_X100_STORY_BRIDGE_DECK_MESH',(2.5,1.25,0.24),'AUR_MAT_STRUCTURAL_GALV_STEEL','AUR-STORY-009','telescopic rescue bridge deck segment','bridge_state'),
    'WINCH_BASE': ('AUR_X100_STORY_WINCH_BASE_MESH',(1.2,1.0,0.72),'M_AUR_TECH_DARK','AUR-STORY-010','rescue winch/service base','rescue_support'),
    'STABILIZER': ('AUR_X100_STORY_STABILIZER_MESH',(0.42,0.42,1.2),'AUR_MAT_STRUCTURAL_GALV_STEEL','AUR-STORY-011','adjustable rescue stabilizer','rescue_support'),
    'INDEX_PLATE': ('AUR_X100_STORY_INDEX_PLATE_MESH',(0.50,0.08,0.70),'AUR_MAT_CLOCK_BRONZE_CAL','AUR-STORY-012','mechanical local state/index receipt','state_index'),
    'BARRIER_PANEL_WIDE': ('AUR_X100_STORY_BARRIER_PANEL_WIDE_MESH',(3.72,0.16,2.35),'AUR_MAT_CERAMIC_COMPOSITE_PANEL','AUR-STORY-013','Window B lateral-slide barrier sized to close physical aperture','window_state'),
}

COLLISION_SPECS = [
    ('COL_AUR_STORY_ACCIDENT_FOOTPRINT_MESH',(20,16,2),'ACCIDENT','static_site_footprint'),
    ('COL_AUR_STORY_ACCIDENT_ECHO_CORRIDOR_MESH',(14,5,3),'ACCIDENT','local_echo_motion_clearance'),
    ('COL_AUR_STORY_RESCUE_GATE_A_MESH',(4.5,3.0,3.2),'RESCUE','access_window_A_clearance'),
    ('COL_AUR_STORY_RESCUE_GATE_B_MESH',(5.0,3.5,3.2),'RESCUE','access_window_B_clearance'),
    ('COL_AUR_STORY_RESCUE_BRIDGE_MESH',(9.0,3.0,2.5),'RESCUE','bridge_traversal_clearance'),
]


def ensure_collection(name):
    root = bpy.data.collections.get('ARES_IX_ROOT') or bpy.context.scene.collection
    c = bpy.data.collections.get(name)
    if not c:
        c = bpy.data.collections.new(name)
        root.children.link(c)
    return c


def box_mesh(name, dims, material, family_id, purpose, cause):
    old = bpy.data.meshes.get(name)
    if old and old.users == 0:
        bpy.data.meshes.remove(old)
    dx,dy,dz=[d/2 for d in dims]
    verts=[(-dx,-dy,-dz),(dx,-dy,-dz),(dx,dy,-dz),(-dx,dy,-dz),(-dx,-dy,dz),(dx,-dy,dz),(dx,dy,dz),(-dx,dy,dz)]
    faces=[(0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(2,6,7,3),(4,0,3,7)]
    me=bpy.data.meshes.new(name); me.from_pydata(verts,[],faces); me.update(); me.use_fake_user=True; me.materials.append(material)
    me['family_id']=family_id; me['purpose']=purpose; me['failure_cause']=cause; me['dimensions_m']=list(dims)
    me['lod_policy']='NO_EXTRA_GEOMETRIC_LOD_AT_BLOCKOUT: 12-triangle envelope; production detail must preserve envelope'
    return me


def build():
    scene=bpy.context.scene
    terrain=bpy.data.objects['AURORA_MACRO_TERRAIN']
    acc=ensure_collection('44_X100_PLAIN_ACCIDENT_SITE'); res=ensure_collection('45_X100_PLAIN_RESCUE_SITE'); qa=ensure_collection('46_X100_PLAIN_STORY_QA')
    for col in (acc,res,qa):
        for o in list(col.objects): bpy.data.objects.remove(o,do_unlink=True)

    F={}
    for key,(name,dims,mat_name,fid,purpose,cause) in FAMILY_SPECS.items():
        mat=bpy.data.materials.get(mat_name)
        if not mat: raise RuntimeError(f'Missing material {mat_name}')
        F[key]=box_mesh(name,dims,mat,fid,purpose,cause)
    foundation=bpy.data.materials['AUR_MAT_MINERAL_FOUNDATION']
    for name,dims,site,role in COLLISION_SPECS:
        me=box_mesh(name,dims,foundation,name.replace('_MESH',''),role,'collision_proxy_contract')
        me['site']=site; me['collision_role']=role; me['render_geometry']=False

    verts_world=[terrain.matrix_world@v.co for v in terrain.data.vertices]
    def tz(x,y): return min(verts_world,key=lambda v:(v.x-x)**2+(v.y-y)**2).z

    def inst(col,name,key,loc,rot=(0,0,0),site='ACCIDENT',state='AFTERMATH',default='AFTERMATH',stable_id=None,cause=None,profile=None):
        o=bpy.data.objects.new(name,F[key]); col.objects.link(o); o.location=loc; o.rotation_euler=rot
        o['x100_workunit']=WORKUNIT; o['site_id']=site; o['runtime_state']=state; o['stable_component_id']=stable_id or name; o['family_id']=F[key]['family_id']; o['family_key']=key
        o['local_temporal_authority']='LOCAL_SITE_ONLY'; o['save_state_mutation']='FORBIDDEN'; o['global_rewind']='FORBIDDEN'; o['causal_category']=cause or F[key]['failure_cause']; o['runtime_default_visible']=state==default
        if profile: o['access_window_profile']=profile
        o.hide_render=state!=default; o.hide_viewport=state!=default
        return o

    # ACCIDENT: Q_AURORA_M02 — stable recorder/mast components across PRE_EVENT, ECHO_ACTIVE, AFTERMATH.
    ax,ay=ACCIDENT_CENTER; ag=tz(ax,ay); default='AFTERMATH'
    for state in ['PRE_EVENT','ECHO_ACTIVE','AFTERMATH']:
        inst(acc,f'AUR_ACC_{state}_BASE','MAST_BASE',(ax,ay,ag+0.225),site='ACCIDENT',state=state,default=default,stable_id='ACC_BASE_001')
        angle={'PRE_EVENT':0,'ECHO_ACTIVE':24,'AFTERMATH':78}[state]; th=math.radians(angle); L=4.2; t=0.36
        sx=ax+(L/2)*math.sin(th); sz=ag+0.04+0.5*(L*abs(math.cos(th))+t*abs(math.sin(th)))
        inst(acc,f'AUR_ACC_{state}_MAST','MAST_SPAR',(sx,ay,sz),(0,th,0),'ACCIDENT',state,default,'ACC_MAST_001','impact_bend')
        if state=='PRE_EVENT':
            inst(acc,'AUR_ACC_PRE_EVENT_CRADLE','RECORDER_CRADLE',(ax+1.1,ay,ag+2.55),site='ACCIDENT',state=state,default=default,stable_id='ACC_CRADLE_001')
            inst(acc,'AUR_ACC_PRE_EVENT_PANEL','SERVICE_PANEL',(ax-0.95,ay-0.38,ag+2.2),site='ACCIDENT',state=state,default=default,stable_id='ACC_PANEL_001')
        elif state=='ECHO_ACTIVE':
            inst(acc,'AUR_ACC_ECHO_ACTIVE_CRADLE','RECORDER_CRADLE',(ax+3.0,ay+0.2,tz(ax+3,ay+0.2)+1.35),(0,math.radians(18),math.radians(5)),'ACCIDENT',state,default,'ACC_CRADLE_001','local_echo_displacement')
            inst(acc,'AUR_ACC_ECHO_ACTIVE_PANEL','SERVICE_PANEL',(ax+1.8,ay-0.7,tz(ax+1.8,ay-0.7)+0.9),(math.radians(25),0,math.radians(14)),'ACCIDENT',state,default,'ACC_PANEL_001','local_echo_displacement')
            inst(acc,'AUR_ACC_ECHO_ACTIVE_BEACON','EMERGENCY_BEACON',(ax-3.2,ay+2.8,tz(ax-3.2,ay+2.8)+0.75),site='ACCIDENT',state=state,default=default,stable_id='ACC_BEACON_001')
        else:
            inst(acc,'AUR_ACC_AFTERMATH_CRADLE','RECORDER_CRADLE',(ax+5.2,ay+0.7,tz(ax+5.2,ay+0.7)+0.42),(math.radians(8),math.radians(82),math.radians(9)),'ACCIDENT',state,default,'ACC_CRADLE_001')
            inst(acc,'AUR_ACC_AFTERMATH_PANEL','SERVICE_PANEL',(ax+6.5,ay-1.0,tz(ax+6.5,ay-1)+0.72),(math.radians(82),0,math.radians(22)),'ACCIDENT',state,default,'ACC_PANEL_001')
            inst(acc,'AUR_ACC_AFTERMATH_BEACON','EMERGENCY_BEACON',(ax-3.2,ay+2.8,tz(ax-3.2,ay+2.8)+0.75),site='ACCIDENT',state=state,default=default,stable_id='ACC_BEACON_001')
            for i,(dx,dy,rz) in enumerate([(5.8,2.2,12),(7.2,1.4,-8),(8.4,-0.6,25),(6.8,-2.5,42),(9.4,2.8,-30)]):
                inst(acc,f'AUR_ACC_AFTER_DEBRIS_{i}','DEBRIS_CASSETTE',(ax+dx,ay+dy,tz(ax+dx,ay+dy)+0.14),(0,math.radians(6+i*3),math.radians(rz)),'ACCIDENT',state,default,f'ACC_DEBRIS_{i:02d}','impact_scatter')
    inst(acc,'AUR_ACC_AFTER_INDEX','INDEX_PLATE',(ax-2.7,ay-1.2,tz(ax-2.7,ay-1.2)+0.42),site='ACCIDENT',state='AFTERMATH',default='AFTERMATH',stable_id='ACC_INDEX_001')

    # RESCUE: Q_AURORA_M03 — Window A vertical raise; Window B lateral slide; stable components across 3 states.
    rx,ry=RESCUE_CENTER; default='CLOSED'; A=(rx-5.0,ry); B=(rx+6.0,ry+5.0)
    for state in ['CLOSED','OPEN_WINDOW','MISSED_COLLAPSED']:
        for side,sx in [('L',A[0]-1.7),('R',A[0]+1.7)]:
            inst(res,f'AUR_RES_{state}_A_UPRIGHT_{side}','GATE_UPRIGHT',(sx,A[1],tz(sx,A[1])+1.6),site='RESCUE',state=state,default=default,stable_id=f'RES_GATE_A_{side}',profile='WINDOW_A_VERTICAL_RAISE')
        for side,sy in [('L',B[1]-2.1),('R',B[1]+2.1)]:
            inst(res,f'AUR_RES_{state}_B_UPRIGHT_{side}','GATE_UPRIGHT',(B[0],sy,tz(B[0],sy)+1.6),(0,0,math.radians(90)),'RESCUE',state,default,f'RES_GATE_B_{side}',profile='WINDOW_B_LATERAL_SLIDE')
        if state=='CLOSED':
            inst(res,'AUR_RES_CLOSED_A_PANEL','BARRIER_PANEL',(A[0],A[1],tz(*A)+1.25),site='RESCUE',state=state,default=default,stable_id='RES_PANEL_A',profile='WINDOW_A_VERTICAL_RAISE')
            inst(res,'AUR_RES_CLOSED_B_PANEL','BARRIER_PANEL_WIDE',(B[0],B[1],tz(*B)+1.25),(0,0,math.radians(90)),'RESCUE',state,default,'RES_PANEL_B',profile='WINDOW_B_LATERAL_SLIDE')
        elif state=='OPEN_WINDOW':
            inst(res,'AUR_RES_OPEN_A_PANEL','BARRIER_PANEL',(A[0],A[1],tz(*A)+3.55),site='RESCUE',state=state,default=default,stable_id='RES_PANEL_A',profile='WINDOW_A_VERTICAL_RAISE')
            inst(res,'AUR_RES_OPEN_B_PANEL','BARRIER_PANEL_WIDE',(B[0],B[1]+4.2,tz(B[0],B[1]+4.2)+1.25),(0,0,math.radians(90)),'RESCUE',state,default,'RES_PANEL_B',profile='WINDOW_B_LATERAL_SLIDE')
            for i in range(3):
                x=rx+0.8+i*2.4; y=ry+2.2+i*0.9
                inst(res,f'AUR_RES_OPEN_BRIDGE_{i}','BRIDGE_DECK',(x,y,tz(x,y)+0.35),(0,0,math.radians(20)),'RESCUE',state,default,f'RES_BRIDGE_{i:02d}')
        else:
            inst(res,'AUR_RES_MISSED_A_PANEL','BARRIER_PANEL',(A[0]+1.8,A[1]-0.8,tz(A[0]+1.8,A[1]-0.8)+0.18),(math.radians(83),0,math.radians(12)),'RESCUE',state,default,'RES_PANEL_A','missed_window_collapse','WINDOW_A_VERTICAL_RAISE')
            inst(res,'AUR_RES_MISSED_B_PANEL','BARRIER_PANEL_WIDE',(B[0],B[1]+2.6,tz(B[0],B[1]+2.6)+0.25),(math.radians(70),0,math.radians(90)),'RESCUE',state,default,'RES_PANEL_B','missed_window_collapse','WINDOW_B_LATERAL_SLIDE')
            for i in range(3):
                x=rx+0.8+i*2.4; y=ry+2.2+i*0.9
                inst(res,f'AUR_RES_MISSED_BRIDGE_{i}','BRIDGE_DECK',(x,y,tz(x,y)+0.18),(math.radians(12+i*8),math.radians(8),math.radians(20+i*3)),'RESCUE',state,default,f'RES_BRIDGE_{i:02d}','missed_window_collapse')
        inst(res,f'AUR_RES_{state}_WINCH','WINCH_BASE',(rx-0.5,ry-4.0,tz(rx-0.5,ry-4)+0.36),site='RESCUE',state=state,default=default,stable_id='RES_WINCH_001')
        for j,(dx,dy) in enumerate([(-2.0,-4.0),(1.1,-4.0)]):
            inst(res,f'AUR_RES_{state}_STAB_{j}','STABILIZER',(rx+dx,ry+dy,tz(rx+dx,ry+dy)+0.6),site='RESCUE',state=state,default=default,stable_id=f'RES_STAB_{j:02d}')
        inst(res,f'AUR_RES_{state}_BEACON','EMERGENCY_BEACON',(rx+3.0,ry-3.2,tz(rx+3,ry-3.2)+0.75),site='RESCUE',state=state,default=default,stable_id='RES_BEACON_001')
        inst(res,f'AUR_RES_{state}_INDEX','INDEX_PLATE',(rx-3.0,ry-3.2,tz(rx-3,ry-3.2)+0.42),site='RESCUE',state=state,default=default,stable_id='RES_INDEX_001')

    for site,states,default,center in [('ACCIDENT',['PRE_EVENT','ECHO_ACTIVE','AFTERMATH'],'AFTERMATH',ACCIDENT_CENTER),('RESCUE',['CLOSED','OPEN_WINDOW','MISSED_COLLAPSED'],'CLOSED',RESCUE_CENTER)]:
        e=bpy.data.objects.new(f'META_AUR_STORY_{site}',None); qa.objects.link(e); e.hide_render=True; e.hide_viewport=True
        e['site_id']=site; e['states']='|'.join(states); e['default_state']=default; e['local_temporal_authority']='LOCAL_SITE_ONLY'; e['global_rewind']='FORBIDDEN'; e['save_state_mutation']='FORBIDDEN'; e['center_xy']=list(center)

    scene['x100_protocol']='EXOVANT-X100-v1'; scene['x100_last_workunit']=WORKUNIT; scene['status']='X100_PLAIN_STORY_SITES_R34_WINDOW_B_QA'; scene['plain_story_family_count']=13
    return {'status':scene['status'],'families':len(F),'accident_objects':len(acc.objects),'rescue_objects':len(res.objects)}

if __name__ == '__main__':
    print(build())
