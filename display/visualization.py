"""
Description:

"""
import numpy as np
import plotly.graph_objects as go
from geometry.readinput import read_rad_files_polygons
from general.paths import decode_path_manager_panda
from ladybug_geometry.geometry3d.pointvector import Point3D


#%%
def polygon_to_go(polygon, color, colorscale, opacity):
    
    x=[0.0, 0.0, 0.0, 0.0]
    y=[0.0, 0.0, 0.0, 0.0]
    z=[0.0, 0.0, 0.0, 0.0]
    
    for point in range(len(polygon)):
        x[point] = polygon[point].x
        y[point] = polygon[point].y
        z[point] = polygon[point].z
            
    #https://community.plotly.com/t/vertical-surface-with-3d-topography/32349/4
    #Vertical surface plot
    if all(elem == x[0] for elem in x): 
        yy = np.linspace(min(y),max(y),2)
        zz = np.linspace(min(z),max(z),2)
        yy, zz = np.meshgrid(yy, zz)
        xx=np.ones(yy.shape)*x[0]
        go_data = go.Surface(x=xx, y=yy, z=zz, opacity=opacity,
                               surfacecolor = xx,
                               colorscale=colorscale, 
                               showscale=False)
    
    #Vertical surface plot
    elif all(elem == y[0] for elem in y):
        xx = np.linspace(min(x),max(x),2)
        zz = np.linspace(min(z),max(z),2)
        xx, zz = np.meshgrid(xx, zz)
        yy=np.ones(xx.shape)*y[0]
        go_data = go.Surface(x=xx, y=yy, z=zz, opacity=opacity,
                               surfacecolor = yy,
                               colorscale=colorscale, 
                               showscale=False)

    #Horizontal surface plot
    else:
        go_data = go.Mesh3d(x=x, y=y, z=z, color = color,
                                              opacity=opacity)
            
    return go_data

#%%
def load_rad_to_plotly(rad_files_list):
    #Assuming the order of the list is:
    #
    #volume_massing.rad
    #volume_massing_rest.rad
    #context.rad
    polygons_nested = read_rad_files_polygons(rad_files_list)
    
    colors = ["red", "blue", "green"]
    colorscales = ["Reds", "Blues", "Greens"]
    opacities = [1.0, 1.0, 0.5]
    data = []

    for i in range(len(polygons_nested)):
        for j in range(len(polygons_nested[i])):
            polygon = polygons_nested[i][j]
            
            go_data = polygon_to_go(polygon, color = colors[i],
                                    colorscale = colorscales[i],
                                    opacity = opacities[i])
            
            data.append(go_data)

    return data


    

#%%
def load_radiation_mesh_to_plotly(path_mananger_pd):
    #Since it is only for visualization purposes in jupyter notebook
    #   mesh is loaded from file (instead of passing mesh through API)
    
    
    out = decode_path_manager_panda(path_mananger_pd, ["RADIATION_ALL_MESH_FILE",
                                                       "MESH_FILE_HEADER_VERTICES",
                                                       "MESH_FILE_HEADER_FACES"])
    RADIATION_ALL_MESH_FILE = out[0]
    MESH_FILE_HEADER_VERTICES = out[1]
    MESH_FILE_HEADER_FACES = out[2]
    
    with open(RADIATION_ALL_MESH_FILE, "r") as infile:
        content = infile.readlines()
    
    V = []
    F = []
    
    read_vertices = False
    read_fases = False
    
    for i in range(len(content)):
        
        if MESH_FILE_HEADER_VERTICES in content[i]:
            read_vertices = True
            read_fases = False
            continue
            
        elif MESH_FILE_HEADER_FACES in content[i]:
            read_vertices = False
            read_fases = True
            continue
        
        if read_vertices:
            numbers = content[i].split(" ")
            V.append([float(numbers[0]),
            float(numbers[1]),
            float(numbers[2])])
            
        elif read_fases:
            numbers = content[i].split(" ")
            F.append([int(numbers[0]),
            int(numbers[1]),
            int(numbers[2]),
            int(numbers[3])])

    data = []
    colors = ["red", "blue", "green"]
    colorscales = ["Reds", "Blues", "Greens"]
    j = 0
    for i in range(len(F)):
        polygon = [Point3D(V[F[i][0]][0], V[F[i][0]][1], V[F[i][0]][2]),
                   Point3D(V[F[i][1]][0], V[F[i][1]][1], V[F[i][1]][2]),
                   Point3D(V[F[i][2]][0], V[F[i][2]][1], V[F[i][2]][2]),
                   Point3D(V[F[i][3]][0], V[F[i][3]][1], V[F[i][3]][2])]
    

        go_data = polygon_to_go(polygon, color = colors[j],
                                        colorscale = colorscales[j],
                                        opacity = 1.0)
            
        data.append(go_data)
        
        j += 1
        if j == 3:
            j=0

    return data
    