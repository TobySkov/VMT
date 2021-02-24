"""Description."""


from externalcommands.radiancecommands import run_epw2wea, run_gendaymtx, \
                            run_rfluxmtx_radiation, run_dctimestep, \
                            run_rmtxop

from geometry.radiationgrid import radiation_mesh_grid

from postprocessing.radiationanalysispostprocess import radiation_post_processing




def radiationanalysis_radiance(info):

    #epw2wea
    run_epw2wea(info)
    
    #wea2smx, only using resolution = 1 (145 patches)
    #Since it is a radiation study this is full spektrum
    run_gendaymtx(info,
				  spektrum = "full spektrum", 
				  sky_resolution = 1)
    
    #Create grid for at volume massing
    radiation_mesh_grid(info)
    
    #create dmx
    run_rfluxmtx_radiation(info)
    
    #Dctimestep matrix multiplikation in all three channels
    run_dctimestep(info, simulation_type = "RADIATION_ANALYSIS")
    
    #Combining the three channels into one
    run_rmtxop(info, simulation_type = "RADIATION_ANALYSIS")

    #Calculating cummulative result
    radiation_post_processing(info)


    
def radiationanalysis_accelerad():
    pass