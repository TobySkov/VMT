
from geometry.dayligthgrid import daylight_mesh_grid
from externalcommands.radiancecommands import run_rfluxmtx_day_vmx, \
    run_rfluxmtx_day_dmx, run_gendaymtx, run_dctimestep_day, run_rmtxop_day

from postprocessing.daypostprocess import calc_da


def daylightanalysis_baseline(info):
    
    #Create gridded mesh for each room.
    daylight_mesh_grid(info)
    
    #Create vmx (for each room)
    for i in range(len(info.approved_rooms)):
        run_rfluxmtx_day_vmx(info,i)
    
    #Create dmx (for each room)
    for i in range(len(info.approved_rooms)):
        run_rfluxmtx_day_dmx(info,i)
    
    #Create smx
    run_gendaymtx(info,
				  spektrum = "visible spektrum", 
				  sky_resolution = 1)
    
    #run dcitimestep (for each room)
    for i in range(len(info.approved_rooms)):
        run_dctimestep_day(info, i)
    
    #run rmtxop (for each room)
    for i in range(len(info.approved_rooms)):
        run_rmtxop_day(info, i)
    
    #annual metrics (for each room)
    calc_da(info)