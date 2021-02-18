"""
Description:

"""

def write_rad_file_facade_only(file_name, facade_face,i,j):
    #Needs to have material proporties implemented
    
    pts = facade_face.vertices
    
    with open(file_name,"w") as outfile:
        outfile.write(f"void polygon surf_{i}__room_{j}_extWall\n")
        outfile.write("0\n")
        outfile.write("0\n")
        outfile.write("12 " + \
                      f"{pts[0].x} {pts[0].y} {pts[0].z} " + \
                      f"{pts[1].x} {pts[1].y} {pts[1].z} " + \
                      f"{pts[2].x} {pts[2].y} {pts[2].z} " + \
                      f"{pts[3].x} {pts[3].y} {pts[3].z}\n\n\n")