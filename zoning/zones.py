"""
Description:

"""
from ladybug_geometry.geometry3d.polyface import Polyface3D
from ladybug_geometry.geometry3d.face import Face3D
from ladybug_geometry.geometry3d.pointvector import Point3D, Vector3D
import numpy as np
from geometry.writeoutput import write_room_to_rad


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
                    
                    
                    room = create_room(info, ext_wall, count, i)
                    
                    approved_rooms_current_face.append(room)
                    count += 1
                    break
                
            if len(approved_rooms_current_face) == info.max_rooms_per_surface:
                break
                
        info.approved_rooms.extend(approved_rooms_current_face)



    for i in range(len(info.approved_rooms)):
        write_room_to_rad(info, info.approved_rooms[i])



#%%

def create_room(info, ext_wall, count, i):
    
    room = room_class()
    
    room.room_id = count
    room.surf_id = i
    
    room.geo_window = ext_wall.sub_faces_by_ratio(ratio = info.room_WWR)[0]
    room.geo_ene_ext_wall = ext_wall
    
    #https://www.ladybug.tools/ladybug-geometry/docs/ladybug_geometry.geometry3d.polyface.html
    #When a polyface is initialized this way, the first face of the 
    #   Polysurface3D.faces will always be the input face used to create 
    #   the object, the last face will be the offset version of the face, 
    #   and all other faces will form the extrusion connecting the two.
    
    room_unstructured = Polyface3D.from_offset_face(ext_wall.flip(), 
                                                    info.room_dim_depth)
    
    #You need to flip the ext_wall and use a positive offset, else the 
    #   normals will be inwards.
    
    #A boolean to note whether the polyface is solid (True) or is open (False).
    #Note that all solid polyface objects will have faces pointing outwards.
    if not room_unstructured.is_solid:
        raise Exception("Room is not solid (outward facing normals")
    
    room_unstructured_faces = room_unstructured._faces
    z = Vector3D(0,0,1)
    n = ext_wall.normal.normalize()
    v_in_plane = z.cross(n).normalize()
    
    for i in range(len(room_unstructured_faces)):
        
        current_face_normal = room_unstructured_faces[i].normal.normalize()
        
        if (current_face_normal - (-z)).is_zero(tolerance=1e-10):
            room.geo_floor = room_unstructured_faces[i]
        
        elif (current_face_normal - (z)).is_zero(tolerance=1e-10):
            room.geo_ceiling = room_unstructured_faces[i]
            
        elif (current_face_normal - (-n)).is_zero(tolerance=1e-10):
            room.geo_back_wall = room_unstructured_faces[i]
            
        elif (current_face_normal - (v_in_plane)).is_zero(tolerance=1e-10):
            room.geo_right_wall = room_unstructured_faces[i]
            
        elif (current_face_normal - (-v_in_plane)).is_zero(tolerance=1e-10):
            room.geo_left_wall = room_unstructured_faces[i]
        
    
    
    #Creating extwall for radiance
    w_v = room.geo_window.upper_left_counter_clockwise_vertices
    e_v = room.geo_ene_ext_wall.upper_left_counter_clockwise_vertices
    for i in range(3):

        face = Face3D([e_v[i], e_v[i+1], w_v[i+1], w_v[i]])
        room.geo_rad_ext_wall_list.append(face)

    face = Face3D([e_v[3], e_v[0], w_v[0], w_v[3]])
    room.geo_rad_ext_wall_list.append(face)
    
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


    