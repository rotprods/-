"""Aurora Veil manufactured material calibration r15 — Blender 5.2.

Calibrates Campamento manufactured material roles only. Natural terrain lithology remains
explicitly undecided. No random procedural texture/noise is created.
"""
import bpy

CONTRACT='AUR-MAT-v1-r15'

def srgb_to_linear(c):
    c=c/255.0
    return c/12.92 if c<=0.04045 else ((c+0.055)/1.055)**2.4

def rgb8(v): return tuple(srgb_to_linear(x) for x in v)

def calibrate(name,srgb,metal,rough,rrange,ior=1.5,trans=0.0,coat=0.0,coat_rough=.03,role='',manufacturing='',wear='',forbidden=''):
    m=bpy.data.materials.get(name) or bpy.data.materials.new(name); m.use_nodes=True
    p=m.node_tree.nodes.get('Principled BSDF')
    p.inputs['Base Color'].default_value=(*rgb8(srgb),1)
    p.inputs['Metallic'].default_value=metal; p.inputs['Roughness'].default_value=rough; p.inputs['IOR'].default_value=ior
    p.inputs['Transmission Weight'].default_value=trans; p.inputs['Coat Weight'].default_value=coat; p.inputs['Coat Roughness'].default_value=coat_rough
    m['aurora_material_contract']=CONTRACT; m['status']='CALIBRATED_CANDIDATE'; m['role']=role; m['base_color_srgb_8bit']=list(srgb)
    m['metallic']=metal; m['roughness_nominal']=rough; m['roughness_authored_range']=list(rrange); m['ior']=ior; m['transmission_weight']=trans; m['coat_weight']=coat; m['coat_roughness']=coat_rough
    m['manufacturing']=manufacturing; m['wear_causality']=wear; m['forbidden_shortcuts']=forbidden
    m['texture_status']='PENDING_AUTHORED_PBR'; m['microdetail_status']='PENDING_CAUSAL_NORMAL_ROUGHNESS'
    return m

def build():
    specs=[
      ('AUR_MAT_STRUCTURAL_GALV_STEEL',(118,128,132),1.0,.34,(.28,.60),1.5,0,0,.03,'primary structure / frames / ring boxes','zinc-coated fabricated steel','contact/tool abrasion; zinc oxidation/chalking; rust only after coating breach','uniform edge wear; blanket rust; random scratches'),
      ('AUR_MAT_CERAMIC_COMPOSITE_PANEL',(150,154,152),.02,.56,(.48,.74),1.50,0,.08,.32,'weather shell / insulated cassette faces','ceramic/mineral composite cassette on rails','dust below seams; chips at impacts; water streaks need drainage path','plastic sheen; equal edge damage; arbitrary grime'),
      ('AUR_MAT_EPDM_GASKET',(20,23,25),0,.90,(.82,.96),1.52,0,0,.03,'weather/pressure seals','extruded EPDM under compression','compression polish; UV chalking; dust on exposed lip','metallic response; random cracking'),
      ('AUR_MAT_DARK_TEMPERED_GLASS',(24,42,48),0,.12,(.05,.28),1.52,.62,.03,.08,'observation glazing / instrument windows','laminated/tempered glazing in gasketed frames','dust/condensation; service handling; impact chips only','opaque plastic; uniform scratches'),
      ('AUR_MAT_CLOCK_BRONZE_CAL',(112,64,24),1.0,.40,(.28,.68),1.5,0,0,.03,'calibrated mechanical clock/instrument hardware','machined/cast copper alloy','handling polish; exposure-dependent oxidation; local bearing grease','global green patina; arbitrary edge wear'),
      ('AUR_MAT_MINERAL_FOUNDATION',(92,88,82),0,.84,(.72,.95),1.50,0,0,.03,'manufactured foundation pads / grout, NOT planetary lithology','precast mineral/concrete-like pad plus site grout','ground splash/dust; drainage streaks; impact/freeze spall only','use as natural terrain; uniform cracks; noise-only roughness'),
      ('AUR_MAT_SERVICE_TRAY',(96,101,104),.90,.47,(.38,.66),1.5,0,0,.03,'folded service trays / cable support metal','zinc-coated folded sheet metal','tool abrasion at covers/fasteners; dust on horizontal trays','uniform corrosion; inaccessible scratches')]
    mats=[calibrate(*s) for s in specs]
    root=bpy.data.collections.get('AURORA_VEIL_ROOT') or bpy.context.scene.collection
    meta=bpy.data.collections.get('22_MATERIAL_LIBRARY_META')
    if not meta: meta=bpy.data.collections.new('22_MATERIAL_LIBRARY_META'); root.children.link(meta)
    for o in list(meta.objects): bpy.data.objects.remove(o,do_unlink=True)
    meta.hide_render=True; meta['export_contract']='EMPTY_METADATA_ONLY'
    for i,m in enumerate(mats):
        e=bpy.data.objects.new('MAT_META_'+m.name,None); meta.objects.link(e); e.location=(0,0,-1000-i); e['material_name']=m.name; e['role']=m['role']; e['status']=m['status']
    s=bpy.context.scene; s['material_contract_version']=CONTRACT; s['material_board_scope']='MANUFACTURED_CAMP_MATERIALS_ONLY'; s['terrain_lithology_material_status']='PENDING_LITHOLOGY_DO_NOT_CANONIZE_MINERAL_FOUNDATION_AS_TERRAIN'; s['material_texture_policy']='authored PBR later; no random procedural noise as realism substitute'; s['status']='WAVE2_MATERIAL_CALIBRATION_R15'
    return [m.name for m in mats]

if __name__=='__main__': print(build())
