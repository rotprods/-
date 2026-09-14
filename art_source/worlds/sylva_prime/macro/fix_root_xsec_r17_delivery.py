"""R17b delivery fix: keep custom bevel profile objects unlinked from scene collections.

The R17 path curves still reference these Blender datablocks and evaluate correctly, but
unlinked helper objects must not become standalone GLB scene nodes/primitives.
"""
from __future__ import annotations
import bpy

CONTRACT='SYLVA_MACRO_ROOT_XSEC_R17_AB'
PROFILES=['SYLVA_PROFILE_R17_R01','SYLVA_PROFILE_R17_R03']
ROOTS=['SYLVA_ROOT_PRIMARY_R01','SYLVA_ROOT_PRIMARY_R03']

def main():
    root=bpy.data.objects.get('SYLVA_WORLD_ROOT')
    if not root or root.get('build_status')!='WAVE1O_R17_ROOT_XSEC_AB_EXPERIMENT':
        raise RuntimeError('Expected committed R17 AB input')
    for rn,pn in zip(ROOTS,PROFILES):
        r=bpy.data.objects.get(rn); p=bpy.data.objects.get(pn)
        if not r or not p or r.data.bevel_object is not p or r.get('macro_root_xsec_contract')!=CONTRACT:
            raise RuntimeError('Broken R17 profile dependency '+rn)
        for c in list(p.users_collection):
            c.objects.unlink(p)
        if len(p.users_collection)!=0:
            raise RuntimeError('Profile still linked '+pn)
        p['delivery_visibility']='INTERNAL_DATABLOCK_UNLINKED_FROM_SCENE'
    root['macro_root_xsec_delivery_contract']='R17_INTERNAL_PROFILE_DATABLOCKS'
    root['build_status']='WAVE1O_R17_ROOT_XSEC_AB_DELIVERY_CLEAN'
    bpy.context.view_layer.update()
    # Verify roots still evaluate after helper unlink.
    dg=bpy.context.evaluated_depsgraph_get()
    for rn in ROOTS:
        ev=bpy.data.objects[rn].evaluated_get(dg); me=ev.to_mesh()
        if len(me.vertices)==0 or len(me.polygons)==0:
            ev.to_mesh_clear(); raise RuntimeError('Root lost evaluated geometry '+rn)
        ev.to_mesh_clear()
    bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
    return {'status':'R17_DELIVERY_HELPERS_UNLINKED','profiles':PROFILES,'roots':ROOTS,'geometry_silhouette_changed':False}

if __name__=='__main__':
    print(main())
