"""
Description:

"""

from ladybug_geometry.geometry3d.face import Face3D
from honeybee.face import Face
from ladybug_geometry.geometry3d.pointvector import Point3D, Vector3D
import numpy as np
from geometry.readinput import read_rad_file_polygons_to_levels
import os


#%%


def level_logic(info):
    
    levels = read_rad_file_polygons_to_levels(info.vmt_dst)
    info.real_levels_list = levels
    
    ## Indentify unique geometry levels
    unique_levels = [levels[0]] #First level is always unique
    level_unique_level_id = [0] 
    
    for i in range(1,len(levels)):
        for j in range(len(unique_levels)):
            
            move_vec = unique_levels[j]["floor"].center - \
                levels[i]["floor"].center
            
            bool1 = unique_levels[j]["floor"].is_geometrically_equivalent(
                levels[i]["floor"].move(move_vec),0.001)
            
            bool2 = unique_levels[j]["ceiling"].is_geometrically_equivalent(
                levels[i]["ceiling"].move(move_vec),0.001)
            
            if not (bool1 and bool2):
                unique_levels.append(levels[i])
                level_unique_level_id.append(len(unique_levels))
                
            elif (bool1 and bool2): #If the current level corresponds
                                    #to a level already in unique levels list
                level_unique_level_id.append(j)
                
    level_unique_level_id = np.array(level_unique_level_id)
        
    ## Create V-matrix rad files for unique levels
    
    unique_level_ID = 0
    for i in range(len(unique_levels)):
        unique_level_dict = {}
        
        window_rad_string = rad_glow_sting()
        level_rad_string = rad_materials_string(info)
        
        wall_ID = 0 #Relative to unique level
        for j in range(len(unique_levels[i]["walls"])): #For each wall
            hb_face = Face(f"unique_lvl_{unique_level_ID}__wall_{wall_ID}", 
                           unique_levels[i]["walls"][j])
            
            hb_face.apertures_by_ratio_rectangle(
                    info.day_win_ratio, 
                    info.day_win_aperture_height, 
                    info.day_win_sill_height, 
                    info.day_win_horizontal_separation, 
                    info.day_win_vertical_separation)
            
    
            mesh = hb_face.punched_geometry.triangulated_mesh3d
            for k in range(len(mesh.faces)):
                idx = mesh.faces[k]
                pts = []
                for y in range(len(idx)):
                    pts.append(mesh.vertices[idx[y]])
                name = f"unique_lvl_{unique_level_ID}__wall_{wall_ID}__piece_{k}"
                modifier = "wall_mat"
                level_rad_string  += \
                    rad_triangle_string(modifier, name, pts)
            wall_ID += 1

            window_ID = 0 #Relevative to wall
            for k in range(len(hb_face.apertures)):
                name = f"unique_lvl_{unique_level_ID}__wall_{wall_ID}" + \
                    f"__window_{window_ID}"
                window_rad_string  += \
                    f"#@rfluxmtx h=kf u=+Z o={name}.vmtx\n"
                aperature = hb_face.apertures[k]
                pts = list(
                    aperature.geometry.flip().upper_left_counter_clockwise_vertices)
                modifier = "window_mat"
                window_rad_string  += \
                    rad_polygon_string(modifier, name, pts)
                window_ID+=1
                
                
        ## Ceiling and floor
        pts = list(unique_levels[i]["ceiling"].vertices)
        name = f"unique_lvl_{unique_level_ID}__ceiling"
        modifier = "ceiling_mat"
        level_rad_string += rad_polygon_string(modifier, name, pts)
        
        pts = list(unique_levels[i]["floor"].vertices)
        name = f"unique_lvl_{unique_level_ID}__floor"
        modifier = "floor_mat"
        level_rad_string += rad_polygon_string(modifier, name, pts)
        
        
        ##Write to files for this unique level
        folder = info.vmx_folder.joinpath(
            f"unique_lvl_{unique_level_ID}")
        
        if not os.path.exists(folder):
            os.makedirs(folder)
        
        file = folder.joinpath("vmx_windows.rad")
        unique_level_dict["vmx_windows.rad"] = file
        with open(file,"w") as outfile:
            outfile.write(window_rad_string)
            
        file = folder.joinpath("vmx_zone.rad")
        unique_level_dict["vmx_zone.rad"] = file
        with open(file,"w") as outfile:
            outfile.write(level_rad_string)
        
        ##Daylight grid
        daylight_grid = unique_levels[i]["floor"].mesh_grid(
                    x_dim = info.day_grid_x_dim,
                    y_dim = info.day_grid_y_dim,
                    offset = info.day_sensorpoint_height,
                    flip = True,
                    generate_centroids=True)
        
        face_centroids = daylight_grid.face_centroids
        face_normals = daylight_grid.face_normals
        
        file = folder.joinpath("sensors.pts")
        unique_level_dict["sensors.pts"] = file
        
        with open(file, "w") as outfile: 
        
            for j in range(len(face_centroids)):
                outfile.write(f"{face_centroids[j].x:.3f} " \
                              + f"{face_centroids[j].y:.3f} " \
                              + f"{face_centroids[j].z:.3f} " \
                              + f"{face_normals[j].x:.3f} " \
                              + f"{face_normals[j].y:.3f} " \
                              + f"{face_normals[j].z:.3f}\n")
        
        
        unique_level_dict["unique_level_ID"] = unique_level_ID
        unique_level_dict["corresponding_real_levels_IDs"] = \
            np.where(level_unique_level_id == unique_level_ID)[0]
        
        info.unique_levels_list.append(unique_level_dict)
        unique_level_ID += 1
        

        
#%%
def rad_materials_string(info):
    
    floor_reflec =      info.day_floor_reflectance
    wall_reflec =       info.day_wall_reflectance
    ceiling_reflec =    info.day_ceiling_reflectance
    
    string = "void plastic floor_mat\n" + \
            "0\n" + \
            "0\n" + \
            f"5 {floor_reflec} {floor_reflec} {floor_reflec} 0.0 0.0\n\n" + \
            "void plastic wall_mat\n" + \
            "0\n" + \
            "0\n" + \
            f"5 {wall_reflec} {wall_reflec} {wall_reflec} 0.0 0.0\n\n" + \
            "void plastic ceiling_mat\n" + \
            "0\n" + \
            "0\n" + \
            f"5 {ceiling_reflec} {ceiling_reflec} {ceiling_reflec} 0.0 0.0\n\n"
                
    return string

#%%
def rad_glow_sting():
    
    string = "void glow window_mat\n" + \
                "0\n" + \
                "0\n" + \
                "4 1.0 1.0 1.0 0.0\n\n\n"
                
    return string

#%%

def rad_triangle_string(modifier, name, pts):
    
    string = f"{modifier} polygon {name}\n" + \
            "0\n" + \
            "0\n" + \
            "9 " + \
            f"{pts[0].x} {pts[0].y} {pts[0].z} " + \
            f"{pts[1].x} {pts[1].y} {pts[1].z} " + \
            f"{pts[2].x} {pts[2].y} {pts[2].z}\n\n\n"
            
    return string




#%%

def rad_polygon_string(modifier, name, pts):
    
    string = f"{modifier} polygon {name}\n" + \
            "0\n" + \
            "0\n" + \
            "12 " + \
            f"{pts[0].x} {pts[0].y} {pts[0].z} " + \
            f"{pts[1].x} {pts[1].y} {pts[1].z} " + \
            f"{pts[2].x} {pts[2].y} {pts[2].z} " + \
            f"{pts[3].x} {pts[3].y} {pts[3].z}\n\n\n"
            
    return string

    