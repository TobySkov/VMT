"""
Description:
    
    This is the Baseline implementation. 
    It will only rely on CPU based computations.
    It will only contain calculations from Radiance and EnergyPlus
"""
from recipes.radiationanalysis import radiationanalysis_radiance

def baseline(path_mananger_pd,
             RESOLUTION,
             ROOM_DIM):
    pass

    #Run radiation study
    radiationanalysis_radiance(path_mananger_pd,
                               RESOLUTION,
                               ROOM_DIM)
    
    #Perform clustering
    
    #3-phase method for all rooms
    
    #EnergyPlus simulation for all rooms
    
    