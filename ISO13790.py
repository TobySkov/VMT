"""
Description:

"""

import time 
import numpy as np

#%%

def heat_transfer_coef(H__ve,  H__tr_is, H__tr_w, H__tr_ms):
    
    #ISO 13790
    #Equations: (C.6), (C.7), (C.8)
    
    H__tr_1 = 1/(1/(H__ve) + 1/(H__tr_is))
    H__tr_2 = H__tr_1 + H__tr_w
    H__tr_3 = 1/(1/(H__tr_2) + 1/(H__tr_ms))
    
    return H__tr_1, H__tr_2, H__tr_3



#%%

def heat_gains(Phi__int, Phi__sol, A__m, A__t, H__tr_w):
    
    #ISO 13790
    #Equations: (C.1), (C.2), (C.3)
    
    Phi__ia = 0.5*Phi__int
    Phi__m = (A__m/A__t)*(0.5*Phi__int + Phi__sol)
    Phi__st = (1-(A__m/A__t)-H__tr_w/(9.1*A__t))*(0.5*Phi__int + Phi__sol)
    
    return Phi__ia, Phi__m, Phi__st


#%% 

def ventilation():
    pass
    #return H__ve


#%%

def average_tempterature_equations(theta__m_t, theta__m_tm1, 
                           theta__e,  theta__sup,
                           Phi__st, Phi__ia,Phi__HC_nd,
                           H__tr_w,  H__tr_ms, H__tr_1, H__ve, H__tr_is):
    
    #ISO 13790
    #Equations: (C.9), (C.10), (C.11)
    
    
    theta__m = 0.5*(theta__m_t + theta__m_tm1)
    
    theta__s = (H__tr_ms*theta__m + Phi__st + H__tr_w*theta__e + \
                H__tr_1*(theta__sup + \
                (Phi__ia + Phi__HC_nd)/H__ve))/(H__tr_ms + H__tr_w + \
                + H__tr_1)
    
    theta__air = (H__tr_is*theta__s + H__ve*theta__sup + Phi__ia + \
        Phi__HC_nd)/(H__tr_is + H__ve)
    
    return theta__m, theta__s, theta__air


#%%

def pit_temperautre_equations(Phi__m, Phi__st, Phi__ia, Phi__HC_nd, 
                              H__tr_em, H__tr_3, H__tr_w, H__tr_1, 
                              H__ve, H__tr_2, 
                              theta__e, theta__sup, theta__m_tm1, C__m):
    
    #ISO 13790
    #Equations: (C.4), (C.5)
    
    Phi__mtot = Phi__m + H__tr_em*theta__e + \
        H__tr_3*((Phi__st + H__tr_w*theta__e + H__tr_1 * (theta__sup + \
        (Phi__ia + Phi__HC_nd)/(H__ve)))/(H__tr_2))
    
    theta__m_t = (theta__m_tm1*(C__m/3600 - (0.5*(H__tr_3 + H__tr_em))) \
                  + Phi__mtot)/(C__m/3600 + (0.5*(H__tr_3 + H__tr_em)))
    
    return theta__m_t

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
    

    
    theta__m_tm1 = 22 #Initial value

    #Warming up
    #while(warmup):
    #    pass
    theta__air_list = np.zeros((8760))
    #Running for entire year
    for i in range(8760):

        Phi__int = 0
        Phi__sol = 0
        theta__e = 10
        theta__sup = 10
        
        #Internal gains
        Phi__ia, Phi__m, Phi__st = \
            heat_gains(Phi__int, Phi__sol, A__m, A__t, H__tr_w)
            
        #Ventilation/infiltration
        H__ve = 2.5
        
        #Heat transfer coefficients
        H__tr_1, H__tr_2, H__tr_3 = \
            heat_transfer_coef(H__ve,  H__tr_is, H__tr_w, H__tr_ms)
        
        
        Phi__HC_nd = 0
        
        theta__m_t_0 = \
            pit_temperautre_equations(Phi__m, Phi__st, Phi__ia, Phi__HC_nd, 
                              H__tr_em, H__tr_3, H__tr_w, H__tr_1, 
                              H__ve, H__tr_2, 
                              theta__e, theta__sup, theta__m_tm1, C__m)
            
        theta__m_0, theta__s_0, theta__air_0 = \
            average_tempterature_equations(theta__m_t_0, theta__m_tm1, 
                           theta__e,  theta__sup,
                           Phi__st, Phi__ia,Phi__HC_nd,
                           H__tr_w,  H__tr_ms, H__tr_1, H__ve, H__tr_is)
        
        
        #Free floating condiation
        if (setpoint_heating <= theta__air_0) and \
            (theta__air_0 <= setpoint_cooling):
                
                theta__air_list[i] = theta__air_0
                theta__m_tm1 = theta__m_t_0
                
        else:
            #Trying heating of 10 W/m2
            Phi__HC_nd_10 = 10*A__f
            
            theta__m_t_10 = \
            pit_temperautre_equations(Phi__m, Phi__st, Phi__ia, Phi__HC_nd_10, 
                              H__tr_em, H__tr_3, H__tr_w, H__tr_1, 
                              H__ve, H__tr_2, 
                              theta__e, theta__sup, theta__m_tm1, C__m)
            
            theta__m_10, theta__s_10, theta__air_10 = \
            average_tempterature_equations(theta__m_t_10, theta__m_tm1, 
                           theta__e,  theta__sup,
                           Phi__st, Phi__ia, Phi__HC_nd_10,
                           H__tr_w,  H__tr_ms, H__tr_1, H__ve, H__tr_is)
            
            if (theta__air_0 < setpoint_heating):
                theta__air_set = setpoint_heating
                
            elif (setpoint_cooling < theta__air_0):
                theta__air_set = setpoint_cooling
                
            Phi__HC_nd = Phi__HC_nd_10*((theta__air_set - \
                                         theta__air_0)/(theta__air_10 - \
                                                        theta__air_0))
        
                                                        
            #Calculation with correct heating and cooling
            theta__m_t = \
            pit_temperautre_equations(Phi__m, Phi__st, Phi__ia, Phi__HC_nd, 
                              H__tr_em, H__tr_3, H__tr_w, H__tr_1, 
                              H__ve, H__tr_2, 
                              theta__e, theta__sup, theta__m_tm1, C__m)
            
            theta__m, theta__s, theta__air = \
            average_tempterature_equations(theta__m_t, theta__m_tm1, 
                           theta__e,  theta__sup,
                           Phi__st, Phi__ia, Phi__HC_nd,
                           H__tr_w,  H__tr_ms, H__tr_1, H__ve, H__tr_is)
        
            theta__air_list[i] = theta__air
            theta__m_tm1 = theta__m_t
        
    return theta__air_list
    
#%%

if __name__ == "__main__":
    start = time.time()
    theta__air_list = run_sim()
    end = time.time()
    duration = (end - start)*10**(6)


