"""Description."""


from externalcommands.radiancecommands import run_epw2wea, run_gendaymtx, \
    run_rfluxmtx_radiation
    
from geometry.radiationgrid import gen_pts_and_sub_mesh


def radiationanalysis_radiance(path_mananger_pd):
    
    #epw2wea
    run_epw2wea(path_mananger_pd)
    
    #wea2smx
    run_gendaymtx(path_mananger_pd,
				  spektrum = "full spektrum",
				  resolution = 1)
    
    
    #Create grid for at volume massing
    out = gen_pts_and_sub_mesh(path_mananger_pd,
                               x_dim = 4,
                               y_dim = 4,
                               offset = 0.01)
    
    no_of_sensor_points_total = out[6]
    
    #create dmx
    #   run for each surface of the volume massing
    run_rfluxmtx_radiation(path_mananger_pd,
                           no_of_sensor_points_total)
    



def radiationanalysis_accelerad():
    pass