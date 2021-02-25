"""
Description:
    
    This is the Baseline implementation. 
    It will only rely on CPU based computations.
    It will only contain calculations from Radiance and EnergyPlus
"""
from recipes.radiationanalysis import radiationanalysis_baseline
from zoning.zones import zones_logic
from recipes.dayligthanalysis import daylightanalysis_baseline
from general.paths import write_to_json


def baseline(info):

    #Run radiation study
    print("################### Radiation analysis ###################")
    radiationanalysis_baseline(info)
    
    #Insert rooms
    print("################### Zone distribution ###################")
    zones_logic(info)

    #3-phase method for all rooms
    print("################### Daylight analysis ###################")
    daylightanalysis_baseline(info)
    
    #EnergyPlus simulation for all rooms
    
    
    #Updating json
    write_to_json(info)