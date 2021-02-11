"""
Description:

"""

from ladybug_geometry.geometry3d.pointvector import Point3D

def read_rad_files_polygons(rad_files_list):
    
    polygons_nested = []
    
    for i in range(len(rad_files_list)):
    
        with open(rad_files_list[i], "r") as infile:
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
            
        polygons_nested.append(polygons)
        
    return polygons_nested