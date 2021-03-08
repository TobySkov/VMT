"""Description."""

from externalcommands.runcommands import run_command
from externalcommands.parameters import rtrace_parameters



#%%
def run_epw2wea(info):
    
    cmd_list = [str(info.radiance_bin.joinpath("epw2wea")),
                str(info.epw_dst), 
				str(info.wea_path)]
		
    run_command(info,
                cmd_list)

#%%
def run_gendaymtx(info,
				  spektrum,
				  sky_resolution):


    cmd_list = [str(info.radiance_bin.joinpath("gendaymtx"))]
	
    if spektrum == "visible spektrum":
        spektrum_cmd = "0"
        output_file_path = info.smx_O0_path
        
    elif spektrum == "full spektrum":
        spektrum_cmd = "1"
        output_file_path = info.smx_O1_path
        
    else:
        raise Exception('''Unknown input for variable: spektrum
                        Options are: (visible spektrum, full spektrum)''')

    cmd_list.append(f"-O{spektrum_cmd}")
	
    assert sky_resolution in [1, 2, 4], "Unkown input for variable: resolution"
	
    cmd_list.extend(["-m", f"{sky_resolution}"])
	
	
    cmd_list.extend(["-r", "0.0",
                     f"{info.wea_path}"])
		
    run_command(info,
                cmd_list, 
                output_file_path)


    
#%%
def run_rfluxmtx_day_dmx(info,i):
       
    cmd_list = [str(info.radiance_bin.joinpath("rfluxmtx"))]
    
    cmd_list.extend(rtrace_parameters(info.sim_resolution))
    
    cmd_list.extend([f"{info.dmx_radfile_path_list[i]}",   
                     f"{info.skyrad_dst}",
                     f"{info.vmt_facade_dst}",
                     f"{info.vmt_rest_dst}",
                     f"{info.context_dst}",])
    
    run_command(info,
                cmd_list, 
				output_file_path = info.dmx_matrix_path_list[i])


#%%
def run_rfluxmtx_day_vmx(info,i):
    #Assuming that all rooms are the same - running rfluxmtx only once
    room = info.approved_rooms[i]
    
    cmd_list = [str(info.radiance_bin.joinpath("rfluxmtx")),
			     "-y", f"{room.no_of_sensorpoints}",
				 "-I"]
    
    cmd_list.extend(rtrace_parameters(info.sim_resolution))
    

    cmd_list.extend(["-",   #This specifies that sender is from stdin
                     f"{info.vmx_radfile_path_list[i]}",
                     f"{info.room_radfile_path_list[i]}"])
    
    run_command(info,
                cmd_list, 
				output_file_path = info.vmx_matrix_path_list[i],
                input_file_path = info.day_points_path_list[i])
    
    
#%%
def run_rfluxmtx_radiation(info):
       
    ##https://www.radiance-online.org/learning/tutorials/matrix-based-methods
    # page 41
    # - denotes that sender will be given through standard input
    cmd_list = [str(info.radiance_bin.joinpath("rfluxmtx")),
			     "-y", f"{info.rad_no_of_sensor_points}",
				 "-I"]
    
    cmd_list.extend(rtrace_parameters(info.sim_resolution))
    

    cmd_list.extend(["-",   #This specifies that sender is from stdin
                     f"{info.skyrad_dst}",
                     f"{info.context_dst}"])
    
    run_command(info,
                cmd_list, 
				output_file_path = info.rad_coefficients,
                input_file_path = info.rad_points_all)



#%%
def run_dctimestep(info,
                   simulation_type):

    if simulation_type == "RADIATION_ANALYSIS":
    
        cmd_list = [str(info.radiance_bin.joinpath("dctimestep")),
    			      f"{info.rad_coefficients}", 
    				  f"{info.smx_O1_path}"]
        
        output_file_path = info.rad_results_rgb
		
    run_command(info,
                cmd_list,
                output_file_path)
    
#%%
def run_dctimestep_day(info,i):
    
    cmd_list = [str(info.radiance_bin.joinpath("dctimestep")),
    			      f"{info.vmx_matrix_path_list[i]}",
                      f"{info.day_tmx}", 
                      f"{info.dmx_matrix_path_list[i]}", 
    				  f"{info.smx_O0_path}"]
        
    output_file_path = info.day_results_rgb_list[i]
		
    run_command(info,
                cmd_list,
                output_file_path)



#%%
def run_rmtxop(info,
               simulation_type):

    if simulation_type == "RADIATION_ANALYSIS":
    
        cmd_list = [str(info.radiance_bin.joinpath("rmtxop")),
    			      "-c", "0.265", "0.67", "0.065", "-fa",
    				  f"{info.rad_results_rgb}"]
        #-fa = format ascii
        #179*(0.265*R + 0.67*G + 0.065*B) = 47.435*R + 119.93*G + 11.635*B
        
        output_file_path = info.rad_results_wh
		
    run_command(info,
                cmd_list,
                output_file_path)




#%%
def run_rmtxop_day(info,i):

    
    cmd_list = [str(info.radiance_bin.joinpath("rmtxop")),
			      "-c", "47.435", "119.93", "11.635", "-fa",
				  f"{info.day_results_rgb_list[i]}"]

    
    output_file_path = info.day_results_ill_list[i]
		
    run_command(info,
                cmd_list,
                output_file_path)


