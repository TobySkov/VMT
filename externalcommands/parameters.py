"""Description."""

def rtrace_parameters(complexity):
	#Important to implement lw
	if complexity == 0:
		rtrace_cmd = ["-aa", "0.25", "-ab 3", "-ad", "1000", "-ar", "16"] 

	elif complexity == 1:
		rtrace_cmd = ["-aa", "0.2", "-ab 5", "-ad", "5000", "-ar", "64"] 
				
	elif complexity == 2:
		rtrace_cmd = ["-aa", "0.1", "-ab 7", "-ad", "20000", "-ar", "128"] 

	else:
		raise Exception("""Unknown input for variable: complexity
				  Options are: (0, 1, 2)""")
	
	return rtrace_cmd