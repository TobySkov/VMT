"""Description.

https://www.cyberciti.biz/faq/python-run-external-command-and-get-output/

"""


from subprocess import Popen, PIPE
import os
from general.paths import decode_path_manager_panda


def read_stdin(input_file_path):
    
    string = ""
    with open(input_file_path, "r") as infile:
        for line in infile:
            string = string + line
            
    bytes_input = string.encode()
    
    return bytes_input
	

def run_command(path_mananger_pd,
                cmd_list, 
				output_file_path = None,
                input_file_path = False):
    
    out = decode_path_manager_panda(path_mananger_pd, ["RADIANCE_PATH",
                                                       "ACCELERAD_PATH"])
    RADIANCE_PATH = out[0]
    ACCELERAD_PATH = out[1]
    
	#Setting enviromental variable PATH
    os.environ["PATH"] = f"{RADIANCE_PATH}\\bin;{ACCELERAD_PATH}\\bin;" \
		+ "{}".format(os.environ["PATH"])
	
	#Setting enviromental variable RAYPATH
    os.environ["RAYPATH"] = f".;{RADIANCE_PATH}\\lib;{ACCELERAD_PATH}\\lib;"

    print("START - Subprocess: {}".format(cmd_list[0]))
	
	# Run process
    p = Popen(cmd_list, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    if input_file_path != False:
        
        output, err = p.communicate(read_stdin(input_file_path))
    else:
        output, err = p.communicate(b"This is stdin (type:bytes)")
    rc = p.returncode
	
    print("DONE  - Subprocess: {}. Returncode: {}".format(cmd_list[0],rc))
	

	#Saving output in plain text
    if output_file_path:
        print("START - Writing ASCII data")
        with open(output_file_path, "wb") as outfile:
            outfile.write(output)
        print("DONE  - Writing ASCII data")
			
		
	