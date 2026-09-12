"""Audit the actual GLB candidate, without granting ART/PERF gates."""
from pathlib import Path
import json, struct, sys, hashlib
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools'))
from asset_audit import inspect_glb

def audit(path):
    stats=inspect_glb(path);raw=path.read_bytes()
    n=struct.unpack_from('<I',raw,12)[0];d=json.loads(raw[20:20+n])
    errors=[]; textured=0; mapped=0
    collision_meshes={x['mesh'] for x in d['nodes'] if x.get('name','').endswith('-colonly') and 'mesh' in x}
    for i,m in enumerate(d.get('meshes',[])):
        for p in m['primitives']:
            if 'NORMAL' not in p['attributes']:errors.append(f'mesh {i} lacks normals')
            if 'TEXCOORD_0' not in p['attributes'] and i not in collision_meshes:errors.append(f'mesh {i} lacks UV0')
            else:mapped+=1
            a=d['accessors'][p['attributes']['POSITION']]
            if any(abs(x)>1000 for x in a.get('min',[])+a.get('max',[])):errors.append('unexpected kilometre geometry')
    for m in d.get('materials',[]):
        p=m.get('pbrMetallicRoughness',{})
        if 'baseColorTexture' in p:
            textured+=1
            if 'normalTexture' not in m:errors.append('textured material lacks normal texture: '+m.get('name',''))
            if 'metallicRoughnessTexture' not in p:errors.append('textured material lacks roughness texture')
    roots=[x['name'] for x in d['nodes'] if x.get('name','').startswith(('ENV_','PR_','KIT_','BIO_')) and 'mesh' not in x]
    if len(roots)<10:errors.append('missing assembly roots')
    if textured!=4:errors.append(f'expected four textured material families, found {textured}')
    if len(d.get('images',[]))<12:errors.append('packed map set incomplete')
    if len(collision_meshes)!=11:errors.append(f'expected 11 explicit collision source meshes, found {len(collision_meshes)}')
    return dict(stats,passed=not errors,errors=errors,assembly_roots=roots,uv_primitives=mapped,collision_source_meshes=len(collision_meshes),
        textured_materials=textured,embedded_images=len(d.get('images',[])),
        scope='GLB interchange integrity only. Native import, human art review and GPU performance separate.')

if __name__=='__main__':
    path=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).parent/'EXOVANT_Terra_Kit.glb'
    r=audit(path)
    if len(sys.argv)>2:Path(sys.argv[2]).write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps(r,indent=2));raise SystemExit(not r['passed'])
