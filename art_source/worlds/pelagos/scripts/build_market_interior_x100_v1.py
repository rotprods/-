"""PELAGOS / Mercado de Boyas — systemic service/listening/custody interior v1.

Rebuild target:
- collection 13_MERCADO_INTERIOR_X100_V1
- collection 13_MERCADO_INTERIOR_X100_TECH
- root PEL-MKT-INTERIOR-SVC-001 centered at (-504,-90,14.02)
- final structural checkpoint rev34.

This is Blender-side source. Runtime door/audio/portal/HLOD thresholds, collision semantics and target-GPU qualification remain engine-gated.
"""
import bpy, math
from mathutils import Vector

MAIN='13_MERCADO_INTERIOR_X100_V1'
TECH='13_MERCADO_INTERIOR_X100_TECH'
CENTER=(-504,-90,14.02)
CLAIM='PEL/MKT/ARCH-X100-002'

for cname in (MAIN,TECH):
    c=bpy.data.collections.get(cname)
    if c:
        for o in list(c.objects): bpy.data.objects.remove(o,do_unlink=True)
        bpy.data.collections.remove(c)

def mkcoll(name):
    c=bpy.data.collections.new(name); bpy.context.scene.collection.children.link(c); return c
main=mkcoll(MAIN); tech=mkcoll(TECH)

def mat(name,fallback): return bpy.data.materials.get(name) or bpy.data.materials.get(fallback)
M={
 'ivory':mat('PEL_MAT_IvoryCeramic_Marine','PEL_Human_IvoryCeramic'),
 'bronze':mat('PEL_MAT_Bronze_Oxidized_Marine','PEL_Precursor_Bronze'),
 'dark':mat('PEL_MAT_DarkTechnicalComposite','PEL_TechnicalFabric'),
 'textile':mat('PEL_MAT_WaterproofTextile','PEL_TechnicalFabric'),
 'cyan':mat('PEL_Memory_Cyan','PEL_LivingCoral'),
 'amber':mat('PEL_Refuge_Amber','PEL_Human_IvoryCeramic'),
 'coral':mat('PEL_LivingCoral','PEL_Human_IvoryCeramic'),
}

def move(o,c):
    for old in list(o.users_collection): old.objects.unlink(o)
    c.objects.link(o)

def tag(o,aid,role,era='ERA_1_OCCUPATION',extra=None):
    o['world']='pelagos'; o['asset_id']=aid; o['role']=role; o['claim_id']=CLAIM
    o['production_state']='INTERIOR_SYSTEMIC_FOUNDATION_V1'; o['story_era']=era; o['x100_protocol']='EXOVANT_X100_v1'
    if extra:
        for k,v in extra.items(): o[k]=v

def empty(name,loc,aid,role='assembly_root',era='ERA_1_OCCUPATION',extra=None,c=main):
    o=bpy.data.objects.new(name,None); c.objects.link(o); o.location=loc; tag(o,aid,role,era,extra); return o

def box(name,parent,loc,dims,material,aid,role,era='ERA_1_OCCUPATION',c=main,hidden=False,extra=None):
    bpy.ops.mesh.primitive_cube_add(size=1,location=(0,0,0)); o=bpy.context.object; o.name=name; move(o,c)
    o.dimensions=dims; bpy.ops.object.transform_apply(location=False,rotation=False,scale=True); o.parent=parent; o.location=loc
    if material: o.data.materials.append(material)
    tag(o,aid,role,era,extra); o.hide_render=hidden; o.hide_viewport=hidden; return o

def cyl(name,parent,loc,radius,depth,material,aid,role,era='ERA_1_OCCUPATION',rot=(0,0,0),c=main,hidden=False,extra=None,verts=12):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts,radius=radius,depth=depth,location=(0,0,0)); o=bpy.context.object; o.name=name; move(o,c)
    o.parent=parent; o.location=loc; o.rotation_euler=rot
    if material: o.data.materials.append(material)
    tag(o,aid,role,era,extra); o.hide_render=hidden; o.hide_viewport=hidden; return o

root=empty('PEL_MKT_INT_ServiceListeningCell_ROOT',CENTER,'PEL-MKT-INTERIOR-SVC-001','interior_cell_root','ERA_2_CURRENT',{
 'semantic_purpose':'service_listening_memory_custody_cell','cell_size_m':'8x6','clear_height_m':3.2,'snap_grid_m':0.25,
 'wall_slot_count':4,'wall_panel_types':'solid|service|acoustic|custody|open','valid_wall_layouts':280,'floor_patterns':3,'ceiling_patterns':2,'temporal_states':4,'credible_configurations':6720,
 'current_layout':'west=service;north=acoustic;south=custody;east=threshold/open','service_channel_interface':'PEL_MKT_V1_ServiceChannel_05 west interface','utility_riser_interface':'PEL_MKT_V1_UtilityRiser adjacent west-north',
 'bridge_clearance':'bay chosen between bridge centerlines; no bridge centerline occupancy','iconography':'UNKNOWN_DO_NOT_INVENT','engine_state':'NOT_IMPORTED_NOT_PORTAL_CULLED_NOT_GPU_QUALIFIED',
 'central_clear_corridor_width_m':0.90,'central_clear_corridor_policy':'reserved x local [-0.45,+0.45], y local [-2.25,+2.25]'
})

# ERA 0 — original load-bearing, drainable construction.
frame='PEL-MKT-INT-FRAME-001'; floor='PEL-MKT-INT-FLOOR-001'; drain='PEL-MKT-INT-DRAIN-001'; ceiling='PEL-MKT-INT-CEILING-001'
box('PEL_MKT_INT_Floor_E',root,(2,0,.03),(4,5.8,.14),M['ivory'],floor,'drained_floor_plate','ERA_0_ORIGINAL')
box('PEL_MKT_INT_Floor_W',root,(-2.45,0,.03),(3,5.8,.14),M['ivory'],floor,'removable_service_floor_plate','ERA_0_ORIGINAL')
box('PEL_MKT_INT_ServiceGrate',root,(-.65,0,.07),(.55,5.7,.12),M['dark'],floor,'longitudinal_service_grate','ERA_0_ORIGINAL',extra={'alignment':'parallel_to_underfloor_service_channel'})
box('PEL_MKT_INT_DrainTrench',root,(-3.72,0,.08),(.22,5.6,.16),M['bronze'],drain,'drainage_trench','ERA_0_ORIGINAL',extra={'cause':'wet_service_wall_and_utility_access'})
for x in (-3.82,3.82):
    for y in (-2.82,2.82): box(f'PEL_MKT_INT_FramePost_{x}_{y}',root,(x,y,1.65),(.18,.18,3.30),M['bronze'],frame,'load_bearing_frame_post','ERA_0_ORIGINAL')
for y in (-2.82,2.82): box(f'PEL_MKT_INT_TopBeam_Y{y}',root,(0,y,3.22),(7.8,.18,.22),M['bronze'],frame,'overhead_frame_beam','ERA_0_ORIGINAL')
for x in (-3.82,3.82): box(f'PEL_MKT_INT_TopBeam_X{x}',root,(x,0,3.22),(.18,5.8,.22),M['bronze'],frame,'overhead_frame_beam','ERA_0_ORIGINAL')
box('PEL_MKT_INT_CeilingMembrane',root,(.5,0,3.12),(6.2,5.4,.10),M['textile'],ceiling,'replaceable_ceiling_membrane','ERA_0_ORIGINAL',extra={'construction':'lightweight_detachable_not_primary_structure'})
box('PEL_MKT_INT_CeilingServiceTray',root,(-3.35,0,2.98),(.42,5.2,.18),M['dark'],ceiling,'overhead_service_tray','ERA_1_OCCUPATION',extra={'service_logic':'aligned_to_west_utility_interface'})

# ERA 1 — swappable occupation modules.
solid='PEL-MKT-INT-WALL-SOLID-001'; service='PEL-MKT-INT-WALL-SERVICE-001'; acoustic='PEL-MKT-INT-WALL-ACOUSTIC-001'; custody='PEL-MKT-INT-WALL-CUSTODY-001'; threshold='PEL-MKT-INT-THRESHOLD-001'
for y in (-1.85,1.85): box(f'PEL_MKT_INT_WestPanel_{y}',root,(-3.72,y,1.55),(.16,1.9,3.0),M['ivory'],solid,'wall_panel')
box('PEL_MKT_INT_ServiceBacker',root,(-3.68,0,1.48),(.12,1.55,2.5),M['dark'],service,'service_wall_backer')
for i,z in enumerate((.82,1.42,2.02)): cyl(f'PEL_MKT_INT_Manifold_{i}',root,(-3.55,-.15,z),.16,.22,M['bronze'],service,'service_manifold_port',rot=(0,math.radians(90),0),extra={'interface':'wet_glove_quick_disconnect'})
box('PEL_MKT_INT_ServicePanel',root,(-3.51,.48,1.45),(.10,.52,1.35),M['ivory'],service,'removable_service_panel')
for i,x in enumerate((-2.6,-1.3,0,1.3,2.6)):
    box(f'PEL_MKT_INT_AcousticBaffle_{i}',root,(x,2.70,1.55),(1.06,.24,2.85),M['textile'],acoustic,'acoustic_baffle_panel',extra={'function':'reduce_reflection_and_support_listening'})
    if i in (1,3): cyl(f'PEL_MKT_INT_HydroSocket_{i}',root,(x,2.52,1.55),.13,.16,M['cyan'],acoustic,'hydrophone_receiver_socket',rot=(math.radians(90),0,0),extra={'emissive_meaning':'active_listening_receiver'})
for i,x in enumerate((-2.7,-.9,.9,2.7)):
    box(f'PEL_MKT_INT_CustodyShell_{i}',root,(x,-2.70,1.45),(1.45,.28,2.55),M['ivory'],custody,'memory_custody_niche')
    box(f'PEL_MKT_INT_CustodyDoor_{i}',root,(x,-2.51,1.45),(1.18,.08,2.22),M['dark'],custody,'custody_access_door')
    box(f'PEL_MKT_INT_CustodyHandle_{i}',root,(x+.42,-2.44,1.45),(.12,.08,.46),M['bronze'],custody,'wet_glove_handle')
    box(f'PEL_MKT_INT_CustodySeal_{i}',root,(x-.40,-2.43,2.25),(.18,.05,.18),M['cyan'],custody,'custody_status_seal',extra={'emissive_meaning':'custody_state_not_decoration'})
for y in (-2.05,2.05): box(f'PEL_MKT_INT_EastWall_{y}',root,(3.72,y,1.55),(.16,1.45,3.0),M['ivory'],solid,'wall_panel')
box('PEL_MKT_INT_ThresholdHeader',root,(3.72,0,2.72),(.18,1.65,.28),M['bronze'],threshold,'threshold_header')
box('PEL_MKT_INT_SlidingHatch_PARKED',root,(3.62,1.26,1.42),(.12,1.22,2.45),M['dark'],threshold,'sliding_hatch_parked_open',extra={'gameplay_state':'open','clear_width_m':1.5,'runtime_animation':'PENDING_ENGINE'})
box('PEL_MKT_INT_ThresholdStateCarrier',root,(3.52,-1.15,1.25),(.12,.42,1.20),M['ivory'],threshold,'physical_threshold_state_carrier',extra={'symbol_language':'UNSPECIFIED_DO_NOT_INVENT'})
for i,(z,ma) in enumerate(((.95,M['dark']),(1.25,M['amber']),(1.55,M['cyan']))): box(f'PEL_MKT_INT_ThresholdToken_{i}',root,(3.44,-1.38,z),(.06,.18,.16),ma,threshold,'threshold_state_token')

# Integrated work/support modules. Workbench final position includes the rev34 0.30m corridor correction.
bench='PEL-MKT-INT-WORKBENCH-001'; locker='PEL-MKT-INT-LOCKER-001'; light='PEL-MKT-INT-LIGHT-001'
box('PEL_MKT_INT_WorkbenchTop',root,(-1.8,1.75,.92),(2.3,.72,.14),M['ivory'],bench,'integrated_service_workbench')
for x in (-2.75,-.85): box(f'PEL_MKT_INT_WorkbenchLeg_{x}',root,(x,1.75,.48),(.16,.60,.88),M['bronze'],bench,'workbench_support')
box('PEL_MKT_INT_WorkbenchToolRail',root,(-1.8,2.30,1.45),(2.1,.10,.16),M['bronze'],bench,'service_tool_rail')
for i in range(3):
    box(f'PEL_MKT_INT_Locker_{i}',root,(1.45+i*.75,1.95,1.05),(.62,.55,2.0),M['dark'],locker,'wet_storage_locker')
    box(f'PEL_MKT_INT_LockerVent_{i}',root,(1.45+i*.75,1.64,1.55),(.38,.05,.12),M['bronze'],locker,'locker_drain_vent')
for x in (-1.8,1.8):
    cyl(f'PEL_MKT_INT_TaskLightStem_{x}',root,(x,.8,2.86),.04,.32,M['bronze'],light,'task_light_mount')
    box(f'PEL_MKT_INT_TaskLight_{x}',root,(x,.8,2.66),(.52,.22,.12),M['amber'],light,'amber_task_light',extra={'emissive_meaning':'low_glare_service_task_light'})

# ERA 2 — localized repair/adaptation, never global random grunge.
repair='PEL-MKT-INT-REPAIR-001'
box('PEL_MKT_INT_ReplacementFloorPlate',root,(-2.45,-1.65,.13),(1.35,1.45,.08),M['dark'],repair,'mismatched_replacement_floor_plate','ERA_2_CURRENT',extra={'cause':'repeated_service_access_over_underfloor_channel'})
for sx,sy in ((-3,-2.10),(-2,-2.10),(-3,-1.18),(-2,-1.18)): cyl(f'PEL_MKT_INT_RepairFastener_{sx}_{sy}',root,(sx,sy,.20),.045,.08,M['bronze'],repair,'repair_fastener','ERA_2_CURRENT',verts=8)
box('PEL_MKT_INT_ServiceWallPatch',root,(-3.43,.55,1.65),(.07,.62,.78),M['dark'],repair,'field_repair_patch','ERA_2_CURRENT',extra={'cause':'utility_service_damage','repair_language':'visible_misfit_panel'})
for i,y in enumerate((-1.8,-.6,.7,1.9)): cyl(f'PEL_MKT_INT_DrainFouling_{i}',root,(-3.55,y,.16),.10+.02*(i%2),.16,M['coral'],repair,'wet_edge_biological_fouling','ERA_2_CURRENT',extra={'cause':'persistent_moisture_at_drainage_edge'})
box('PEL_MKT_INT_CeilingRepairStrip',root,(-1.7,-1.6,3.07),(2.15,.26,.08),M['ivory'],repair,'ceiling_membrane_repair_strip','ERA_2_CURRENT',extra={'cause':'membrane_tear_repair'})

# Technical shards: collision, LOD1, HLOD. Hidden by default.
col='PEL-MKT-INTERIOR-SVC-001-COL'; lod='PEL-MKT-INTERIOR-SVC-001-LOD1'; hlod='PEL-MKT-INTERIOR-SVC-001-HLOD'
tr=empty('PEL_MKT_INT_TECH_ROOT',CENTER,'PEL-MKT-INTERIOR-SVC-001-TECH','technical_root','ERA_2_CURRENT',{'collision_asset_id':col,'lod1_asset_id':lod,'hlod_asset_id':hlod,'visibility_strategy':'room_or_portal_culling_candidate','engine_state':'PENDING_ENGINE'},tech)
box('PEL_MKT_INT_COL_Floor',tr,(0,0,.02),(7.8,5.8,.12),None,col,'collision_floor','ERA_2_CURRENT',tech,True,{'collision_intent':'blocking_static_proposal'})
box('PEL_MKT_INT_COL_West',tr,(-3.75,0,1.5),(.18,5.7,3.0),None,col,'collision_wall','ERA_2_CURRENT',tech,True,{'collision_intent':'blocking_static_proposal'})
box('PEL_MKT_INT_COL_North',tr,(0,2.75,1.5),(7.5,.18,3.0),None,col,'collision_wall','ERA_2_CURRENT',tech,True,{'collision_intent':'blocking_static_proposal'})
box('PEL_MKT_INT_COL_South',tr,(0,-2.75,1.5),(7.5,.18,3.0),None,col,'collision_wall','ERA_2_CURRENT',tech,True,{'collision_intent':'blocking_static_proposal'})
for y in (-2.05,2.05): box(f'PEL_MKT_INT_COL_East_{y}',tr,(3.75,y,1.5),(.18,1.45,3.0),None,col,'collision_wall','ERA_2_CURRENT',tech,True,{'collision_intent':'blocking_static_proposal'})
l1=empty('PEL_MKT_INT_LOD1_ROOT',CENTER,lod,'lod_root','ERA_2_CURRENT',{'lod':'1'},tech)
for side,loc,dims in [('W',(-3.72,0,1.55),(.14,5.6,3.0)),('N',(0,2.70,1.55),(7.5,.14,3.0)),('S',(0,-2.70,1.55),(7.5,.14,3.0))]: box(f'PEL_MKT_INT_LOD1_{side}',l1,loc,dims,M['ivory'],lod,'lod1_wall_envelope','ERA_2_CURRENT',tech,True,{'lod':'1'})
box('PEL_MKT_INT_LOD1_Floor',l1,(0,0,.04),(7.8,5.8,.14),M['dark'],lod,'lod1_floor','ERA_2_CURRENT',tech,True,{'lod':'1'})
h=empty('PEL_MKT_INT_HLOD_ROOT',CENTER,hlod,'hlod_root','ERA_2_CURRENT',{'hlod':'1','switch_threshold':'PENDING_ENGINE'},tech)
box('PEL_MKT_INT_HLOD_Envelope',h,(0,0,1.55),(7.9,5.9,3.15),M['dark'],hlod,'hlod_cell_envelope','ERA_2_CURRENT',tech,True,{'hlod':'1'})
empty('PEL_MKT_INT_METADATA',CENTER,'PEL-MKT-INTERIOR-SVC-001-META','system_metadata','ERA_2_CURRENT',{'module_families':'frame|floor|drain|solid_wall|service_wall|acoustic_wall|custody_wall|threshold|ceiling|workbench|locker|light|repair','wall_slots':4,'wall_panel_types':5,'valid_wall_layouts':280,'floor_patterns':3,'ceiling_patterns':2,'temporal_states':4,'credible_configurations':6720,'minimum_threshold_clearance_m':1.5,'nominal_clear_height_m':3.2,'runtime_audio':'PENDING_ENGINE','runtime_door':'PENDING_ENGINE','portal_culling':'PENDING_ENGINE'},tech)
for o in tech.objects:
    if o.type=='MESH' and str(o.get('role','')).startswith('collision'): o.display_type='WIRE'

bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
