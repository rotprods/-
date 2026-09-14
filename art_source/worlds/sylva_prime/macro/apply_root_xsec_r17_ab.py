"""SYLVA PRIME — R17 controlled non-circular macro-root section A/B.

Input: accepted R16 at scene revision 17.
Targets: R01 (Puerto) + R03 (VESPER) only.
This experiment preserves centerlines and R16 per-point taper; it replaces circular curve
bevels with hidden 2D structural profile objects. No terrain/routes/collision/streaming/provider
geometry is intentionally changed.
"""
from __future__ import annotations

import bpy

CONTRACT = "SYLVA_MACRO_ROOT_XSEC_R17_AB"
PROFILE_FAMILY = "BILATERAL_FLATTENED_LOAD_SECTION_V1"
PROFILE_NORMALIZED = [
    (1.00,0.00),(0.88,0.32),(0.62,0.55),(0.28,0.68),(0.00,0.72),
    (-0.28,0.68),(-0.62,0.55),(-0.88,0.32),(-1.00,0.00),(-0.92,-0.30),
    (-0.68,-0.53),(-0.30,-0.65),(0.00,-0.68),(0.30,-0.65),(0.68,-0.53),(0.92,-0.30),
]
TARGETS = {
    "SYLVA_ROOT_PRIMARY_R01": {"depth":48.0,"width":1.10,"height":0.70,"region":"PUERTO"},
    "SYLVA_ROOT_PRIMARY_R03": {"depth":72.0,"width":1.18,"height":0.66,"region":"VESPER"},
}


def ensure_collection(name: str):
    c=bpy.data.collections.get(name)
    if c is None:
        c=bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(c)
    return c


def make_profile(root_name: str, depth: float, width: float, height: float, collection):
    name=root_name.replace('SYLVA_ROOT_PRIMARY_','SYLVA_PROFILE_R17_')
    if bpy.data.objects.get(name):
        raise RuntimeError('R17 profile already exists: '+name)
    cu=bpy.data.curves.new(name+'_CURVE','CURVE')
    cu.dimensions='2D'
    cu.resolution_u=1
    cu.fill_mode='BOTH'
    sp=cu.splines.new('POLY')
    sp.points.add(len(PROFILE_NORMALIZED)-1)
    for p,(x,y) in zip(sp.points,PROFILE_NORMALIZED):
        p.co=(x*depth*width,y*depth*height,0.0,1.0)
    sp.use_cyclic_u=True
    obj=bpy.data.objects.new(name,cu)
    collection.objects.link(obj)
    obj.hide_render=True
    obj.hide_set(True)
    obj['owner_claim']='CLM-SYLVA-MACRO-001'
    obj['contract']=CONTRACT
    obj['profile_family']=PROFILE_FAMILY
    obj['base_depth_m']=depth
    obj['width_factor']=width
    obj['height_factor']=height
    return obj


def main():
    root=bpy.data.objects.get('SYLVA_WORLD_ROOT')
    if not root or root.get('build_status')!='WAVE1N_R16_ROOT_TAPER_MEMBERSHIP_RECONCILED':
        raise RuntimeError('Expected accepted R16 revision17 scene')
    if root.get('macro_root_xsec_contract'):
        raise RuntimeError('Cross-section contract already present')

    collection=ensure_collection('SYLVA_00_META_ROOT_PROFILES_R17')
    changed=[]
    for name,spec in TARGETS.items():
        obj=bpy.data.objects.get(name)
        if obj is None or obj.type!='CURVE' or len(obj.data.splines)!=1:
            raise RuntimeError('Missing/invalid target '+name)
        spline=obj.data.splines[0]
        if spline.type!='BEZIER' or len(spline.bezier_points)!=5:
            raise RuntimeError('R17 expects five-point Bezier '+name)
        before_pts=[tuple(float(v) for v in p.co) for p in spline.bezier_points]
        before_radii=[float(p.radius) for p in spline.bezier_points]
        if obj.data.bevel_mode!='ROUND' or abs(float(obj.data.bevel_depth)-spec['depth'])>1e-6:
            raise RuntimeError('Unexpected R16 bevel state '+name)
        profile=make_profile(name,spec['depth'],spec['width'],spec['height'],collection)
        obj['r17_previous_bevel_mode']='ROUND'
        obj['r17_previous_bevel_depth_m']=spec['depth']
        obj.data.bevel_mode='OBJECT'
        obj.data.bevel_object=profile
        obj.data.twist_mode='Z_UP'
        obj.data.use_fill_caps=True
        after_pts=[tuple(float(v) for v in p.co) for p in spline.bezier_points]
        after_radii=[float(p.radius) for p in spline.bezier_points]
        if before_pts!=after_pts:
            raise RuntimeError('Centerline drift '+name)
        if before_radii!=after_radii:
            raise RuntimeError('R16 taper drift '+name)
        obj['macro_root_xsec_contract']=CONTRACT
        obj['macro_root_profile_family']=PROFILE_FAMILY
        obj['macro_root_profile_region']=spec['region']
        obj['macro_root_cross_section_status']='R17_AB_STRUCTURAL_PROFILE_EXPERIMENT'
        changed.append(name)

    root['macro_root_xsec_contract']=CONTRACT
    root['macro_root_xsec_experiment_targets']='SYLVA_ROOT_PRIMARY_R01|SYLVA_ROOT_PRIMARY_R03'
    root['build_status']='WAVE1O_R17_ROOT_XSEC_AB_EXPERIMENT'
    bpy.context.view_layer.update()
    bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
    return {
        'status':'R17_ROOT_XSEC_AB_APPLIED',
        'contract':CONTRACT,
        'targets':changed,
        'profile_family':PROFILE_FAMILY,
        'centerlines_changed':False,
        'r16_taper_changed':False,
    }

if __name__=='__main__':
    print(main())
