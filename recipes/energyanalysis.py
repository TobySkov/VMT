
import copy
from externalcommands.energypluscommands import run_energyplus
import os
import pandas as pd

from geometry.readinput import read_rad_file_polygons

#%%
def energyanalysis_baseline(info):
    
    write_idf_files(info)
    
    run_idf_files(info)
    
    ene_calculate_cummulative_results(info)

#%%
def ene_calculate_cummulative_results(info):
    
    for i in range(len(info.ene_idf_files_list)):
        folder = info.ene_idf_files_list[i].parents[0]
        
        csv_file = folder.joinpath("eplusout.csv")
        
        data = pd.read_csv(csv_file)
        
        floor_area = info.approved_rooms[i].geo_floor.area
        
        #kWh
        ideal_heating = (data["ZONENAME IDEAL LOADS AIR SYSTEM:Zone Ideal" + \
        " Loads Supply Air Total" + \
            " Heating Energy [J](Hourly)"].sum()/3600000)/floor_area
            
        ideal_cooling = (data["ZONENAME IDEAL LOADS AIR SYSTEM:Zone Ideal" + \
        " Loads Supply Air Total" + \
            " Cooling Energy [J](Hourly)"].sum()/3600000)/floor_area

        #W
        ideal_cooling_h = data["ZONENAME IDEAL LOADS AIR SYSTEM:Zone Ideal Loads Supply Air Total Cooling Energy [J](Hourly)"]/3600
        peak_cooling_index = ideal_cooling_h.idxmax()
        peak_cooling_load = ideal_cooling_h[peak_cooling_index]
        
        peak_cooling_load_PIT= str(data["Date/Time"].iloc[peak_cooling_index])
        
        
        output_file = folder.joinpath("cummulative_results.txt")
        info.ene_cumm_results_list.append(output_file)
        with open(output_file, "w") as outfile:
            outfile.write(f"{ideal_heating} #Cummulative heating load [kWh/(m2.year)]\n")
            outfile.write(f"{ideal_cooling} #Cummulative cooling load [kWh/(m2.year)]\n")
            outfile.write(f"{peak_cooling_load} #Peak cooling load [W]\n")
            outfile.write(f"{peak_cooling_load_PIT} #Peak cooling load timestamp\n")



    
#%%
def run_idf_files(info):
    
    for i in range(len(info.ene_idf_files_list)):
        
        idf = str(info.ene_idf_files_list[i])
        
        cwd_folder = info.ene_idf_files_list[i].parents[0]
        
        cmd_list = [str(info.enerplus_exe),
                    "-i", str(info.enerplus_idd),
                    "-w", str(info.epw_dst),
                    "-x", "-r",
                    idf]

        run_energyplus(info, cmd_list, cwd_folder)
    
    
    
#%%
def write_idf_files(info):
    
    idf_default_string = load_default_ep_objects(info)
    
    #Adding context and vmt rest (this does not change between rooms)
    idf_default_string += load_vmtrest_and_context(info)
    
    for i in range(len(info.approved_rooms)):
        
        idf_current_string = copy.deepcopy(idf_default_string)
        
        room = info.approved_rooms[i]
        
        idf_current_string += create_geometry_string(room)
        
        idf_current_string += load_window_construction(info)
        
        #Include shading from vmt facades
        idf_current_string += add_vmt_shading(info,i)
        
        folder = info.energy_folder.joinpath(room.room_name)
        if not os.path.exists(folder):
            os.makedirs(folder)
        
        filepath = folder.joinpath(room.room_name + ".idf")
        info.ene_idf_files_list.append(filepath)
        with open(filepath, "w") as outfile:
            outfile.write(idf_current_string)

#%%
def add_vmt_shading(info,i):
    string = ""
    vmt_facades = info.approved_rooms_corresponding_vmt[i]
    
    holed_mesh = vmt_facades[0]

    for i in range(len(holed_mesh.faces)):
        idx = holed_mesh.faces[i]
        pts = []
        for j in range(len(idx)):
            pts.append(holed_mesh.vertices[idx[j]])
        name = f"holed_facade_face_{i}"
        string += ep_triangle_shade(pts,name)
        
        
    for i in range(len(vmt_facades)-1):
        i = i + 1
        
        pts = vmt_facades[i].vertices
        name = f"other_facades_{i}"
        string += ep_face_shade(pts,name)
        
        
    return string
    
    
#%%
def load_vmtrest_and_context(info):
    

    string = ""
    
    polygons = read_rad_file_polygons(info.context_dst)
    for i in range(len(polygons)):
        string += ep_face_shade(pts = polygons[i], 
                                name = f"Shade_context_{i}")
    
    polygons = read_rad_file_polygons(info.vmt_rest_dst)
    for i in range(len(polygons)):
        string += ep_face_shade(pts = polygons[i], 
                                name = f"Shade_vmtrest_{i}")

    return string

#%%
def ep_triangle_shade(pts,name):
    
    string = "Shading:Building:Detailed,\n" + \
            f"\t{name}, !- Name\n" + \
            "\t, !-Transmittance Schedule Name (default zero)\n" + \
            "\t3, !- Number Vertices\n" + \
            f"\t{pts[0].x}, {pts[0].y}, {pts[0].z}, !- X,Y,Z Vertex 1\n" + \
            f"\t{pts[1].x}, {pts[1].y}, {pts[1].z}, !- X,Y,Z Vertex 2\n" + \
            f"\t{pts[2].x}, {pts[2].y}, {pts[2].z}; !- X,Y,Z Vertex 3\n\n\n"
            
    return string
    
#%%
def ep_face_shade(pts,name):
    
    string = "Shading:Building:Detailed,\n" + \
            f"\t{name}, !- Name\n" + \
            "\t, !-Transmittance Schedule Name (default zero)\n" + \
            "\t4, !- Number Vertices\n" + \
            f"\t{pts[0].x}, {pts[0].y}, {pts[0].z}, !- X,Y,Z Vertex 1\n" + \
            f"\t{pts[1].x}, {pts[1].y}, {pts[1].z}, !- X,Y,Z Vertex 2\n" + \
            f"\t{pts[2].x}, {pts[2].y}, {pts[2].z}, !- X,Y,Z Vertex 3\n" + \
            f"\t{pts[3].x}, {pts[3].y}, {pts[3].z}; !- X,Y,Z Vertex 4\n\n\n"
            
    return string

#%%

def load_default_ep_objects(info):
    
    idf_default_string = ""
    
    for i in range(len(info.ene_default_ep_objects)):
        with open(info.ene_default_ep_objects[i], "r") as infile:
            for line in infile:
                idf_default_string += line
    
    return idf_default_string


#%%

def load_window_construction(info):
    
    idf_window_string = ""
    
    with open(info.ene_tmx, "r") as infile:
        for line in infile:
            idf_window_string += line
    
    return idf_window_string

#%%
def create_geometry_string(room):
    
    room_string = ""
    
    
    zone_name = "ZONENAME"
    
    #External wall
    room_string += create_building_surface_string(
        name = "EXTWALL", 
        surface_type = "Wall", 
        construction_name = "EXTWALL_CONSTRUCTION",
        zone_name = zone_name, 
        outside_boundary_condition = "Outdoors",
        sun_exposure = "SunExposed", 
        wind_exposure = "WindExposed",
        pts = room.geo_ene_ext_wall.upper_left_counter_clockwise_vertices)
    
    
    #Window
    room_string += create_fenestration_surface_string(
        name = "WINDOW", 
        construction_name = "WINDOW_CONSTRUCTION",
        parent_surface = "EXTWALL", 
        pts = room.geo_window.upper_left_counter_clockwise_vertices)
    
    
    #Internal surfaces
    sun_exposure = "NoSun"
    wind_exposure = "NoWind"
    outside_boundary_condition = "Adiabatic"
    
    
    name = "FLOOR"
    surface_type = "Floor"
    construction_name = "FLOOR_CONSTRUCTION"
    pts = room.geo_floor.upper_left_counter_clockwise_vertices
    room_string += create_building_surface_string(name, surface_type, 
                                                  construction_name,
                                   zone_name, outside_boundary_condition,
                                   sun_exposure, wind_exposure,
                                   pts)
    
    
    name = "CEILING"
    surface_type = "Ceiling"
    construction_name = "CEILING_CONSTRUCTION"
    pts = room.geo_ceiling.upper_left_counter_clockwise_vertices
    room_string += create_building_surface_string(name, surface_type, 
                                                  construction_name,
                                   zone_name, outside_boundary_condition,
                                   sun_exposure, wind_exposure,
                                   pts)
    
    name = "BACK_WALL"
    surface_type = "Wall"
    construction_name = "INTWALL_CONSTRUCTION"
    pts = room.geo_back_wall.upper_left_counter_clockwise_vertices
    room_string += create_building_surface_string(name, surface_type, 
                                                  construction_name,
                                   zone_name, outside_boundary_condition,
                                   sun_exposure, wind_exposure,
                                   pts)
        
    name = "LEFT_WALL"
    surface_type = "Wall"
    construction_name = "INTWALL_CONSTRUCTION"
    pts = room.geo_left_wall.upper_left_counter_clockwise_vertices
    room_string += create_building_surface_string(name, surface_type, 
                                                  construction_name,
                                   zone_name, outside_boundary_condition,
                                   sun_exposure, wind_exposure,
                                   pts)
    
    name = "RIGHT_WALL"
    surface_type = "Wall"
    construction_name = "INTWALL_CONSTRUCTION"
    pts = room.geo_right_wall.upper_left_counter_clockwise_vertices
    room_string += create_building_surface_string(name, surface_type, 
                                                  construction_name,
                                   zone_name, outside_boundary_condition,
                                   sun_exposure, wind_exposure,
                                   pts)
    
    return room_string


#%%


def create_building_surface_string(name, surface_type, construction_name,
                                   zone_name, outside_boundary_condition,
                                   sun_exposure, wind_exposure,
                                   pts):


    string  = f"""
BuildingSurface:Detailed,
  {name},                               !- Name
  {surface_type},                       !- Surface Type
  {construction_name},                  !- Construction Name
  {zone_name},                          !- Zone Name
  {outside_boundary_condition},         !- Outside Boundary Condition
  ,                                     !- Outside Boundary Condition Object
  {sun_exposure},                       !- Sun Exposure
  {wind_exposure},                      !- Wind Exposure
  ,                                     !- View Factor to Ground
  ,                                     !- Number of Vertices
  {pts[0].x}, {pts[0].y}, {pts[0].z},   !- X,Y,Z Vertex 1 [m]
  {pts[1].x}, {pts[1].y}, {pts[1].z},   !- X,Y,Z Vertex 2 [m]
  {pts[2].x}, {pts[2].y}, {pts[2].z},   !- X,Y,Z Vertex 3 [m]
  {pts[3].x}, {pts[3].y}, {pts[3].z};   !- X,Y,Z Vertex 4 [m]
"""

    return string


#%%

def create_fenestration_surface_string(name, construction_name,
                                       parent_surface, pts):
    
    string = f"""
FenestrationSurface:Detailed,
  {name},                                 !- Name
  Window,                                 !- Surface Type
  {construction_name},                    !- Construction Name
  {parent_surface},                       !- Building Surface Name
  ,                                       !- Outside Boundary Condition Object
  ,                                       !- View Factor to Ground
  ,                                       !- Frame and Divider Name
  ,                                       !- Multiplier
  ,                                       !- Number of Vertices
  {pts[0].x}, {pts[0].y}, {pts[0].z},   !- X,Y,Z Vertex 1 [m]
  {pts[1].x}, {pts[1].y}, {pts[1].z},   !- X,Y,Z Vertex 2 [m]
  {pts[2].x}, {pts[2].y}, {pts[2].z},   !- X,Y,Z Vertex 3 [m]
  {pts[3].x}, {pts[3].y}, {pts[3].z};   !- X,Y,Z Vertex 4 [m]
"""

    return string

