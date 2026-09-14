"""PELAGOS /EXOVANT-X100 — Mercado machinery systemic generator v1.

Claim: PEL/MKT/MACH-X100-003
Purpose: deterministic Blender-side semantic rebuild of the Mercado utility gallery.
Truth boundary: engineering proposals derived from marine constraints; exact energy/control
technology is intentionally unspecified until gameplay/engine authority exists.
"""
import bpy, math
from mathutils import Vector

CLAIM = "PEL/MKT/MACH-X100-003"
FLOOR_Z = 14.02
COLLECTION = "13_MERCADO_MACHINERY_X100_V1"
VARIANTS = ("compact", "standard", "heavy")
STATES = ("pristine", "used", "damaged_repaired", "abandoned")

# Current-state production assembly. Dimensions are the verified rev.36 envelopes.
FAMILIES = {
    "ACOUSTIC": {"asset_id":"PEL-MACH-ACOUSTIC-RELAY-001", "purpose":"acoustic relay / conditioning cabinet", "loc":(-517.25,-88.03), "size":(1.025,0.697,1.238), "variant":"compact", "state":"used"},
    "BALLAST": {"asset_id":"PEL-MACH-BALLAST-TRANSFER-001", "purpose":"ballast / buoyancy transfer", "loc":(-512.35,-92.00), "size":(1.550,0.960,1.135), "variant":"standard", "state":"used"},
    "DRAIN": {"asset_id":"PEL-MACH-DRAIN-PUMP-001", "purpose":"drainage / bilge pump", "loc":(-517.25,-92.00), "size":(1.450,1.180,0.880), "variant":"standard", "state":"used"},
    "FILTER": {"asset_id":"PEL-MACH-FILTER-SKID-001", "purpose":"service filtration skid", "loc":(-514.80,-92.00), "size":(1.829,1.121,1.617), "variant":"heavy", "state":"damaged_repaired"},
    "HOIST": {"asset_id":"PEL-MACH-SERVICE-HOIST-001", "purpose":"maintenance service hoist", "loc":(-512.545,-88.00), "size":(1.459,0.900,1.740), "variant":"standard", "state":"used"},
    "HX": {"asset_id":"PEL-MACH-HEAT-EXCHANGER-001", "purpose":"fluid heat-exchange skid", "loc":(-514.80,-88.00), "size":(1.450,0.880,1.350), "variant":"standard", "state":"abandoned"},
    "MANIF": {"asset_id":"PEL-MACH-EQUALIZATION-MANIFOLD-001", "purpose":"pressure / equalization manifold", "loc":(-512.60,-90.00), "size":(1.550,0.900,1.500), "variant":"standard", "state":"used"},
    "STORM": {"asset_id":"PEL-MACH-STORM-RELEASE-001", "purpose":"mooring overload / storm release", "loc":(-514.80,-90.00), "size":(1.450,0.900,1.330), "variant":"standard", "state":"pristine"},
    "WINCH": {"asset_id":"PEL-MACH-MOORING-WINCH-001", "purpose":"mooring tension winch", "loc":(-517.25,-90.00), "size":(1.829,1.180,1.333), "variant":"heavy", "state":"damaged_repaired"},
}

PLACEMENT_CONTRACT = {
    "bay_xy": (-518.5,-93.0,-509.5,-87.0),
    "utility_riser_min_clearance_m": 1.20,
    "interior_min_clearance_m": 1.20,
    "service_channel": "PEL_MKT_V1_ServiceChannel_05",
    "utility_riser": "PEL_MKT_V1_UtilityRiser",
    "floor_z_m": FLOOR_Z,
}

STATE_CAUSALITY = {
    "pristine": "no artificial wear overlay",
    "used": "handling/contact wear at access and load-transfer zones only",
    "damaged_repaired": "mismatched field repair patch + fasteners at service/load surfaces",
    "abandoned": "lower wet-zone fouling and decommissioned access state",
}


def _collection(name):
    c=bpy.data.collections.get(name)
    if c is None:
        c=bpy.data.collections.new(name); bpy.context.scene.collection.children.link(c)
    return c


def _mat(name, color, metallic=0.0, roughness=0.5):
    m=bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes=True
    bs=m.node_tree.nodes.get('Principled BSDF')
    bs.inputs['Base Color'].default_value=(*color,1)
    bs.inputs['Metallic'].default_value=metallic
    bs.inputs['Roughness'].default_value=roughness
    return m


def _link_only(obj, col):
    for c in list(obj.users_collection): c.objects.unlink(obj)
    col.objects.link(obj)


def _cube(name, loc, dims, mat, col, props=None):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    o=bpy.context.object; o.name=name; o.dimensions=dims
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    o.data.materials.append(mat); _link_only(o,col)
    # Stable UV0 for simple production proxy geometry.
    if not o.data.uv_layers: o.data.uv_layers.new(name='UVMap')
    if props:
        for k,v in props.items(): o[k]=v
    return o


def _cyl(name, loc, radius, depth, mat, col, props=None, vertices=16):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=loc)
    o=bpy.context.object; o.name=name; o.data.materials.append(mat); _link_only(o,col)
    if not o.data.uv_layers: o.data.uv_layers.new(name='UVMap')
    if props:
        for k,v in props.items(): o[k]=v
    return o


def _parent_keep_local(o, root):
    o.parent=root; o.matrix_parent_inverse.identity()


def build_machine(code, spec, col, mats):
    x,y=spec['loc']; sx,sy,sz=spec['size']
    root=bpy.data.objects.new(f"PEL_MACH_{code}",None); col.objects.link(root)
    root.location=(x,y,FLOOR_Z)
    for k,v in {"asset_id":spec['asset_id'],"role":"machine_root","claim_id":CLAIM,"purpose":spec['purpose'],"variant":spec['variant'],"state":spec['state'],"era":"ERA_1_OCCUPATION"}.items(): root[k]=v

    # Load-spreading skid / feet.
    skid=_cube(f"PEL_MACH_{code}_Skid",(0,0,0.06),(sx,sy,0.12),mats['dark'],col,{"asset_id":spec['asset_id'],"role":"service_skid"}); _parent_keep_local(skid,root)
    for ix in (-0.38,0.38):
        for iy in (-0.34,0.34):
            foot=_cube(f"PEL_MACH_{code}_Foot_{ix}_{iy}",(ix*sx,iy*sy,0.05),(0.12,0.12,0.10),mats['bronze'],col,{"asset_id":spec['asset_id'],"role":"load_spreading_foot"}); _parent_keep_local(foot,root)

    # Serviceable body; intentionally not decorative greeble.
    body=_cube(f"PEL_MACH_{code}_Body",(0,0,sz*0.50),(sx*0.82,sy*0.72,sz*0.82),mats['ivory'],col,{"asset_id":spec['asset_id'],"role":"serviceable_machine_body"}); _parent_keep_local(body,root)
    panel=_cube(f"PEL_MACH_{code}_Access",(sx*0.415,0,sz*0.54),(0.06,sy*0.48,sz*0.36),mats['dark'],col,{"asset_id":spec['asset_id'],"role":"replaceable_access_panel"}); _parent_keep_local(panel,root)
    for iy in (-0.22,0.22):
        p=_cyl(f"PEL_MACH_{code}_Port_{iy}",(0,iy*sy,sz*0.58),min(sx,sy)*0.08,min(sx,sy)*0.10,mats['bronze'],col,{"asset_id":spec['asset_id'],"role":"service_socket"}); p.rotation_euler=(0,math.pi/2,0); _parent_keep_local(p,root)

    # Family-specific functional signature.
    if code in {'DRAIN','BALLAST'}:
        imp=_cyl(f"PEL_MACH_{code}_Pump",(-sx*0.18,0,sz*0.50),min(sx,sy)*0.22,sy*0.42,mats['bronze'],col,{"asset_id":spec['asset_id'],"role":"fluid_transfer_pump"}); imp.rotation_euler=(math.pi/2,0,0); _parent_keep_local(imp,root)
    elif code=='FILTER':
        for iy in (-0.20,0.20):
            c=_cyl(f"PEL_MACH_{code}_Canister_{iy}",(0,iy*sy,sz*0.60),sy*0.13,sz*0.68,mats['ivory'],col,{"asset_id":spec['asset_id'],"role":"replaceable_filter_canister"}); _parent_keep_local(c,root)
    elif code=='WINCH':
        drum=_cyl(f"PEL_MACH_{code}_Drum",(0,0,sz*0.58),sy*0.23,sx*0.42,mats['bronze'],col,{"asset_id":spec['asset_id'],"role":"mooring_tension_drum"}); drum.rotation_euler=(0,math.pi/2,0); _parent_keep_local(drum,root)
    elif code=='STORM':
        pin=_cyl(f"PEL_MACH_{code}_ReleasePin",(0,0,sz*0.62),sy*0.14,sx*0.46,mats['amber'],col,{"asset_id":spec['asset_id'],"role":"mechanical_overload_release"}); pin.rotation_euler=(0,math.pi/2,0); _parent_keep_local(pin,root)
    elif code=='MANIF':
        for iy in (-0.25,0,0.25):
            v=_cyl(f"PEL_MACH_{code}_Valve_{iy}",(sx*0.28,iy*sy,sz*0.62),sy*0.09,0.10,mats['bronze'],col,{"asset_id":spec['asset_id'],"role":"manual_valve"}); v.rotation_euler=(0,math.pi/2,0); _parent_keep_local(v,root)
    elif code=='ACOUSTIC':
        face=_cube(f"PEL_MACH_{code}_AcousticFace",(sx*0.42,0,sz*0.56),(0.05,sy*0.54,sz*0.44),mats['cyan'],col,{"asset_id":spec['asset_id'],"role":"acoustic_status_interface"}); _parent_keep_local(face,root)
    elif code=='HX':
        for i in range(4):
            plate=_cube(f"PEL_MACH_{code}_Plate_{i}",(-sx*0.12+i*sx*0.08,0,sz*0.57),(0.035,sy*0.60,sz*0.56),mats['bronze'],col,{"asset_id":spec['asset_id'],"role":"serviceable_exchange_plate_edge"}); _parent_keep_local(plate,root)
    elif code=='HOIST':
        mast=_cube(f"PEL_MACH_{code}_Mast",(-sx*0.26,0,sz*0.64),(0.16,0.16,sz*0.72),mats['bronze'],col,{"asset_id":spec['asset_id'],"role":"service_hoist_mast"}); _parent_keep_local(mast,root)
        arm=_cube(f"PEL_MACH_{code}_Arm",(0,0,sz*0.88),(sx*0.68,0.14,0.14),mats['bronze'],col,{"asset_id":spec['asset_id'],"role":"service_hoist_arm"}); _parent_keep_local(arm,root)

    # Causal current state, not random grunge.
    state=spec['state']
    if state=='used':
        wear=_cube(f"PEL_MACH_{code}_ContactWear",(sx*0.43,0,sz*0.46),(0.025,sy*0.22,sz*0.16),mats['wear'],col,{"asset_id":spec['asset_id'],"role":"causal_contact_wear","era":"ERA_2_CURRENT"}); _parent_keep_local(wear,root)
    elif state=='damaged_repaired':
        patch=_cube(f"PEL_MACH_{code}_RepairPatch",(sx*0.43,sy*0.16,sz*0.56),(0.035,sy*0.28,sz*0.30),mats['repair'],col,{"asset_id":spec['asset_id'],"role":"field_repair_patch","era":"ERA_2_CURRENT"}); _parent_keep_local(patch,root)
    elif state=='abandoned':
        foul=_cube(f"PEL_MACH_{code}_WetFouling",(0,0,0.13),(sx*0.72,sy*0.66,0.12),mats['fouling'],col,{"asset_id":spec['asset_id'],"role":"wet_zone_biofouling","era":"ERA_2_CURRENT"}); _parent_keep_local(foul,root)

    # Hidden runtime technical proxies.
    for suffix,scale,aid_suffix,role in [('COL',0.82,'-COL','collision_proxy'),('LOD1',0.76,'-LOD1','lod1_semantic_machine_envelope')]:
        tr=bpy.data.objects.new(f"PEL_MACH_{code}_{suffix}_ROOT",None); col.objects.link(tr); tr.location=root.location
        tr['asset_id']=spec['asset_id']+aid_suffix; tr['role']=suffix.lower()+'_root'
        p=_cube(f"PEL_MACH_{code}_{suffix}_Proxy",(0,0,sz*0.50),(sx*scale,sy*scale,sz*scale),mats['debug'],col,{"asset_id":spec['asset_id']+aid_suffix,"role":role,"technical":True})
        _parent_keep_local(p,tr); p.hide_render=True; p.hide_viewport=True
    return root


def main():
    # Rebuild collection atomically.
    old=bpy.data.collections.get(COLLECTION)
    if old:
        for o in list(old.objects): bpy.data.objects.remove(o,do_unlink=True)
        bpy.data.collections.remove(old)
    col=_collection(COLLECTION)
    mats={
        'ivory':_mat('PEL_MACH_Ivory',(0.63,0.65,0.58),0.05,0.42),
        'dark':_mat('PEL_MACH_DarkComposite',(0.035,0.055,0.06),0.08,0.62),
        'bronze':_mat('PEL_MACH_OxBronze',(0.20,0.29,0.25),0.70,0.45),
        'amber':_mat('PEL_MACH_Amber',(0.35,0.14,0.02),0.08,0.34),
        'cyan':_mat('PEL_MACH_MemoryCyan',(0.025,0.30,0.39),0.03,0.30),
        'wear':_mat('PEL_MACH_ContactWear',(0.12,0.13,0.12),0.10,0.50),
        'repair':_mat('PEL_MACH_RepairPatch',(0.25,0.21,0.15),0.55,0.46),
        'fouling':_mat('PEL_MACH_WetFouling',(0.07,0.18,0.12),0.0,0.80),
        'debug':_mat('PEL_MACH_TechDebug',(0.10,0.02,0.14),0.0,0.90),
    }
    roots=[build_machine(code,spec,col,mats) for code,spec in FAMILIES.items()]
    meta=bpy.data.objects.new('PEL_MACH_X100_META',None); col.objects.link(meta)
    meta['claim_id']=CLAIM; meta['direct_configurations']=len(FAMILIES)*len(VARIANTS)*len(STATES)
    meta['cardinal_yaw_configurations']=meta['direct_configurations']*4
    meta['placement_contract']=str(PLACEMENT_CONTRACT); meta['state_causality']=str(STATE_CAUSALITY)
    return roots

if __name__=='__main__':
    main()
