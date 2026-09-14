import bpy, math
from mathutils import Vector

WORKUNIT = 'AUR-X100-CAMP-HISTORY-001'
SELECTED_HOSTS = [0, 3, 4, 6, 9, 11]

FAMILY_SPECS = {
    'REPAIR_PLATE': ('AUR_X100_HIST_REPAIR_PLATE_MESH', (1.20,0.06,0.80), 'AUR_MAT_STRUCTURAL_GALV_STEEL', 'AUR-HIST-001', 'impact_or_local_panel_failure'),
    'CLAMP': ('AUR_X100_HIST_EXTERNAL_CLAMP_MESH', (0.32,0.18,0.55), 'AUR_MAT_STRUCTURAL_GALV_STEEL', 'AUR-HIST-002', 'joint_slip_or_frame_crack'),
    'REPLACEMENT_PANEL': ('AUR_X100_HIST_REPLACEMENT_PANEL_MESH', (1.80,0.08,1.40), 'AUR_MAT_CERAMIC_COMPOSITE_PANEL', 'AUR-HIST-003', 'weather_or_impact_panel_replacement'),
    'DRAIN_SCUPPER': ('AUR_X100_HIST_DRAIN_SCUPPER_MESH', (1.40,0.35,0.20), 'AUR_MAT_SERVICE_TRAY', 'AUR-HIST-004', 'moisture_accumulation'),
    'CABLE_SEGMENT': ('AUR_X100_HIST_CABLE_BYPASS_SEGMENT_MESH', (1.20,0.08,0.08), 'AUR_MAT_CABLE_DATA_JACKET', 'AUR-HIST-005', 'service_reroute'),
    'GASKET_STRIP': ('AUR_X100_HIST_GASKET_SEAL_MESH', (1.80,0.05,0.08), 'AUR_MAT_EPDM_GASKET', 'AUR-HIST-006', 'seal_failure'),
    'INDEX_TAB': ('AUR_X100_HIST_INDEX_TAB_MESH', (0.36,0.06,0.50), 'AUR_MAT_CLOCK_BRONZE_CAL', 'AUR-HIST-007', 'recalibration_or_component_swap'),
    'ROOT_GUARD': ('AUR_X100_HIST_ROOT_GUARD_MESH', (1.50,0.50,0.12), 'AUR_MAT_STRUCTURAL_GALV_STEEL', 'AUR-HIST-008', 'vegetation_encroachment'),
}


def _ensure_collection(name):
    root = bpy.data.collections.get('ARES_IX_ROOT') or bpy.context.scene.collection
    col = bpy.data.collections.get(name)
    if not col:
        col = bpy.data.collections.new(name)
        root.children.link(col)
    return col


def _box_mesh(name, dims, material, family_id, cause):
    old = bpy.data.meshes.get(name)
    if old and old.users == 0:
        bpy.data.meshes.remove(old)
    dx,dy,dz = [d/2 for d in dims]
    verts=[(-dx,-dy,-dz),(dx,-dy,-dz),(dx,dy,-dz),(-dx,dy,-dz),(-dx,-dy,dz),(dx,-dy,dz),(dx,dy,dz),(-dx,dy,dz)]
    faces=[(0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(2,6,7,3),(4,0,3,7)]
    me=bpy.data.meshes.new(name); me.from_pydata(verts,[],faces); me.update(); me.use_fake_user=True
    me.materials.append(material)
    me['family_id']=family_id
    me['failure_cause']=cause
    me['dimensions_m']=list(dims)
    me['lod_policy']='NO_EXTRA_GEOMETRIC_LOD_AT_BLOCKOUT: 12-triangle source; preserve envelope until production detail exists'
    me['collision_policy']='SIMPLE_BOX_OR_NONE_BY_GAMEPLAY; engine instantiation BLOCKED_EXO_012'
    return me


def build():
    scene=bpy.context.scene
    proof=_ensure_collection('42_X100_CAMP_HISTORY_PROOF')
    qa=_ensure_collection('43_X100_CAMP_HISTORY_QA')
    for col in (proof,qa):
        for o in list(col.objects): bpy.data.objects.remove(o,do_unlink=True)

    materials={m:bpy.data.materials.get(m) for _,_,m,_,_ in FAMILY_SPECS.values()}
    missing=[k for k,v in materials.items() if not v]
    if missing: raise RuntimeError(f'Missing materials: {missing}')

    families={}
    for key,(name,dims,mat_name,fid,cause) in FAMILY_SPECS.items():
        families[key]=_box_mesh(name,dims,materials[mat_name],fid,cause)

    terrain=bpy.data.objects['AURORA_MACRO_TERRAIN']
    verts_world=[terrain.matrix_world @ v.co for v in terrain.data.vertices]
    def terrain_z(x,y):
        return min(verts_world,key=lambda v:(v.x-x)**2+(v.y-y)**2).z

    def inst(name,key,loc,rot=(0,0,0),era='ERA_1',host=None,cause=None,state='ACTIVE'):
        o=bpy.data.objects.new(name,families[key]); proof.objects.link(o); o.location=loc; o.rotation_euler=rot
        o['x100_workunit']=WORKUNIT; o['family_key']=key; o['family_id']=families[key]['family_id']; o['era']=era; o['host_config']=host
        o['causal_category']=cause or families[key]['failure_cause']; o['history_state']=state
        return o

    def cable_route(prefix,points,host,era):
        objs=[]
        for i in range(len(points)-1):
            a,b=Vector(points[i]),Vector(points[i+1]); d=b-a; n=max(1,round(d.length/1.2))
            for j in range(n):
                p=a.lerp(b,(j+0.5)/n); o=inst(f'{prefix}_{i}_{j}','CABLE_SEGMENT',p,era=era,host=host,cause='service_reroute')
                o.rotation_euler=d.to_track_quat('X','Z').to_euler(); objs.append(o)
        return objs

    for idx in SELECTED_HOSTS:
        floors=[o for o in bpy.data.objects if o.name.startswith(f'AUR_X100_CAMP_CONFIG_{idx:02d}_FLOOR_')]
        if not floors: raise RuntimeError(f'Host {idx} floors missing')
        xmin=min(o.matrix_world.translation.x-o.dimensions.x/2 for o in floors); xmax=max(o.matrix_world.translation.x+o.dimensions.x/2 for o in floors)
        ymin=min(o.matrix_world.translation.y-o.dimensions.y/2 for o in floors); ymax=max(o.matrix_world.translation.y+o.dimensions.y/2 for o in floors)
        floor_top=max(o.matrix_world.translation.z+o.dimensions.z/2 for o in floors); wall_z=floor_top+1.60; cx=(xmin+xmax)/2; cy=(ymin+ymax)/2
        if idx==0:
            inst('AUR_HIST_00_REPLACEMENT_PANEL','REPLACEMENT_PANEL',(cx-1.4,ymin-0.08,wall_z),era='ERA_1',host=idx)
            inst('AUR_HIST_00_INDEX_TAB','INDEX_TAB',(cx+2.1,ymin-0.13,wall_z+0.25),era='ERA_1',host=idx)
            inst('AUR_HIST_00_DRAIN','DRAIN_SCUPPER',(xmax-1.0,ymin-0.24,floor_top+0.18),era='ERA_2',host=idx)
            inst('AUR_HIST_00_ROOT_GUARD','ROOT_GUARD',(xmin+1.1,ymin-0.55,terrain_z(xmin+1.1,ymin-0.55)+0.06),era='ERA_2',host=idx)
        elif idx==3:
            inst('AUR_HIST_03_PLATE','REPAIR_PLATE',(cx-1.1,ymin-0.13,wall_z),era='ERA_1',host=idx)
            inst('AUR_HIST_03_CLAMP','CLAMP',(xmin+0.16,ymin-0.20,wall_z+0.7),era='ERA_1',host=idx)
            inst('AUR_HIST_03_GASKET','GASKET_STRIP',(cx+1.2,ymin-0.19,wall_z-0.55),era='ERA_2',host=idx)
            cable_route('AUR_HIST_03_BYPASS',[(xmax+0.15,cy-2,floor_top+0.5),(xmax+0.15,cy-2,wall_z+0.8),(xmax+0.15,cy+1.5,wall_z+0.8)],idx,'ERA_2')
        elif idx==4:
            inst('AUR_HIST_04_PANEL','REPLACEMENT_PANEL',(xmax+0.09,cy,wall_z),(0,0,math.radians(90)),'ERA_1',idx)
            cable_route('AUR_HIST_04_BYPASS',[(xmin-0.15,cy-2,floor_top+0.6),(xmin-0.15,cy-2,wall_z+0.7),(xmin-0.15,cy+2.2,wall_z+0.7)],idx,'ERA_1')
            inst('AUR_HIST_04_DRAIN','DRAIN_SCUPPER',(cx+2.4,ymin-0.24,floor_top+0.18),era='ERA_2',host=idx)
            inst('AUR_HIST_04_ROOT_GUARD','ROOT_GUARD',(xmax-1.1,ymin-0.55,terrain_z(xmax-1.1,ymin-0.55)+0.06),era='ERA_2',host=idx)
        elif idx==6:
            inst('AUR_HIST_06_PLATE','REPAIR_PLATE',(cx,ymin-0.14,wall_z+0.1),era='ERA_1',host=idx)
            inst('AUR_HIST_06_CLAMP_A','CLAMP',(cx-1.5,ymin-0.20,wall_z+0.75),era='ERA_1',host=idx)
            inst('AUR_HIST_06_CLAMP_B','CLAMP',(cx+1.5,ymin-0.20,wall_z+0.75),era='ERA_1',host=idx)
            cable_route('AUR_HIST_06_BYPASS',[(xmax+0.15,cy-2.5,floor_top+0.6),(xmax+0.15,cy-2.5,wall_z+0.9),(xmax+0.15,cy+2.5,wall_z+0.9)],idx,'ERA_2')
            inst('AUR_HIST_06_GASKET','GASKET_STRIP',(cx,ymin-0.19,wall_z-0.7),era='ERA_2',host=idx)
        elif idx==9:
            inst('AUR_HIST_09_PANEL','REPLACEMENT_PANEL',(cx+1.4,ymin-0.08,wall_z),era='ERA_1',host=idx)
            inst('AUR_HIST_09_PLATE','REPAIR_PLATE',(cx-1.5,ymin-0.13,wall_z-0.2),era='ERA_1',host=idx)
            inst('AUR_HIST_09_DRAIN_LOOSE','DRAIN_SCUPPER',(xmax-1.2,ymin-0.45,terrain_z(xmax-1.2,ymin-0.45)+0.16),(math.radians(9),0,math.radians(4)),'ERA_2',idx,'deferred_maintenance','LOOSENED')
            inst('AUR_HIST_09_ROOT_GUARD','ROOT_GUARD',(xmin+1.0,ymin-0.55,terrain_z(xmin+1.0,ymin-0.55)+0.06),era='ERA_2',host=idx)
        elif idx==11:
            cable_route('AUR_HIST_11_BYPASS',[(xmin-0.15,cy-3,floor_top+0.5),(xmin-0.15,cy-3,wall_z+0.8),(xmin-0.15,cy+2,wall_z+0.8)],idx,'ERA_1')
            inst('AUR_HIST_11_CLAMP','CLAMP',(xmax-0.2,ymin-0.20,wall_z+0.7),era='ERA_1',host=idx)
            inst('AUR_HIST_11_INDEX_FALLEN','INDEX_TAB',(cx+1.2,ymin-0.7,terrain_z(cx+1.2,ymin-0.7)+0.27),(math.radians(78),0,math.radians(11)),'ERA_2',idx,'deferred_maintenance','DETACHED')
            inst('AUR_HIST_11_ROOT_GUARD','ROOT_GUARD',(xmax-1.2,ymin-0.60,terrain_z(xmax-1.2,ymin-0.6)+0.06),era='ERA_2',host=idx)

    scene['x100_protocol']='EXOVANT-X100-v1'; scene['x100_last_workunit']=WORKUNIT; scene['status']='X100_CAMP_HISTORY_R32'
    return {'status':scene['status'],'proof_objects':len(proof.objects),'source_families':len(families)}

if __name__ == '__main__':
    print(build())
