"""
Description:

"""

from general.ascii import read_ascii_header 
import numpy as np

def radiation_post_processing(info):
    
    start = info.rad_period[0]
    end = info.rad_period[1]
    
    nrows, ncols, ncomp, skiplines = read_ascii_header(info.rad_results_wh)
    
    data = np.loadtxt(info.rad_results_wh, skiprows=skiplines)
    
    cummulative_result = np.sum(data[:,start:end],axis=1)
    

    np.savetxt(info.rad_results_cummulative, cummulative_result, 
               delimiter="\n")
    
    count = 0
    for i in range(len(info.rad_no_of_sensor_points_list)):
        
        with open(info.rad_results_cummulative_list[i], "w") as outfile:
            
            for j in range(info.rad_no_of_sensor_points_list[i]):
                
                outfile.write(f"{cummulative_result[count]}\n")
                count+=1
    
    
    
    
    """
    
    header = RADIATION_RESULTS_CUM_HEADER + \
                   f", period = [{start}:{end}]"
                   
                   
    cummulative_results_list = []
    idx_start = 0
    idx_end = no_of_sensor_points_list[0]
    for i in range(len(no_of_sensor_points_list)):
        np.savetxt(RADIATION_RESULTS_CUM.replace("XXX",f"{i}"), 
                   cummulative_result[idx_start:idx_end], 
                   delimiter="\n", header = RADIATION_RESULTS_CUM_HEADER + \
                   f", period = [{start}:{end}]")
        
        cummulative_results_list.append(cummulative_result[idx_start:idx_end])
        try:
            idx_start = idx_start + no_of_sensor_points_list[i]
            idx_end = idx_end + no_of_sensor_points_list[i+1]
            
        except:
            pass
    """

    #return cummulative_results_list




