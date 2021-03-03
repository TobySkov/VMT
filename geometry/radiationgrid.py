
#https://github.com/ladybug-tools/ladybug-rhino/blob/master/ladybug_rhino/togeometry.py

#https://github.com/ladybug-tools/ladybug-geometry/blob/master/ladybug_geometry/geometry3d/face.py

#import ladybug_geometry as lg
from ladybug_geometry.geometry3d.face import Face3D
from geometry.readinput import read_rad_file_polygons
import json


#%%

def radiation_mesh_grid(info):
    
    polygons = read_rad_file_polygons(info.vmt_facade_dst)
    
    #For each facade
    for i in range(len(polygons)):
        
        surf_face = Face3D(polygons[i])
        info.vmt_faces.append(surf_face)

        surf_mesh = surf_face.mesh_grid(x_dim = info.rad_grid_x_dim,
                                        y_dim = info.rad_grid_y_dim,
                                        offset = info.rad_grid_offset,
                                        flip = False,
                                        generate_centroids=True)
        
        save_mesh_to_info(info, surf_mesh)
        
        
    save_rad_mesh_to_files(info)
        

#%%

def save_mesh_to_info(info, surf_mesh):

    info.rad_surf_mesh_data.append(surf_mesh)
    info.rad_no_of_sensor_points += len(surf_mesh.face_centroids)


#%%

def save_rad_mesh_to_files(info):
    
    #Writing all points file (in Radiance format)
    with open(info.rad_points_all, "w") as outfile: 
    
        for i in range(len(info.rad_surf_mesh_data)):
            
            face_centroids = info.rad_surf_mesh_data[i].face_centroids
            face_normals = info.rad_surf_mesh_data[i].face_normals
            
            info.rad_no_of_sensor_points_list.append(len(face_centroids))
            
            for j in range(len(face_centroids)):
                outfile.write(f"{face_centroids[j].x:.3f} " \
                              + f"{face_centroids[j].y:.3f} " \
                              + f"{face_centroids[j].z:.3f} " \
                              + f"{face_normals[j].x:.3f} " \
                              + f"{face_normals[j].y:.3f} " \
                              + f"{face_normals[j].z:.3f}\n")
            
            #Dump mesh to json
            with open(info.rad_mesh_files_list[i], 'w') as outfile2:   
                json.dump(info.rad_surf_mesh_data[i].to_dict(), outfile2, indent = "\t")
        


#%%










