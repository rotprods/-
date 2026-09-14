"""Restore R01/R03 to accepted R16 circular taper after R17 helper-profile persistence failure."""
import bpy
TARGETS={
    'SYLVA_ROOT_PRIMARY_R01':48.0,
    'SYLVA_ROOT_PRIMARY_R03':72.0,
}
root=bpy.data.objects.get('SYLVA_WORLD_ROOT')
if not root or root.get('build_status')!='WAVE1O_R17_ROOT_XSEC_AB_DELIVERY_CLEAN':
    raise RuntimeError('Expected failed R17 delivery-clean checkpoint')
for name,depth in TARGETS.items():
    o=bpy.data.objects.get(name)
    if o is None or o.type!='CURVE':
        raise RuntimeError('Missing root '+name)
    o.data.bevel_mode='ROUND'
    o.data.bevel_object=None
    o.data.bevel_depth=depth
    o.data.twist_mode='MINIMUM'
    o.data.use_fill_caps=False
    o['macro_root_cross_section_status']='CIRCULAR_PROXY_FINAL_SECTION_PENDING'
    o['r17_rollback_reason']='UNLINKED_BEVEL_PROFILE_NOT_PERSISTED_ACROSS_BLEND_REOPEN'
root['macro_root_xsec_contract']='R17_REJECTED_ROLLED_BACK_TO_R16'
root['macro_root_xsec_delivery_contract']='R17_REJECTED'
root['build_status']='WAVE1N_R16_ROOT_TAPER_MEMBERSHIP_RECONCILED'
bpy.context.view_layer.update()
bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
result={'status':'R17_REJECTED_R16_RESTORED','targets':list(TARGETS),'geometry_source':'R16_CIRCULAR_TAPER'}
