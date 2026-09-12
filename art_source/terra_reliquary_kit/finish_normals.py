"""Revision 4: correct close-up faceting while preserving hard construction edges."""
import bpy, math
changed=[]
for obj in bpy.data.collections['EXO_TERRA_KIT_EDITABLE'].objects:
 if obj.type!='MESH':continue
 mesh=obj.data
 face_by_edge={tuple(sorted(e.vertices)):[] for e in mesh.edges}
 for face in mesh.polygons:
  face.use_smooth=True
  for key in face.edge_keys:face_by_edge[tuple(sorted(key))].append(face.normal.copy())
 sharp=mesh.attributes.get('sharp_edge') or mesh.attributes.new('sharp_edge','BOOLEAN','EDGE')
 for e in mesh.edges:
  faces=face_by_edge[tuple(sorted(e.vertices))]
  sharp.data[e.index].value=len(faces)!=2 or faces[0].dot(faces[1])<math.cos(math.radians(35))
 mesh.update();changed.append(obj.name)
bpy.context.scene['normal_review']='Close-up r3 showed faceted cylindrical surfaces. r4 smooth shading with explicit >35 degree hard-edge boundaries; weighted normals/editable bevels preserved.'
result={'mesh_objects_corrected':len(changed),'hard_edge_angle_degrees':35,'geometry_added':False,'revision_scope':'4'}
