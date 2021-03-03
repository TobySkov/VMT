"""
Description:

"""


from subprocess import Popen, PIPE
import os

def run_energyplus(info, cmd_list, cwd_folder):

    #os.environ["PATH"] = f"{info.energyplus_folder};" \
	#	+ "{}".format(os.environ["PATH"])
        
    prior = os.getcwd()
    os.chdir(cwd_folder)
    
    print("START - Subprocess: {}".format(cmd_list[0]))
	
	# Run process
    p = Popen(cmd_list, stdin=PIPE, stdout=PIPE, stderr=PIPE)

    output, err = p.communicate(b"This is stdin (type:bytes)")
    rc = p.returncode
    
    if rc != 0:
        print(f"Error code: \n {err}")
	
    print("DONE  - Subprocess: {}. Returncode: {}".format(cmd_list[0],rc))
    
    os.chdir(prior)
    
    string = output.decode()
	

