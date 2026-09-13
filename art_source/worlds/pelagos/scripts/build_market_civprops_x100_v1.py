"""PELAGOS / Mercado de Boyas — X100 civilization prop systemic kit v1.

Rebuilds nine repair-first marine prop families as a deterministic staging matrix.
Source checkpoint: Blender rev 32 / PELAGOS-X100-MERCADO-CIVPROP-001.
Runtime interaction, LOD switching thresholds and collision semantics remain engine-gated.
"""
import bpy, math, json
from mathutils import Vector

MAIN='12_MERCADO_CIVPROP_X100_V1'
LOD='12_MERCADO_CIVPROP_X100_LOD'
TECH='12_MERCADO_CIVPROP_X100_TECH'
CLAIM='PEL/CIV/PROP-X100-001'
DECK_TOP=20.4
ROOT_Z=20.42

FAMILIES=[
 ('MEMCUST','PEL-PROP-MEMCUST-001','memory_custody_container','memory_custody|inspect|carry','dry_service_deck'),
 ('HYDRO','PEL-PROP-HYDROPHONE-001','hydrophone_listening_station','listen|record|inspect','deck_edge_or_service_spine'),
 ('FUNERAL','PEL-PROP-FUNERAL-BUOY-001','funeral_buoy','quest_signal|listen|memorial','mooring_or_water_edge'),
 ('TRADE','PEL-PROP-TRADE-SIGNAL-001','trade_channel_signal','navigation|route_state|inspect','dock_edge'),
 ('CONSENT','PEL-PROP-CONSENT-MARKER-001','consent_timetable_marker','route_permission|inspect','threshold_or_dock_entry'),
 ('CLAMP','PEL-PROP-REEF-CLAMP-001','reef_safe_clamp','mount|repair|reef_interface','reef_interface_only'),
 ('CRATE','PEL-PROP-MAINT-CRATE-001','maintenance_crate','storage|repair_supply|movable','service_deck'),
 ('REEL','PEL-PROP-SERVICE-REEL-001','service_hose_reel','maintenance|hose_cable_route','service_spine'),
 ('RACK','PEL-PROP-WET-GEAR-RACK-001','wet_gear_rack','domestic_work|equipment_storage','covered_market_service_zone'),
]
STATES=['pristine','used','damaged','abandoned']
SCALES=[0.82,1.0,1.22]
ROW_VARIANT=[0,1,2,0]


def wipe_collection(name):
    c=bpy.data.collections.get(name)
    if c:
        for o in list(c.objects): bpy.data.objects.remove(o,do_unlink=True)
        bpy.data.collections.remove(c)

def mkcoll(name):
    c=bpy.data.collections.new(name); bpy.context.scene.collection.children.link(c); return c

for n in (MAIN,LOD,TECH): wipe_collection(n)
main=mkcoll(MAIN); lodc=mkcoll(LOD); tech=mkcoll(TECH)

def material(name,fallback): return bpy.data.materials.get(name) or bpy.data.materials.get(fallback)
M={
 'ivory':material('PEL_MAT_IvoryCeramic_Marine','PEL_Human_IvoryCeramic'),
 'bronze':material('PEL_MAT_Bronze_Oxidized_Marine','PEL_Precursor_Bronze'),
 'dark':material('PEL_MAT_DarkTechnicalComposite','PEL_TechnicalFabric'),
 'textile':material('PEL_MAT_WaterproofTextile','PEL_TechnicalFabric'),
 'amber':material('PEL_Refuge_Amber','PEL_Human_IvoryCeramic'),
 'cyan':material('PEL_Memory_Cyan','PEL_LivingCoral'),
 'coral':material('PEL_LivingCoral','PEL_Human_IvoryCeramic'),
}

def move_to(o,c):
    for old in list(o.users_collection): old.objects.unlink(o)
    c.objects.link(o)

def tag(o,aid,role,extra=None):
    o['world']='pelagos'; o['asset_id']=aid; o['role']=role
    o['production_state']='SYSTEMIC_FAMILY_FOUNDATION_V1'; o['claim_id']=CLAIM; o['x100_protocol']='EXOVANT_X100_v1'
    if extra:
        for k,v in extra.items(): o[k]=v

def empty(name,loc,aid,role='family_root',extra=None,c=main):
    o=bpy.data.objects.new(name,None); c.objects.link(o); o.location=loc; tag(o,aid,role,extra); return o

def box(name,p,loc,dims,mat,role,aid=None,c=main,hidden=False,extra=None):
    bpy.ops.mesh.primitive_cube_add(size=1,location=(0,0,0)); o=bpy.context.object; o.name=name; move_to(o,c)
    o.dimensions=dims; bpy.ops.object.transform_apply(location=False,rotation=False,scale=True); o.parent=p; o.location=loc
    if mat: o.data.materials.append(mat)
    tag(o,aid or p['asset_id'],role,extra); o.hide_render=hidden; o.hide_viewport=hidden; return o

def cyl(name,p,loc,r,depth,mat,role,aid=None,c=main,rot=(0,0,0),verts=12,hidden=False,extra=None):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts,radius=r,depth=depth,location=(0,0,0)); o=bpy.context.object; o.name=name; move_to(o,c)
    o.parent=p; o.location=loc; o.rotation_euler=rot
    if mat: o.data.materials.append(mat)
    tag(o,aid or p['asset_id'],role,extra); o.hide_render=hidden; o.hide_viewport=hidden; return o

def torus(name,p,loc,major,minor,mat,role,aid=None,c=main,rot=(0,0,0),hidden=False,extra=None):
    bpy.ops.mesh.primitive_torus_add(major_radius=major,minor_radius=minor,major_segments=12,minor_segments=6,location=(0,0,0)); o=bpy.context.object; o.name=name; move_to(o,c)
    o.parent=p; o.location=loc; o.rotation_euler=rot
    if mat: o.data.materials.append(mat)
    tag(o,aid or p['asset_id'],role,extra); o.hide_render=hidden; o.hide_viewport=hidden; return o

def sphere(name,p,loc,r,mat,role,aid=None,c=main,hidden=False,extra=None):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,radius=r,location=(0,0,0)); o=bpy.context.object; o.name=name; move_to(o,c)
    o.parent=p; o.location=loc
    if mat: o.data.materials.append(mat)
    tag(o,aid or p['asset_id'],role,extra); o.hide_render=hidden; o.hide_viewport=hidden; return o

def root_meta(r,fam,v,state):
    r['family_code']=fam[0]; r['family_name']=fam[2]; r['semantic_purpose']=fam[2]; r['gameplay_tags']=fam[3]; r['placement_rule']=fam[4]
    r['variant_index']=v; r['state']=state; r['variant_set']='compact|standard|heavy'; r['state_set']='pristine|used|damaged|abandoned'
    r['configuration_key']=f'{fam[0]}:v{v}:{state}'; r['snap_grid_m']=0.25; r['allowed_yaw_deg']='0|90|180|270'
    r['pivot_contract']='assembly root at support/contact plane'; r['culture_dna']='repair-first|marine-corrosion|field-maintainable|wet-glove-ergonomics'
    r['manufacturing_logic']='visible fasteners; replaceable panels; corrosion-resistant frame; causal service access'
    r['material_history']='state-specific and cause-bound; no random grunge'; r['lod_strategy']='LOD0 assembly; LOD1 semantic proxy; LOD2 silhouette proxy; thresholds PENDING_ENGINE'
    r['engine_state']='NOT_IMPORTED_NOT_RUNTIME_QUALIFIED'; r['story_era']={'pristine':'ERA_0_OR_RECENT_REPLACEMENT','used':'ERA_1_OCCUPATION','damaged':'ERA_1_REPAIR_AFTER_DAMAGE','abandoned':'ERA_2_DEGRADATION_ADAPTATION'}[state]

def causality(r,state,wear,repair,foul,s):
    if state=='used': box(r.name+'_CONTACT_WEAR',r,wear,(.34*s,.06*s,.10*s),M['bronze'],'causal_contact_wear_marker',extra={'cause':'repeated_hand_tool_contact'})
    elif state=='damaged':
        box(r.name+'_FIELD_REPAIR',r,repair,(.42*s,.08*s,.30*s),M['dark'],'field_repair_patch',extra={'cause':'impact_or_service_damage','repair_language':'visible_mismatched_replacement'})
        cyl(r.name+'_PATCH_FASTENER',r,(repair[0],repair[1]-.05*s,repair[2]),.04*s,.12*s,M['bronze'],'repair_fastener',rot=(math.radians(90),0,0),verts=8)
    elif state=='abandoned':
        for j,(x,y,z) in enumerate([(-.16,0,.04),(.10,.06,.08),(.02,-.09,.12)]): sphere(r.name+f'_FOUL_{j}',r,(foul[0]+x*s,foul[1]+y*s,foul[2]+z*s),.11*s*(1+.15*j),M['coral'],'biological_fouling',extra={'cause':'persistent_wet_contact_and_abandonment'})

def build_mem(r,s,state):
    w,d,h=.92*s,.62*s,.52*s; box(r.name+'_BODY',r,(0,0,h/2),(w,d,h),M['ivory'],'pressure_case_body'); box(r.name+'_LID',r,(0,0,h+.07*s),(w*.96,d*.96,.14*s),M['dark'],'replaceable_lid'); box(r.name+'_HANDLE',r,(0,-d*.53,h*.64),(.42*s,.10*s,.12*s),M['bronze'],'wet_glove_handle'); box(r.name+'_SEAL',r,(0,0,h*.94),(w*.88,d*.88,.05*s),M['cyan'],'memory_custody_seal',extra={'emissive_meaning':'custody_status_not_decoration'}); causality(r,state,(0,-d*.58,h*.64),(w*.35,-d*.51,h*.55),(-w*.32,d*.35,.05*s),s); return (1.15*w,1.25*d,h+.2*s)
def build_hydro(r,s,state):
    box(r.name+'_BASE',r,(0,0,.08*s),(.78*s,.72*s,.16*s),M['dark'],'drained_mount_base'); cyl(r.name+'_MAST',r,(0,0,.76*s),.075*s,1.36*s,M['bronze'],'hydrophone_mast',verts=10); torus(r.name+'_RING',r,(0,0,1.36*s),.33*s,.045*s,M['ivory'],'hydrophone_array_ring'); sphere(r.name+'_CORE',r,(0,0,1.36*s),.16*s,M['cyan'],'acoustic_memory_receiver',extra={'emissive_meaning':'active_listening_state'}); [box(r.name+f'_BRACE_{a}',r,(a*.22*s,0,.42*s),(.06*s,.16*s,.70*s),M['ivory'],'service_brace') for a in (-1,1)]; causality(r,state,(0,.11*s,.72*s),(.20*s,-.09*s,.62*s),(-.25*s,.22*s,.06*s),s); return (.95*s,.9*s,1.6*s)
def build_funeral(r,s,state):
    cyl(r.name+'_BALLAST',r,(0,0,.16*s),.46*s,.32*s,M['bronze'],'low_ballast_mass'); cyl(r.name+'_BODY',r,(0,0,.86*s),.31*s,1.18*s,M['ivory'],'funeral_buoy_body'); torus(r.name+'_TIDELINE',r,(0,0,.53*s),.35*s,.045*s,M['dark'],'tide_line_protection_ring'); cyl(r.name+'_SIGNAL_STEM',r,(0,0,1.62*s),.055*s,.60*s,M['bronze'],'audible_signal_stem',verts=10); sphere(r.name+'_SIGNAL_HEAD',r,(0,0,1.95*s),.22*s,M['amber'],'audible_funeral_signal',extra={'story_tag':'funeral_buoy','iconography':'UNSPECIFIED_DO_NOT_INVENT'}); causality(r,state,(0,-.34*s,.76*s),(.28*s,-.25*s,1.05*s),(-.30*s,.20*s,.10*s),s); return (1*s,1*s,2.2*s)
def build_trade(r,s,state):
    box(r.name+'_BASE',r,(0,0,.09*s),(.62*s,.62*s,.18*s),M['dark'],'dock_signal_base'); cyl(r.name+'_POST',r,(0,0,.95*s),.065*s,1.72*s,M['bronze'],'trade_signal_post',verts=10)
    for side in (-1,1): box(r.name+f'_DIR_{side}',r,(side*.24*s,0,1.43*s),(.38*s,.12*s,.20*s),M['ivory'],'directional_signal_vane'); sphere(r.name+f'_AMBER_{side}',r,(side*.24*s,-.09*s,1.43*s),.075*s,M['amber'],'trade_channel_status_light',extra={'emissive_meaning':'navigation_route_status'})
    causality(r,state,(0,.10*s,1*s),(.20*s,-.10*s,1.18*s),(-.22*s,.18*s,.05*s),s); return (1*s,.8*s,1.9*s)
def build_consent(r,s,state):
    cyl(r.name+'_BASE',r,(0,0,.10*s),.30*s,.20*s,M['bronze'],'threshold_base',verts=10); box(r.name+'_POST',r,(0,0,.87*s),(.16*s,.18*s,1.54*s),M['ivory'],'consent_marker_post')
    for i,(z,ma) in enumerate([(.55,M['dark']),(.92,M['amber']),(1.29,M['cyan'])]): box(r.name+f'_TOKEN_{i}',r,(0,-.13*s,z*s),(.46*s,.09*s,.18*s),ma,'physical_state_token',extra={'semantic':'consent_or_timetable_state_carrier','symbol_language':'UNSPECIFIED_DO_NOT_INVENT'})
    causality(r,state,(0,-.14*s,.88*s),(.16*s,-.12*s,.42*s),(-.20*s,.16*s,.05*s),s); return (.72*s,.65*s,1.72*s)
def build_clamp(r,s,state):
    zoff=-.12*s
    box(r.name+'_SPINE',r,(0,0,.26*s+zoff),(.86*s,.22*s,.28*s),M['bronze'],'reef_safe_clamp_spine')
    for side in (-1,1): box(r.name+f'_JAW_{side}',r,(side*.34*s,0,.48*s+zoff),(.18*s,.34*s,.56*s),M['ivory'],'compliant_clamp_jaw'); box(r.name+f'_PAD_{side}',r,(side*.34*s,.16*s,.48*s+zoff),(.14*s,.08*s,.34*s),M['textile'],'reef_contact_pad',extra={'cause':'non_destructive_living_surface_contact'})
    cyl(r.name+'_TENSION',r,(0,-.14*s,.26*s+zoff),.06*s,.70*s,M['dark'],'tension_member',rot=(0,math.radians(90),0),verts=10); causality(r,state,(.34*s,.18*s,.36*s),(0,-.16*s,.18*s),(-.30*s,-.08*s,.05*s),s); return (.95*s,.65*s,.82*s)
def build_crate(r,s,state):
    w,d,h=1*s,.70*s,.62*s; box(r.name+'_BODY',r,(0,0,h/2),(w,d,h),M['dark'],'maintenance_crate_body'); box(r.name+'_LID',r,(0,0,h+.05*s),(w*.96,d*.96,.10*s),M['ivory'],'replaceable_crate_lid'); [box(r.name+f'_HANDLE_{side}',r,(side*w*.52,0,h*.55),(.10*s,.40*s,.16*s),M['bronze'],'wet_glove_handle') for side in (-1,1)]
    for sx in (-1,1):
        for sy in (-1,1): box(r.name+f'_CORNER_{sx}_{sy}',r,(sx*w*.46,sy*d*.43,h*.50),(.10*s,.10*s,h*.90),M['bronze'],'impact_corner_guard')
    causality(r,state,(w*.53,0,h*.55),(w*.32,-d*.51,h*.48),(-w*.36,d*.30,.05*s),s); return (1.18*w,1.18*d,h+.16*s)
def build_reel(r,s,state):
    box(r.name+'_BASE',r,(0,0,.10*s),(1*s,.72*s,.20*s),M['dark'],'service_reel_base'); [box(r.name+f'_SUPPORT_{side}',r,(side*.34*s,0,.62*s),(.16*s,.48*s,.95*s),M['ivory'],'reel_support_frame') for side in (-1,1)]; cyl(r.name+'_DRUM',r,(0,0,.68*s),.33*s,.60*s,M['bronze'],'service_hose_drum',rot=(math.radians(90),0,0),verts=12); torus(r.name+'_HOSE',r,(0,0,.68*s),.34*s,.055*s,M['textile'],'coiled_service_hose',rot=(math.radians(90),0,0)); box(r.name+'_HANDLE',r,(.48*s,-.26*s,.84*s),(.10*s,.12*s,.30*s),M['bronze'],'manual_reel_handle'); causality(r,state,(.48*s,-.29*s,.84*s),(.34*s,-.26*s,.52*s),(-.36*s,.26*s,.05*s),s); return (1.25*s,1*s,1.2*s)
def build_rack(r,s,state):
    w,h=1.45*s,1.75*s
    for side in (-1,1): box(r.name+f'_POST_{side}',r,(side*w*.42,0,h*.50),(.10*s,.18*s,h),M['bronze'],'gear_rack_post'); box(r.name+f'_FOOT_{side}',r,(side*w*.42,0,.06*s),(.42*s,.48*s,.12*s),M['dark'],'drained_rack_foot')
    box(r.name+'_BAR',r,(0,0,h*.84),(w,.14*s,.12*s),M['ivory'],'gear_rack_crossbar')
    for i in range(5): box(r.name+f'_HOOK_{i}',r,((-.5+i*.25)*w,-.12*s,h*.72),(.06*s,.18*s,.20*s),M['bronze'],'wet_gear_hook')
    box(r.name+'_DRIP',r,(0,0,.11*s),(w*.90,.58*s,.10*s),M['dark'],'drainage_tray'); causality(r,state,(0,-.12*s,h*.84),(w*.25,-.10*s,h*.82),(-w*.36,.18*s,.08*s),s); return (w*1.06,.82*s,h*1.05)

BUILD={'MEMCUST':build_mem,'HYDRO':build_hydro,'FUNERAL':build_funeral,'TRADE':build_trade,'CONSENT':build_consent,'CLAMP':build_clamp,'CRATE':build_crate,'REEL':build_reel,'RACK':build_rack}
family_max={}; roots=[]; x0=-715.2; dx=2.65; ys=[-97,-92,-87,-82]
for ci,fam in enumerate(FAMILIES):
    mx=[0,0,0]
    for ri,state in enumerate(STATES):
        v=ROW_VARIANT[ri]; s=SCALES[v]; r=empty(f'PEL_X100_{fam[0]}_V{v}_{state.upper()}',(x0+dx*ci,ys[ri],ROOT_Z),fam[1]); root_meta(r,fam,v,state); roots.append(r); dims=BUILD[fam[0]](r,s,state); r['approx_bbox_m']=json.dumps([round(x,3) for x in dims]); mx=[max(mx[i],dims[i]) for i in range(3)]
    family_max[fam[0]]=mx

# Family LOD/collision technical shards. These remain hidden and engine-gated.
for i,fam in enumerate(FAMILIES):
    dims=family_max[fam[0]]; base=(x0+dx*i,ys[0],ROOT_Z)
    empty(f'PEL_X100_{fam[0]}_TECHMETA',base,fam[1]+'-TECH','technical_metadata',{'source_family':fam[1],'lod1_asset_id':fam[1]+'-LOD1','lod2_asset_id':fam[1]+'-LOD2','collision_asset_id':fam[1]+'-COL','switch_thresholds':'PENDING_ENGINE_CAMERA_PROFILE','collision_semantics':'PROPOSAL_PENDING_ENGINE','family_complete':'NO_FOUNDATION_ONLY'},tech)
    l1=empty(f'PEL_X100_{fam[0]}_LOD1_ROOT',base,fam[1]+'-LOD1','lod_root',{'lod':'1','source_family':fam[1]},lodc); box(f'PEL_X100_{fam[0]}_LOD1_BODY',l1,(0,0,dims[2]*.45),(dims[0]*.82,dims[1]*.82,max(.18,dims[2]*.90)),M['ivory'],'lod1_semantic_envelope',fam[1]+'-LOD1',lodc,True,{'lod':'1'})
    l2=empty(f'PEL_X100_{fam[0]}_LOD2_ROOT',base,fam[1]+'-LOD2','lod_root',{'lod':'2','source_family':fam[1]},lodc); box(f'PEL_X100_{fam[0]}_LOD2_BODY',l2,(0,0,dims[2]*.42),(dims[0]*.72,dims[1]*.72,max(.15,dims[2]*.84)),M['dark'],'lod2_silhouette_proxy',fam[1]+'-LOD2',lodc,True,{'lod':'2'})
    cr=empty(f'PEL_X100_{fam[0]}_COL_ROOT',base,fam[1]+'-COL','collision_root',{'source_family':fam[1]},tech); intent='overlap_or_none_proposal' if fam[0]=='CLAMP' else 'simple_blocking_proxy_proposal'; co=box(f'PEL_X100_{fam[0]}_COL',cr,(0,0,dims[2]*.42),(dims[0]*.78,dims[1]*.78,max(.16,dims[2]*.84)),None,'collision_proxy',fam[1]+'-COL',tech,True,{'collision_intent':intent}); co.display_type='WIRE'

empty('PEL_X100_MERCADO_CIVPROP_METADATA',(-705,-90,ROOT_Z),'PEL-PROP-SYSTEM-MERCADO-X100-001','system_metadata',{'families':9,'variants_per_family':3,'states_per_family':4,'direct_configurations':108,'cardinal_yaw_multiplier':4,'credible_configurations_min':432,'culture_iconography':'UNKNOWN_DO_NOT_INVENT','engine_state':'NOT_IMPORTED_NOT_GPU_QUALIFIED','placement_surface':'Mercado specimen/service deck top z=20.4m','generator_contract':'deterministic by family/variant/state/grid slot'},tech)

# Final deterministic grounding: physical, non-state-overlay geometry touches support plane.
for r in roots:
    pts=[]
    for o in r.children_recursive:
        if o.type not in {'MESH','CURVE'} or o.hide_render or o.get('role') in {'causal_contact_wear_marker','field_repair_patch','repair_fastener','biological_fouling'}: continue
        pts.extend([o.matrix_world@Vector(c) for c in o.bound_box])
    if pts:
        dz=DECK_TOP-min(p.z for p in pts); r.location.z+=dz; r['deck_contact_fix_m']=round(float(dz),5); r['deck_contact_verified']='PHYSICAL_CORE_MIN_TO_DECK_TOP'

bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
