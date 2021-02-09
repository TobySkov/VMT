"""
Description:
    
    This is the Baseline implementation. 
    It will only rely on CPU based computations.
    It will only contain calculations from Radiance and EnergyPlus
"""
from recipes.radiationanalysis import radiationanalysis_radiance

def baseline(simulation_folder_path,
             location):
    pass

    #Create simulation folder
    
    #Copy epw file to simulation folder 
    #   (Cross reference desired location with database)
    epw_file_path = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Desktop\baseline_test\simulation_files\sky\NOR_Oslo.Fornebu.014880_IWEC.epw"
    
    #Run radiation study
    volume_massing_rad_path = None
    context_rad_path = None
    radiationanalysis_radiance(epw_file_path,
                               volume_massing_rad_path,
                               context_rad_path)
    
    #Perform clustering
    
    #3-phase method for all rooms
    
    #EnergyPlus simulation for all rooms
    
    