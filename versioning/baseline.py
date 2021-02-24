"""
Description:
    
    This is the Baseline implementation. 
    It will only rely on CPU based computations.
    It will only contain calculations from Radiance and EnergyPlus
"""
from recipes.radiationanalysis import radiationanalysis_radiance

#from zoning.zones import zones_logic


def baseline(info):
    pass

    #Run radiation study
    radiationanalysis_radiance(info)
    
    #Insert rooms
    #zones_logic(data_and_path_manager)



    #3-phase method for all rooms
    
    #EnergyPlus simulation for all rooms
    
    