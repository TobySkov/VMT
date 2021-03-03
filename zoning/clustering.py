"""
Description:

"""

from sklearn.cluster import KMeans, AffinityPropagation, \
    AgglomerativeClustering, Birch, MiniBatchKMeans
    
import numpy as np
from general.paths import decode_path_manager_panda

from scipy.spatial.transform import Rotation as R

def clustering(path_mananger_pd,
                      no_of_sensor_points_list,
                      n_clusters):
    
    
    out = decode_path_manager_panda(path_mananger_pd, ["RADIATION_POINT_FILES",
                                                       "RADIATION_RESULTS_CUM",
                                                       "RADIATION_CLUSTERING_LABEL",
                                                       "RADIATION_CLUSTERING_CENTER"])
    
    RADIATION_POINT_FILES = out[0]
    RADIATION_RESULTS_CUM = out[1]
    RADIATION_CLUSTERING_LABEL = out[2]
    RADIATION_CLUSTERING_CENTER = out[3]
    
    pts_files = []
    results_files= []
    for i in range(len(no_of_sensor_points_list)):
        pts_files.append(RADIATION_POINT_FILES.replace("XXX",f"{i}"))
        results_files.append(RADIATION_RESULTS_CUM.replace("XXX",f"{i}"))
        

    center_points_list = []
    surf_normal = np.zeros((3))
    
    for i in range(len(no_of_sensor_points_list)):
        
        X = np.zeros((no_of_sensor_points_list[i], 4))
        
        with open(pts_files[i], "r") as infile:
            content = infile.readlines()
            
        for j in range(len(content)):
            line = content[j].split(" ")
            X[j,0] = float(line[0])
            X[j,1] = float(line[1])
            X[j,2] = float(line[2])
            
            if j == 0:
                surf_normal[0] = float(line[3])
                surf_normal[1] = float(line[4])
                surf_normal[2] = float(line[5])
                
        
        with open(results_files[i], "r") as infile:
            content = infile.readlines()
    
        for j in range(1,len(content)):
            X[(j-1),3] = float(content[j])
    
        
    
        ##### Applying rotation of points #Assuming vertical surface
        rot_axis = np.cross(surf_normal, np.array([0,0,1]))
        rot_angle = np.pi/2
        rotation_vector = rot_angle * rot_axis
        rotation = R.from_rotvec(rotation_vector)
        rot_matrix = rotation.as_matrix()  
    
        rotated_points = np.dot(rot_matrix,X[:,0:3].T).T
        
        z = rotated_points[:,2]
        if not all(elem == z[0] for elem in z):
            raise Exception("Unsuccesfull rotation of surface in Kmeans clustering")
            
        X = np.concatenate((rotated_points[:,0:2], np.array([X[:,3]]).T),axis=1)
        #####
    
    
    
        ### K-maens clustering
        #model = AffinityPropagation(damping = 0.7) #dampning = 0.9
        ####model = AgglomerativeClustering(n_clusters=n_clusters)
        
        #model = Birch(threshold=0.01, n_clusters=n_clusters)
        
        #model = KMeans(n_clusters=n_clusters)
        
        model = MiniBatchKMeans(n_clusters=n_clusters)
        
        
        
        ###
        model.fit(X)
        model_predicted = model.predict(X)   
        
        ####model_predicted = model.fit_predict(X)  # Only used for AgglomerativeClustering


        center_points = model.cluster_centers_[:,0:2]
        ###center_points = model.subcluster_centers_[:,0:2]
        
        
        
        ###Rotating centerpoints back
        z = z[:len(center_points)]
        center_points = np.concatenate((center_points, np.array([z]).T),axis=1)
        
        center_points = np.dot(rot_matrix.T,center_points.T).T
        ###
        
        

        np.savetxt(RADIATION_CLUSTERING_LABEL.replace("XXX",f"{i}"), 
                   model_predicted, 
                   delimiter="\n",
                   fmt="%d")
        
        np.savetxt(RADIATION_CLUSTERING_CENTER.replace("XXX",f"{i}"), 
                   center_points)
        
        center_points_list.append(center_points)


    return center_points_list



if __name__ == "__main__":
    #Example:
    #https://www.kaggle.com/timi01/k-means-clustering-and-3d-plotting
    pass

