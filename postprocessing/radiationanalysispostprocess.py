"""
Description:

"""

from general.paths import decode_path_manager_panda
from general.ascii import read_ascii_header 
import numpy as np

def radiation_post_processing(path_mananger_pd,
                              no_of_sensor_points_list,
                              period = [0,8759]):
    
    start = period[0]
    end = period[1]
    
    out = decode_path_manager_panda(path_mananger_pd, ["RADIATION_RESULTS_W",
                                                       "RADIATION_RESULTS_CUM",
                                                       "RADIATION_RESULTS_CUM_ALL",
                                                       "RADIATION_RESULTS_CUM_HEADER"])
    
    RADIATION_RESULTS_W = out[0]
    RADIATION_RESULTS_CUM = out[1]
    RADIATION_RESULTS_CUM_ALL = out[2]
    RADIATION_RESULTS_CUM_HEADER = out[3]
    
    nrows, ncols, ncomp, skiplines = read_ascii_header(RADIATION_RESULTS_W)
    
    data = np.loadtxt(RADIATION_RESULTS_W, skiprows=skiplines)
    
    cummulative_result = np.sum(data[:,start:end],axis=1)
    

    np.savetxt(RADIATION_RESULTS_CUM_ALL, cummulative_result, delimiter="\n", 
               header = RADIATION_RESULTS_CUM_HEADER + \
                   f", period = [{start}:{end}]")
        
    idx_start = 0
    idx_end = no_of_sensor_points_list[0]
    for i in range(len(no_of_sensor_points_list)):
        np.savetxt(RADIATION_RESULTS_CUM.replace("XXX",f"{i}"), 
                   cummulative_result[idx_start:idx_end], 
                   delimiter="\n", header = RADIATION_RESULTS_CUM_HEADER + \
                   f", period = [{start}:{end}]")

        try:
            idx_start = idx_start + no_of_sensor_points_list[i]
            idx_end = idx_end + no_of_sensor_points_list[i+1]
            
        except:
            pass







