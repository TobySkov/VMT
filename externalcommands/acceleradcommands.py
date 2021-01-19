"""Description."""

from externalcommands import ACCELERAD_PATH
from externalcommands.runcommands import run_command, run_command_save_output
from externalcommands.parameters import rtrace_parameters

def run_rfluxmtx(complexity,
				 irradiance,
				 sender_rad,
				 reciever_rad,
				 system_rad,
				 output_file_path):
	

	rtrace_params = rtrace_parameters(complexity)
	
	if irradiance:
		number_of_points = get_num_points(reciever_rad)
		rtrace_params = rtrace_params + f"-I -y {number_of_points}"
		
		cmd_list = [f"{ACCELERAD_PATH}\\bin\\accelerad_rfluxmtx.exe"] \
					+ rtrace_params \
					+
			      f"{input_file_path}", 
				  f"{output_file_path}"]
		
		run_command_save_output(cmd_list, output_file_path)
		
		
	elif not irradiance:
		rtrace_params = rtrace_params + "-c 1000"
		
	else:
		raise Exception("""Unknown input for variable: irradiance
				  Options are: (True, False)""")
	
		
		
