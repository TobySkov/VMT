"""Description.

https://www.cyberciti.biz/faq/python-run-external-command-and-get-output/

"""


from subprocess import Popen, PIPE
import os

#%%
def read_stdin(input_file_path):
    
    string = ""
    with open(input_file_path, "r") as infile:
        for line in infile:
            string = string + line
            
    bytes_input = string.encode()
    
    return bytes_input
	
#%%
def run_command(info,
                cmd_list, 
				output_file_path = False,
                input_file_path = False):
    
    
	#Setting enviromental variable PATH
    os.environ["PATH"] = f"{info.radiance_bin};{info.accelerad_bin};" \
		+ "{}".format(os.environ["PATH"])
	
	#Setting enviromental variable RAYPATH
    os.environ["RAYPATH"] = f".;{info.radiance_lib};{info.accelerad_lib};"

    print("START - Subprocess: {}".format(cmd_list[0]))
	
	# Run process
    p = Popen(cmd_list, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    if input_file_path != False:
        
        output, err = p.communicate(read_stdin(input_file_path))
    else:
        output, err = p.communicate(b"This is stdin (type:bytes)")
    rc = p.returncode
    
    if rc != 0:
        print(f"Error code: \n {err}")
	
    print("DONE  - Subprocess: {}. Returncode: {}".format(cmd_list[0],rc))
	

	#Saving output in plain text
    if output_file_path:
        print("START - Writing ASCII data")
        with open(output_file_path, "wb") as outfile:
            outfile.write(output)
        print("DONE  - Writing ASCII data")
			
		
#%%
