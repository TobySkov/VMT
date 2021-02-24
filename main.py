"""This is the main file

Geometry handling will be called from the main script

"""

from versioning.baseline import baseline
from general.paths import collect_info
import sys

def VMT():
    
    #Reading path to input json from command line arguments
    input_json_path = sys.argv[1]
        
    #Data and path manager
    info = collect_info(input_json_path)

    #Running baseline implementation
    baseline(info)


if __name__ == "__main__":
    VMT()
    
