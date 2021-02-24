"""
Description:

"""

def write_room_to_rad(info, room):
    #Needs to have material proporties implemented
    
    room_dict = room.__dict__
    
    #Writing file for dmx calculation
    name = f"surf_{room.surf_id}__room_{room.room_id}__vmx"
    file_name = info.room_folder.joinpath(name + ".rad")
    with open(file_name,"w") as outfile:
        
        for key in room_dict:
            if ("id" not in key) and ("ene_ext_wall" not in key):
                
                if "wall" in key:
                    rad_mat = "wall_mat"
                elif "ceiling" in key:
                    rad_mat = "ceiling_mat"
                elif "floor" in key: 
                    rad_mat = "floor_mat"
                elif "window" in key:
                    rad_mat = "window_glow"
                
                
                if ("list" not in key) and ("window" not in key):
                    pts = room_dict[key].vertices
                    outfile.write(rad_polygon_string(rad_mat, key, pts))
                    
                elif "window" in key:
                    #Window normals needs to be facing inwards
                    pts = room_dict[key].flip().vertices 
                    outfile.write(rad_glow_sting())
                    outfile.write(rad_polygon_string(rad_mat, key, pts))

                else:
                    for i in range(len(room_dict[key])):
                        pts = room_dict[key][i].vertices
                        outfile.write(rad_polygon_string(rad_mat, key + f"_{i}", 
                                                         pts))

        outfile.write(rad_materials_string(info))
        
    #Writing files for dmx calculation (small offset from wall)
    name = f"surf_{room.surf_id}__room_{room.room_id}__dmx"
    file_name = info.room_folder.joinpath(name + ".rad")
    with open(file_name,"w") as outfile:
        
        offset_vec = room_dict["window"].normal.normalize() * 0.01
        pts = room_dict["window"].move(offset_vec).flip().vertices
        
        outfile.write(rad_glow_sting())
        outfile.write(rad_polygon_string(rad_mat, key, pts))


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