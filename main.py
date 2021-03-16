"""This is the main file

Geometry handling will be called from the main script

"""

import sys
from versioning.ver_0_0_0 import ver_0_0_0
from versioning.ver_0_0_1 import ver_0_0_1
from general.paths import collect_info

def main():

    #Reading path to input json from command line arguments
    input_json_path = sys.argv[1]

    #Data and path manager
    info = collect_info(input_json_path)

    #Running baseline implementation
    if info.method == "ver_0_0_0":
        ver_0_0_0(info)
        
    #Running baseline implementation
    if info.method == "ver_0_0_1":
        ver_0_0_1(info)


if __name__ == "__main__":
    main()
