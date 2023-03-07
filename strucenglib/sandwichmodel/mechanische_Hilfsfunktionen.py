import mathematische_Hilfsfunktionen as mH
#----------------------------------------------------------------------------------------------------------------------------------
#mechansiche Hilfsfunktionen
#----------------------------------------------------------------------------------------------------------------------------------
#In this file functions are defined which have no norm dependency

# Spannungstransformation Mohrkreis (rotation)
def s_xi(s_x,s_y,s_xy,a):
    s_xi = s_x*mH.cos(a)**2+s_y*mH.sin(a)**2+2*s_xy*mH.sin(a)*mH.cos(a)
    return s_xi

def s_eta(s_x,s_y,s_xy,a):
    s_eta = s_x*mH.sin(a)**2+s_y*mH.cos(a)**2-2*s_xy*mH.sin(a)*mH.cos(a)
    return s_eta

def s_xieta(s_x,s_y,s_xy,a):
    s_xieta = (s_y-s_x)*mH.sin(a)*mH.cos(a)+s_xy*(mH.cos(a)**2-mH.sin(a)**2)
    return s_xieta


# relative longitudinal reinforcement
def rho(s,psi,kk,s_xieta,fs_d):
    rhox = max((s/mH.sin(psi)+kk*abs(s_xieta/mH.sin(psi)))/fs_d , 0)  
    return rhox

# absolute longitudinal reinforcement
def a_s(rhox,t):
    as_i = rhox*t*1000
    return as_i


# minimal relative longitudinal reinforcement
def rho_min(fct_m, fs_d):
    rho_min = fct_m / fs_d
    return rho_min

"""
# Theta in cover (not in use)
def theta(k, psi, s_xieta, alpha):
    if s_xieta >= 0:
       theta = mH.arccot((k-mH.cos(psi))/mH.sin(psi))-alpha
    elif s_xieta < 0:
        theta = mH.arccot((-k-mH.cos(psi))/mH.sin(psi))-alpha
    
    while theta < 0:
        if theta < 0:
            theta +=180
    
    return theta

"""