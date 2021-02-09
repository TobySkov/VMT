"""Description."""

from externalcommands import RADIANCE_PATH
from externalcommands import ACCELERAD_PATH
from externalcommands.radiancecommands import run_epw2wea, run_gendaymtx



def radiationanalysis_radiance(epw_file_path,
                               volume_massing_rad_path,
                               context_rad_path):
    
    #epw2wea
    input_file_path = epw_file_path
    output_file_path = epw_file_path.replace(".epw",".wea")
    run_epw2wea(input_file_path, output_file_path)
    
    #wea2smx
    input_file_path = output_file_path
    output_file_path = epw_file_path.replace(".epw","_O1.smx")
    run_gendaymtx(input_file_path,
				  output_file_path,
				  spektrum = "full spektrum",
				  resolution = 1)
    
    #Create grid for at volume massing
    #   select only faces that are almost vertical.
    # 
    
    #create dmx
    #   run for each surface of the volume massing
    
    pass


def radiationanalysis_accelerad():
    pass