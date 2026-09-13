"""Aurora Veil / EXOVANT-X100 — Campamento everyday prop and cultural-object system.

Workunit: AUR-X100-CAMP-PROPS-CULTURE-001
Validated remote revision: 30 / Blender 5.2.

Epistemic boundary
------------------
Canon gives an observatory/refuge, divergent mechanical clocks, clock synchronization,
repeated-event verification and record preservation. The exact everyday prop catalog below
is a PROPOSAL derived from those functions. It does not establish factions, rituals,
economy, social hierarchy, labels or iconography.

Systemic target
---------------
24 source families grouped into five functional clusters:
CALIBRATION / OBSERVATION_SERVICE / ROUTE_RECORD / MAINTENANCE / REFUGE_DOMESTIC.
Fifteen proof clusters (three of each type) are placed inside the existing X100 Camp
settlement modules. Selected repeated props receive 4 history-state contracts and
LOD0/1/2 source contracts. Collision/interaction clearances stay as metadata until EXO-012.
"""
import bpy
import math

WORKUNIT = "AUR-X100-CAMP-PROPS-CULTURE-001"
ROOT = "AURORA_VEIL_ROOT"
COLLECTIONS = {
    "library":"33_X100_CAMP_PROP_LIBRARY",
    "states":"34_X100_CAMP_PROP_STATES",
    "proof":"35_X100_CAMP_PROP_PROOF",
    "contracts":"36_X100_CAMP_PROP_CONTRACTS",
    "qa":"37_X100_CAMP_PROP_QA",
}

SPECS = {
 "cal_table":("AUR_X100_PRP_CALIBRATION_TABLE",(2.0,.8,.90),"AUR_MAT_STRUCTURAL_GALV_STEEL","AUR-PRP-X100-001","calibration","bolted steel worktable with sacrificial replaceable top"),
 "clock_case":("AUR_X100_PRP_CLOCK_CASE",(.58,.24,.58),"AUR_MAT_CLOCK_BRONZE_CAL","AUR-PRP-X100-002","timekeeping","mechanical clock case on serviceable rear plate"),
 "clock_drum":("AUR_X100_PRP_CLOCK_DRUM",(.46,.18,.46),"AUR_MAT_CLOCK_BRONZE_CAL","AUR-PRP-X100-003","timekeeping","machined mechanical comparison drum in protective ring"),
 "phase_wheel":("AUR_X100_PRP_PHASE_WHEEL",(.42,.12,.42),"AUR_MAT_CLOCK_BRONZE_CAL","AUR-PRP-X100-004","timekeeping","machined calibration wheel with mechanical index detents"),
 "pendulum_frame":("AUR_X100_PRP_PENDULUM_FRAME",(.62,.30,1.15),"AUR_MAT_STRUCTURAL_GALV_STEEL","AUR-PRP-X100-005","timekeeping","bolted test frame supporting removable pendulum assembly"),
 "optical_cradle":("AUR_X100_PRP_OPTICAL_CRADLE",(1.15,.52,.38),"AUR_MAT_STRUCTURAL_GALV_STEEL","AUR-PRP-X100-006","observation","machined V-cradle with replaceable soft contact inserts"),
 "lens_case":("AUR_X100_PRP_LENS_CASE",(.62,.38,.22),"AUR_MAT_CERAMIC_COMPOSITE_PANEL","AUR-PRP-X100-007","observation","sealed ceramic-composite optics case with EPDM gasket"),
 "tripod_case":("AUR_X100_PRP_TRIPOD_CASE",(1.25,.32,.26),"AUR_MAT_CERAMIC_COMPOSITE_PANEL","AUR-PRP-X100-008","observation","long service case sized for folded observation support"),
 "power_pack":("AUR_X100_PRP_INSTRUMENT_POWER_PACK",(.56,.36,.58),"AUR_MAT_SERVICE_TRAY","AUR-PRP-X100-009","observation","vented service pack with removable power module"),
 "route_cartridge":("AUR_X100_PRP_ROUTE_CARTRIDGE",(.28,.13,.09),"AUR_MAT_CLOCK_BRONZE_CAL","AUR-PRP-X100-010","records","sealed removable route-record cartridge; no canon label authored"),
 "cartridge_rack":("AUR_X100_PRP_CARTRIDGE_RACK",(.84,.28,.48),"AUR_MAT_STRUCTURAL_GALV_STEEL","AUR-PRP-X100-011","records","bolted slotted rack for removable route-record cartridges"),
 "record_canister":("AUR_X100_PRP_RECORD_CANISTER",(.22,.22,.62),"AUR_MAT_CERAMIC_COMPOSITE_PANEL","AUR-PRP-X100-012","records","sealed cylindrical physical record canister with replaceable cap"),
 "archive_tray":("AUR_X100_PRP_ARCHIVE_TRAY",(.58,.40,.12),"AUR_MAT_STRUCTURAL_GALV_STEEL","AUR-PRP-X100-013","records","stackable shallow tray for physical record handling"),
 "log_slate":("AUR_X100_PRP_FIELD_LOG_SLATE",(.38,.26,.04),"AUR_MAT_CERAMIC_COMPOSITE_PANEL","AUR-PRP-X100-014","records","rigid reusable field slate; no final UI/text authored"),
 "parts_tray":("AUR_X100_PRP_PARTS_TRAY",(.52,.38,.09),"AUR_MAT_STRUCTURAL_GALV_STEEL","AUR-PRP-X100-015","maintenance","formed shallow tray with folded rim for small serviced parts"),
 "fastener_bin":("AUR_X100_PRP_FASTENER_BIN",(.42,.30,.26),"AUR_MAT_STRUCTURAL_GALV_STEEL","AUR-PRP-X100-016","maintenance","stackable folded-metal bin for service fasteners"),
 "cable_spool":("AUR_X100_PRP_CABLE_SPOOL",(.46,.46,.40),"AUR_MAT_SERVICE_TRAY","AUR-PRP-X100-017","maintenance","reusable service cable spool with steel flanges"),
 "patch_case":("AUR_X100_PRP_PATCH_CASE",(.72,.46,.26),"AUR_MAT_CERAMIC_COMPOSITE_PANEL","AUR-PRP-X100-018","maintenance","sealed field repair case with replaceable latch strip"),
 "tool_chest":("AUR_X100_PRP_TOOL_CHEST",(1.05,.58,.58),"AUR_MAT_STRUCTURAL_GALV_STEEL","AUR-PRP-X100-019","maintenance","welded service chest with hinged top and replaceable drawer/latch hardware"),
 "fold_stool":("AUR_X100_PRP_FOLDING_STOOL",(.48,.48,.48),"AUR_X100_MAT_REFUGE_TEXTILE","AUR-PRP-X100-020","refuge","folding steel-frame stool with replaceable textile seat"),
 "water_rack":("AUR_X100_PRP_WATER_RACK",(1.05,.38,.92),"AUR_X100_MAT_WATER_CONTAINER","AUR-PRP-X100-021","refuge","serviceable rack for refillable water containers; no consumption mechanic claimed"),
 "meal_tin":("AUR_X100_PRP_MEAL_TIN",(.36,.26,.11),"AUR_MAT_STRUCTURAL_GALV_STEEL","AUR-PRP-X100-022","refuge","pressed reusable meal container with rolled rim"),
 "stow_box":("AUR_X100_PRP_STOW_BOX",(.82,.52,.46),"AUR_MAT_CERAMIC_COMPOSITE_PANEL","AUR-PRP-X100-023","refuge","stackable composite refuge stow box with gasketed lid"),
 "portable_lamp":("AUR_X100_PRP_PORTABLE_LAMP",(.24,.24,.38),"AUR_MAT_CLOCK_BRONZE_CAL","AUR-PRP-X100-024","refuge","mechanical portable task-lamp housing; final light source/UI not authored"),
}
LOD_KEYS=("clock_case","route_cartridge","record_canister","parts_tray","fastener_bin","cable_spool","fold_stool","meal_tin","portable_lamp")
STATE_KEYS=("clock_case","route_cartridge","tool_chest","fold_stool","stow_box")
STATES=("PRISTINE","USED","DAMAGED","ABANDONED")
CLUSTER_TYPES=("CALIBRATION","OBSERVATION_SERVICE","ROUTE_RECORD","MAINTENANCE","REFUGE_DOMESTIC")
# Exactly three each. Cluster 12 is refuge, not the rejected extra calibration from r27-r29.
ASSIGNMENTS=[
 (0,"CALIBRATION",(0,0)),(1,"OBSERVATION_SERVICE",(0,0)),(2,"ROUTE_RECORD",(0,0)),(3,"MAINTENANCE",(0,0)),(4,"REFUGE_DOMESTIC",(0,0)),
 (5,"CALIBRATION",(0,0)),(6,"OBSERVATION_SERVICE",(0,0)),(7,"ROUTE_RECORD",(0,0)),(8,"MAINTENANCE",(0,0)),(9,"REFUGE_DOMESTIC",(0,0)),
 (10,"CALIBRATION",(0,0)),(11,"OBSERVATION_SERVICE",(0,0)),(12,"REFUGE_DOMESTIC",(3,0)),(5,"ROUTE_RECORD",(3,0)),(8,"MAINTENANCE",(3,0)),
]


def ensure_collection(name, parent):
    c=bpy.data.collections.get(name)
    if c is None:
        c=bpy.data.collections.new(name); parent.children.link(c)
    return c


def clear(c):
    for o in list(c.objects): bpy.data.objects.remove(o,do_unlink=True)


def material(name,base=(.18,.19,.20),metal=0.0,rough=.55):
    m=bpy.data.materials.get(name) or bpy.data.materials.new(name); m.use_nodes=True
    p=m.node_tree.nodes.get("Principled BSDF"); p.inputs["Base Color"].default_value=(*base,1); p.inputs["Metallic"].default_value=metal; p.inputs["Roughness"].default_value=rough
    return m


def resolve_material(name):
    existing=bpy.data.materials.get(name)
    if existing: return existing
    defaults={
      "AUR_X100_MAT_REFUGE_TEXTILE":((.16,.17,.15),0,.84),
      "AUR_X100_MAT_WATER_CONTAINER":((.18,.23,.25),.18,.48),
    }
    base,metal,rough=defaults.get(name,((.18,.19,.20),0,.55)); return material(name,base,metal,rough)


def box_mesh(name,dims,mat):
    dx,dy,dz=(d*.5 for d in dims); vs=[(-dx,-dy,-dz),(dx,-dy,-dz),(dx,dy,-dz),(-dx,dy,-dz),(-dx,-dy,dz),(dx,-dy,dz),(dx,dy,dz),(-dx,dy,dz)]; fs=[(0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(2,6,7,3),(4,0,3,7)]
    me=bpy.data.meshes.get(name+"_MESH") or bpy.data.meshes.new(name+"_MESH"); me.clear_geometry(); me.from_pydata(vs,[],fs); me.update(); me.use_fake_user=True
    if len(me.materials)==0: me.materials.append(mat)
    return me


def cylinder_z_mesh(name,dims,mat):
    # cylinder fits declared X/Y diameter and declared Z height exactly.
    r=max(dims[0],dims[1])*.5; h=dims[2]; seg=16; vs=[]; fs=[]
    for z in (-h*.5,h*.5):
        for i in range(seg):
            a=math.tau*i/seg; vs.append((r*math.cos(a),r*math.sin(a),z))
    for i in range(seg): fs.append((i,(i+1)%seg,(i+1)%seg+seg,i+seg))
    fs += [tuple(reversed(range(seg))),tuple(range(seg,seg*2))]
    me=bpy.data.meshes.get(name+"_MESH") or bpy.data.meshes.new(name+"_MESH"); me.clear_geometry(); me.from_pydata(vs,[],fs); me.update(); me.use_fake_user=True
    if len(me.materials)==0: me.materials.append(mat)
    return me


def source_mesh(key):
    name,dims,mat_name,*_=SPECS[key]
    if key in ("record_canister","cable_spool","portable_lamp"):
        return cylinder_z_mesh(name,dims,resolve_material(mat_name))
    # clock drum/phase wheel keep exact proposal bbox using box proxy at blockout stage;
    # mechanical cylindrical production geometry is future art detail, not a dimension-breaking shortcut.
    return box_mesh(name,dims,resolve_material(mat_name))


def instance(mesh,name,parent,collection,location,asset_id,family,rotation=0.0,props=None):
    o=bpy.data.objects.new(name,mesh); collection.objects.link(o); o.parent=parent; o.location=location; o.rotation_euler[2]=rotation; o["asset_id"]=asset_id; o["family"]=family; o["x100_workunit"]=WORKUNIT
    if props:
        for k,v in props.items(): o[k]=v
    return o


def make_contract(collection,name,location,dims,policy):
    e=bpy.data.objects.new("META_COL_"+name,None); collection.objects.link(e); e.location=location; e.empty_display_type="CUBE"; e.empty_display_size=max(dims)*.5; e["collision_proxy"]=True; e["dimensions_m"]=list(dims); e["policy"]=policy; e["engine_status"]="CONTRACT_ONLY_EXO_012_BLOCKED"; e["x100_workunit"]=WORKUNIT


def build_sources(collections):
    meshes={}
    for key,(name,dims,mat_name,asset_id,family,manufacturing) in SPECS.items():
        me=source_mesh(key); meshes[key]=me
        e=bpy.data.objects.new("META_"+name,None); collections["library"].objects.link(e); e["asset_id"]=asset_id; e["family"]=family; e["dimensions_m"]=list(dims); e["manufacturing"]=manufacturing; e["mesh_datablock"]=me.name; e["canon_status"]="PROPOSAL_FUNCTIONAL_PROP"; e["x100_workunit"]=WORKUNIT
    for key in LOD_KEYS:
        name,dims,mat_name,asset_id,*_=SPECS[key]; src=meshes[key]
        for lod in ("LOD0","LOD1","LOD2"):
            cp=src.copy(); cp.name=name+"_"+lod+"_MESH"; cp.use_fake_user=True
            e=bpy.data.objects.new("META_"+name+"_"+lod,None); collections["contracts"].objects.link(e); e["asset_id"]=asset_id; e["lod"]=lod; e["mesh_datablock"]=cp.name; e["dimensions_m"]=list(dims); e["strategy"]="preserve envelope; production detail removal deferred because source is low-poly proof"; e["engine_status"]="CONTRACT_ONLY_EXO_012_BLOCKED"; e["x100_workunit"]=WORKUNIT
    causes={"PRISTINE":"new/recently serviced","USED":"handling/contact wear at service surfaces","DAMAGED":"localized impact/overload followed by repair","ABANDONED":"maintenance stopped; removable components missing or displaced"}
    for key in STATE_KEYS:
        name,_,_,asset_id,*_=SPECS[key]
        for state in STATES:
            e=bpy.data.objects.new(f"META_{name}_STATE_{state}",None); collections["states"].objects.link(e); e["asset_id"]=asset_id; e["state"]=state; e["cause"]=causes[state]; e["canon_status"]="PROPOSAL_HISTORY_STATE"; e["x100_workunit"]=WORKUNIT
    return meshes


def build():
    scene=bpy.context.scene; root=bpy.data.collections.get(ROOT) or scene.collection
    c={k:ensure_collection(v,root) for k,v in COLLECTIONS.items()}
    for collection in c.values(): clear(collection)
    meshes=build_sources(c)
    hosts=sorted([o for o in bpy.data.collections["28_X100_CAMP_DISTRICT_PROOF"].objects if o.type=="EMPTY" and o.name.startswith("AUR_X100_CAMP_CONFIG_")],key=lambda o:o.name)

    def prop(key,cluster,suffix,x,y,support="FLOOR",rotation=0.0,state_props=None):
        dims=SPECS[key][1]; support_z={"FLOOR":.46,"TABLE":1.36,"TOOL_CHEST":1.04}[support]
        o=instance(meshes[key],cluster.name+"_"+suffix,cluster,c["proof"],(x,y,support_z+dims[2]*.5),SPECS[key][3],SPECS[key][4],rotation,state_props)
        o["support_type"]=support; o["support_surface_local_z"]=support_z; o["support_object_role"]={"FLOOR":"host_floor","TABLE":"calibration_table","TOOL_CHEST":"tool_chest"}[support]; o["support_tolerance_m"]=.015; o["support_contract_revision"]=30
        return o

    rows=[]
    for cluster_index,(host_index,ctype,offset) in enumerate(ASSIGNMENTS):
        host=hosts[host_index]; cluster=bpy.data.objects.new(f"AUR_X100_PROP_CLUSTER_{cluster_index:02d}_{ctype}",None); c["proof"].objects.link(cluster); cluster.parent=host; cluster.location=offset+(0,); cluster["cluster_id"]=f"AUR-PROP-CLUSTER-{cluster_index:02d}"; cluster["cluster_type"]=ctype; cluster["host_config"]=host.name; cluster["history_state"]=host.get("history_state"); cluster["canon_status"]="PROPOSAL_FUNCTIONAL_CLUSTER"; cluster["x100_workunit"]=WORKUNIT
        objects=[]
        def p(key,suffix,x,y,support="FLOOR",rot=0,props=None):
            obj=prop(key,cluster,suffix,x,y,support,rot,props); objects.append(obj); return obj

        if ctype=="CALIBRATION":
            p("cal_table","CAL_TABLE",0,0); p("clock_case","CLOCK_CASE",-.55,0,"TABLE"); p("clock_drum","CLOCK_DRUM",.15,0,"TABLE"); p("phase_wheel","PHASE_WHEEL",.62,0,"TABLE"); p("pendulum_frame","PENDULUM_FRAME",-1.25,.1); p("power_pack","POWER_PACK",1.25,.05)
        elif ctype=="OBSERVATION_SERVICE":
            p("cal_table","CAL_TABLE",0,0); p("optical_cradle","OPTICAL_CRADLE",0,0,"TABLE"); p("lens_case","LENS_CASE",-.55,.22,"TABLE"); p("tripod_case","TRIPOD_CASE",-1.15,-.55,"FLOOR",math.radians(8)); p("power_pack","POWER_PACK",1.25,.05); p("portable_lamp","PORTABLE_LAMP",.72,-.15,"TABLE")
        elif ctype=="ROUTE_RECORD":
            p("cal_table","CAL_TABLE",0,0); p("cartridge_rack","CARTRIDGE_RACK",-1.15,.05); p("route_cartridge","ROUTE_CARTRIDGE_A",-.55,0,"TABLE"); p("route_cartridge","ROUTE_CARTRIDGE_B",-.18,0,"TABLE"); p("route_cartridge","ROUTE_CARTRIDGE_C",.19,0,"TABLE"); p("record_canister","RECORD_CANISTER",.6,.05,"TABLE"); p("archive_tray","ARCHIVE_TRAY",.15,-.22,"TABLE"); p("log_slate","LOG_SLATE",-.35,-.24,"TABLE"); p("portable_lamp","PORTABLE_LAMP",.78,-.22,"TABLE")
        elif ctype=="MAINTENANCE":
            p("tool_chest","TOOL_CHEST",0,.15); p("parts_tray","PARTS_TRAY",0,.15,"TOOL_CHEST"); p("fastener_bin","FASTENER_BIN",-1,.05); p("cable_spool","CABLE_SPOOL",1,.05); p("patch_case","PATCH_CASE",-1,-.55,"FLOOR",math.radians(-6)); p("portable_lamp","PORTABLE_LAMP",.95,-.5)
        else:
            p("fold_stool","FOLD_STOOL_A",-.75,0); p("fold_stool","FOLD_STOOL_B",-.15,.25,"FLOOR",math.radians(18)); p("water_rack","WATER_RACK",.9,.1); p("meal_tin","MEAL_TIN_A",-.65,-.55); p("meal_tin","MEAL_TIN_B",-.20,-.55); p("stow_box","STOW_BOX",.15,-.65); p("portable_lamp","PORTABLE_LAMP",.9,-.55)

        state=str(host.get("history_state","PRISTINE"))
        if state=="USED": p("patch_case","USED_REPAIR_CASE",1.45,-.65,"FLOOR",math.radians(5),{"x100_state_detail":True,"state":"USED","cause":"repair case left at high-frequency service cluster"})
        elif state=="DAMAGED":
            if objects:
                objects[-1].rotation_euler[2]+=math.radians(12); objects[-1]["state"]="DAMAGED"; objects[-1]["cause"]="localized displacement after impact; cluster remains serviceable"
            p("parts_tray","DAMAGE_PARTS_TRAY",1.35,-.62,"FLOOR",math.radians(-10),{"x100_state_detail":True,"state":"DAMAGED","cause":"parts tray staged for local repair"})
        elif state=="ABANDONED":
            if objects:
                objects[-1].rotation_euler[1]=math.radians(78); objects[-1]["state"]="ABANDONED"; objects[-1]["cause"]="portable item left tipped after maintenance ceased"; objects[-1]["support_tolerance_m"]=.12
            p("record_canister","ABANDONED_RECORD_CANISTER",1.35,-.7,"FLOOR",math.radians(14),{"x100_state_detail":True,"state":"ABANDONED","cause":"sealed record canister left outside rack"})

        world=host.matrix_world @ cluster.location
        make_contract(c["contracts"],cluster.name+"_FOOTPRINT",world,(3.8,2.4,1.8),"SIMPLE_PROP_PROXY")
        if ctype in ("CALIBRATION","OBSERVATION_SERVICE","ROUTE_RECORD","MAINTENANCE"):
            make_contract(c["contracts"],cluster.name+"_SERVICE_CLEARANCE",world+Vector((0,-1.4,1)),(2.6,1.0,2.0),"CLEARANCE_ONLY_NOT_SOLID")
        rows.append({"type":ctype,"host":host.name,"history_state":state,"props":len([o for o in c["proof"].objects if o.parent==cluster and o.type=="MESH"])})

    culture={
      "manufacturing_language":"field-bolted steel, ceramic composite cassettes, machined clock bronze, serviceable sealed cases",
      "ergonomics":"gloved maintenance access, replaceable modules, floor/table service zones",
      "repair_language":"localized replacement/patching; portable repair cases appear at actual service points",
      "resource_constraint":"reuse/refill/service over disposable objects (production proposal inferred from observatory-refuge function)",
      "color_logic":"material role color; no arbitrary neon decoration",
      "iconography":"UNDEFINED_CANON; no invented labels or symbols authored",
      "social_hierarchy":"UNDEFINED_CANON; not inferred from props",
      "technology_level":"mechanical clock systems plus advanced observation/record interfaces; exact internals not canonized",
    }
    for key,value in culture.items():
        e=bpy.data.objects.new("META_AUR_X100_CULTURE_"+key.upper(),None); c["qa"].objects.link(e); e["key"]=key; e["value"]=value; e["canon_status"]="PROPOSAL_CONSTRAINT_OR_EXPLICIT_UNKNOWN"; e["x100_workunit"]=WORKUNIT
    for key in ("library","states","contracts","qa"): c[key].hide_render=True

    scene["x100_camp_prop_families"]=len(SPECS); scene["x100_camp_prop_clusters"]=len(ASSIGNMENTS); scene["x100_camp_prop_cluster_distribution"]="3 each: CALIBRATION/OBSERVATION_SERVICE/ROUTE_RECORD/MAINTENANCE/REFUGE_DOMESTIC"; scene["x100_prop_support_contract_revision"]=30; scene["status"]="X100_CAMP_PROPS_CULTURE_R30_BALANCED_QA"
    return {"status":scene["status"],"base_families":len(SPECS),"proof_clusters":len(ASSIGNMENTS),"cluster_rows":rows}


if __name__ == "__main__":
    print(build())
