"""
Description:

"""

from general.ascii import read_ascii_header 
import numpy as np

def radiation_post_processing(info):
    
    start = info.rad_period_start
    end = info.rad_period_end
    
    nrows, ncols, ncomp, skiplines = read_ascii_header(info.rad_results_wh)
    
    data = np.loadtxt(info.rad_results_wh, skiprows=skiplines)
    
    
    cummulative_result = np.sum(data[:,start:end],axis=1)
    
    
    indicies = np.cumsum(info.rad_no_of_sensor_points_list[:-1])
    cummulative_result_data = \
        np.split(cummulative_result, indicies)
    
    
    #Save to info
    info.rad_cumm_resuls_data.extend(cummulative_result_data)
    
    #Write to files
    np.savetxt(info.rad_results_cummulative, cummulative_result, 
               delimiter="\n")
    
    for i in range(len(cummulative_result_data)):
        
        np.savetxt(info.rad_results_cummulative_list[i], 
                   cummulative_result_data[i], 
                   delimiter="\n")
        

    
    
    
    



