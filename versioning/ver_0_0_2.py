"""
Description:
    
    This is the Baseline implementation. 
    It will only rely on CPU based computations.
    It will only contain calculations from Radiance and EnergyPlus
"""

from zoning.levels import level_logic
from recipes.dayligthanalysis_2 import daylightanalysis_2
from general.paths import write_to_json


def ver_0_0_2(info):
    
    
    print("################### Levels handling ###################")
    level_logic(info)

    print("################### Daylight analysis ###################")
    #daylightanalysis_2(info, engine = "Accelerad")

    #Updating json
    write_to_json(info)

