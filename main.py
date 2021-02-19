"""This is the main file

Geometry handling will be called from the main script

"""

from versioning.baseline import baseline
from general.paths import path_manager
import os 

def VMT(*args, **kwargs):
    
    #User inputs
    RADIANCE_PATH = r"C:\Radiance"
    ACCELERAD_PATH = r"C:\Accelerad"
    SIMULATION_FOLDER = r"C:\baseline_test" #Needs to be without whitespace
    LOCATION = "Copenhagen"
    RESOLUTION = 0
    ROOM_DIM = [3.5,4.5,6] #Height, Width, Depth - this should not be multiple with grid size (otherwise rooms will align on boundaries)
    max_rooms_per_surface = 4
    
    INPUT_GEO_FILES = ["examples\\example1\\volume_massing.rad",
                       "examples\\example1\\volume_massing_rest.rad",
                       "examples\\example1\\context.rad"]
    
    #Other inputs
    MAIN_PATH = os.path.dirname(__file__)
    
    #Path manager
    path_mananger_pd = path_manager(RADIANCE_PATH,ACCELERAD_PATH,
                                    SIMULATION_FOLDER, LOCATION,
                                    MAIN_PATH,RESOLUTION,
                                    INPUT_GEO_FILES,
                                    ROOM_DIM)

    #At this stage run grasshopper script

    baseline(path_mananger_pd,
             max_rooms_per_surface)


if __name__ == "__main__":
    VMT()
    
