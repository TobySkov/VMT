"""Description."""


from externalcommands.radiancecommands import run_epw2wea, run_gendaymtx, \
    run_rfluxmtx_radiation, run_dctimestep, run_rmtxop
    
from geometry.radiationgrid import gen_pts_and_sub_mesh

from postprocessing.radiationanalysispostprocess import radiation_post_processing

from clustering.kmeans import kmeans_clustering

def radiationanalysis_radiance(path_mananger_pd):
    """
    #epw2wea
    run_epw2wea(path_mananger_pd)
    
    #wea2smx
    run_gendaymtx(path_mananger_pd,
				  spektrum = "full spektrum",
				  resolution = 1)
    
    """
    #Create grid for at volume massing
    out = gen_pts_and_sub_mesh(path_mananger_pd,
                               x_dim = 1,
                               y_dim = 1,
                               offset = 0.01)
    
    no_of_sensor_points_total = out[6]
    no_of_sensor_points_list = out[7]
    """
    #create dmx
    #   run for each surface of the volume massing
    run_rfluxmtx_radiation(path_mananger_pd,
                           no_of_sensor_points_total)
    

    run_dctimestep(path_mananger_pd,
              simulation_type = "RADIATION_ANALYSIS")
    
    run_rmtxop(path_mananger_pd,
        simulation_type = "RADIATION_ANALYSIS")

    
    radiation_post_processing(path_mananger_pd,
                              no_of_sensor_points_list)
    """
    kmeans_clustering(path_mananger_pd,
                      no_of_sensor_points_list,
                      n_clusters = 3)
    
def radiationanalysis_accelerad():
    pass