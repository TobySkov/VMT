"""
Description:

"""
from ladybug_geometry.geometry3d.face import Face3D
from ladybug_geometry.geometry3d.pointvector import Point3D, Vector3D
from general.paths import decode_path_manager_panda
import numpy as np
from geometry.writeoutput import write_rad_file_facade_only

#%%
def create_facade(center_point, face_normal, ROOM_DIM):
    
    height_halved = ROOM_DIM[0]/2
    width_halved = ROOM_DIM[1]/2
    
    z = Vector3D(0,0,1)
    
    face_normal = face_normal.normalize()
    horizontal_vector_in_plane = face_normal.cross(z)
    
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

def check_facade_collisions(corner_points, approved_facades):
    
    approved_no_collide = True
    for i in range(len(approved_facades)):
        for j in range(len(corner_points)):
        
            bool_tmp = approved_facades[i].is_point_on_face(corner_points[j], 
                                                     tolerance=0.1)
            
            if bool_tmp: #If the corner point of the new facade is inside
                            # an already approved one, then disapprove
                approved_no_collide = False
    
    return approved_no_collide

#%%

def read_cummulative_results():
    pass

#%%

def zones_logic(path_mananger_pd, submesh_out,cummulative_results_list):
    
    out = decode_path_manager_panda(path_mananger_pd, 
                                        ["ROOM_DIM",
                                         "ROOM_RAD_FILES"])
    ROOM_DIM = out[0]
    ROOM_RAD_FILES = out[1]


    max_rooms_per_surface = 3
    
    
    
    approved_facades_all = []
    for i in range(len(cummulative_results_list)):
        result_radiation = cummulative_results_list[i]
        sim_points = np.asarray(submesh_out[0][i])
        polygon = submesh_out[8][i]
        
        parent_face = Face3D(polygon)
        face_normal = parent_face.normal
        
        #From lowest to highest
        ordered_sim_points = sim_points[np.argsort(result_radiation)] 
    
        len_list = len(ordered_sim_points)
        max_tries = int(len_list/max_rooms_per_surface)
        
    
        if max_rooms_per_surface == 1:
            idx = [len_list-1]
            
            traverse_direction = ["from_top"]
            
        elif max_rooms_per_surface == 2:
            idx = [len_list-1,
                   0]
            
            traverse_direction = ["from_top","from_bottom"]
         
        else:
            #In which order should the splitted lists be accessed in:
            idx = [len_list-1,
                   0,
                   int(len_list/2)] 
            
            traverse_direction = ["from_top", "from_bottom", "from_top"]
            
            random_indicies = np.linspace(0, len_list-1, max_rooms_per_surface)
            np.random.shuffle(random_indicies)
            
            random_indicies = np.round(random_indicies).astype(int)
            
            for j in range(len(random_indicies)):
                index = random_indicies[j]
                if not any(x == index for x in idx) :
                    idx.append(index)
                    traverse_direction.append("from_top")
                
                
        
        approved_facades = []

        for j in range(max_rooms_per_surface):
            for k in range(max_tries):
            
                if traverse_direction[j] == "from_top":
                    center_point = ordered_sim_points[(idx[j]-k),:]
                    
                elif traverse_direction[j] == "from_bottom":
                    center_point = ordered_sim_points[(idx[j]+k),:]
                
                
                    
                corner_points = create_facade(center_point, face_normal, ROOM_DIM)
                
                approved_inside = check_facade_inside(parent_face,corner_points)
                approved_no_collide = check_facade_collisions(corner_points, 
                                                              approved_facades)
        
                
                if approved_inside and approved_no_collide:
                    if i == 1:
                        a = 2+2
                    approved_facades.append(Face3D(corner_points))
                    break
                
            if len(approved_facades) == max_rooms_per_surface:
                break
                
        approved_facades_all.append(approved_facades)


        ### Save result
        for j in range(len(approved_facades)):
            file_name = \
                ROOM_RAD_FILES.replace("XXX", str(i)).replace("YYY",str(j))
            
            write_rad_file_facade_only(file_name,approved_facades[j],i,j)
    










    