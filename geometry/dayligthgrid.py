"""
Description:

"""
from ladybug_geometry.geometry3d.pointvector import Vector3D
import json

def daylight_mesh_grid(info):
    
    for i in range(len(info.approved_rooms)):
        
        offset_vec = Vector3D(0,0,1)*info.day_sensorpoint_height
        
        mesh = info.approved_rooms[i].geo_floor.flip().move(offset_vec).mesh_grid(
                    x_dim = info.day_grid_x_dim,
                    y_dim = info.day_grid_y_dim,
                    offset = info.rad_grid_offset,
                    flip = False,
                    generate_centroids=True)
        
        info.approved_rooms[i].mesh_grid = mesh
        
        save_day_mesh_to_files(info, i, mesh)
        
#%%

def save_day_mesh_to_files(info, i, mesh):
    
    file_name = info.daylight_points_folder.joinpath(
        info.approved_rooms[i].room_name + ".pts")
    
    info.day_points_path_list.append(file_name)
    
    face_centroids = mesh.face_centroids
    face_normals = mesh.face_normals
        
    info.approved_rooms[i].no_of_sensorpoints = len(face_centroids)
    
    #Writing all points file (in Radiance format)
    with open(file_name, "w") as outfile: 
    
        for j in range(len(face_centroids)):
            outfile.write(f"{face_centroids[j].x:.3f} " \
                          + f"{face_centroids[j].y:.3f} " \
                          + f"{face_centroids[j].z:.3f} " \
                          + f"{face_normals[j].x:.3f} " \
                          + f"{face_normals[j].y:.3f} " \
                          + f"{face_normals[j].z:.3f}\n")
            
    #Dump mesh to json
    file_name = info.daylight_mesh_folder.joinpath(
        info.approved_rooms[i].room_name + ".json")
    
    info.day_mesh_path_list.append(file_name)
    
    with open(file_name, 'w') as outfile:   
        json.dump(mesh.to_dict(), outfile, indent = "\t")


    #Append filenames
    info.vmx_matrix_path_list.append(
        info.daylight_matrix_folder.joinpath(
            info.approved_rooms[i].room_name + ".vmx"))
        
    info.dmx_matrix_path_list.append(
        info.daylight_matrix_folder.joinpath(
            info.approved_rooms[i].room_name + ".dmx"))
        
    info.day_results_rgb_list.append(
        info.daylight_results_folder.joinpath(
            info.approved_rooms[i].room_name + ".rgb"))
    
    info.day_results_ill_list.append(
        info.daylight_results_folder.joinpath(
            info.approved_rooms[i].room_name + ".ill"))
    
    info.day_results_da_list.append(
        info.daylight_results_folder.joinpath(
            info.approved_rooms[i].room_name + "__da.txt"))
        
        
        
        