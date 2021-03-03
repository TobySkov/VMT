"""
Description:

"""
from general.ascii import read_ascii_header 
import numpy as np


#%%
def calc_da(info):
    
    for i in range(len(info.approved_rooms)):
        
        #room = info.approved_rooms[i]
        
        nrows, ncols, ncomp, skiplines = \
            read_ascii_header(info.day_results_ill_list[i])
    
        data = np.loadtxt(info.day_results_ill_list[i], skiprows=skiplines).T
        
        occ_sch = get_occ_hours()
        
        #Picking out data in occ_sch
        idx = occ_sch==1
        data = data[idx,:]
        
        #daylight antonomy
        above_300 = data > 300
        da = (((above_300).sum(axis=0))/above_300.shape[0])*100
        
        #Write to files
        np.savetxt(info.day_results_da_list[i], da, 
                   delimiter="\n")
        
        
        
        
#%%

def get_occ_hours():
    
    weekday = [0]*8 + [1]*9 + [0]*7
    weekend = [0]*24
    
    week = weekday*5+weekend*2
    
    year = week*52 + weekend
    
    return np.array(year)