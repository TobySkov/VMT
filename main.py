"""This is the main file

Geometry handling will be called from the main script

"""

from versioning.baseline import baseline
from general.paths import path_manager
import os 
from display.visualization import load_radiation_mesh_to_plotly

def VMT(*args, **kwargs):
    
    #User inputs
    RADIANCE_PATH = r"C:\Radiance"
    ACCELERAD_PATH = r"C:\Accelerad"
    SIMULATION_FOLDER = r"C:\baseline_test" #Needs to be without whitespace
    LOCATION = "Copenhagen"
    RESOLUTION = "1"
    
    INPUT_GEO_FILES = ["examples\\example1\\volume_massing.rad",
                       "examples\\example1\\volume_massing_rest.rad",
                       "examples\\example1\\context.rad"]
    
    #Other inputs
    MAIN_PATH = os.path.dirname(__file__)
    
    #Path manager
    path_mananger_pd = path_manager(RADIANCE_PATH,ACCELERAD_PATH,
                                    SIMULATION_FOLDER, LOCATION,
                                    MAIN_PATH,RESOLUTION,
                                    INPUT_GEO_FILES)

    #At this stage run grasshopper script

    baseline(path_mananger_pd)
    load_radiation_mesh_to_plotly(path_mananger_pd)


if __name__ == "__main__":
    VMT()
    
