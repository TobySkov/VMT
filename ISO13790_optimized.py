"""
Description:

"""

import time 
import numpy as np


#%%

def ventilation():
    pass
    #return H__ve


#%% Calculated twice before runtime
def before_runtime(H__ve,
                   H__tr_is, H__tr_w, H__tr_ms, H__tr_em,
                   A__m, A__t, C__m):
    
    #The function should be called two times, once for each value of H__ve

    #Equations: (C.6), (C.7), (C.8)
    H__tr_1 = 1/(1/(H__ve) + 1/(H__tr_is))
    H__tr_2 = H__tr_1 + H__tr_w
    H__tr_3 = 1/(1/(H__tr_2) + 1/(H__tr_ms))


    tmp0 = A__m/A__t
    tmp1 = H__tr_w/(9.1*A__t)
    tmp2 = H__tr_3/H__tr_2
    tmp3 = 1/H__ve
    
    
    local_tmp = C__m/3600
    local_tmp2 = 0.5*(H__tr_3 + H__tr_em)
    tmp4 = local_tmp - local_tmp2
    tmp5 = 1/(local_tmp + local_tmp2)
    
    tmp6 = 1/(H__tr_ms + H__tr_w + H__tr_1)
    tmp7 = 1/(H__tr_is + H__ve)

    tmp8 = H__tr_1
    
    params = [tmp0,
              tmp1,
              tmp2,
              tmp3,
              tmp4,
              tmp5,
              tmp6,
              tmp7,
              tmp8]

    return params



#%%

def at_runtime(Phi__int, Phi__sol, Phi__HC_nd, 
               theta__e, theta__sup, theta__m_tm1,
               H__tr_em, H__tr_w, H__tr_ms, H__ve, 
               H__tr_is, params):
    

    #ISO 13790
    #Equations: (C.1), (C.2), (C.3)
    Phi__ia = 0.5*Phi__int
    Phi__m = params[0]*(0.5*Phi__int + Phi__sol)
    Phi__st = (1 - params[0]- params[1])*(0.5*Phi__int + Phi__sol)
    

    #ISO 13790
    #Equations: (C.4), (C.5)
    local_tmp = Phi__st + H__tr_w*theta__e + \
        params[8]*(params[3]*(Phi__ia + Phi__HC_nd) + theta__sup)
        
    Phi__mtot = Phi__m + H__tr_em*theta__e + \
        params[2]*local_tmp
        
    theta__m_t = (theta__m_tm1*params[4] - Phi__mtot)*params[5]


    #ISO 13790
    #Equations: (C.9), (C.10), (C.11)
    theta__m = 0.5*(theta__m_t + theta__m_tm1)
    
    theta__s = (H__tr_ms*theta__m + local_tmp)*params[6]
    
    theta__air = (H__tr_is*theta__s + H__ve*theta__sup + \
                  Phi__ia + Phi__HC_nd)*params[7]
    
    return theta__m_t, theta__m, theta__s, theta__air





#%%

def run_sim():
    
    #Define constant parameters (stay the same throught simulation period)
    H__tr_em = 2.5
    H__tr_is = 20.5
    H__tr_w = 2.5
    H__tr_ms = 20.5
    A__f = 25
    C__m = 165000*A__f
    A__m = 2.5*A__f
    A__t = 4.5*A__f
    
    setpoint_cooling = 24
    setpoint_heating = 20
    

    #Establishing ventilation
    H__ve = 1
    params__wo_vent = before_runtime(H__ve,
                                     H__tr_is, H__tr_w, H__tr_ms, H__tr_em,
                                     A__m, A__t, C__m)
    
    H__ve = 2
    params__w_vent = before_runtime(H__ve,
                                     H__tr_is, H__tr_w, H__tr_ms, H__tr_em,
                                     A__m, A__t, C__m)
    
    
    theta__m_tm1 = 22 #Initial value

    #Warming up
    #while(warmup):
    #    pass
    theta__air_list = np.zeros((8760))
    #Running for entire year
    for i in range(8760):

        
        #Select ventaltion case:
        if i%2 == 0:
            H__ve = 1
            params = params__wo_vent
        else:
            H__ve = 2
            params = params__w_vent

        Phi__int = 0
        Phi__sol = 0
        theta__e = 10
        theta__sup = 10
        
        
        #Free floating condiation
        Phi__HC_nd_0 = 0
        
        theta__m_t_0, theta__m_0, theta__s_0, theta__air_0 = \
            at_runtime(Phi__int, Phi__sol, Phi__HC_nd_0, 
                       theta__e, theta__sup, theta__m_tm1,
                       H__tr_em, H__tr_w, H__tr_ms, H__ve, 
                       H__tr_is, params)
        
        
        #Check free floating condiation
        if (setpoint_heating <= theta__air_0) and \
            (theta__air_0 <= setpoint_cooling):
                
                theta__air_list[i] = theta__air_0
                theta__m_tm1 = theta__m_t_0
                
        else:
            #Trying heating of 10 W/m2
            Phi__HC_nd_10 = 10*A__f
            
            theta__m_t_10, theta__m_10, theta__s_10, theta__air_10 = \
            at_runtime(Phi__int, Phi__sol, Phi__HC_nd_10, 
                       theta__e, theta__sup, theta__m_tm1,
                       H__tr_em, H__tr_w, H__tr_ms, H__ve, 
                       H__tr_is, params)
            
            
            if (theta__air_0 < setpoint_heating):
                theta__air_set = setpoint_heating
                
            elif (setpoint_cooling < theta__air_0):
                theta__air_set = setpoint_cooling
                
            Phi__HC_nd = Phi__HC_nd_10*((theta__air_set - \
                                         theta__air_0)/(theta__air_10 - \
                                                        theta__air_0))
        
                                                        
            #Calculation with correct heating and cooling
            theta__m_t, theta__m, theta__s, theta__air = \
            at_runtime(Phi__int, Phi__sol, Phi__HC_nd, 
                       theta__e, theta__sup, theta__m_tm1,
                       H__tr_em, H__tr_w, H__tr_ms, H__ve, 
                       H__tr_is, params)
        
            theta__air_list[i] = theta__air
            theta__m_tm1 = theta__m_t
        
    return theta__air_list
    
#%%

if __name__ == "__main__":
    start = time.time()
    theta__air_list = run_sim()
    end = time.time()
    duration = (end - start)*10**(6)


