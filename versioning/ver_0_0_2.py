"""
Description:
    
    This is the Baseline implementation. 
    It will only rely on CPU based computations.
    It will only contain calculations from Radiance and EnergyPlus
"""

from zoning.levels import level_logic

from general.paths import write_to_json


def ver_0_0_2(info):
    
    #Insert rooms
    print("################### Zone distribution ###################")
    level_logic(info)


    #Updating json
    write_to_json(info)

