"""
Description:
    
For managing paths and file headers

"""

import os
import shutil 
from pathlib import Path
import json
import copy


#Consider: It is slower to have one single dict for all file paths.
#           Could also consider nested classes.


#%% class containing info about folder structure
class folderstructure:
    
    def __init__(self, input_json):
        
        #Simulation programs
        self.radiance_folder =    Path(input_json["radiance_folder"])
        self.accelerad_folder =   Path(input_json["accelerad_folder"])
        
        self.radiance_bin = self.radiance_folder.joinpath("bin")
        self.radiance_lib = self.radiance_folder.joinpath("lib")
        
        self.accelerad_bin = self.accelerad_folder.joinpath("bin")
        self.accelerad_lib = self.accelerad_folder.joinpath("lib")
        
        self.energyplus_folder = Path(input_json["energyplus_folder"])
        self.enerplus_exe = self.energyplus_folder.joinpath("energyplus.exe")
        self.enerplus_idd = self.energyplus_folder.joinpath("Energy+.idd")
        
        
        #API placement
        self.main_folder =      Path(input_json["main_folder"])
        
        #Root level output folder structure
        self.root =             Path(input_json["output_folder"])
        self.input_folder =     Path(input_json["output_folder"] + "\\input")
        self.sky_folder=        Path(input_json["output_folder"] + "\\sky")
        self.radiation_folder = Path(input_json["output_folder"] + \
                                     "\\radiation_analysis")
        
        self.daylight_folder =  Path(input_json["output_folder"] + \
                                                     "\\daylight_analysis")
            
        self.energy_folder =  Path(input_json["output_folder"] + \
                                                     "\\energy_analysis")

        #Radiation subfolders
        self.radiation_mesh_folder = \
            self.radiation_folder.joinpath("mesh_grid") 
        self.radiation_points_folder = \
            self.radiation_folder.joinpath("points")
        self.radiation_results_folder = \
            self.radiation_folder.joinpath("results")
        
        #Daylight subfolder
        self.room_folder = self.daylight_folder.joinpath("rooms")
        
        self.daylight_matrix_folder = \
            self.daylight_folder.joinpath("matrices")
        self.daylight_results_folder = \
            self.daylight_folder.joinpath("results")
        self.daylight_mesh_folder = \
            self.daylight_folder.joinpath("mesh")
        self.daylight_points_folder = \
            self.daylight_folder.joinpath("points")
            
            

    def createfolders(self):
        create_folders_from_list([self.input_folder,
                                  self.sky_folder,
                                  self.radiation_folder,
                                  self.radiation_mesh_folder,
                                  self.radiation_points_folder,
                                  self.radiation_results_folder,
                                  self.daylight_folder,
                                  self.energy_folder,
                                  self.room_folder,
                                  self.daylight_matrix_folder,
                                  self.daylight_results_folder,
                                  self.daylight_mesh_folder,
                                  self.daylight_points_folder])



#%% class containing info about input geometry files
class inputfiles(folderstructure):
    
    def __init__(self, f, input_json):
        
        self.vmt_facade_src = Path(input_json["vmt_facade_src"])
        file_name = self.vmt_facade_src.name
        self.vmt_facade_dst = f.input_folder.joinpath(file_name)
        
        self.vmt_rest_src = Path(input_json["vmt_rest_src"])
        file_name = self.vmt_rest_src.name
        self.vmt_rest_dst = f.input_folder.joinpath(file_name)
        
        self.context_src = Path(input_json["context_src"])
        file_name = self.context_src.name
        self.context_dst = f.input_folder.joinpath(file_name)
        
    def copyfiles(self):
        src_list = [self.vmt_facade_src,
                    self.vmt_rest_src,
                    self.context_src]
        
        dst_list = [self.vmt_facade_dst,
                    self.vmt_rest_dst,
                    self.context_dst]
        
        copy_files(src_list, dst_list)
        

#%% class containing info about skymodel
class skymodels:
    
    def __init__(self, f, input_json):
        
        #Paths
        self.epw_src = find_epw(input_json["location"], f)
        self.epw_dst = f.sky_folder.joinpath(self.epw_src.name)
        
        self.skyrad_src = \
            f.main_folder.joinpath("database\\smx\\rfluxsky.rad")
        self.skyrad_dst = f.sky_folder.joinpath(self.skyrad_src.name)
        
        self.wea_path = self.epw_dst.with_suffix(".wea")
        self.smx_O0_path = self.epw_dst.with_suffix(".O0smx")
        self.smx_O1_path = self.epw_dst.with_suffix(".O1smx")
        
        
        #Data
        self.epw_data = None
        self.wea_data = None
        self.smx_O0_data = None
        self.smx_O1_data = None
        
        
    def copyfiles(self):
        
        src_list = [self.epw_src,
                    self.skyrad_src]
        
        dst_list = [self.epw_dst,
                    self.skyrad_dst]
        
        copy_files(src_list, dst_list)



#%% class related to radiation study

class radiationanalysis:
    
    def __init__(self, i, f):
        
        ### Counting how many facades present
        self.facade_count = count_facades(i.vmt_facade_dst)
    
        #All points and mesh files
        self.rad_mesh_all = f.radiation_mesh_folder.joinpath("mesh_all.txt")
        self.rad_points_all = f.radiation_points_folder.joinpath("points_all.txt")
        
        ### Lists of files for each facade
        self.rad_mesh_files_list = []
        #self.rad_points_files_list = []
        #self.rad_normals_files_list = []
        self.rad_results_cummulative_list = []
        #self.rad_results_labels_list = []
        #self.rad_results_centers_list = []
        
        for i in range(self.facade_count):
            self.rad_mesh_files_list.append(
                f.radiation_mesh_folder.joinpath(f"mesh_{i}.txt"))
            
           # self.rad_points_files_list.append(
           #    f.radiation_points_folder.joinpath(f"points_{i}.txt"))
            
            #self.rad_normals_files_list.append(
            #    f.radiation_points_folder.joinpath(f"normals_{i}.txt"))
            
            self.rad_results_cummulative_list.append(
                f.radiation_results_folder.joinpath(f"cummulative_{i}.txt"))
            
            #self.rad_results_labels_list.append(
            #    f.radiation_results_folder.joinpath(f"labels_{i}.txt"))
    
            #self.rad_results_centers_list.append(
            #    f.radiation_results_folder.joinpath(f"centers_{i}.txt"))
    
        
        ### All results files
        self.rad_coefficients = f.radiation_results_folder.joinpath(
            "daylight_coefficients.dmx")
 
        self.rad_results_rgb = \
            f.radiation_results_folder.joinpath("result_rgb.rgb")
        self.rad_results_wh = f.radiation_results_folder.joinpath("result_wh.txt")

        self.rad_results_cummulative = f.radiation_results_folder.joinpath(
            "cummulative.txt")

        ### Headers
        self.rad_results_cummulative_header =   "### Cummulative results\n"

        ### Data
        self.rad_surf_mesh_data = []
        self.rad_cumm_resuls_data = []
    
        self.rad_no_of_sensor_points = 0
        self.rad_no_of_sensor_points_list = []

#%%

class others:
    
    def __init__(self, i, f, input_json):
    
        self.sim_resolution = input_json["simulation_resolution"]
        self.room_dim_height = input_json["room_dim_height"]
        self.room_dim_width = input_json["room_dim_width"]
        self.room_dim_depth = input_json["room_dim_depth"]
        self.max_rooms_per_surface = input_json["max_rooms_per_surface"]
        self.path_json = \
            f.root.joinpath("info.json")
        self.rad_grid_x_dim = input_json["rad_grid_x_dim"]
        self.rad_grid_y_dim = input_json["rad_grid_y_dim"]
        self.rad_grid_offset = input_json["rad_grid_offset"]
        self.rad_period_start = input_json["rad_period_start"]
        self.rad_period_end =   input_json["rad_period_end"]
        self.vmt_faces = []
        self.room_WWR = input_json["room_WWR"]
        self.approved_rooms = []
        self.approved_rooms_corresponding_vmt = []
        self.method = input_json["method"]
        
#%%

class daylightanalysis:
    def __init__(self, f, input_json):
        
        self.context_reflectance = input_json["context_reflectance"]
        self.floor_reflectance = input_json["floor_reflectance"]
        self.wall_reflectance = input_json["wall_reflectance"]
        self.ceiling_reflectance = input_json["ceiling_reflectance"]
        
        self.vmx_matrix_path_list = []
        self.dmx_matrix_path_list = []

        self.window_radfile_path_list = []
        self.room_radfile_path_list = []
        self.vmt_radfile_path_list = []
        
        self.day_points_path_list = []
        self.day_mesh_path_list = []
        
        self.day_sensorpoint_height = input_json["day_sensorpoint_height"]
        
        self.day_grid_x_dim = input_json["day_grid_x_dim"]
        self.day_grid_y_dim = input_json["day_grid_y_dim"] 
        
        self.day_results_rgb_list = []
        self.day_results_ill_list = []
        self.day_results_da_list = []
        
        #self.day_rotated_floors_list = []
        #self.day_rotated_mesh_list = []
        
        self.day_tmx = input_json["day_tmx"]

#%%

class energyanalysis:
    def __init__(self, f, input_json):
        
        ep_objects_folder = \
            f.main_folder.joinpath("database\\idfcomponents\\defaultsobjects")
        
        ep_objects_names = os.listdir(ep_objects_folder)
        
        self.ene_default_ep_objects = []
        
        for i in range(len(ep_objects_names)):
            self.ene_default_ep_objects.append(ep_objects_folder.joinpath(
                ep_objects_names[i]))
            
        self.ene_tmx = input_json["ene_tmx"]
        
        self.ene_idf_files_list = []
        self.ene_cumm_results_list = []
        
            
        

#%%
class empty:
    pass

#%%
def combineinstances(list_of_instances):
    
    info = empty()
    
    for i in range(len(list_of_instances)):
        info.__dict__.update(list_of_instances[i].__dict__)

    return info


#%%
def read_json(input_json_path):
    with open(input_json_path, 'r') as infile:
        json_data = json.load(infile)
    return json_data

#%%

def collect_info(input_json_path):
    
    input_json = read_json(input_json_path)
    
    
    #Folder structure
    f = folderstructure(input_json)
    f.createfolders()

    #Input geometry files    
    i = inputfiles(f, input_json)
    i.copyfiles()
    
    #Sky model
    s = skymodels(f,input_json)
    s.copyfiles()
    
    #Radiation analysis
    r = radiationanalysis(i,f)
    
    #Other info
    o = others(i, f, input_json)
    
    #Daylight analysis
    d = daylightanalysis(f, input_json)

    e = energyanalysis(f, input_json)
    
    info = combineinstances([f,i,s,r,o,d,e])
    
    write_to_json(info)
    
    return info


#%%
def write_to_json(info):
    
    #Convert paths to strings
    info_copy = copy.deepcopy(info.__dict__)
    
    for key in info_copy:
        
        if type(info_copy[key]) == list:
            for i in range(len(info_copy[key])):
                info_copy[key][i] = str(info_copy[key][i])
                
        else:
            info_copy[key] = str(info_copy[key])
        
    #Dump to json
    with open(info.path_json, 'w') as outfile:   
        json.dump(info_copy, outfile, indent = "\t")
        
        
        

#%%

def create_folders_from_list(path_list):
    for i in range(len(path_list)):
        if not os.path.exists(path_list[i]):
            os.makedirs(path_list[i])
        else:
            print(f"Path already exsists:\n{path_list[i]}")
            print("BE CAREFULL to have other files in these folders, " + \
                  "as it may be overwritten\n")

#%%

def copy_files(src_list, dst_list):
    
    length_1 = len(src_list)
    assert length_1 == len(dst_list), "The length of the two lists" + \
        " should be identical"
        
    for i in range(length_1):
        if os.path.isfile(dst_list[i]):
            print(f"File will be overwritten: \n {dst_list[i]}")
            
        shutil.copy(src_list[i], dst_list[i])
            
        
    

#%%

def find_epw(location, f):
    
    location = location.lower()
    
    file = f.main_folder.joinpath("database\\smx\\overview.txt")
    
    with open(file, "r") as infile:
        content = infile.readlines()
    
    found = False
    for i in range(len(content)):
        if location == content[i].split(", ")[0]:
            epw_src = f.main_folder.joinpath(content[i].split(", ")[1])
            found = True
            break
            
    if not found:
        raise Exception(f"Location name not found in database: {location}")
        
    return epw_src


#%%

def count_facades(volume_massing_facades_rad):
    
    count = 0
    with open(volume_massing_facades_rad, 'r') as infile:
        for line in infile:
            if "polygon" in line:
                count += 1
                
    return count
        


    