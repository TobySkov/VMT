"""This is the main file

Geometry handling will be called from the main script

"""

from versioning.baseline import baseline

def VMT(*args, **kwargs):
    
    simulation_folder_path = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Desktop\baseline_test"
    location = "Copenhagen"
    
    baseline(simulation_folder_path,
             location)



if __name__ == "__main__":
    VMT()
