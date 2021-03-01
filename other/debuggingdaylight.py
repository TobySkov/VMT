"""
Description:

"""

import numpy as np
from general.ascii import read_ascii_header
import matplotlib.pyplot as plt

#%%



def read_data(filepath):
    
    nrows, ncols, ncomp, skiplines = read_ascii_header(filepath)
    
    #data = np.zeros((nrows,ncols))
    
    #with open(filepath) as infile:
    #    content = infile.readlines()
            
    #for i in range(nrows):
    #    content[skiplines + i].split("\t")[:-2]
    
    data = np.loadtxt(filepath, skiprows=skiplines)
    
    return data

#%%


vmx_hb_path = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT\frontend\DaylightAnalysis\gridbased_threephase\result\matrix\Window_88.vmx"
dmx_hb_path = r"C:\Users\Pedersen_Admin\OneDrive - Perkins and Will\Documents\GitHub\VMT\frontend\DaylightAnalysis\gridbased_threephase\result\matrix\Window_88_1.dmx"

vmx_vmt_path = r"C:\baseline_test_2\daylight_analysis\matrices\surf_2__room_0.vmx"
dmx_vmt_path = r"C:\baseline_test_2\daylight_analysis\matrices\surf_2__room_0.dmx"



#%%

vmx_hb_data = read_data(vmx_hb_path)
dmx_hb_data = read_data(dmx_hb_path)

vmx_vmt_data = read_data(vmx_vmt_path)
dmx_vmt_data = read_data(dmx_vmt_path)


#%%

fig = plt.figure()
ax = fig.add_subplot(111)
cax = ax.matshow(vmx_hb_data)
fig.colorbar(cax)
plt.show()

#%%

fig = plt.figure()
ax = fig.add_subplot(111)
cax = ax.matshow(vmx_vmt_data)
fig.colorbar(cax)
plt.show()

#%%

fig = plt.figure()
ax = fig.add_subplot(111)
cax = ax.matshow(vmx_vmt_data-vmx_hb_data)
fig.colorbar(cax)
plt.show()

#%%

fig = plt.figure()
ax = fig.add_subplot(111)
cax = ax.matshow(dmx_vmt_data-dmx_hb_data)
fig.colorbar(cax)
plt.show()


