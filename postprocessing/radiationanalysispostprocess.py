"""
Description:

"""

from general.paths import decode_path_manager_panda
from general.ascii import read_ascii_header 
import numpy as np

def radiation_post_processing(path_mananger_pd,
                              period = [0,8759]):
    
    out = decode_path_manager_panda(path_mananger_pd, ["RADIATION_RESULTS_W",
                                                       "RADIATION_RESULTS_CUM",
                                                       "RADIATION_RESULTS_CUM_HEADER"])
    
    RADIATION_RESULTS_W = out[0]
    RADIATION_RESULTS_CUM = out[1]
    RADIATION_RESULTS_CUM_HEADER = out[2]
    
    nrows, ncols, ncomp, skiplines = read_ascii_header(RADIATION_RESULTS_W)
    
    data = np.loadtxt(RADIATION_RESULTS_W, skiprows=skiplines)
    
    start = period[0]
    end = period[1]
    
    cummulative_result = np.sum(data[:,start:end],axis=1)
    
    np.savetxt(RADIATION_RESULTS_CUM, cummulative_result, delimiter="\n", 
               header = RADIATION_RESULTS_CUM_HEADER + \
                   f", period = [{start}:{end}]")