"""Check GLB interchange integrity and count geometry without pretending to judge art."""
from pathlib import Path
import hashlib,json,struct
from project_control import ROOT

def inspect_glb(path):
    b=path.read_bytes()
    if len(b)<20:raise ValueError('truncated GLB header')
    magic,version,size=struct.unpack_from('<4sII',b)
    if magic!=b'glTF' or version!=2 or size!=len(b):raise ValueError('invalid GLB envelope')
    pos=12;document=None;bin_size=0
    while pos<len(b):
        if pos+8>len(b):raise ValueError('truncated chunk')
        length,kind=struct.unpack_from('<I4s',b,pos);pos+=8
        if pos+length>len(b):raise ValueError('chunk overflow')
        if kind==b'JSON':document=json.loads(b[pos:pos+length])
        elif kind==b'BIN\0':bin_size+=length
        pos+=length
    if document is None:raise ValueError('missing GLB JSON')
    if any(x.get('uri') for x in document.get('buffers',[])):raise ValueError('external buffer dependency')
    if any(x.get('uri') and not x['uri'].startswith('data:') for x in document.get('images',[])):raise ValueError('external texture dependency')
    for view in document.get('bufferViews',[]):
        if view.get('byteOffset',0)+view['byteLength']>bin_size:raise ValueError('buffer view out of bounds')
    tris=0;primitives=0;accessors=document.get('accessors',[])
    for mesh in document.get('meshes',[]):
        for p in mesh['primitives']:
            primitives+=1
            if p.get('mode',4)==4:
                index=p.get('indices',p.get('attributes',{}).get('POSITION'))
                if index is None or index>=len(accessors):raise ValueError('invalid primitive accessor')
                count=accessors[index]['count']
                if count%3:raise ValueError('triangle count not divisible by three')
                tris+=count//3
    return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'nodes':len(document.get('nodes',[])),'meshes':len(document.get('meshes',[])),'materials':len(document.get('materials',[])),'triangle_primitives':primitives,'indexed_or_vertex_triangles':tris,'animations':len(document.get('animations',[])),'scope':'export geometry including presentation; no artistic/performance approval'}
if __name__=='__main__':
    result=inspect_glb(ROOT/'assets/reliquary_gate.glb');result['passed']=True
    source=ROOT/'art_source/reliquary_gate/EXOVANT_Reliquary_Gate.blend'
    if not source.is_file():raise ValueError('editable source missing')
    result['editable_blend_sha256']=hashlib.sha256(source.read_bytes()).hexdigest()
    (ROOT/'evidence/asset-audit.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
