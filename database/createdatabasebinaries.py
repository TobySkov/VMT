"""Description."""

from externalcommands.radiancecommands import run_epw2wea
from externalcommands.radiancecommands import run_gendaymtx
import torch
from general.ascii import read_ascii_data


def smtx_to_tensor(smtx_path):
	ascii_data = read_ascii_data(smtx_path)
	ascii_data_tensor = torch.tensor(ascii_data,dtype = torch.float32)
	print("START - Saving ascii data to torch tensor")
	torch.save(ascii_data_tensor, smtx_path.replace(".smx",".pt"))
	print("DONE - Saving ascii data to torch tensor")
	
def create_smtx_binaries(epw_path, base_path):
	
	wea_path = epw_path.replace(".epw",".wea")
	run_epw2wea(epw_path, wea_path)
	
	smtx_path = epw_path.replace(".epw","__vis_m1.smx")
	print(f"Creating {smtx_path}")
	run_gendaymtx(wea_path, smtx_path, 
			      spektrum = "visible spektrum",
				  resolution = 1)
	smtx_to_tensor(smtx_path)
	
	smtx_path = epw_path.replace(".epw","__vis_m2.smx")
	print(f"Creating {smtx_path}")
	run_gendaymtx(wea_path, smtx_path, 
			      spektrum = "visible spektrum",
				  resolution = 2)
	smtx_to_tensor(smtx_path)
	
	smtx_path = epw_path.replace(".epw","__vis_m4.smx")
	print(f"Creating {smtx_path}")
	run_gendaymtx(wea_path, smtx_path, 
			      spektrum = "visible spektrum",
				  resolution = 4)
	smtx_to_tensor(smtx_path)
	
	smtx_path = epw_path.replace(".epw","__sol_m1.smx")
	print(f"Creating {smtx_path}")
	run_gendaymtx(wea_path, smtx_path, 
			      spektrum = "full spektrum",
				  resolution = 1)
	smtx_to_tensor(smtx_path)
	
	smtx_path = epw_path.replace(".epw","__sol_m2.smx")
	print(f"Creating {smtx_path}")
	run_gendaymtx(wea_path, smtx_path, 
			      spektrum = "full spektrum",
				  resolution = 2)
	smtx_to_tensor(smtx_path)
	
	smtx_path = epw_path.replace(".epw","__sol_m4.smx")
	print(f"Creating {smtx_path}")
	run_gendaymtx(wea_path, smtx_path, 
			      spektrum = "full spektrum",
				  resolution = 4)
	smtx_to_tensor(smtx_path)
		
	with open(base_path + "\\DONE.txt", 'w') as outfile:
		outfile.write("All skymodels have been created and saved in ascii" \
				+ " and torch binary for this location/epw-file")

	
def update_smtx_database():
	#Finding folder tree for smx folder 
	# and calling create_smtx_binaries() on all epw files,
	#which are not already DONE (DONE.txt)
	pass
	#Check that "create_smtx_binaries"
	# have been run for entire database
	
	
	
def create_tmtx_binaries():
	pass
	#Seperate into the 8 different matrices in xml file and save through torch
	
def update_tmtx_database():
	pass
	#Check that "create_tmtx_binaries"
	# have been run for entire database
	

if __name__ == "__main__":
	epw_path = r"C:\Users\Tubsp\OneDrive\Skrivebord\Thesis\VMT\database\smx\IWEC\Denmark\Copenhagen\DNK_Copenhagen.061800_IWEC.epw"
	base_path = r"C:\Users\Tubsp\OneDrive\Skrivebord\Thesis\VMT\database\smx\IWEC\Denmark\Copenhagen"
	create_smtx_binaries(epw_path, base_path)