"""
Description:

"""
import numpy as np
import plotly.graph_objects as go
from geometry.readinput import read_rad_files_polygons


def load_rad_to_plotly(rad_files_list):
    #Assuming the order of the list is:
    #
    #volume_massing.rad
    #volume_massing_rest.rad
    #context.rad
    polygons_nested = read_rad_files_polygons(rad_files_list)
    
    x=[0.0, 0.0, 0.0, 0.0]
    y=[0.0, 0.0, 0.0, 0.0]
    z=[0.0, 0.0, 0.0, 0.0]
    
    colors = ["red", "blue", "green"]
    colorscales = ["Reds", "Blues", "Greens"]
    opacities = [1.0, 1.0, 0.5]
    data = []

    for i in range(len(polygons_nested)):
        for j in range(len(polygons_nested[i])):
            polygon = polygons_nested[i][j]
            
            for k in range(len(polygon)):
                x[k] = polygon[k].x
                y[k] = polygon[k].y
                z[k] = polygon[k].z
            
            #https://community.plotly.com/t/vertical-surface-with-3d-topography/32349/4
            #Vertical surface plot
            if all(elem == x[0] for elem in x): 
                yy = np.linspace(min(y),max(y),2)
                zz = np.linspace(min(z),max(z),2)
                yy, zz = np.meshgrid(yy, zz)
                xx=np.ones(yy.shape)*x[0]
                data.append(go.Surface(x=xx, y=yy, z=zz, opacity=opacities[i],
                                       surfacecolor = xx,
                                       colorscale=colorscales[i], 
                                       showscale=False))
            
            #Vertical surface plot
            elif all(elem == y[0] for elem in y):
                xx = np.linspace(min(x),max(x),2)
                zz = np.linspace(min(z),max(z),2)
                xx, zz = np.meshgrid(xx, zz)
                yy=np.ones(xx.shape)*y[0]
                data.append(go.Surface(x=xx, y=yy, z=zz, opacity=opacities[i],
                                       surfacecolor = yy,
                                       colorscale=colorscales[i], 
                                       showscale=False))

            #Horizontal surface plot
            else:
                data.append(go.Mesh3d(x=x, y=y, z=z, color = colors[i],
                                                      opacity=opacities[i]))

    """
    i = 0

    x = [-2.0, -2.0, 21.0, 21.0]
    y = [-7, 5, 5, -7]
    z = [8.0, 8.0, 8.0, 8.0]
    data.append(go.Mesh3d(x=x, y=y, z=z, 
                          opacity=opacities[i]))
    

    x = [-2.0, -2.0, 21.0, 21.0]
    y = [-7, 5, 5, -7]
    z = [8.0*2, 8.0*2, 8.0*2, 8.0*2]
    data.append(go.Mesh3d(x=x, y=y, z=z, 
                          opacity=opacities[i]))
    
    x = [-2.0, -2.0, 21.0, 21.0]
    y = [-5, -5, -5, -5]
    z = [8.0, 8.0*2, 8.0*2, 8.0]
    data.append(go.Mesh3d(x=x, y=y, z=z, 
                          opacity=opacities[i]))
            """
    return data

if __name__ == "__main__":
    
    rad_files_list = ["..\\examples\\example1\\volume_massing.rad",
                      "..\\examples\\example1\\volume_massing_rest.rad",
                      "..\\examples\\example1\\context.rad"]
    
    data = load_rad_to_plotly(rad_files_list)
    
    fig = go.Figure(data=data)
    fig.show()