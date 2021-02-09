
#https://github.com/ladybug-tools/ladybug-rhino/blob/master/ladybug_rhino/togeometry.py

#https://github.com/ladybug-tools/ladybug-geometry/blob/master/ladybug_geometry/geometry3d/face.py

#import ladybug_geometry as lg
from ladybug_geometry.geometry3d.pointvector import Point3D
from ladybug_geometry.geometry3d.face import Face3D


test_surf_points = [Point3D(0,0,0),
             Point3D(0,0,1),
             Point3D(1,0,1),
             Point3D(1,0,0)]

test_surf_face = Face3D(test_surf_points)

test_surf_mesh = test_surf_face.mesh_grid(x_dim = 0.2,
                                          y_dim = 0.2,
                                          offset = 0.05,
                                          flip = False,
                                          generate_centroids=True)


#Meshes (this can be used for constructing meshes in for instance HB)
test_surf_mesh.vertices
test_surf_mesh.faces


#Radiance points:
test_surf_mesh.face_centroids
test_surf_mesh.face_normals
