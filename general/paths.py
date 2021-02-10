"""
Description:
    
For managing paths and file headers

"""

import pandas as pd
import os
import shutil 

#%%

def create_folder(path_list):
    for i in range(len(path_list)):
        if not os.path.exists(path_list[i]):
            os.makedirs(path_list[i])
        else:
            print(f"Path already exsists:\n{path_list[i]}")
            print("BE CAREFULL to have other files in these folders, " + \
                  "as it may be overwritten\n")

#%%

def find_epw(LOCATION, MAIN_PATH):
    
    with open(MAIN_PATH + "\\database\\smx\\overview.txt", "r") as infile:
        content = infile.readlines()
    
    found = False
    for i in range(len(content)):
        if LOCATION == content[i].split(", ")[0]:
            EPW_FILE_DATABASE = MAIN_PATH + content[i].split(", ")[1]
            found = True
            
    if not found:
        raise Exception(f"Location name not found in database: {LOCATION}")
        
    return EPW_FILE_DATABASE

#%%

def path_manager(RADIANCE_PATH, ACCELERAD_PATH,
                 SIMULATION_FOLDER, LOCATION,
                 MAIN_PATH, RESOLUTION):
    
    LOCATION = LOCATION.lower()
    
    ###Geometry input files:
    INPUT_FOLDER = SIMULATION_FOLDER + "\\input\\"
    VMT_RAD_FILE = INPUT_FOLDER + "volume_massing.rad"
    VMT_RAD_FILE_REST = INPUT_FOLDER + "volume_massing_rest.rad"
    CONTEXT_RAD_FILE = INPUT_FOLDER + "context.rad"
    
    ###Radiation study files (mesh)
    RADIATION_FOLDER = SIMULATION_FOLDER + "\\radiation_grid\\"
    RADIATION_MESH_FILES = RADIATION_FOLDER + "mesh_XXX.txt"
    RADIATION_POINT_FILES = RADIATION_FOLDER + "surf_XXX.pts"
    RADIATION_ALL_PTS_FILE = RADIATION_FOLDER + "surf_all.pts"
    RADIATION_COEFFICIENTS = RADIATION_FOLDER + "radiation_coefficients.dmx"
    
    MESH_FILE_HEADER_VERTICES = "### Mesh vertices\n"
    MESH_FILE_HEADER_FACES = "### Mesh faces\n"
    
    ###Sky folder
    SKY_FOLDER = SIMULATION_FOLDER + "\\sky\\"
    EPW_FILE_DATABASE = find_epw(LOCATION, MAIN_PATH)
    EPW_FILE = SIMULATION_FOLDER + "\\sky\\" + f"{LOCATION}.epw"
    WEA_FILE = SIMULATION_FOLDER + "\\sky\\" + f"{LOCATION}.wea"
    SMX_FILE_O0 = SIMULATION_FOLDER + "\\sky\\" + f"{LOCATION}_O0.smx"
    SMX_FILE_O1 = SIMULATION_FOLDER + "\\sky\\" + f"{LOCATION}_O1.smx"
    
    ###Room folder
    ROOM_FOLDER = SIMULATION_FOLDER + "\\rooms\\"
    
    #Creating folders
    create_folder([SIMULATION_FOLDER,
                   INPUT_FOLDER,
                   RADIATION_FOLDER,
                   SKY_FOLDER,
                   ROOM_FOLDER])
    
    #Copying upside down sky (after folder creation)
    RFLUXSKY_RAD_DATABASE = MAIN_PATH + r"\database\smx\rfluxsky.rad"
    RFLUXSKY_RAD = SIMULATION_FOLDER + "\\sky\\rfluxsky.rad"
    shutil.copy(RFLUXSKY_RAD_DATABASE, RFLUXSKY_RAD)
    
    #Copying weather file (after folder creation)
    shutil.copy(EPW_FILE_DATABASE, EPW_FILE)
    
    
    
    keys = ["RADIANCE_PATH",
            "ACCELERAD_PATH",
            "VMT_RAD_FILE",
            "VMT_RAD_FILE_REST",
            "CONTEXT_RAD_FILE",
            "RADIATION_MESH_FILES",
            "RADIATION_POINT_FILES",
            "RADIATION_ALL_PTS_FILE",
            "RADIATION_COEFFICIENTS",
            "MESH_FILE_HEADER_VERTICES",
            "MESH_FILE_HEADER_FACES",
            "EPW_FILE",
            "WEA_FILE",
            "SMX_FILE_O0",
            "SMX_FILE_O1",
            "RESOLUTION",
            "RFLUXSKY_RAD"] 
    
    values = [RADIANCE_PATH,
              ACCELERAD_PATH,
              VMT_RAD_FILE,
              VMT_RAD_FILE_REST,
              CONTEXT_RAD_FILE,
              RADIATION_MESH_FILES,
              RADIATION_POINT_FILES,
              RADIATION_ALL_PTS_FILE,
              RADIATION_COEFFICIENTS,
              MESH_FILE_HEADER_VERTICES,
              MESH_FILE_HEADER_FACES,
              EPW_FILE,
              WEA_FILE,
              SMX_FILE_O0,
              SMX_FILE_O1,
              RESOLUTION,
              RFLUXSKY_RAD]
    
    d = {'Name': keys, 'Path/Header': values}
    path_mananger_pd = pd.DataFrame(data=d)
    
    return path_mananger_pd

#%%

def decode_path_manager_panda(path_mananger_pd, keys_list):
    values_list = []
    for i in range(len(keys_list)):
        try:
            boolean = path_mananger_pd["Name"] == keys_list[i]
            values = path_mananger_pd["Path/Header"]
            values_list.append(values[boolean].to_numpy()[0])
        except:
            print(f"Couldn't find key: {keys_list[i]}")
    return values_list
    