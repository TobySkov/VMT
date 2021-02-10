"""Description."""

from externalcommands.runcommands import run_command
from general.paths import decode_path_manager_panda
from externalcommands.parameters import rtrace_parameters

#%%
def run_rfluxmtx_radiation(path_mananger_pd,
                           no_of_sensor_points_total):
    
    out = decode_path_manager_panda(path_mananger_pd, ["RADIANCE_PATH",
                                                       "RESOLUTION",
                                                       "RFLUXSKY_RAD",
                                                       "VMT_RAD_FILE",
                                                       "VMT_RAD_FILE_REST",
                                                       "CONTEXT_RAD_FILE",
                                                       "RADIATION_ALL_PTS_FILE",
                                                       "RADIATION_COEFFICIENTS"])
    RADIANCE_PATH = out[0]
    RESOLUTION = out[1]
    RFLUXSKY_RAD = out[2]
    VMT_RAD_FILE = out[3]
    VMT_RAD_FILE_REST = out[4]
    CONTEXT_RAD_FILE = out[5]
    RADIATION_ALL_PTS_FILE = out[6]
    RADIATION_COEFFICIENTS = out[7]
    
    ##https://www.radiance-online.org/learning/tutorials/matrix-based-methods
    # page 41
    # - denotes that sender will be given through standard input
    
    cmd_list = [f"{RADIANCE_PATH}\\bin\\rfluxmtx",
			     "-y", f"{no_of_sensor_points_total}",
				 "-I"]
    
    cmd_list.extend(rtrace_parameters(RESOLUTION,
                                      sim_type = "RADIATION"))
    

    cmd_list.extend(["-",   #This specifies that sender is from stdin
                     f"{RFLUXSKY_RAD}",
                     f"{VMT_RAD_FILE}",
                     f"{VMT_RAD_FILE_REST}",
                     f"{CONTEXT_RAD_FILE}",])
    
    run_command(path_mananger_pd,
                cmd_list, 
				output_file_path = RADIATION_COEFFICIENTS,
                input_file_path = RADIATION_ALL_PTS_FILE)
    

#%%
def run_epw2wea(path_mananger_pd):

    out = decode_path_manager_panda(path_mananger_pd, ["RADIANCE_PATH",
                                                       "EPW_FILE",
                                                       "WEA_FILE"])
    RADIANCE_PATH = out[0]
    EPW_FILE = out[1]
    WEA_FILE = out[2]
    
    cmd_list = [f"{RADIANCE_PATH}\\bin\\epw2wea",
			      f"{EPW_FILE}", 
				  f"{WEA_FILE}"]
		
    run_command(path_mananger_pd,
                cmd_list)

#%%
def run_gendaymtx(path_mananger_pd,
				  spektrum,
				  resolution):

    out = decode_path_manager_panda(path_mananger_pd, ["RADIANCE_PATH",
                                                       "WEA_FILE"])
    RADIANCE_PATH = out[0]
    WEA_FILE = out[1]

    
    cmd_list = [f"{RADIANCE_PATH}\\bin\\gendaymtx"]
	
    if spektrum == "visible spektrum":
        spektrum_cmd = "0"
        key = "SMX_FILE_O0"
    elif spektrum == "full spektrum":
        spektrum_cmd = "1"
        key = "SMX_FILE_O1"
    else:
        raise Exception("""Unknown input for variable: spektrum
                        Options are: (visible spektrum, full spektrum)""")
                  
    out = decode_path_manager_panda(path_mananger_pd, [key])		
    output_file_path = out[0]
    
    cmd_list.append(f"-O{spektrum_cmd}")
	
    assert resolution in [1, 2, 4], "Unkown input for variable: resolution"
	
    cmd_list.extend(["-m", f"{resolution}"])
	
	
    cmd_list.extend(["-r", "0.0",
                     f"{WEA_FILE}"])
		
    run_command(path_mananger_pd,
                cmd_list, 
                output_file_path)
