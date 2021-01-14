"""Description.

https://www.cyberciti.biz/faq/python-run-external-command-and-get-output/

"""

import subprocess
from subprocess import Popen, PIPE
import sys
import os
from externalcommands import RADIANCE_PATH, ACCELERAD_PATH


def run_command(cmd_list):
	
	#Setting enviromental variable PATH
	os.environ["PATH"] = f"{RADIANCE_PATH}\\bin;{ACCELERAD_PATH}\\bin;" \
		+ "{}".format(os.environ["PATH"])
	
	#Setting enviromental variable RAYPATH
	os.environ["RAYPATH"] = f".;{RADIANCE_PATH}\\lib;{ACCELERAD_PATH}\\lib;"

	print("Running subprocess: {}".format(cmd_list[0]))
	#subprocess.call(cmd_list) this provides no ouput
	
	# Run process
	p = Popen(cmd_list, stdin=PIPE, stdout=PIPE, stderr=PIPE)
	output, err = p.communicate(b"input data that is passed to subprocess' stdin")
	rc = p.returncode
	print("Done subprocess: {}. Returncode: {}".format(cmd_list[0],rc))
	

	
def run_command_save_output(cmd_list, output_file_path):
	
	#Setting enviromental variable PATH
	os.environ["PATH"] = f"{RADIANCE_PATH}\\bin;{ACCELERAD_PATH}\\bin;" \
		+ "{}".format(os.environ["PATH"])
	
	#Setting enviromental variable RAYPATH
	os.environ["RAYPATH"] = f".;{RADIANCE_PATH}\\lib;{ACCELERAD_PATH}\\lib;"

	print("Running subprocess: {}".format(cmd_list[0]))
	#subprocess.call(cmd_list) this provides no ouput
	
	# Run process
	p = Popen(cmd_list, stdin=PIPE, stdout=PIPE, stderr=PIPE)
	output, err = p.communicate(b"input data that is passed to subprocess' stdin")
	rc = p.returncode
	with open(output_file_path, "wb") as outfile:
		outfile.write(output)
	print("Done subprocess: {}. Returncode: {}".format(cmd_list[0],rc))
	
