"""
Description:

"""

from sklearn.cluster import KMeans
import numpy as np
from general.paths import decode_path_manager_panda

def kmeans_clustering(path_mananger_pd,
                      no_of_sensor_points_list,
                      n_clusters):
    
    
    out = decode_path_manager_panda(path_mananger_pd, ["RADIATION_POINT_FILES",
                                                       "RADIATION_RESULTS_CUM",
                                                       "RADIATION_CLUSTERING"])
    
    RADIATION_POINT_FILES = out[0]
    RADIATION_RESULTS_CUM = out[1]
    RADIATION_CLUSTERING = out[2]
    
    pts_files = []
    results_files= []
    for i in range(len(no_of_sensor_points_list)):
        pts_files.append(RADIATION_POINT_FILES.replace("XXX",f"{i}"))
        results_files.append(RADIATION_RESULTS_CUM.replace("XXX",f"{i}"))
        

    for i in range(len(no_of_sensor_points_list)):
        
        X = np.zeros((no_of_sensor_points_list[i], 4))
        
        with open(pts_files[i], "r") as infile:
            content = infile.readlines()
            
        for j in range(len(content)):
            line = content[j].split(" ")
            X[j,0] = float(line[0])
            X[j,1] = float(line[1])
            X[j,2] = float(line[2])
        
        with open(results_files[i], "r") as infile:
            content = infile.readlines()
    
        for j in range(1,len(content)):
            X[(j-1),3] = float(content[j])
    
        
        k_means = KMeans(n_clusters=n_clusters)
        
        #norm = np.linalg.norm(X)
        #X = X/norm
        k_means.fit(X)
            
        k_means_predicted = k_means.predict(X)     

        np.savetxt(RADIATION_CLUSTERING.replace("XXX",f"{i}"), 
                   k_means_predicted, 
                   delimiter="\n",
                   fmt="%d")









if __name__ == "__main__":
    #Example:
    #https://www.kaggle.com/timi01/k-means-clustering-and-3d-plotting
    pass

