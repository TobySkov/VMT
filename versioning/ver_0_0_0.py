"""
Description:
    
    This is the Baseline implementation. 
    It will only rely on CPU based computations.
    It will only contain calculations from Radiance and EnergyPlus
"""
from recipes.radiationanalysis import radiationanalysis
from zoning.zones import zones_logic
from recipes.dayligthanalysis import daylightanalysis
from general.paths import write_to_json
from recipes.energyanalysis import energyanalysis


def ver_0_0_0(info):

    #Run radiation study
    print("################### Radiation analysis ###################")
    radiationanalysis(info, engine = "Radiance")
    
    #Insert rooms
    print("################### Zone distribution ###################")
    zones_logic(info)

    #3-phase method for all rooms
    print("################### Daylight analysis ###################")
    daylightanalysis(info, engine = "Radiance")
    
    #EnergyPlus simulation for all rooms
    print("################### Energy analysis ###################")
    energyanalysis(info)
    
    #Updating json
    write_to_json(info)

