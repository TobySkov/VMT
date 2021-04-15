"""
Description:

"""

import time 
import numpy as np

#%%

def heat_transfer_coef(H__ve, tmp2 ,H__tr_w, tmp3):
    
    #ISO 13790
    #Equations: (C.6), (C.7), (C.8)
    
    #tmp2 = 1/(H__tr_is)
    #tmp3 = 1/(H__tr_ms)
    
    H__tr_1 = 1/(1/(H__ve) + tmp2)
    H__tr_2 = H__tr_1 + H__tr_w
    H__tr_3 = 1/(1/(H__tr_2) + tmp3)
    
    return H__tr_1, H__tr_2, H__tr_3



#%%

def heat_gains(Phi__int, Phi__sol, tmp4, A__t, H__tr_w):
    
    #ISO 13790
    #Equations: (C.1), (C.2), (C.3)
    
    l_tmp1 = 0.5*Phi__int
    l_tmp3 = (l_tmp1+Phi__sol)
    
    Phi__ia = l_tmp1
    Phi__m = tmp4*l_tmp3
    Phi__st = (1-tmp4-H__tr_w/(9.1*A__t))*l_tmp3
    
    return Phi__ia, Phi__m, Phi__st


#%% 

def ventilation():
    pass
    #return H__ve


#%%

def average_tempterature_equations(theta__m_t, theta__m_tm1, 
                           theta__e,  theta__sup,
                           Phi__st, Phi__ia,Phi__HC_nd,
                           H__tr_w,  H__tr_ms, H__tr_1, H__ve, H__tr_is,
                           tmp5):
    
    #ISO 13790
    #Equations: (C.9), (C.10), (C.11)
    
    
    theta__m = 0.5*(theta__m_t + theta__m_tm1)
    
    theta__s = (H__tr_ms*theta__m + Phi__st + H__tr_w*theta__e + \
                H__tr_1*(theta__sup + (Phi__ia+Phi__HC_nd)/H__ve))/(tmp5 + \
                + H__tr_1)
    
    theta__air = (H__tr_is*theta__s + H__ve*theta__sup + Phi__ia + \
        Phi__HC_nd)/(H__tr_is + H__ve)
    
    return theta__m, theta__s, theta__air


#%%

def pit_temperautre_equations(Phi__m, Phi_st, Phi__ia, Phi__HC_nd, 
                              H__tr_em, H__tr_3, H__tr_w, H__tr_1, 
                              H__ve, H__tr_2, 
                              theta__e, theta__sup, theta__m_tm1,
                              tmp1):
    
    #ISO 13790
    #Equations: (C.4), (C.5)
    l_tmp1 = 0.5*(H__tr_3 + H__tr_em)
    
    Phi__mtot = Phi__m + H__tr_em*theta__e + \
        H__tr_3*((Phi_st + H__tr_w*theta__e + H__tr_1 * (theta__sup + \
        (Phi__ia + Phi__HC_nd)/(H__ve)))/(H__tr_2))
    
    theta__m_t = (theta__m_tm1*(tmp1 - l_tmp1) \
                  + Phi__mtot)/(tmp1 + l_tmp1)
    
    return theta__m_t

#%%

def run_sim():
    
    #Define constant parameters (stay the same throught simulation period)
    H__tr_em = 2.5
    H__tr_is = 2.5
    H__tr_w = 2.5
    H__tr_ms = 2.5
    H__tr_w = 2.5
    A__f = 25
    C__m = 165000*A__f
    A__m = 2.5*A__f
    A__t = 4.5*A__f
    
    #Assign tmp constant parameters (the same computations that would 
    #   otherwise have been done again and again)
    tmp1 = C__m/3600
    tmp2 = 1/(H__tr_is)
    tmp3 = 1/(H__tr_ms)
    tmp4 = A__m/A__t
    tmp5 = H__tr_ms + H__tr_w

    
    theta__m_tm1 = -10 #Initial value

    #Warming up
    #while(warmup):
    #    pass
    theta__air__list = np.zeros((8760))
    #Running for entire year
    for i in range(8760):
        
        
        Phi__int = 20
        Phi__sol = 100
        theta__e = 10
        theta__sup = 16
        
        #Internal gains
        Phi__ia, Phi__m, Phi__st = \
            heat_gains(Phi__int, Phi__sol, tmp4, A__t, H__tr_w)
            
        #Ventilation/infiltration
        H__ve = 2.5
        
        #Heat transfer coefficients
        H__tr_1, H__tr_2, H__tr_3 = \
            heat_transfer_coef(H__ve, tmp2 ,H__tr_w, tmp3)
        
        
        Phi__HC_nd = 0
        
        theta__m_t_0 = \
            pit_temperautre_equations(Phi__m, Phi__st, Phi__ia, Phi__HC_nd, 
                              H__tr_em, H__tr_3, H__tr_w, H__tr_1, 
                              H__ve, H__tr_2, 
                              theta__e, theta__sup, theta__m_tm1,
                              tmp1)
            
        theta__m, theta__s, theta__air_0 = \
            average_tempterature_equations(theta__m_t_0, theta__m_tm1, 
                           theta__e,  theta__sup,
                           Phi__st, Phi__ia,Phi__HC_nd,
                           H__tr_w,  H__tr_ms, H__tr_1, H__ve, H__tr_is,
                           tmp5)
        
        
        #Free floating condiation
        if (setpoint_heating <= theta__air_0) and \
            (theta__air_0 <= setpoint_cooling):
                theta__air__list[i] = theta__air
                theta__m_tm1 = theta__m_t
                
        else:
            Phi__HC_nd = 10*A__f
            
            theta__m_t_10 = \
            pit_temperautre_equations(Phi__m, Phi__st, Phi__ia, Phi__HC_nd, 
                              H__tr_em, H__tr_3, H__tr_w, H__tr_1, 
                              H__ve, H__tr_2, 
                              theta__e, theta__sup, theta__m_tm1,
                              tmp1)
            
            theta__m, theta__s, theta__air_10 = \
            average_tempterature_equations(theta__m_t_10, theta__m_tm1, 
                           theta__e,  theta__sup,
                           Phi__st, Phi__ia,Phi__HC_nd,
                           H__tr_w,  H__tr_ms, H__tr_1, H__ve, H__tr_is,
                           tmp5)
            
            Phi__HC_nd = 
        
        
        
        
    return theta__air__list
    
#%%

if __name__ == "__main__":
    start = time.time()
    theta__air__list = run_sim()
    end = time.time()
    duration = end - start


