
import copy


#%%
def energyanalysis_baseline(info):
    
    idf_default_string = load_default_ep_objects(info)
    
    for i in range(len(info.approved_rooms)):
        
        idf_current_string = copy.deepcopy(idf_default_string)
        
        room = info.approved_rooms[i]
        
        create_geometry_string(info,room)
        


#%%

def load_default_ep_objects(info):
    
    idf_default_string = ""
    
    for i in range(len(info.ene_default_ep_objects)):
        with open(info.ene_default_ep_objects[i], "r") as infile:
            for line in infile:
                idf_default_string += line
    
    return idf_default_string


#%%
def create_geometry_string(info,room):
    
    room_string = ""
    
    
    return room_string


#%%


def create_building_surface_string(name, surface_type, construction_name,
                                   name_name, outside_boundary_condition,
                                   sun_exposure, wind_exposure):


    string  = f"""
BuildingSurface:Detailed,
  {name},                               !- Name
  {surface_type},                         !- Surface Type
  Generic Interior Ceiling,               !- Construction Name
  Second_last_top_floor_c960af8b,         !- Zone Name
  Adiabatic,                              !- Outside Boundary Condition
  ,                                       !- Outside Boundary Condition Object
  NoSun,                                  !- Sun Exposure
  NoWind,                                 !- Wind Exposure
  ,                                       !- View Factor to Ground
  ,                                       !- Number of Vertices
  -12.0525360984798, 10.4695804842649, 18.4999783335109, !- X,Y,Z Vertex 1 [m]
  -12.0525360984798, 29.4495807702184, 18.4999783335109, !- X,Y,Z Vertex 2 [m]
  -79.0325378702316, 29.4495807702184, 18.4999783335109, !- X,Y,Z Vertex 3 [m]
  -79.0325378702316, 10.4695804842649, 18.4999783335109; !- X,Y,Z Vertex 4 [m]
"""

    return string
#%%


