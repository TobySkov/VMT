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
    
    def __init__(self, input_json, cmd_folder):
        
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
        self.main_folder =      cmd_folder
        
        #Root level output folder structure
        self.root =             Path(input_json["output_folder"])
        self.input_folder =     Path(input_json["output_folder"] + "\\input")
        self.sky_folder=        Path(input_json["output_folder"] + "\\sky")

        
        self.daylight_folder =  Path(input_json["output_folder"] + \
                                                     "\\daylight_analysis")
            
        self.energy_folder =  Path(input_json["output_folder"] + \
                                                     "\\energy_analysis")


        #Daylight subfolder
        self.vmx_folder = self.daylight_folder.joinpath("vmx")

    def createfolders(self):
        create_folders_from_list([self.input_folder,
                                  self.sky_folder,
                                  self.daylight_folder,
                                  self.energy_folder,
                                  self.vmx_folder])



#%% class containing info about input geometry files
class inputfiles(folderstructure):
    
    def __init__(self, f, input_json):
        
        try: #Works for version 0_0_0 and 0_0_1
            self.vmt_facade_src = Path(input_json["vmt_facade_src"])
            file_name = self.vmt_facade_src.name
            self.vmt_facade_dst = f.input_folder.joinpath(file_name)
            
            self.vmt_rest_src = Path(input_json["vmt_rest_src"])
            file_name = self.vmt_rest_src.name
            self.vmt_rest_dst = f.input_folder.joinpath(file_name)
        except: 
            pass
        
        try: #Works for version 0_0_2
            self.vmt_src = Path(input_json["vmt_src"])
            file_name = self.vmt_src.name
            self.vmt_dst = f.input_folder.joinpath(file_name)
        except: 
            pass
            
        
        self.context_src = Path(input_json["context_src"])
        file_name = self.context_src.name
        self.context_dst = f.input_folder.joinpath(file_name)
        
    def copyfiles(self):
        
        src_list = [self.vmt_src,
                    self.context_src]
        
        dst_list = [self.vmt_dst,
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




#%%

class others:
    
    def __init__(self, i, f, input_json):
    
        self.sim_resolution = input_json["simulation_resolution"]

        
        self.path_json = \
            f.root.joinpath("info.json")

        self.method = input_json["method"]
        
#%%

class daylightanalysis:
    def __init__(self, f, input_json):
        
        self.day_context_reflectance = input_json["context_reflectance"]
        self.day_floor_reflectance = input_json["floor_reflectance"]
        self.day_wall_reflectance = input_json["wall_reflectance"]
        self.day_ceiling_reflectance = input_json["ceiling_reflectance"]
        
        self.unique_levels_list = []
        self.real_levels_list = []
        
        self.day_sensorpoint_height = input_json["day_sensorpoint_height"]
        
        self.day_grid_x_dim = input_json["day_grid_x_dim"]
        self.day_grid_y_dim = input_json["day_grid_y_dim"] 
        
        self.sim_period_start = input_json["sim_period_start"]
        self.sim_period_end = input_json["sim_period_end"]
        self.day_win_ratio = input_json["day_win_ratio"]
        self.day_win_aperture_height = input_json["day_win_aperture_height"]
        self.day_win_sill_height = input_json["day_win_sill_height"]
        self.day_win_horizontal_separation = input_json["day_win_horizontal_separation"]
        self.day_win_vertical_separation = input_json["day_win_vertical_separation"]
        
        tmx_no = input_json["tmx_no"]
        self.day_tmx = \
            f.main_folder.joinpath(f"database\\tmx\\{tmx_no}\\{tmx_no}.xml")
        
        
        

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
            
        tmx_no = input_json["tmx_no"]
        self.ene_tmx = f.main_folder.joinpath(
            f"database\\tmx\\{tmx_no}\\GlzSys_{tmx_no}_Bsdf.idf")
        
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

def collect_info_2(input_json_path, cmd_folder):
    
    input_json = read_json(input_json_path)
    
    
    #Folder structure
    f = folderstructure(input_json, cmd_folder)
    f.createfolders()

    #Input geometry files    
    i = inputfiles(f, input_json)
    i.copyfiles()
    
    #Sky model
    s = skymodels(f,input_json)
    s.copyfiles()
    

    #Other info
    o = others(i, f, input_json)
    
    #Daylight analysis
    d = daylightanalysis(f, input_json)

    e = energyanalysis(f, input_json)
    
    info = combineinstances([f,i,s,o,d,e])
    
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
        


    