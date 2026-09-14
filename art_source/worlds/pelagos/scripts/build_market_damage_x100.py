"""PELAGOS /EXOVANT-X100 — Mercado architecture damage/recovery state-swap kit v1.

Claim: PEL/MKT/DAMAGE-X100-005

Reversible overlay/replacement-module system. Base architecture is never destructively
edited by this generator. Runtime fracture, navmesh mutation, debris physics and save
persistence remain outside this Blender-side authority.
"""
import bpy
import math
from mathutils import Vector

CLAIM = "PEL/MKT/DAMAGE-X100-005"
COLLECTION = "15_MERCADO_DAMAGE_X100_V1"
STATES = ("stressed", "damaged", "field_repaired", "abandoned")
VARIANTS = ("minor", "standard", "severe")

FAMILIES = {
    "DECK": {
        "asset_id":"PEL-DMG-DECK-IMPACT-001", "target":"PEL_MKT_Platform_00",
        "point":(-552,-90,13.5), "normal":(0,0,1),
        "driver":"docking_or_dropped_load_impact", "current":"field_repaired", "scale":1.15,
    },
    "CANOPY": {
        "asset_id":"PEL-DMG-CANOPY-TEAR-001", "target":"PEL_MKT_V1_CanopyMembrane_3",
        "point":(-510.56097,-89.43903,39.17073), "normal":(0.56604,-0.56604,0.59933),
        "driver":"storm_tension_uv_and_flex_tear", "current":"damaged", "scale":1.30,
    },
    "BRIDGE": {
        "asset_id":"PEL-DMG-BRIDGE-HINGE-001", "target":"PEL_MKT_Bridge_0_3",
        "point":(-517,10,16), "normal":(0.95106,0,-0.30901),
        "driver":"cyclic_flex_and_hinge_overload", "current":"field_repaired", "scale":1.05,
    },
    "HATCH": {
        "asset_id":"PEL-DMG-HATCH-SEAL-001", "target":"PEL_MKT_V1_Hatch",
        "point":(-520.00006,-80,14.425), "normal":(0,0,1),
        "driver":"salt_corrosion_and_seal_ingress", "current":"stressed", "scale":1.15,
    },
    "BUOY": {
        "asset_id":"PEL-DMG-BUOY-LEAK-001", "target":"PEL_MKT_V1_BuoyPod_06",
        "point":(-555.20001,-80,4.5), "normal":(-0.98769,-0.15645,0),
        "driver":"docking_impact_pressure_shell_leak", "current":"field_repaired", "scale":1.20,
    },
    "MOORING": {
        "asset_id":"PEL-DMG-MOORING-OVERLOAD-001", "target":"PEL_MKT_V1_MooringCleat_04",
        "point":(-558,-80,14.675), "normal":(0,0,1),
        "driver":"storm_or_tow_overload_at_mooring_load_path", "current":"damaged", "scale":0.85,
    },
    "UTILITY": {
        "asset_id":"PEL-DMG-UTILITY-INGRESS-001", "target":"PEL_MKT_V1_ServiceChannel_04",
        "point":(-531.1051,-99.78462,13.745), "normal":(0.80018,-0.46197,0.38248),
        "driver":"fluid_ingress_and_service_cover_failure", "current":"field_repaired", "scale":1.10,
    },
    "SHELL": {
        "asset_id":"PEL-DMG-SHELL-STRESS-001", "target":"PEL_MKT_CommandShell",
        "point":(-507.2876,-92.90078,23), "normal":(0.47215,-0.84607,0.24746),
        "driver":"platform_flex_and_shell_stress_concentration", "current":"field_repaired", "scale":1.35,
    },
}


def _reset_collection(name):
    old=bpy.data.collections.get(name)
    if old:
        for o in list(old.objects): bpy.data.objects.remove(o,do_unlink=True)
        bpy.data.collections.remove(old)
    c=bpy.data.collections.new(name); bpy.context.scene.collection.children.link(c); return c


def _link_only(o,col):
    for c in list(o.users_collection): c.objects.unlink(o)
    col.objects.link(o)


def _mat(name,color,rough=.55,metal=0.0):
    m=bpy.data.materials.get(name) or bpy.data.materials.new(name); m.use_nodes=True
    bs=m.node_tree.nodes.get('Principled BSDF'); bs.inputs['Base Color'].default_value=(*color,1); bs.inputs['Roughness'].default_value=rough; bs.inputs['Metallic'].default_value=metal
    return m


def _semantic(o,spec,code,state,role,variant='standard',extra=None):
    data={
        'asset_id':spec['asset_id'],'claim_id':CLAIM,'family':code,'damage_state':state,'role':role,
        'variant':variant,'target_object':spec['target'],'damage_driver':spec['driver'],
        'collision_policy':'none_or_query_until_runtime_damage_binding',
        'gameplay_tag':'damage_state_swap_candidate',
    }
    if extra: data.update(extra)
    for k,v in data.items(): o[k]=v


def _parent(o,r): o.parent=r; o.matrix_parent_inverse.identity()


def _cube(name,loc,dims,ma,r,spec,code,state,role,col,variant='standard',rot=None,extra=None):
    bpy.ops.mesh.primitive_cube_add(location=loc); o=bpy.context.object; o.name=name; o.dimensions=dims
    if rot: o.rotation_euler=rot
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True); o.data.materials.append(ma); _link_only(o,col)
    if not o.data.uv_layers: o.data.uv_layers.new(name='UVMap')
    _semantic(o,spec,code,state,role,variant,extra); _parent(o,r); return o


def _cyl(name,loc,rad,depth,ma,r,spec,code,state,role,col,variant='standard',rot=None,vertices=12,extra=None):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices,radius=rad,depth=depth,location=loc); o=bpy.context.object; o.name=name
    if rot: o.rotation_euler=rot
    o.data.materials.append(ma); _link_only(o,col); _semantic(o,spec,code,state,role,variant,extra); _parent(o,r); return o


def _ico(name,loc,rad,ma,r,spec,code,state,role,col,variant='standard',scale=None,extra=None):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,radius=rad,location=loc); o=bpy.context.object; o.name=name
    if scale:
        o.scale=scale; bpy.context.view_layer.objects.active=o; o.select_set(True); bpy.ops.object.transform_apply(location=False,rotation=False,scale=True); o.select_set(False)
    o.data.materials.append(ma); _link_only(o,col); _semantic(o,spec,code,state,role,variant,extra); _parent(o,r); return o


def _fasteners(root,spec,code,state,s,mats,col):
    for x,y in ((-.38,-.26),(-.38,.26),(.38,-.26),(.38,.26)):
        _cyl(f'{root.name}_FAST_{x}_{y}',(x*s,y*s,.06),.045*s,.10,mats['bronze'],root,spec,code,state,'repair_fastener',col,vertices=10)


def _stress(root,spec,code,state,s,mats,col):
    for i,(ang,length) in enumerate(((-.55,.72),(-.15,.95),(.28,.76))):
        _cube(f'{root.name}_STRESS_{i}',(.11*math.cos(ang),.11*math.sin(ang),.022),(length*s,.035*s,.035),mats['dark'],root,spec,code,state,'stress_concentration_trace',col,rot=(0,0,ang))


def _patch(root,spec,code,state,s,mats,col,material='ivory'):
    _cube(root.name+'_PATCH',(0,0,.045),(1.0*s,.72*s,.09),mats[material],root,spec,code,state,'mismatched_field_repair_patch',col)
    _fasteners(root,spec,code,state,s*.95,mats,col)


def _abandoned(root,spec,code,state,s,mats,col):
    _stress(root,spec,code,state,s,mats,col)
    for i,(x,y) in enumerate(((-.28,-.18),(.18,.20),(.34,-.12))):
        _ico(f'{root.name}_FOUL_{i}',(x*s,y*s,.07),.12*s,mats['fouling'],root,spec,code,state,'persistent_wet_fouling',col,scale=(1.5,1.0,.35))


def _family_geometry(root,spec,code,state,s,mats,col):
    # All contact faces begin at local z=0 and extend outward along local +Z.
    if code=='DECK':
        if state in ('damaged','abandoned'): _stress(root,spec,code,state,s*1.15,mats,col)
        if state=='field_repaired': _patch(root,spec,code,state,s*1.15,mats,col,'ivory')
        _cube(root.name+'_LOAD_EDGE',(-.52*s,0,.035),(.08,.78*s,.07),mats['bronze'],root,spec,code,state,'load_spread_edge_plate',col)

    elif code=='CANOPY':
        if state=='stressed':
            for a in (-.25,.25): _cube(f'{root.name}_TENSION_{a}',(0,a*s,.018),(1.05*s,.055,.035),mats['textile'],root,spec,code,state,'tension_whitening_reinforcement_line',col,rot=(0,0,.18*a))
        elif state=='damaged':
            _cube(root.name+'_TEAR_EDGE',(-.18*s,0,.035),(.06,1.15*s,.07),mats['dark'],root,spec,code,state,'tear_edge_restraint',col)
            _cube(root.name+'_LIFTED_FLAP',(.15*s,.10*s,.10),(.52*s,.62*s,.035),mats['textile'],root,spec,code,state,'lifted_torn_membrane_flap',col,rot=(math.radians(12),math.radians(-8),.12))
        elif state=='field_repaired':
            _cube(root.name+'_TEXTILE_PATCH',(0,0,.026),(1.05*s,.82*s,.045),mats['textile'],root,spec,code,state,'stitched_membrane_patch',col)
            for a in (-.55,.55): _cube(f'{root.name}_STRAP_{a}',(0,0,.055),(1.30*s,.05,.04),mats['bronze'],root,spec,code,state,'repair_tension_strap',col,rot=(0,0,a))
        else: _abandoned(root,spec,code,state,s,mats,col)

    elif code=='BRIDGE':
        _cyl(root.name+'_HINGE_COLLAR',(0,0,.10),.34*s,.18,mats['bronze'],root,spec,code,state,'hinge_reinforcement_collar',col,rot=(math.pi/2,0,0),vertices=16)
        if state=='stressed': _stress(root,spec,code,state,s*.65,mats,col)
        elif state=='damaged': _cube(root.name+'_BENT_GUSSET',(.20*s,0,.16),(.60*s,.16,.18),mats['dark'],root,spec,code,state,'bent_hinge_gusset',col,rot=(0,.18,.22))
        elif state=='field_repaired':
            for y in (-.28,.28): _cube(f'{root.name}_BRACE_{y}',(0,y*s,.12),(.85*s,.12,.16),mats['bronze'],root,spec,code,state,'external_hinge_brace',col,rot=(0,0,.08*y))
        else: _abandoned(root,spec,code,state,s*.8,mats,col)

    elif code=='HATCH':
        for x,y,dx,dy in ((0,.48*s,.88*s,.06),(0,-.48*s,.88*s,.06),(.48*s,0,.06,.88*s),(-.48*s,0,.06,.88*s)):
            _cube(f'{root.name}_SEAL_{x}_{y}',(x,y,.025),(dx,dy,.05),mats['dark'],root,spec,code,state,'service_hatch_seal_band',col)
        if state=='stressed': _stress(root,spec,code,state,s*.55,mats,col)
        elif state=='damaged': _cube(root.name+'_SEAL_LIFT',(.30*s,.32*s,.08),(.42*s,.08,.10),mats['corrosion'],root,spec,code,state,'locally_lifted_corroded_seal',col,rot=(0,.10,.22))
        elif state=='field_repaired': _fasteners(root,spec,code,state,s*.9,mats,col)
        else: _abandoned(root,spec,code,state,s*.65,mats,col)

    elif code=='BUOY':
        if state=='stressed':
            for y in (-.34,.34): _cube(f'{root.name}_BAND_{y}',(0,y*s,.035),(1.05*s,.08,.07),mats['bronze'],root,spec,code,state,'pressure_shell_reinforcement_band',col)
        elif state=='damaged':
            _ico(root.name+'_DENT',(0,0,.06),.36*s,mats['dark'],root,spec,code,state,'impact_dent_marker',col,scale=(1.45,.85,.24))
            _cube(root.name+'_LEAK_TRACE',(.10*s,0,.10),(.12,.52*s,.06),mats['amber'],root,spec,code,state,'pressure_leak_service_marker',col)
        elif state=='field_repaired':
            _patch(root,spec,code,state,s,mats,col,'bronze')
            for y in (-.38,.38): _cube(f'{root.name}_CLAMP_{y}',(0,y*s,.10),(1.25*s,.07,.10),mats['dark'],root,spec,code,state,'leak_repair_clamp_band',col)
        else: _abandoned(root,spec,code,state,s*.8,mats,col)

    elif code=='MOORING':
        _cube(root.name+'_OVERLOAD_PLATE',(0,0,.035),(.92*s,.62*s,.07),mats['bronze'],root,spec,code,state,'mooring_overload_spreader_plate',col)
        if state=='stressed': _stress(root,spec,code,state,s*.55,mats,col)
        elif state=='damaged': _cube(root.name+'_YIELD_BAR',(.05*s,0,.15),(.75*s,.10,.18),mats['dark'],root,spec,code,state,'yielded_load_path_bar',col,rot=(0,.18,.15))
        elif state=='field_repaired': _fasteners(root,spec,code,state,s*.78,mats,col)
        else: _abandoned(root,spec,code,state,s*.65,mats,col)

    elif code=='UTILITY':
        _cube(root.name+'_COVER',(0,0,.035),(1.25*s,.62*s,.07),mats['ivory'],root,spec,code,state,'replaceable_service_channel_cover',col)
        for y in (-.36,.36): _cube(f'{root.name}_DRAIN_LIP_{y}',(0,y*s,.075),(1.22*s,.055,.08),mats['bronze'],root,spec,code,state,'drainage_edge_lip',col)
        if state=='stressed': _stress(root,spec,code,state,s*.55,mats,col)
        elif state=='damaged': _cube(root.name+'_OPEN_EDGE',(.38*s,0,.13),(.45*s,.14,.15),mats['dark'],root,spec,code,state,'exposed_service_edge',col,rot=(0,.12,.08))
        elif state=='field_repaired': _fasteners(root,spec,code,state,s*.95,mats,col)
        else: _abandoned(root,spec,code,state,s*.7,mats,col)

    else:  # SHELL
        _stress(root,spec,code,state,s*.95,mats,col)
        if state=='damaged': _cube(root.name+'_LOCAL_DEFORMATION',(0,0,.08),(.70*s,.50*s,.12),mats['dark'],root,spec,code,state,'shell_local_deformation_indicator',col,rot=(0,.08,-.10))
        elif state=='field_repaired':
            for a in (-.55,.55): _cube(f'{root.name}_EMERGENCY_BRACE_{a}',(0,0,.10),(1.45*s,.09,.12),mats['bronze'],root,spec,code,state,'emergency_external_brace',col,rot=(0,0,a))
            _fasteners(root,spec,code,state,s*.92,mats,col)
        elif state=='abandoned': _abandoned(root,spec,code,state,s*.85,mats,col)


def _build_state(code,spec,state,visible,mats,col):
    root=bpy.data.objects.new(f'PEL_DMG_{code}_{state.upper()}',None); col.objects.link(root)
    root.location=spec['point']; root.rotation_mode='QUATERNION'; root.rotation_quaternion=Vector(spec['normal']).normalized().to_track_quat('Z','Y')
    variant='standard' if state in ('stressed','field_repaired') else ('severe' if state=='abandoned' else 'minor')
    for k,v in {
        'asset_id':spec['asset_id'],'claim_id':CLAIM,'role':'damage_state_root','family':code,'damage_state':state,
        'variant':variant,'target_object':spec['target'],'damage_driver':spec['driver'],'surface_point':spec['point'],
        'surface_normal':spec['normal'],'is_current_state':bool(visible),'state_swap_group':spec['asset_id'],
        'collision_policy':'none_or_query_until_runtime_damage_binding','gameplay_tag':'damage_state_swap_candidate',
    }.items(): root[k]=v
    _family_geometry(root,spec,code,state,spec['scale'],mats,col)
    if not visible:
        root.hide_viewport=True; root.hide_render=True
        for c in root.children: c.hide_viewport=True; c.hide_render=True
    return root


def main():
    col=_reset_collection(COLLECTION)
    mats={
        'ivory':_mat('PEL_DMG_IvoryPatch',(.64,.65,.57),.42,.04),
        'dark':_mat('PEL_DMG_DarkScar',(.045,.055,.055),.68,.06),
        'bronze':_mat('PEL_DMG_RepairBronze',(.23,.30,.26),.48,.65),
        'textile':_mat('PEL_DMG_TextilePatch',(.025,.045,.052),.76,0),
        'corrosion':_mat('PEL_DMG_Corrosion',(.25,.20,.12),.82,.18),
        'fouling':_mat('PEL_DMG_Fouling',(.07,.18,.12),.84,0),
        'amber':_mat('PEL_DMG_Amber',(.34,.13,.02),.38,.08),
        'debug':_mat('PEL_DMG_Tech',(.12,.02,.14),.90,0),
    }
    roots=[]
    for code,spec in FAMILIES.items():
        for state in STATES:
            roots.append(_build_state(code,spec,state,state==spec['current'],mats,col))

    for code,spec in FAMILIES.items():
        tr=bpy.data.objects.new(f'PEL_DMG_{code}_LOD1_ROOT',None); col.objects.link(tr); tr.location=spec['point']; tr.rotation_mode='QUATERNION'; tr.rotation_quaternion=Vector(spec['normal']).normalized().to_track_quat('Z','Y')
        tr['asset_id']=spec['asset_id']+'-LOD1'; tr['role']='lod1_damage_family_root'; tr['technical']=True
        p=_cube(f'PEL_DMG_{code}_LOD1_PROXY',(0,0,.04),(.85*spec['scale'],.60*spec['scale'],.08),mats['debug'],tr,spec,code,'technical','lod1_damage_envelope',col,extra={'technical':True})
        p.hide_viewport=True; p.hide_render=True; tr.hide_viewport=True; tr.hide_render=True

    meta=bpy.data.objects.new('PEL_DMG_X100_META',None); col.objects.link(meta)
    meta['claim_id']=CLAIM; meta['family_count']=8; meta['states_per_family']=4; meta['authored_state_roots']=32
    meta['variants']=3; meta['direct_variant_state_combinations']=96
    meta['runtime_truth']='OVERLAY_STATE_SWAP_FOUNDATION_ONLY__NO_FRACTURE_PHYSICS'
    bpy.context.view_layer.update(); return roots

if __name__=='__main__':
    main()
