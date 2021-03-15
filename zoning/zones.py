"""
Description:

"""
from ladybug_geometry.geometry3d.polyface import Polyface3D
from ladybug_geometry.geometry3d.face import Face3D
from ladybug_geometry.geometry3d.pointvector import Point3D, Vector3D
import numpy as np
from geometry.writeoutput import write_room_to_rad, write_vmt_to_rad


#%%

class room_class:
    
    def __init__(self):
        self.geo_floor = None
    
        self.geo_ceiling = None
        
        self.geo_back_wall = None
        
        #When looking at the room, from the end of the room with the window
        self.geo_left_wall = None   
        self.geo_right_wall = None
        
        self.geo_window = None
        
        self.geo_ene_ext_wall = None
        
        self.geo_rad_ext_wall_list = []
        
        self.surf_id = None
        self.room_id = None
        
        self.room_name = None
        
        self.mesh_grid = None
        self.no_of_sensorpoints = None



#%%

def zones_logic(info):

    for i in range(len(info.vmt_faces)):
        
        result_radiation = info.rad_cumm_resuls_data[i]
        sim_points = np.asarray(info.rad_surf_mesh_data[i].face_centroids)
        
        parent_face = info.vmt_faces[i]
        face_normal = parent_face.normal
        
        #From lowest to highest
        ordered_sim_points = sim_points[np.argsort(result_radiation)] 
    
        len_list = len(ordered_sim_points)
        max_tries = int(len_list/info.max_rooms_per_surface)
        
    
        if info.max_rooms_per_surface == 1:
            idx = [len_list-1]
            
            traverse_direction = ["from_top"]
            
        elif info.max_rooms_per_surface == 2:
            idx = [len_list-1,
                   0]
            
            traverse_direction = ["from_top","from_bottom"]
         
        else:
            #In which order should the splitted lists be accessed in:
            idx = [len_list-1,
                   0,
                   int(len_list/2)] 
            
            traverse_direction = ["from_top", "from_bottom", "from_top"]
            
            random_indicies = np.linspace(0, len_list-1, info.max_rooms_per_surface)
            np.random.shuffle(random_indicies)
            
            random_indicies = np.round(random_indicies).astype(int)
            
            for j in range(len(random_indicies)):
                index = random_indicies[j]
                if not any(x == index for x in idx) :
                    idx.append(index)
                    traverse_direction.append("from_top")
                
                
        
        approved_rooms_current_face = []
        count = 0
        for j in range(info.max_rooms_per_surface):
            for k in range(max_tries):
            
                if traverse_direction[j] == "from_top":
                    center_point = ordered_sim_points[(idx[j]-k),:]
                    
                elif traverse_direction[j] == "from_bottom":
                    center_point = ordered_sim_points[(idx[j]+k),:]
                
                
                corner_points = create_facade(info, center_point, face_normal)
                
                approved_inside = check_facade_inside(parent_face,corner_points)
                approved_no_collide = check_facade_collisions(corner_points, 
                                            approved_rooms_current_face)
        
                
                if approved_inside and approved_no_collide:
                    
                    ext_wall = Face3D(corner_points)
                    
                    if ext_wall.is_clockwise:
                        raise Exception(
                            "External wall have been generated as clockwise")
                    
                    #Create VMT face with hole in it
                    vmt_mesh_with_hole = \
                        Face3D.from_punched_geometry(parent_face, [ext_wall])
                    
                    vmt_mesh_with_hole = \
                        vmt_mesh_with_hole.triangulated_mesh3d
        
                    vmt_faces_rest = []
                    for a in range(len(info.vmt_faces)):
                        if a!=i:
                            vmt_faces_rest.append(info.vmt_faces[a])

                    info.approved_rooms_corresponding_vmt.append(
                        [vmt_mesh_with_hole] + vmt_faces_rest)
        
                    room = create_room(info, ext_wall, count, i)
                    
                    approved_rooms_current_face.append(room)
                    count += 1
                    break
                
            if len(approved_rooms_current_face) == info.max_rooms_per_surface:
                break
                
        info.approved_rooms.extend(approved_rooms_current_face)

        
    #Write rooms to rad
    for i in range(len(info.approved_rooms)):
        write_room_to_rad(info, info.approved_rooms[i])
        
        
    #Write vmt with hole in facade to rad
    for i in range(len(info.approved_rooms_corresponding_vmt)):
        write_vmt_to_rad(info, info.approved_rooms[i], 
                         info.approved_rooms_corresponding_vmt[i])


#%%

def create_room(info, ext_wall, count, i):
    
    room = room_class()
    
    room.room_id = count
    room.surf_id = i
    
    room.geo_window = ext_wall.sub_faces_by_ratio(ratio = info.room_WWR)[0]
    room.geo_ene_ext_wall = ext_wall
    
    
    #Creating extwall for radiance
    w_v = room.geo_window.upper_left_counter_clockwise_vertices
    e_v = room.geo_ene_ext_wall.upper_left_counter_clockwise_vertices
    for i in range(3):

        face = Face3D([e_v[i], e_v[i+1], w_v[i+1], w_v[i]])
        room.geo_rad_ext_wall_list.append(face)

    face = Face3D([e_v[3], e_v[0], w_v[0], w_v[3]])
    room.geo_rad_ext_wall_list.append(face)
    
    #
    n = ext_wall.normal.normalize()
    
    
    points = list(ext_wall.upper_left_counter_clockwise_vertices)
    for i in range(4):
        points.append(points[i] + (-n)*info.room_dim_depth)
    
    room.geo_floor = Face3D([points[5], points[6], points[2], points[1]])
    
    room.geo_left_wall = Face3D([points[4], points[5], points[1], points[0]])
    
    room.geo_right_wall = Face3D([points[3], points[2], points[6], points[7]])
    
    room.geo_back_wall = Face3D([points[7], points[6], points[5], points[4]])
    
    room.geo_ceiling =  Face3D([points[0], points[3], points[7], points[4]])
    
    return room
    
    

        

#%%
def create_facade(info, center_point, face_normal):
    
    height_halved = info.room_dim_height/2
    width_halved = info.room_dim_width/2
    
    z = Vector3D(0,0,1)
    
    face_normal = face_normal.normalize()
    horizontal_vector_in_plane = z.cross(face_normal)
    
    corner_points =     [Point3D.from_array(center_point + \
                                 horizontal_vector_in_plane*width_halved - \
                                 z*height_halved),
                         Point3D.from_array(center_point + \
                                 horizontal_vector_in_plane*width_halved + \
                                 z*height_halved),
                         Point3D.from_array(center_point - \
                                 horizontal_vector_in_plane*width_halved + \
                                 z*height_halved),
                         Point3D.from_array(center_point - \
                                 horizontal_vector_in_plane*width_halved - \
                                 z*height_halved)]
    
    return corner_points


#%%

def check_facade_inside(parent_face, corner_points):
    
    approved_inside = True
    for i in range(len(corner_points)):
        
        bool_tmp = parent_face.is_point_on_face(corner_points[i], 
                                                 tolerance=0.1)
        
        if not bool_tmp: #If the corner point is not inside parent face, 
                        # disapprove
            approved_inside = False
    
    return approved_inside
    
#%%

def check_facade_collisions(corner_points, approved_rooms_current_face):
    
    approved_no_collide = True
    for i in range(len(approved_rooms_current_face)):
        current_ext_wall = approved_rooms_current_face[i].geo_ene_ext_wall
        for j in range(len(corner_points)):
        
            bool_tmp = current_ext_wall.is_point_on_face(corner_points[j], 
                                                     tolerance=0.1)
            
            if bool_tmp: #If the corner point of the new facade is inside
                            # an already approved one, then disapprove
                approved_no_collide = False
    
    return approved_no_collide


    