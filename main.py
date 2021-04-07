"""This is the main file

Geometry handling will be called from the main script

"""

import json
import sys
from versioning.ver_0_0_0 import ver_0_0_0
from versioning.ver_0_0_1 import ver_0_0_1
from versioning.ver_0_0_2 import ver_0_0_2
from general.paths import collect_info
from general.paths_2 import collect_info_2

from pathlib import Path
import time

#%%

def read_json(input_json_path):
    with open(input_json_path, 'r') as infile:
        json_data = json.load(infile)
    return json_data

#%%
def read_version(input_json_path):
    input_json = read_json(input_json_path)
    return input_json["method"]

#%%
def main():
    
    
    print(" +++++ VMT tool start +++++")
    
    start = time.time()

    #Finding folder where .py/.exe is run from
    cmd = Path(sys.argv[0])
    cmd_folder = cmd.parent
    
    #Reading path to input json from command line arguments
    input_json_path = sys.argv[1]


    #Running baseline implementation
    if read_version(input_json_path) == "ver_0_0_0":
        info = collect_info(input_json_path, cmd_folder)
        ver_0_0_0(info)
        
    #Running baseline implementation
    if read_version(input_json_path) == "ver_0_0_1":
        info = collect_info(input_json_path, cmd_folder)
        ver_0_0_1(info)

    if read_version(input_json_path) == "ver_0_0_2":
        info = collect_info_2(input_json_path, cmd_folder)
        ver_0_0_2(info)
        
    end = time.time()
    
    print("+++++ VMT tool end +++++")
    print(f"+++++ Wall time: {(end-start)/60} [min] +++++")

if __name__ == "__main__":
    main()


