import bpy, math, json

WORKUNIT = 'AUR-X100-OBSERVATORY-INTERIOR-001'
CENTER = (-1520.0, 550.0)
GRID_M = 4.0
FOOTPRINT_M = (12.0, 12.0)

INTERIOR_SPECS = {
    'CONSOLE': ('AUR_X100_INT_CONSOLE_FRAME_MESH',(2.4,0.78,0.88),'AUR_MAT_STRUCTURAL_GALV_STEEL','AUR-INT-001','calibration/readout console structural frame','bent sheet metal + removable service panels'),
    'ARCHIVE_RACK': ('AUR_X100_INT_ARCHIVE_RACK_MESH',(1.2,0.48,2.0),'AUR_MAT_STRUCTURAL_GALV_STEEL','AUR-INT-002','route/archive cartridge rack','galvanized folded frame + bolted shelves'),
    'SERVICE_CAB': ('AUR_X100_INT_SERVICE_CABINET_MESH',(1.1,0.62,2.0),'AUR_MAT_SERVICE_TRAY','AUR-INT-003','maintenance consumables and patch cabinet','folded service-metal cabinet + replaceable drawers'),
    'PEDESTAL': ('AUR_X100_INT_INSTRUMENT_PEDESTAL_MESH',(0.86,0.86,1.05),'AUR_MAT_CERAMIC_COMPOSITE_PANEL','AUR-INT-004','isolated instrument pedestal','prefab ceramic composite shell over steel subframe'),
    'WALL_RAIL': ('AUR_X100_INT_WALL_SERVICE_RAIL_MESH',(4.0,0.18,0.28),'AUR_MAT_STRUCTURAL_GALV_STEEL','AUR-INT-005','wall service mounting rail','extruded/rolled galvanized rail'),
    'TRENCH_COVER': ('AUR_X100_INT_CABLE_TRENCH_COVER_MESH',(2.0,0.55,0.08),'AUR_MAT_SERVICE_TRAY','AUR-INT-006','removable floor cable trench cover','pressed checker service plate'),
    'BUS_TRAY': ('AUR_X100_INT_OVERHEAD_BUS_TRAY_MESH',(4.0,0.35,0.25),'AUR_MAT_SERVICE_TRAY','AUR-INT-007','overhead power/data distribution tray','folded perforated service tray'),
    'BAFFLE': ('AUR_X100_INT_PARTITION_BAFFLE_MESH',(2.0,0.12,2.2),'AUR_MAT_CERAMIC_COMPOSITE_PANEL','AUR-INT-008','acoustic/optical equipment baffle, non-load-bearing','removable ceramic composite cassette'),
    'ACCESS_PANEL': ('AUR_X100_INT_FLOOR_ACCESS_PANEL_MESH',(1.0,1.0,0.08),'AUR_MAT_SERVICE_TRAY','AUR-INT-009','lift-out floor service access','pressed service-metal cassette'),
    'LIGHT': ('AUR_X100_INT_LIGHT_FIXTURE_MESH',(1.2,0.22,0.10),'AUR_X100_MAT_INT_TASK_LIGHT','AUR-INT-010','replaceable task/egress light fixture','sealed linear housing + removable caps'),
    'SHELF': ('AUR_X100_INT_ARCHIVE_SHELF_INSERT_MESH',(1.0,0.35,0.08),'AUR_MAT_STRUCTURAL_GALV_STEEL','AUR-INT-011','removable archive shelf insert','folded galvanized shelf'),
    'PATCH_PANEL': ('AUR_X100_INT_SERVICE_PATCH_PANEL_MESH',(0.72,0.12,1.0),'M_AUR_TECH_DARK','AUR-INT-012','physical data/service patch field','replaceable instrument-polymer face over service chassis'),
}

SHELL_MESHES = [
    'AUR_X100_ARC_FLOOR_4X4_MESH','AUR_X100_ARC_WALL_SOLID_4M_MESH','AUR_X100_ARC_WALL_SERVICE_4M_MESH',
    'AUR_X100_ARC_WALL_WINDOW_4M_MESH','AUR_X100_ARC_ROOF_FLAT_4X4_MESH','AUR_X100_ARC_ROOF_SERVICE_4X4_MESH'
]

PROP_MESHES = [
    'AUR_X100_PRP_CALIBRATION_TABLE_MESH','AUR_X100_PRP_PHASE_WHEEL_MESH','AUR_X100_PRP_CLOCK_CASE_MESH','AUR_X100_PRP_PENDULUM_FRAME_MESH',
    'AUR_X100_PRP_ARCHIVE_TRAY_MESH','AUR_X100_PRP_RECORD_CANISTER_MESH','AUR_X100_PRP_ROUTE_CARTRIDGE_MESH','AUR_X100_PRP_FIELD_LOG_SLATE_MESH',
    'AUR_X100_PRP_TOOL_CHEST_MESH','AUR_X100_PRP_CABLE_SPOOL_MESH','AUR_X100_PRP_PARTS_TRAY_MESH','AUR_X100_PRP_PATCH_CASE_MESH',
    'AUR_X100_PRP_OPTICAL_CRADLE_MESH','AUR_X100_PRP_LENS_CASE_MESH','AUR_X100_PRP_PORTABLE_LAMP_MESH','AUR_X100_PRP_SERVICE_TROLLEY_MESH'
]


def ensure_collection(name):
    scene = bpy.context.scene
    col = bpy.data.collections.get(name)
    if not col:
        col = bpy.data.collections.new(name)
        scene.collection.children.link(col)
    return col


def box_mesh(name, dims, material, family_id, purpose, manufacturing):
    old = bpy.data.meshes.get(name)
    if old and old.users == 0:
        bpy.data.meshes.remove(old)
    dx,dy,dz = [d/2 for d in dims]
    vs=[(-dx,-dy,-dz),(dx,-dy,-dz),(dx,dy,-dz),(-dx,dy,-dz),(-dx,-dy,dz),(dx,-dy,dz),(dx,dy,dz),(-dx,dy,dz)]
    fs=[(0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(2,6,7,3),(4,0,3,7)]
    me=bpy.data.meshes.new(name); me.from_pydata(vs,[],fs); me.update(); me.use_fake_user=True; me.materials.append(material)
    me['family_id']=family_id; me['purpose']=purpose; me['manufacturing']=manufacturing; me['dimensions_m']=list(dims)
    me['history_states']='PRISTINE|USED|REPAIRED|ISOLATED'
    me['wear_contract']='cause-driven only: handling/contact/dust/service access; no uniform grunge'
    me['lod_policy']='NO_EXTRA_GEOMETRIC_LOD_AT_BLOCKOUT: 12-triangle envelope; future production detail must preserve envelope'
    return me


def build():
    scene=bpy.context.scene; cx,cy=CENTER
    terrain=bpy.data.objects.get('AURORA_MACRO_TERRAIN')
    if not terrain: raise RuntimeError('AURORA_MACRO_TERRAIN missing')
    proof=ensure_collection('48_X100_OBSERVATORY_INTERIOR_PROOF'); lighting=ensure_collection('50_X100_OBSERVATORY_INTERIOR_LIGHTING')
    for col in (proof,lighting):
        for o in list(col.objects): bpy.data.objects.remove(o,do_unlink=True)
    for me in list(bpy.data.meshes):
        if (me.name.startswith('AUR_X100_INT_') or me.name.startswith('COL_AUR_INT_')) and me.users==0:
            bpy.data.meshes.remove(me)

    light_mat=bpy.data.materials.get('AUR_X100_MAT_INT_TASK_LIGHT')
    if not light_mat:
        light_mat=bpy.data.materials.new('AUR_X100_MAT_INT_TASK_LIGHT'); light_mat.use_nodes=True
    p=light_mat.node_tree.nodes.get('Principled BSDF'); p.inputs['Base Color'].default_value=(0.62,0.54,0.40,1); p.inputs['Roughness'].default_value=0.42; p.inputs['Metallic'].default_value=0.05; p.inputs['Emission Color'].default_value=(1.0,0.72,0.42,1); p.inputs['Emission Strength'].default_value=2.2
    light_mat['manufacturing']='sealed replaceable task-light strip'; light_mat['wear_causality']='dust on upper housing; handling at removable end caps'

    for n in SHELL_MESHES+PROP_MESHES+['AUR_X100_HIST_REPAIR_PLATE_MESH','AUR_X100_HIST_GASKET_SEAL_MESH']:
        if not bpy.data.meshes.get(n): raise RuntimeError('required source missing: '+n)

    mats={'AUR_X100_MAT_INT_TASK_LIGHT':light_mat}
    for _,_,mat_name,_,_,_ in INTERIOR_SPECS.values():
        if mat_name not in mats:
            m=bpy.data.materials.get(mat_name)
            if not m: raise RuntimeError('material missing: '+mat_name)
            mats[mat_name]=m
    F={k:box_mesh(name,dims,mats[mat],fid,purpose,mfg) for k,(name,dims,mat,fid,purpose,mfg) in INTERIOR_SPECS.items()}
    foundation=bpy.data.materials.get('AUR_MAT_MINERAL_FOUNDATION')
    collision_specs=[
        ('COL_AUR_INT_FOOTPRINT_MESH',(12,12,3.6),'control_annex_footprint'),('COL_AUR_INT_AISLE_NS_MESH',(2,10,2.2),'central_north_south_aisle_clearance'),
        ('COL_AUR_INT_AISLE_EW_MESH',(10,2,2.2),'central_east_west_aisle_clearance'),('COL_AUR_INT_ENTRY_MESH',(4,2.5,2.4),'south_entry_clearance'),
        ('COL_AUR_INT_CAL_SERVICE_MESH',(3.2,2,2.2),'calibration_service_clearance'),('COL_AUR_INT_ARCHIVE_SERVICE_MESH',(2,4,2.2),'archive_service_clearance')]
    for name,dims,role in collision_specs:
        me=box_mesh(name,dims,foundation,name.replace('_MESH',''),role,'QA contract volume'); me['render_geometry']=False; me['collision_role']=role

    tv=[terrain.matrix_world@v.co for v in terrain.data.vertices]
    def tz(x,y): return min(tv,key=lambda v:(v.x-x)**2+(v.y-y)**2).z
    support_local=[-6,-2,2,6]; samples=[tz(cx+x,cy+y) for x in support_local for y in support_local]
    platform=max(samples)+0.35; floor_center=platform+0.23; floor_top=platform+0.46; wall_center=floor_top+1.60; wall_top=floor_top+3.20; roof_center=wall_top+0.14

    def obj(name,mesh,loc,rot=0,zone='GENERAL',purpose=None,reused=None):
        me=bpy.data.meshes[mesh] if isinstance(mesh,str) else mesh
        o=bpy.data.objects.new(name,me); proof.objects.link(o); o.location=loc; o.rotation_euler=(0,0,math.radians(rot)); o['x100_workunit']=WORKUNIT; o['zone']=zone; o['proof_state']='USED_OPERATIONAL'
        if purpose: o['functional_purpose']=purpose
        if reused: o['reused_qualified_family']=reused
        return o
    def src(name,key,lx,ly,zoff=None,rot=0,zone='GENERAL',purpose=None):
        dz=F[key]['dimensions_m'][2]; z=floor_top+(dz/2 if zoff is None else zoff)
        return obj(name,F[key],(cx+lx,cy+ly,z),rot,zone,purpose)
    def prop(name,mesh,lx,ly,z,rot,zone,purpose): return obj(name,mesh,(cx+lx,cy+ly,z),rot,zone,purpose,mesh)

    # Foundation piers with physical support contact.
    for ix,x in enumerate(support_local):
        for iy,y in enumerate(support_local):
            wz=tz(cx+x,cy+y); h=platform-(wz+0.08)
            me=box_mesh(f'AUR_X100_INT_FOUNDATION_PIER_{ix}_{iy}_MESH',(0.42,0.42,h),mats['AUR_MAT_STRUCTURAL_GALV_STEEL'],'AUR-INT-013','terrain-adjusted annex support pier','cut-to-length galvanized post + bolted foot')
            o=obj(f'AUR_INT_PIER_{ix}_{iy}',me,(cx+x,cy+y,wz+0.08+h/2),0,'FOUNDATION'); o['pier_length_m']=h

    # 12x12 shell on 4m grid; centered south entry remains open.
    for ix,x in enumerate([-4,0,4]):
        for iy,y in enumerate([-4,0,4]): obj(f'AUR_INT_FLOOR_{ix}_{iy}','AUR_X100_ARC_FLOOR_4X4_MESH',(cx+x,cy+y,floor_center),0,'SHELL')
    for i,x in enumerate([-4,0,4]): obj(f'AUR_INT_WALL_N_{i}','AUR_X100_ARC_WALL_WINDOW_4M_MESH',(cx+x,cy+6,wall_center),0,'SHELL')
    for i,y in enumerate([-4,0,4]):
        obj(f'AUR_INT_WALL_W_{i}','AUR_X100_ARC_WALL_SERVICE_4M_MESH',(cx-6,cy+y,wall_center),90,'SHELL'); obj(f'AUR_INT_WALL_E_{i}','AUR_X100_ARC_WALL_SOLID_4M_MESH',(cx+6,cy+y,wall_center),90,'SHELL')
    for i,x in enumerate([-4,4]): obj(f'AUR_INT_WALL_S_{i}','AUR_X100_ARC_WALL_SOLID_4M_MESH',(cx+x,cy-6,wall_center),0,'SHELL')
    for ix,x in enumerate([-4,0,4]):
        for iy,y in enumerate([-4,0,4]): obj(f'AUR_INT_ROOF_{ix}_{iy}','AUR_X100_ARC_ROOF_SERVICE_4X4_MESH' if (ix+iy)%2 else 'AUR_X100_ARC_ROOF_FLAT_4X4_MESH',(cx+x,cy+y,roof_center),0,'SHELL')

    # Four readable functional zones.
    cal=src('AUR_INT_CAL_CONSOLE','CONSOLE',-4.35,-2.7,zone='CALIBRATION',purpose='mechanical timing calibration')
    src('AUR_INT_CAL_PEDESTAL','PEDESTAL',-4.4,-4.2,zone='CALIBRATION',purpose='isolated timing instrument')
    rack0=src('AUR_INT_ARCHIVE_RACK_0','ARCHIVE_RACK',4.95,2.4,rot=90,zone='ROUTE_ARCHIVE',purpose='route-state archive')
    rack1=src('AUR_INT_ARCHIVE_RACK_1','ARCHIVE_RACK',4.95,4.1,rot=90,zone='ROUTE_ARCHIVE',purpose='route-state archive')
    svc=src('AUR_INT_SERVICE_CAB','SERVICE_CAB',4.45,-4.25,zone='INSTRUMENT_SERVICE',purpose='repair consumables')
    patch=src('AUR_INT_PATCH_PANEL','PATCH_PANEL',5.72,-1.8,rot=90,zone='INSTRUMENT_SERVICE',purpose='data/service patch field')
    obs=src('AUR_INT_OBS_CONSOLE','CONSOLE',-3.8,4.55,zone='OBSERVATION_READOUT',purpose='observatory readout desk')
    ped=src('AUR_INT_OBS_PEDESTAL','PEDESTAL',-5.0,2.75,zone='OBSERVATION_READOUT',purpose='optical instrument isolation')
    src('AUR_INT_BAFFLE_W','BAFFLE',-2.35,3.65,rot=90,zone='OBSERVATION_READOUT')
    src('AUR_INT_BAFFLE_E','BAFFLE',2.8,-3.7,rot=90,zone='INSTRUMENT_SERVICE')
    service_console=src('AUR_INT_SERVICE_CONSOLE_R36','CONSOLE',3.55,-2.65,zone='INSTRUMENT_SERVICE',purpose='service inspection/parts console')

    # Floor service routing stays outside the central cross.
    for i,(x,y,rot) in enumerate([(-3.8,-1.4,90),(-3.8,1.5,90),(3.8,-1.5,90),(3.8,1.5,90)]): src(f'AUR_INT_TRENCH_{i}','TRENCH_COVER',x,y,0.04,rot,'SERVICE_ROUTING')
    for i,(x,y) in enumerate([(-4.7,-0.8),(-4.7,0.8),(4.7,-0.8),(4.7,0.8)]): src(f'AUR_INT_ACCESS_{i}','ACCESS_PANEL',x,y,0.04,0,'SERVICE_ROUTING')
    for side,x in [('W',-5.78),('E',5.78)]:
        for j,y in enumerate([-2,2]): src(f'AUR_INT_RAIL_{side}_{j}','WALL_RAIL',x,y,1.35,90,'SERVICE_ROUTING')
    for side,x in [('W',-4.8),('E',4.8)]:
        for j,y in enumerate([-2,2]): src(f'AUR_INT_BUS_{side}_{j}','BUS_TRAY',x,y,wall_top-floor_top-0.25,90,'SERVICE_ROUTING')

    # Archive shelves make all media physically supported.
    shelves=[]
    for r,(x,y) in enumerate([(4.95,2.4),(4.95,4.1)]):
        for level,zoff in enumerate([0.45,1.00,1.55]): shelves.append(src(f'AUR_INT_ARCHIVE_SHELF_{r}_{level}','SHELF',x,y,zoff,90,'ROUTE_ARCHIVE','removable archive shelf'))

    # Motivated task lights only; portable POINT lights accompany fixtures.
    for i,(x,y) in enumerate([(-3,-1.2),(3,-1.2),(-3,3.1),(3,3.1)]):
        fixture=src(f'AUR_INT_LIGHT_FIXTURE_{i}','LIGHT',x,y,wall_top-floor_top-0.08,0,'LIGHTING')
        bpy.ops.object.light_add(type='POINT',location=(cx+x,cy+y,wall_top-0.35)); L=bpy.context.object; L.name=f'AUR_INT_TASK_LIGHT_{i}'; L.data.energy=120; L.data.color=(1.0,0.73,0.46); L.data.shadow_soft_size=1.1
        for c in list(L.users_collection): c.objects.unlink(L)
        lighting.objects.link(L); L['x100_workunit']=WORKUNIT; L['motivated_by']=fixture.name

    # Reuse r30 cultural props; no duplicated source meshes.
    table=prop('AUR_INT_PROP_CAL_TABLE','AUR_X100_PRP_CALIBRATION_TABLE_MESH',-3.6,-3.7,floor_top+0.45,0,'CALIBRATION','instrument working surface')
    phase=prop('AUR_INT_PROP_PHASE_WHEEL','AUR_X100_PRP_PHASE_WHEEL_MESH',-4.75,-2.70,floor_top+0.88,0,'CALIBRATION','phase calibration wheel'); phase.location.z=floor_top+0.88+phase.dimensions.z/2; phase['support_object']=cal.name
    clock=prop('AUR_INT_PROP_CLOCK_CASE','AUR_X100_PRP_CLOCK_CASE_MESH',-4.02,-2.70,floor_top+0.88,0,'CALIBRATION','clock calibration case'); clock.location.z=floor_top+0.88+clock.dimensions.z/2; clock['support_object']=cal.name
    prop('AUR_INT_PROP_PENDULUM','AUR_X100_PRP_PENDULUM_FRAME_MESH',-5.0,-4.55,floor_top+0.575,0,'CALIBRATION','pendulum timing reference')
    canisters=[]
    for i in range(4):
        r=0 if i<2 else 1; x=4.95+(-0.09 if i%2==0 else 0.09); y=2.4 if r==0 else 4.1; shelf=shelves[r*3]; top=shelf.location.z+shelf.dimensions.z/2
        o=prop(f'AUR_INT_PROP_CANISTER_{i}','AUR_X100_PRP_RECORD_CANISTER_MESH',x,y,top,90,'ROUTE_ARCHIVE','route observation record'); o.location.z=top+o.dimensions.z/2; o['support_object']=shelf.name; canisters.append(o)
    for i in range(3):
        r=0 if i<2 else 1; x=4.95+(-0.10 if i%2==0 else 0.10); y=2.4 if r==0 else 4.1; shelf=shelves[r*3+1]; top=shelf.location.z+shelf.dimensions.z/2
        o=prop(f'AUR_INT_PROP_ROUTE_CART_{i}','AUR_X100_PRP_ROUTE_CARTRIDGE_MESH',x,y,top,90,'ROUTE_ARCHIVE','route recorder cartridge'); o.location.z=top+o.dimensions.z/2; o['support_object']=shelf.name
    tray=prop('AUR_INT_PROP_ARCHIVE_TRAY','AUR_X100_PRP_ARCHIVE_TRAY_MESH',3.15,5.0,floor_top,0,'ROUTE_ARCHIVE','active archive tray'); tray.location.z=floor_top+tray.dimensions.z/2
    log=prop('AUR_INT_PROP_LOG_SLATE','AUR_X100_PRP_FIELD_LOG_SLATE_MESH',4.95,4.1,shelves[5].location.z,90,'ROUTE_ARCHIVE','field route log'); log.location.z=shelves[5].location.z+shelves[5].dimensions.z/2+log.dimensions.z/2; log['support_object']=shelves[5].name
    prop('AUR_INT_PROP_TOOL_CHEST','AUR_X100_PRP_TOOL_CHEST_MESH',4.1,-4.9,floor_top+0.29,0,'INSTRUMENT_SERVICE','repair tools')
    prop('AUR_INT_PROP_CABLE_SPOOL','AUR_X100_PRP_CABLE_SPOOL_MESH',3.0,-4.7,floor_top+0.20,0,'INSTRUMENT_SERVICE','service cable stock')
    parts=prop('AUR_INT_PROP_PARTS_TRAY','AUR_X100_PRP_PARTS_TRAY_MESH',3.55,-2.65,floor_top+0.88,0,'INSTRUMENT_SERVICE','small replaceable parts'); parts.location.z=floor_top+0.88+parts.dimensions.z/2; parts['support_object']=service_console.name
    prop('AUR_INT_PROP_PATCH_CASE','AUR_X100_PRP_PATCH_CASE_MESH',3.2,-3.4,floor_top+0.13,0,'INSTRUMENT_SERVICE','field repair patches')
    prop('AUR_INT_PROP_TROLLEY','AUR_X100_PRP_SERVICE_TROLLEY_MESH',2.7,-4.1,floor_top+0.525,0,'INSTRUMENT_SERVICE','movable maintenance support')
    cradle=prop('AUR_INT_PROP_OPTICAL_CRADLE','AUR_X100_PRP_OPTICAL_CRADLE_MESH',-5.0,2.75,ped.location.z+ped.dimensions.z/2,0,'OBSERVATION_READOUT','optical instrument cradle'); cradle.location.z=ped.location.z+ped.dimensions.z/2+cradle.dimensions.z/2; cradle['support_object']=ped.name
    lens=prop('AUR_INT_PROP_LENS_CASE','AUR_X100_PRP_LENS_CASE_MESH',-3.45,4.55,floor_top+0.88,0,'OBSERVATION_READOUT','protected optical element'); lens.location.z=floor_top+0.88+lens.dimensions.z/2; lens['support_object']=obs.name
    lamp=prop('AUR_INT_PROP_PORTABLE_LAMP','AUR_X100_PRP_PORTABLE_LAMP_MESH',-2.9,4.35,floor_top+1.07,0,'OBSERVATION_READOUT','local task lamp')
    # Ensure lamp sits exactly on observation console if source height differs from prior proof.
    lamp.location.z=floor_top+0.88+lamp.dimensions.z/2; lamp['support_object']=obs.name

    # Two physical repair receipts from r32, not decoration.
    repair=obj('AUR_INT_REPAIR_PLATE','AUR_X100_HIST_REPAIR_PLATE_MESH',(cx-5.85,cy-2.8,wall_center+0.2),90,'INSTRUMENT_SERVICE','older internal frame repair'); repair['era']='ERA_1_REPAIR'; repair['causal_category']='local_frame_repair'
    gasket=obj('AUR_INT_REPAIR_GASKET','AUR_X100_HIST_GASKET_SEAL_MESH',(cx+5.84,cy+2.4,wall_center-0.55),90,'ROUTE_ARCHIVE','weather-seal retrofit'); gasket['era']='ERA_1_REPAIR'; gasket['causal_category']='seal_failure'

    # Wall/ceiling service spines.
    def cable(name,pts,mat,role):
        cu=bpy.data.curves.new(name+'_CURVE','CURVE'); cu.dimensions='3D'; cu.bevel_depth=0.025; cu.bevel_resolution=2; sp=cu.splines.new('POLY'); sp.points.add(len(pts)-1)
        for i,p in enumerate(pts): sp.points[i].co=(*p,1)
        cu.materials.append(mat); o=bpy.data.objects.new(name,cu); proof.objects.link(o); o['x100_workunit']=WORKUNIT; o['zone']='SERVICE_ROUTING'; o['route_role']=role; return o
    cable('AUR_INT_DATA_SPINE',[(cx-5.55,cy-4.8,floor_top+1.8),(cx-5.55,cy+4.8,floor_top+1.8),(cx-3.8,cy+4.8,floor_top+1.8)],bpy.data.materials['AUR_MAT_CABLE_DATA_JACKET'],'data')
    cable('AUR_INT_POWER_SPINE',[(cx+5.55,cy-4.8,floor_top+2.35),(cx+5.55,cy+4.8,floor_top+2.35),(cx+3.0,cy+4.8,floor_top+2.35)],bpy.data.materials['AUR_MAT_SERVICE_TRAY'],'power')

    # Accepted maintenance directions after r37 QA.
    maintenance={'AUR_INT_CAL_CONSOLE':(0.8,'NORTH'),'AUR_INT_OBS_CONSOLE':(0.8,'SOUTH'),'AUR_INT_SERVICE_CONSOLE_R36':(0.8,'NORTH'),'AUR_INT_SERVICE_CAB':(0.9,'EAST'),'AUR_INT_ARCHIVE_RACK_0':(0.8,'WEST'),'AUR_INT_ARCHIVE_RACK_1':(0.8,'WEST'),'AUR_INT_PATCH_PANEL':(0.7,'WEST')}
    for name,(clearance,front) in maintenance.items():
        o=bpy.data.objects[name]; o['maintenance_clearance_m']=clearance; o['maintenance_front']=front; o['clearance_contract_revision']=37

    variants=[]
    for cal_dir in ['WEST_FACING','NORTH_FACING']:
        for archive in ['TWIN_RACK','L_RACK','SPLIT_RACK']:
            for service in ['FIXED_CABINET','TROLLEY_FORWARD']:
                variants.append({'id':len(variants),'calibration_orientation':cal_dir,'archive_pattern':archive,'service_pattern':service})
    scene['x100_protocol']='EXOVANT-X100-v1'; scene['x100_last_workunit']=WORKUNIT; scene['status']='X100_OBSERVATORY_INTERIOR_R37_CLEARANCE_QA'
    scene['x100_observatory_interior_center_xy']=[cx,cy]; scene['x100_observatory_interior_platform_z']=platform; scene['x100_observatory_interior_floor_top_z']=floor_top; scene['x100_observatory_interior_state']='USED_OPERATIONAL'; scene['x100_observatory_interior_layout_variants']=json.dumps(variants,separators=(',',':')); scene['x100_observatory_interior_variant_count']=12; scene['x100_observatory_interior_proof_variant']=0
    return {'status':scene['status'],'proof_objects':len(proof.objects),'lighting_objects':len(lighting.objects),'layout_variants':len(variants),'source_families':13,'reused_prop_families':16,'maintenance_contracts':len(maintenance)}

if __name__ == '__main__':
    print(build())
