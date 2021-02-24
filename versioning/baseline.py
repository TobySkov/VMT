"""
Description:
    
    This is the Baseline implementation. 
    It will only rely on CPU based computations.
    It will only contain calculations from Radiance and EnergyPlus
"""
from recipes.radiationanalysis import radiationanalysis_baseline
from zoning.zones import zones_logic
from recipes.dayligthanalysis import daylightanalysis_baseline

def baseline(info):

    #Run radiation study
    radiationanalysis_baseline(info)
    
    #Insert rooms
    zones_logic(info)

    #3-phase method for all rooms
    daylightanalysis_baseline(info)
    
    #EnergyPlus simulation for all rooms
    
    