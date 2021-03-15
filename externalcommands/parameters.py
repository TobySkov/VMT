"""Description."""

def rtrace_parameters(resolution):
	##Most important Radiance parameters:
    #   https://unmethours.com/question/40179/radiance-convergence-simulation-parameters/
    
    ##https://www.radiance-online.org/learning/tutorials/matrix-based-methods
    # page 41 example only using lw, ab and ad
    
    ##Discourse: lw = 1/ad or lower
    #https://discourse.ladybug.tools/t/5-phase-method-simulation-times/2891/6
    if resolution == -1:
        rtrace_cmd = ["-ab", "1"]
    
    #From HB+ for RADIATION
    elif resolution == 0:
        rtrace_cmd = ["-ab", "3", "-ad", "5000", "-lw", f"{1/5000}"]
    		#rtrace_cmd = ["-aa", "0.25", "-ab 3", "-ad", "1000", "-ar", "16"] 
    
    elif resolution == 1:
        rtrace_cmd = ["-ab", "5", "-ad", "15000", "-lw", f"{1/15000}"]
    		#rtrace_cmd = ["-aa", "0.2", "-ab 5", "-ad", "5000", "-ar", "64"] 
    				
    elif resolution == 2:
        rtrace_cmd = ["-ab", "7", "-ad", "25000", "-lw", f"{1/(25000**2)}", 
                      "-ar", "128", "-aa", "0.1", "-as", "4096"]
    		#rtrace_cmd = ["-aa", "0.1", "-ab 7", "-ad", "20000", "-ar", "128"] 
    
    else:
        raise Exception("""Unknown input for variable: complexity
    				  Options are: (0, 1, 2)""")
	
    return rtrace_cmd