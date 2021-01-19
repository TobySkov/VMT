"""Description.

https://www.cyberciti.biz/faq/python-run-external-command-and-get-output/

"""

import subprocess
from subprocess import Popen, PIPE
import sys
import os
import torch
from externalcommands import RADIANCE_PATH, ACCELERAD_PATH
import numpy as np

	
def run_command(cmd_list, 
				output_file_path = None):
	
	#Setting enviromental variable PATH
	os.environ["PATH"] = f"{RADIANCE_PATH}\\bin;{ACCELERAD_PATH}\\bin;" \
		+ "{}".format(os.environ["PATH"])
	
	#Setting enviromental variable RAYPATH
	os.environ["RAYPATH"] = f".;{RADIANCE_PATH}\\lib;{ACCELERAD_PATH}\\lib;"

	print("START - Subprocess: {}".format(cmd_list[0]))
	
	# Run process
	p = Popen(cmd_list, stdin=PIPE, stdout=PIPE, stderr=PIPE)
	output, err = p.communicate(b"input data that is passed to subprocess' stdin")
	rc = p.returncode
	
	print("DONE - Subprocess: {}. Returncode: {}".format(cmd_list[0],rc))
	

	#Saving output in plain text
	if output_file_path:
		print("START - Writing ASCII data")
		with open(output_file_path, "wb") as outfile:
			outfile.write(output)
		print("DONE - Writing ASCII data")
			
		
	