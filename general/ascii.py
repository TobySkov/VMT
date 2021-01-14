"""Description."""

import numpy as np

def read_ascii_header(file_path):
	
	nrows = 0
	ncols = 0
	ncomp = 0
	skiplines = 0
	
	with open(file_path, 'r') as infile:
		
		for index, line in enumerate(infile):
			
			if "NROWS" in line:
				nrows = int(line.split("=")[-1])
				
			elif "NCOLS" in line:
				ncols = int(line.split("=")[-1])
				
			elif "NCOMP" in line:
				ncomp = int(line.split("=")[-1])
				
			elif "FORMAT=ascii" in line:
				skiplines = index + 2
				break
			
	return nrows, ncols, ncomp, skiplines



def read_ascii_data(file_path):
	
	nrows, ncols, ncomp, skiplines = read_ascii_header(file_path)
	print("START - Reading ascii data")
	ascii_data = np.loadtxt(file_path, skiprows = skiplines)
	print("DONE - Reading ascii data")
	return ascii_data
