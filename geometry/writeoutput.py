"""
Description:

"""
#%%
def write_vmt_to_rad(info, room, correspoding_vmt):
    
    string = rad_material_vmt_string(info)
    
    holed_mesh = correspoding_vmt[0]
    
    modifier = "vmt_mat"
    
    for i in range(len(holed_mesh.faces)):
        idx = holed_mesh.faces[i]
        pts = []
        for j in range(len(idx)):
            pts.append(holed_mesh.vertices[idx[j]])
        name = f"holed_facade_face_{i}"
        string += rad_triangle_string(modifier, name, pts)
        
    for i in range(len(correspoding_vmt)-1):
        i = i + 1
        
        pts = correspoding_vmt[i].vertices
        name = f"other_facades_{i}"
        string += rad_polygon_string(modifier, name, pts)
        
    name = f"surf_{room.surf_id}__room_{room.room_id}__vmt"
    file_name = info.room_folder.joinpath(name + ".rad")
    with open(file_name, "w") as outfile:
        outfile.write(string)
        
    info.vmt_radfile_path_list.append(file_name)


#%%

def write_room_to_rad(info, room):
    #Needs to have material proporties implemented
    
    room_dict = room.__dict__
    
    room.room_name = f"surf_{room.surf_id}__room_{room.room_id}"
    
    #Writing files for vmx calculation
    name = f"surf_{room.surf_id}__room_{room.room_id}__room"
    file_name = info.room_folder.joinpath(name + ".rad")
    
    info.room_radfile_path_list.append(file_name)
    
    with open(file_name,"w") as outfile:
        
        outfile.write(rad_materials_string(info))
        
        for key in room_dict:
            if ("geo" in key) and ("ene_ext_wall" not in key):
                
                if "wall" in key:
                    rad_mat = "wall_mat"
                elif "ceiling" in key:
                    rad_mat = "ceiling_mat"
                elif "floor" in key: 
                    rad_mat = "floor_mat"
                elif "window" in key:
                    rad_mat = "window_glow"
                
                
                if "list" in key:
                    for i in range(len(room_dict[key])):
                        pts = room_dict[key][i].vertices
                        outfile.write(rad_polygon_string(rad_mat, key + f"_{i}", 
                                                         pts))
                elif "window" not in key:
                    pts = room_dict[key].vertices
                    outfile.write(rad_polygon_string(rad_mat, key, pts))
                    

        
    
    
    #Window for vmx calculation
    name = f"surf_{room.surf_id}__room_{room.room_id}__window"
    file_name = info.room_folder.joinpath(name + ".rad")
    
    info.window_radfile_path_list.append(file_name)
    
    with open(file_name,"w") as outfile:

        pts = room_dict["geo_window"].flip().vertices
        
        outfile.write(rad_glow_sting())
        modifier = "window_glow" 
        name = "window_vmx"
        outfile.write(rad_polygon_string(modifier, name, pts))
        
    


#%%


def rad_material_vmt_string(info):
    
    context_reflec =      info.context_reflectance

    string = "void plastic vmt_mat\n" + \
             "0\n" + \
             "0\n" + \
             f"5 {context_reflec} {context_reflec} {context_reflec} 0.0 0.0\n\n" 

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
def rad_materials_string(info):
    
    floor_reflec =      info.floor_reflectance
    wall_reflec =       info.wall_reflectance
    ceiling_reflec =    info.ceiling_reflectance
    
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
    
    string = "#@rfluxmtx h=kf u=Z\n" + \
                "void glow window_glow\n" + \
                "0\n" + \
                "0\n" + \
                "4 1.0 1.0 1.0 0.0\n"
                
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