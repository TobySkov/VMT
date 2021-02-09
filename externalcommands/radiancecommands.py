"""Description."""

from externalcommands import RADIANCE_PATH
from externalcommands.runcommands import run_command


def run_epw2wea(input_file_path,
				output_file_path):
	"""Summary.
	
	Converts epw to wea

	Parameters
	----------
	input_file_path : str
		Full path to epw.
	output_file_path : str
		Full path to wea.

	Returns
	-------
	None.

	"""
	cmd_list = [f"{RADIANCE_PATH}\\bin\\epw2wea",
			      f"{input_file_path}", 
				  f"{output_file_path}"]
		
	run_command(cmd_list)


def run_gendaymtx(input_file_path,
				  output_file_path,
				  spektrum,
				  resolution):
	"""Summary.
	
	Converts .wea to .smx

	Parameters
	----------
	input_file_path : str
		Full path to .wea file.
	output_file_path : str
		Full path to .smx file.
	spektrum : TYPE
		DESCRIPTION.
	resolution : TYPE
		DESCRIPTION.

	Raises
	------
	Exception
		DESCRIPTION.

	Returns
	-------
	None.

	"""
	cmd_list = [f"{RADIANCE_PATH}\\bin\\gendaymtx"]
	
	if spektrum == "visible spektrum":
		spektrum_cmd = "0"
	elif spektrum == "full spektrum":
		spektrum_cmd = "1"
	else:
		raise Exception("""Unknown input for variable: spektrum
				  Options are: (visible spektrum, full spektrum)""")
				  
	cmd_list.append(f"-O{spektrum_cmd}")
	
	assert resolution in [1, 2, 4], "Unkown input for variable: resolution"
	
	cmd_list.extend(["-m", f"{resolution}"])
	
	
	cmd_list.extend(["-r", "0.0",
				     f"{input_file_path}"])
		
	run_command(cmd_list, 
				output_file_path)
