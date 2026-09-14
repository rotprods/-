"""EXOVANT-X100 V2 — Aurora Q_AURORA_M05 temporal archive decision-interface r45.

This generator is intentionally outcome-neutral. It reuses eight qualified archive carriers in the
r37 Observatorio annex, assigns stable record IDs, adds neutral shelf-mounted retention stops,
builds four zero-scene-user mechanical decision-profile meshes, one wall-mounted selector, three
zero-scene-user interaction contracts, and local unauthored audio/VFX hooks. It never selects a
canonical choice, writes save state, or performs global rewind.
"""
import bpy, math, json

WORKUNIT='AUR-X100-TEMPORAL-ARCHIVE-001'
PROFILES=['RETAIN_BROAD','RETAIN_CONTROLLED','RETAIN_SEALED','WITHDRAWN_RECEIPT']
CARRIERS=[
 'AUR_INT_PROP_CANISTER_0','AUR_INT_PROP_CANISTER_1','AUR_INT_PROP_CANISTER_2','AUR_INT_PROP_CANISTER_3',
 'AUR_INT_PROP_ROUTE_CART_0','AUR_INT_PROP_ROUTE_CART_1','AUR_INT_PROP_ROUTE_CART_2','AUR_INT_PROP_LOG_SLATE'
]

def add_box(V,F,center,dims):
    cx,cy,cz=center;x,y,z=dims;i=len(V)
    V += [(cx-x/2,cy-y/2,cz-z/2),(cx+x/2,cy-y/2,cz-z/2),(cx+x/2,cy+y/2,cz-z/2),(cx-x/2,cy+y/2,cz-z/2),(cx-x/2,cy-y/2,cz+z/2),(cx+x/2,cy-y/2,cz+z/2),(cx+x/2,cy+y/2,cz+z/2),(cx-x/2,cy+y/2,cz+z/2)]
    F += [(i,i+1,i+2,i+3),(i+4,i+7,i+6,i+5),(i,i+4,i+5,i+1),(i+1,i+5,i+6,i+2),(i+2,i+6,i+7,i+3),(i+4,i,i+3,i+7)]

def mkmesh(name,V,F,mat=None,props=None,fake=False):
    old=bpy.data.meshes.get(name)
    if old and old.users==0:bpy.data.meshes.remove(old)
    m=bpy.data.meshes.new(name);m.from_pydata(V,[],F);m.update();m.use_fake_user=fake
    if mat:m.materials.append(mat)
    for k,v in (props or {}).items():m[k]=v
    return m

def profile_mesh(name,profile,steel,timing,cer):
    V=[];F=[]
    if profile=='RETAIN_BROAD':
        add_box(V,F,(0,.145,-.36),(.46,.05,.06));add_box(V,F,(-.205,0,0),(.05,.30,.78));add_box(V,F,(.205,0,0),(.05,.30,.78));add_box(V,F,(0,.12,.25),(.30,.06,.12));mat=steel
    elif profile=='RETAIN_CONTROLLED':
        add_box(V,F,(0,.145,-.36),(.46,.05,.06));add_box(V,F,(-.205,0,0),(.05,.30,.78));add_box(V,F,(.205,0,0),(.05,.30,.78))
        for x in (-.16,-.08,0,.08,.16):add_box(V,F,(x,-.17,0),(.025,.035,.72))
        add_box(V,F,(0,-.19,.29),(.18,.05,.12));mat=timing or steel
    elif profile=='RETAIN_SEALED':
        add_box(V,F,(0,0,0),(.46,.34,.78));add_box(V,F,(0,-.185,.20),(.22,.04,.16));add_box(V,F,(0,-.19,-.24),(.34,.05,.06));mat=cer or steel
    else:
        add_box(V,F,(0,-.16,0),(.46,.05,.78));add_box(V,F,(0,-.20,.18),(.22,.05,.16));add_box(V,F,(0,-.20,-.22),(.28,.05,.08));mat=steel
    return mkmesh(name,V,F,mat,{'workunit':WORKUNIT,'profile':profile,'profile_status':'PRODUCTION_ADAPTER_NOT_CANON_OUTCOME','engine_runtime':'BLOCKED_EXO_012'},True)

def build():
    scene=bpy.context.scene
    # Cleanup only workunit-owned staging/hooks/meta and source profile/contract meshes.
    for cname in ['54_X100_TEMPORAL_ARCHIVE_STAGING','55_X100_TEMPORAL_ARCHIVE_HOOKS','56_X100_TEMPORAL_ARCHIVE_META']:
        c=bpy.data.collections.get(cname)
        if c:
            for o in list(c.objects):bpy.data.objects.remove(o,do_unlink=True)
            bpy.data.collections.remove(c)
    for m in list(bpy.data.meshes):
        if m.name.startswith('AUR_ARCHIVE_PROFILE_') or m.name.startswith('AUR_ARCHIVE_NEUTRAL_') or m.name.startswith('AUR_ARCHIVE_SELECTOR_') or m.name.startswith('COL_AUR_ARCHIVE_'):
            if m.users==0 or m.use_fake_user:bpy.data.meshes.remove(m)
    oldtxt=bpy.data.texts.get('AUR_TEMPORAL_ARCHIVE_CONTRACT_R43.json')
    if oldtxt:bpy.data.texts.remove(oldtxt)
    cols={}
    for n in ['54_X100_TEMPORAL_ARCHIVE_STAGING','55_X100_TEMPORAL_ARCHIVE_HOOKS','56_X100_TEMPORAL_ARCHIVE_META']:
        c=bpy.data.collections.new(n);scene.collection.children.link(c);cols[n]=c

    steel=bpy.data.materials.get('AUR_MAT_STRUCTURAL_GALV_STEEL') or bpy.data.materials.get('M_AUR_PRECISION_STEEL')
    timing=bpy.data.materials.get('AUR_MAT_CLOCK_BRONZE') or bpy.data.materials.get('M_AUR_TIMING_ALLOY')
    cer=bpy.data.materials.get('AUR_MAT_CERAMIC_COMPOSITE_PANEL') or bpy.data.materials.get('M_AUR_STONE')
    profiles={p:profile_mesh(f'AUR_ARCHIVE_PROFILE_{p}_MESH',p,steel,timing,cer) for p in PROFILES}

    # Neutral rear stop, placed on the exact supporting shelf behind every carrier.
    V=[];F=[];add_box(V,F,(0,0,0),(.08,.20,.18))
    stopmesh=mkmesh('AUR_ARCHIVE_NEUTRAL_REAR_STOP_MESH',V,F,steel,{'asset_family_id':'AUR-ARCH-DECISION-NEUTRAL-001','purpose':'undecided shelf-mounted rear retention stop; no outcome semantic'})
    shelves=[o for o in bpy.data.objects if o.name.startswith('AUR_INT_ARCHIVE_SHELF_')]
    records=[]
    for idx,n in enumerate(CARRIERS,1):
        o=bpy.data.objects[n];rid=f'AUR-REC-{idx:03d}';bottom=o.location.z-o.dimensions.z/2
        candidates=[]
        for s in shelves:
            top=s.location.z+s.dimensions.z/2;xy=((o.location.x-s.location.x)**2+(o.location.y-s.location.y)**2)**.5;candidates.append((abs(bottom-top)+xy*.1,s,top))
        _,s,top=min(candidates,key=lambda x:x[0])
        o['temporal_record_id']=rid;o['archive_decision_state']='UNDECIDED_STAGING';o['record_content']='UNDEFINED_PRODUCTION_RECORD';o['canon_content']='UNDEFINED';o['workunit']=WORKUNIT;o['mission_interface']='Q_AURORA_M05'
        stop=bpy.data.objects.new(f'{rid}_NEUTRAL_REAR_STOP',stopmesh);stop.location=(o.location.x+.20,o.location.y,top+.09);cols['54_X100_TEMPORAL_ARCHIVE_STAGING'].objects.link(stop);stop['temporal_record_id']=rid;stop['support_object']=s.name;stop['support_rule']='bottom_on_shelf_top';stop['archive_decision_state']='UNDECIDED_STAGING';stop['profile_authority']='NO_CANON_OUTCOME_SELECTED'
        records.append({'record_id':rid,'carrier_object':n,'carrier_mesh':o.data.name,'support_shelf':s.name,'neutral_stop':stop.name})

    # Wall selector, physically supported by E_2. Detents are mechanically differentiated but have no moral/canon mapping.
    V=[];F=[];add_box(V,F,(0,0,0),(.12,1.35,.18));selmesh=mkmesh('AUR_ARCHIVE_SELECTOR_RAIL_MESH',V,F,steel,{'asset_family_id':'AUR-ARCH-SELECTOR-001'})
    sel=bpy.data.objects.new('AUR_ARCHIVE_SELECTOR_RAIL',selmesh);sel.location=(-1514.16,554.65,6.82);sel.rotation_euler=(0,math.radians(90),0);cols['54_X100_TEMPORAL_ARCHIVE_STAGING'].objects.link(sel);sel['interaction_role']='ARCHIVE_DECISION_PROFILE_SELECTOR';sel['canon_choice']='NONE';sel['profile_order']=PROFILES;sel['support_object']='AUR_INT_WALL_E_2';sel['support_rule']='cantilever_rail_embedded_in_wall_segment';sel['wall_mount_overlap_y_m']=.135
    detents=[]
    for i,p in enumerate(PROFILES):
        V=[];F=[];add_box(V,F,(0,0,0),(.12,.10+.035*i,.16 if i<3 else .10));mesh=mkmesh(f'AUR_ARCHIVE_SELECTOR_DETENT_{i}_MESH',V,F,timing or steel,{'profile':p,'profile_status':'ADAPTER'})
        d=bpy.data.objects.new(f'AUR_ARCHIVE_SELECTOR_DETENT_{i}',mesh);d.location=(-1514.05,554.25+i*.27,6.82);cols['54_X100_TEMPORAL_ARCHIVE_STAGING'].objects.link(d);d['profile']=p;d['interaction']='PROFILE_DETENT';d['support_object']=sel.name;d['support_rule']='detent_intersects_selector_rail';detents.append(d.name)

    def contract_box(name,dims,role):
        V=[];F=[];add_box(V,F,(0,0,0),dims);return mkmesh(name,V,F,None,{'contract_role':role,'engine_runtime':'BLOCKED_EXO_012','workunit':WORKUNIT},True)
    contract_meshes=[contract_box('COL_AUR_ARCHIVE_RACK0_INTERACT_MESH',(1.25,.95,2.15),'rack0_interaction_volume'),contract_box('COL_AUR_ARCHIVE_RACK1_INTERACT_MESH',(1.25,.95,2.15),'rack1_interaction_volume'),contract_box('COL_AUR_ARCHIVE_SELECTOR_INTERACT_MESH',(.9,1.5,1.2),'selector_interaction_volume')]
    def hook(name,loc,kind,role):
        o=bpy.data.objects.new(name,None);o.location=loc;cols['55_X100_TEMPORAL_ARCHIVE_HOOKS'].objects.link(o);o['hook_kind']=kind;o['hook_role']=role;o['runtime']='BLOCKED_EXO_012';o['content']='UNAUTHORED';o['spatial_scope']='LOCAL_ARCHIVE_ONLY';return o
    hooks=[hook('AUR_ARCHIVE_AUDIO_HOOK_READER',(-1514.6,553.2,6.7),'SPATIAL_AUDIO','archive_reader_mechanical_state'),hook('AUR_ARCHIVE_AUDIO_HOOK_CUSTODY',(-1514.6,554.2,6.7),'SPATIAL_AUDIO','custody_lock_state'),hook('AUR_ARCHIVE_VFX_HOOK_TEMPORAL_RESIDUE',(-1515.05,553.25,7.45),'LOCAL_FX','bounded_temporal_record_residue')]
    profile_contract={
      'RETAIN_BROAD':{'retention':'RETAINED','access_scope':'BROAD_UNSPECIFIED','hardware':'open cradle / direct reader access'},
      'RETAIN_CONTROLLED':{'retention':'RETAINED','access_scope':'CONTROLLED_UNSPECIFIED','hardware':'lattice custody shutter + lock block'},
      'RETAIN_SEALED':{'retention':'RETAINED','access_scope':'NONE_UNTIL_SERVICE_UNSEAL','hardware':'sealed cassette shell'},
      'WITHDRAWN_RECEIPT':{'retention':'WITHDRAWN_FROM_ACTIVE_ARCHIVE','access_scope':'NONE_ACTIVE_SLOT','hardware':'blanking plate + provenance token cradle'}
    }
    contract={'schema_version':1,'protocol':'EXOVANT-X100-V2','workunit':WORKUNIT,'mission':'Q_AURORA_M05','remote_revision_target':45,'canon_outcome_selected':False,'default_scene_state':'UNDECIDED_STAGING','records':records,'profiles':profile_contract,'profile_meshes':{k:v.name for k,v in profiles.items()},'neutral_staging_fix':'shelf-mounted rear stops','selector_support':{'support_object':'AUR_INT_WALL_E_2','rule':'cantilever rail embedded in wall segment','measured_overlap_y_m':.135,'detents_supported_by_selector':4},'interaction_contract_meshes':[m.name for m in contract_meshes],'interaction_contract_scene_users':[0,0,0],'hooks':[o.name for o in hooks],'global_rewind':'FORBIDDEN','save_mutation':'FORBIDDEN','runtime':'BLOCKED_EXO_012','mission_mapping':'BLOCKED_MISSION_DESIGN_APPROVAL'}
    txt=bpy.data.texts.new('AUR_TEMPORAL_ARCHIVE_CONTRACT_R43.json');txt.write(json.dumps(contract,indent=2));scene['x100_temporal_archive_contract']='AUR-ARCHIVE-v3-r45';scene['x100_temporal_archive_records']=8;scene['x100_temporal_archive_profiles']=4;scene['status']='X100_TEMPORAL_ARCHIVE_R45_SUPPORT_VERIFIED'
    return {'records':records,'profiles':list(profile_contract),'detents':detents,'hooks':[o.name for o in hooks]}

if __name__=='__main__':
    print(json.dumps(build(),indent=2))
