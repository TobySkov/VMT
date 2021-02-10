
#https://github.com/ladybug-tools/ladybug-rhino/blob/master/ladybug_rhino/togeometry.py

#https://github.com/ladybug-tools/ladybug-geometry/blob/master/ladybug_geometry/geometry3d/face.py

#import ladybug_geometry as lg
from ladybug_geometry.geometry3d.pointvector import Point3D
from ladybug_geometry.geometry3d.face import Face3D
from general.paths import decode_path_manager_panda

def read_vmt_rad_file(path_mananger_pd):
    
    out = decode_path_manager_panda(path_mananger_pd, ["VMT_RAD_FILE"])
    VMT_RAD_FILE = out[0]
    
    with open(VMT_RAD_FILE, "r") as infile:
        content = infile.readlines()
        
    polygons = []
    for i in range(len(content)):
        try: #In case it is not possible to access element 1 of list.
            if content[i].split(" ")[1] == "polygon" and content[i + 3].split(" ")[0] == "12":
                numbers = content[i + 3].split(" ")
                polygon = [Point3D(numbers[1],numbers[2],numbers[3]),
                           Point3D(numbers[4],numbers[5],numbers[6]),
                           Point3D(numbers[7],numbers[8],numbers[9]),
                           Point3D(numbers[10],numbers[11],numbers[12])]
                polygons.append(polygon)
        except:
            pass
        
    return polygons



def gen_pts_and_sub_mesh(path_mananger_pd, x_dim, y_dim, offset):
    
    polygons = read_vmt_rad_file(path_mananger_pd)
    
    face_centroids = []
    face_normals = []
    
    mesh_vertices = []
    mesh_faces = []
    
    face_centroids_all = []
    face_normals_all = []
    
    no_of_sensor_points_list = []
    
    for i in range(len(polygons)):
        
        surf_face = Face3D(polygons[i])

        surf_mesh = surf_face.mesh_grid(x_dim = x_dim,
                                        y_dim = y_dim,
                                        offset = offset,
                                        flip = False,
                                        generate_centroids=True)
        
        face_centroids.append(surf_mesh.face_centroids)
        face_normals.append(surf_mesh.face_normals)
        
        mesh_vertices.append(surf_mesh.vertices)
        mesh_faces.append(surf_mesh.faces)
        
        face_centroids_all = face_centroids_all + list(surf_mesh.face_centroids)
        face_normals_all = face_normals_all + list(surf_mesh.face_normals)
        
        no_of_sensor_points_list.append(len(face_centroids[i]))
        
        out = decode_path_manager_panda(path_mananger_pd, 
                                        ["RADIATION_POINT_FILES",
                                         "RADIATION_MESH_FILES",
                                         "MESH_FILE_HEADER_VERTICES",
                                         "MESH_FILE_HEADER_FACES",
                                         "RADIATION_ALL_PTS_FILE"])
        RADIATION_POINT_FILES = out[0]
        RADIATION_MESH_FILES = out[1]
        MESH_FILE_HEADER_VERTICES = out[2]
        MESH_FILE_HEADER_FACES = out[3]
        RADIATION_ALL_PTS_FILE = out[4]
        
        ### Writing information to files
        with open(RADIATION_POINT_FILES.replace("XXX",str(i)), "w") as outfile:
            for j in range(len(face_centroids[i])):
                outfile.write(f"{face_centroids[i][j].x:.3f} " \
                              + f"{face_centroids[i][j].y:.3f} " \
                              + f"{face_centroids[i][j].z:.3f} " \
                              + f"{face_normals[i][j].x:.3f} " \
                              + f"{face_normals[i][j].y:.3f} " \
                              + f"{face_normals[i][j].z:.3f}\n")

        with open(RADIATION_MESH_FILES.replace("XXX",str(i)), "w") as outfile:
            outfile.write(MESH_FILE_HEADER_VERTICES)
            for j in range(len(mesh_vertices[i])):
                outfile.write(f"{mesh_vertices[i][j].x:.3f} " \
                              + f"{mesh_vertices[i][j].y:.3f} " \
                              + f"{mesh_vertices[i][j].z:.3f}\n")
                
            outfile.write(MESH_FILE_HEADER_FACES)
            for j in range(len(mesh_faces[i])):
                outfile.write(f"{mesh_faces[i][j][0]} " \
                              + f"{mesh_faces[i][j][1]} " \
                              + f"{mesh_faces[i][j][2]} " \
                              + f"{mesh_faces[i][j][3]}\n")
             
    
    with open(RADIATION_ALL_PTS_FILE, "w") as outfile:
            for i in range(len(face_centroids_all)):
                outfile.write(f"{face_centroids_all[i].x:.3f} " \
                              + f"{face_centroids_all[i].y:.3f} " \
                              + f"{face_centroids_all[i].z:.3f} " \
                              + f"{face_normals_all[i].x:.3f} " \
                              + f"{face_normals_all[i].y:.3f} " \
                              + f"{face_normals_all[i].z:.3f}\n")
                    

    no_of_sensor_points_total = len(face_centroids_all)
    
    return (face_centroids, face_normals, mesh_vertices, mesh_faces, \
            face_centroids_all, face_normals_all, \
                no_of_sensor_points_total, no_of_sensor_points_list)
    









