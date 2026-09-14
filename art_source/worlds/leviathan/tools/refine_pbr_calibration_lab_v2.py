"""LEVIATHAN PBR calibration lab v2 persistence correction.

Corrects v1 GENERATED-image persistence failure observed after provider checkpoint:
`source=GENERATED`, `packed_file=false`, `has_data=false` on re-open.

v2 deterministically regenerates the same texture fields, writes temporary PNGs, reloads them as
FILE images, packs the PNG bytes into the .blend, removes the external temp file and rebuilds each
material with one explicit UVMap node feeding BaseColor/MR/Normal texture nodes.

No geometry or art-role expansion. Existing families only: LEV-MAT-001 / LEV-MAT-002.
"""

import bpy
import hashlib
import math
import os
import tempfile
import numpy as np

STAGE = "LEVIATHAN_PBR_CALIBRATION_LAB_V2_PACKED"
RES = 256

SWATCHES = [
    {"name":"LEV_CAL_TISSUE_WARM","family":"LEV-MAT-001","role":"load-bearing living host tissue","base":(0.37,0.055,0.050),"rough":(0.36,0.58),"metal":0.0,"height_strength":1.8,"pattern":"tissue"},
    {"name":"LEV_CAL_MUCOSA_WET","family":"LEV-MAT-001","role":"moist pressure/lumen surface","base":(0.24,0.025,0.040),"rough":(0.10,0.28),"metal":0.0,"height_strength":1.35,"pattern":"mucosa"},
    {"name":"LEV_CAL_CARTILAGE","family":"LEV-MAT-001","role":"fibrous structural biological frame","base":(0.58,0.48,0.36),"rough":(0.38,0.62),"metal":0.0,"height_strength":1.15,"pattern":"cartilage"},
    {"name":"HUM_CAL_IVORY_CERAMIC","family":"LEV-MAT-002","role":"replaceable human graft shell","base":(0.72,0.69,0.61),"rough":(0.20,0.34),"metal":0.0,"height_strength":0.55,"pattern":"ceramic"},
    {"name":"HUM_CAL_BRUSHED_METAL","family":"LEV-MAT-002","role":"human technical load frame","base":(0.34,0.36,0.38),"rough":(0.24,0.42),"metal":1.0,"height_strength":0.75,"pattern":"metal"},
    {"name":"HUM_CAL_SEAL_RUBBER","family":"LEV-MAT-002","role":"compression gasket / soft technical seal","base":(0.035,0.040,0.045),"rough":(0.56,0.78),"metal":0.0,"height_strength":0.70,"pattern":"rubber"},
]


def _pattern(spec):
    y,x=np.mgrid[0:RES,0:RES].astype(np.float32); u=x/RES; v=y/RES; tau=np.float32(math.tau); p=spec["pattern"]
    if p=="tissue":
        macro=0.55+0.23*np.sin(tau*(u*2.0+0.14*np.sin(v*tau*2.0)))+0.12*np.sin(tau*(v*7.0-u*1.5)); micro=0.5+0.5*np.sin(tau*(u*31.0+v*23.0))*np.sin(tau*(v*37.0-u*11.0)); height=0.70*macro+0.30*micro; color_mod=0.84+0.24*macro
    elif p=="mucosa":
        ridges=0.5+0.5*np.sin(tau*(v*5.0+0.18*np.sin(u*tau*3.0))); pores=0.5+0.5*np.cos(tau*(u*29.0))*np.cos(tau*(v*31.0)); height=0.78*ridges+0.22*pores; color_mod=0.80+0.25*ridges
    elif p=="cartilage":
        fibers=0.5+0.5*np.sin(tau*(u*10.0+0.09*np.sin(v*tau*4.0))); cross=0.5+0.5*np.sin(tau*(v*3.0-u*1.2)); height=0.76*fibers+0.24*cross; color_mod=0.88+0.18*fibers
    elif p=="ceramic":
        speck=0.5+0.5*np.sin(tau*(u*47.0+v*19.0))*np.sin(tau*(u*13.0-v*43.0)); broad=0.5+0.5*np.sin(tau*(u*1.0+v*0.7)); height=0.30*speck+0.70*broad; color_mod=0.96+0.06*speck
    elif p=="metal":
        brush=0.5+0.5*np.sin(tau*(v*96.0+0.05*np.sin(u*tau*2.0))); broad=0.5+0.5*np.sin(tau*(u*2.0)); height=0.86*brush+0.14*broad; color_mod=0.88+0.18*brush
    elif p=="rubber":
        stipple=0.5+0.5*np.sin(tau*(u*41.0+v*17.0))*np.cos(tau*(v*37.0-u*7.0)); wave=0.5+0.5*np.sin(tau*(u*3.0+v*2.0)); height=0.70*stipple+0.30*wave; color_mod=0.88+0.16*stipple
    else:
        height=np.zeros((RES,RES),dtype=np.float32)+0.5; color_mod=np.ones((RES,RES),dtype=np.float32)
    return np.clip(height,0,1).astype(np.float32),np.clip(color_mod,0,1.2).astype(np.float32)


def _arrays(spec):
    height,color_mod=_pattern(spec)
    base=np.zeros((RES,RES,4),dtype=np.float32)
    for i,c in enumerate(spec["base"]): base[:,:,i]=np.clip(c*color_mod,0,1)
    base[:,:,3]=1.0
    rmin,rmax=spec["rough"]; rough=rmin+(rmax-rmin)*(0.25+0.75*height)
    mr=np.zeros((RES,RES,4),dtype=np.float32); mr[:,:,0]=1.0; mr[:,:,1]=np.clip(rough,0,1); mr[:,:,2]=spec["metal"]; mr[:,:,3]=1.0
    gy,gx=np.gradient(height); strength=np.float32(spec["height_strength"]); nx=-gx*strength; ny=-gy*strength; nz=np.ones_like(height); mag=np.sqrt(nx*nx+ny*ny+nz*nz); nx/=mag; ny/=mag; nz/=mag
    normal=np.zeros((RES,RES,4),dtype=np.float32); normal[:,:,0]=nx*0.5+0.5; normal[:,:,1]=ny*0.5+0.5; normal[:,:,2]=nz*0.5+0.5; normal[:,:,3]=1.0
    return base,mr,normal


def _u8_digest(arr):
    q=np.clip(np.rint(arr*255.0),0,255).astype(np.uint8)
    return hashlib.sha256(q.tobytes(order="C")).hexdigest()


def _packed_file_image(final_name, arr, non_color):
    # Temporary GENERATED image is only a writer surface; it is deleted after PNG encoding.
    tmp=bpy.data.images.new(final_name+"__WRITER",width=RES,height=RES,alpha=True,float_buffer=False)
    tmp.pixels.foreach_set(arr.reshape(-1)); tmp.update()
    try: tmp.colorspace_settings.name="Non-Color" if non_color else "sRGB"
    except Exception: pass
    tmp.file_format="PNG"
    fd,path=tempfile.mkstemp(prefix="lev_pbr_",suffix=".png"); os.close(fd)
    try:
        os.remove(path)
        tmp.filepath_raw=path
        tmp.save()
        png_bytes=open(path,"rb").read()
        png_sha=hashlib.sha256(png_bytes).hexdigest()
        loaded=bpy.data.images.load(path,check_existing=False)
        loaded.name=final_name
        try: loaded.colorspace_settings.name="Non-Color" if non_color else "sRGB"
        except Exception: pass
        # Force pixel decode before pack, then embed exact PNG bytes into the blend.
        _=loaded.pixels[0]
        loaded.pack()
        if not loaded.packed_file:
            raise RuntimeError("pack() did not create packed_file for "+final_name)
        loaded["generator_stage"]=STAGE
        loaded["resolution"]=RES
        loaded["source_u8_rgba_sha256"]=_u8_digest(arr)
        loaded["packed_png_sha256"]=png_sha
        # Packed data is authoritative; clear live external dependency after packing.
        loaded.filepath_raw=""
        return loaded, png_sha
    finally:
        if os.path.exists(path): os.remove(path)
        if tmp.name in bpy.data.images: bpy.data.images.remove(tmp)


def _rewire_material(spec, base_img, mr_img, normal_img):
    m=bpy.data.materials.get(spec["name"])
    if m is None: raise RuntimeError("Missing v1 material "+spec["name"])
    m.use_nodes=True; nt=m.node_tree; nt.nodes.clear()
    out=nt.nodes.new("ShaderNodeOutputMaterial"); bs=nt.nodes.new("ShaderNodeBsdfPrincipled")
    uv=nt.nodes.new("ShaderNodeUVMap"); uv.uv_map="UVMap"
    tbase=nt.nodes.new("ShaderNodeTexImage"); tbase.image=base_img; tbase.interpolation="Linear"; tbase.extension="REPEAT"
    tmr=nt.nodes.new("ShaderNodeTexImage"); tmr.image=mr_img; tmr.interpolation="Linear"; tmr.extension="REPEAT"
    sep=nt.nodes.new("ShaderNodeSeparateColor"); sep.mode="RGB"
    tn=nt.nodes.new("ShaderNodeTexImage"); tn.image=normal_img; tn.interpolation="Linear"; tn.extension="REPEAT"
    nmap=nt.nodes.new("ShaderNodeNormalMap"); nmap.space="TANGENT"; nmap.inputs["Strength"].default_value=1.0
    for tex in (tbase,tmr,tn): nt.links.new(uv.outputs["UV"],tex.inputs["Vector"])
    nt.links.new(tbase.outputs["Color"],bs.inputs["Base Color"]); nt.links.new(tmr.outputs["Color"],sep.inputs["Color"]); nt.links.new(sep.outputs["Green"],bs.inputs["Roughness"]); nt.links.new(sep.outputs["Blue"],bs.inputs["Metallic"]); nt.links.new(tn.outputs["Color"],nmap.inputs["Color"]); nt.links.new(nmap.outputs["Normal"],bs.inputs["Normal"]); nt.links.new(bs.outputs["BSDF"],out.inputs["Surface"])
    bs.inputs["IOR"].default_value=1.46 if spec["metal"]==0.0 else 1.50
    m["generator_stage"]=STAGE; m["production_state"]="CALIBRATION_PROTOTYPE_NOT_FINAL"; m["asset_family"]=spec["family"]; m["physical_role"]=spec["role"]
    return m


def build():
    # Remove all v1 calibration texture datablocks after materials are about to be rewired.
    old=[i for i in bpy.data.images if i.name.startswith(("LEV_CAL_","HUM_CAL_")) and any(i.name.endswith(s) for s in ("_BASECOLOR","_MR","_NORMAL"))]
    receipts=[]
    for spec in SWATCHES:
        arrays=_arrays(spec); newimgs=[]; pngs=[]
        for suffix,arr,nc in (("_BASECOLOR",arrays[0],False),("_MR",arrays[1],True),("_NORMAL",arrays[2],True)):
            # Rename matching old image so final_name is free, but keep it alive until rewire finishes.
            oldimg=bpy.data.images.get(spec["name"]+suffix)
            if oldimg: oldimg.name=spec["name"]+suffix+"__V1_REJECTED"
            img,png_sha=_packed_file_image(spec["name"]+suffix,arr,nc); newimgs.append(img); pngs.append(png_sha)
        _rewire_material(spec,*newimgs)
        receipts.append({"name":spec["name"],"asset_family":spec["family"],"source_u8_sha256":[i["source_u8_rgba_sha256"] for i in newimgs],"packed_png_sha256":pngs})
    # Purge rejected v1 GENERATED calibration images after all material users have moved.
    for i in list(bpy.data.images):
        if i.name.endswith("__V1_REJECTED"):
            bpy.data.images.remove(i)
    scene=bpy.context.scene; scene["pbr_calibration_stage"]=STAGE; scene["v1_persistence_contract"]="REJECTED_GENERATED_IMAGES_NOT_DURABLE"; scene["final_art_approved"]=False; scene["world_master_propagation_approved"]=False
    calimgs=[i for i in bpy.data.images if i.name.startswith(("LEV_CAL_","HUM_CAL_")) and any(i.name.endswith(s) for s in ("_BASECOLOR","_MR","_NORMAL"))]
    return {"stage":STAGE,"swatches":receipts,"calibration_images":len(calimgs),"packed_images":sum(1 for i in calimgs if i.packed_file),"external_filepath_images":sum(1 for i in calimgs if i.filepath_raw),"file_sources":sum(1 for i in calimgs if i.source=="FILE"),"uvmap_nodes":sum(1 for m in bpy.data.materials if m.name.startswith(("LEV_CAL_","HUM_CAL_")) for n in m.node_tree.nodes if n.type=="UVMAP"),"status":"PACKED_PERSISTENCE_FIX_NOT_YET_REOPEN_VERIFIED"}

if __name__=="__main__": print(build())
