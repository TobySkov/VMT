"""
Description:

"""

from ladybug_geometry.geometry3d.face import Face3D
from ladybug_geometry.geometry3d.pointvector import Point3D

def read_rad_file_polygons(rad_file):

    with open(rad_file, "r") as infile:
        content = infile.readlines()
        
    polygons = []
    for i in range(len(content)):
        try: #In case it is not possible to access element 1 of list.
            if content[i].split(" ")[1] == "polygon" and content[i + 3].split(" ")[0] == "12":
                numbers = content[i + 3].split(" ")
                polygon = [Point3D(numbers[1],numbers[2],numbers[3]),
                           Point3D(numbers[4],numbers[5],numbers[6]),
                           Point3D(numbers[7],numbers[8],numbers[9]),
                           Point3D(numbers[10],numbers[11],numbers[12])]
                polygons.append(polygon)
        except:
            pass
            
    return polygons


#%%

def read_rad_file_polygons_to_levels(rad_file):

    with open(rad_file, "r") as infile:
        content = infile.readlines()
    
    levels = []
    level = {"walls": []}
    level_count = 0
    count = 0
    for i in range(len(content)):
        try: #In case it is not possible to access element 1 of list.
            if content[i].split(" ")[1] == "polygon" and content[i + 3].split(" ")[0] == "12":
                numbers = content[i + 3].split(" ")
                polygon = [Point3D(numbers[1],numbers[2],numbers[3]),
                           Point3D(numbers[4],numbers[5],numbers[6]),
                           Point3D(numbers[7],numbers[8],numbers[9]),
                           Point3D(numbers[10],numbers[11],numbers[12])]
                count += 1
                
            if "generic_wall" in content[i]:
                level["walls"].append(Face3D(polygon))
                
            elif "generic_floor" in content[i]:
                level["floor"] = Face3D(polygon)
                
            elif "generic_roof" in content[i]:
                level["ceiling"] = Face3D(polygon)
                
            if count == 6:
                level["real_level_ID"] = level_count
                levels.append(level)
                level = {"walls": [], "floor": [], "ceiling": []}
                level_count += 1
                count = 0
                
        except:
            pass
            
    return levels

