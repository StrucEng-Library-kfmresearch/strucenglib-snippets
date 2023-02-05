import math


#----------------------------------------------------------------------------------------------------------------------------------
#Genormte Hilfsfunktionen
#----------------------------------------------------------------------------------------------------------------------------------

#In diesem Modul sind normabhaengige Funktionen definiert:

# GRUNDWERTE
#General values
gamma_c = 1.5                                     # Sicherheitsbeiwert Beton SIA & EC1.5                                     # Sicherheitsbeiwert Beton SIA & EC
E_s = 205000                        #[N/mm2]        E-Modul Stahl
D_max = 32                          #[mm]           Durchmesser des Groesstkorn

#sia related values
eta_t = 1.0                                       # SIA 262 4.2.1.3

#EC related values
a_cc = 1.0                                        # EN 1992-1-1:2004 3.1.6.1 is a coefficient taking account of long term effects on the tensile strength and of unfavourable effects, resulting from the way the load is applied.
#a_ct = 1.0                                        # EN 1992-1-1:2004 3.1.6.2
 
# FUNCTIONS
# Bemessungswert der Betondruckfestigkeit fcd
def fc_d(fc_k,code):
    if code == "sia":
        eta_fc = min((30.0/fc_k)**(1.0/3.0) , 1.0)                    # SIA 262 4.2.1.2
        fc_d = fc_k*eta_fc*eta_t/gamma_c  #[N/mm2]              SIA 262 2.3.2.3 Druckfestigkeit Beton 
        return fc_d
    elif code == "EC":
        fc_d = a_cc * fc_k/gamma_c                              # EN 1992-1-1:2004 3.1.6.1
        return fc_d
    else:
        raise ValueError("code is not defined")

# Mittelwert der Betonzugfestigkeit fctm
def fct_m(fc_k,code):
    if code == "sia" or "EC":                                #Tabelle in sia hat gleiche Werte wie EuroCode deshalb hier EN 1992-1-1:2004 Table 3.1 uebernommen
        if fc_k <= 50.0:
            #fct_m = 0.3*fc_k**(2/3)                          #EN 1992-1-1:2004 Table 3.1
            fct_m = fc_k**(2.0/3.0)*0.3
        elif fc_k >50.0:
            fct_m = 2.12*math.log(1.0+(fc_k+8.0)/10.0)           
        return fct_m
    else:
        raise ValueError("code is not defined")

# Bemessungswert der Schubspannungsgrenze tau_nom
def tau_nom(fc_k, code):
    if code == "sia" or "EC":
        tau_nom = 0.3*fc_k**0.5/gamma_c       #[N/mm2]        Grenzfestigkeit Tau_nom SIA 262 2.3.2.4
        return tau_nom
    else:
        raise ValueError("code is not defined")

# Bemessungswert des Queerkraftwiderstands VRd
def vrd(fc_k, fs_d, d, code):
    if code == "sia":
        tau_nom = 0.3*eta_t*fc_k**0.5/gamma_c    
        e_v = 1.5*fs_d/E_s
        if fc_k > 70.0:
            k_g = 48.0/(16.0+0.0)
        else:
            k_g = 48.0/(16.0+D_max)
        k_d = 1/(1+e_v*d*k_g)
        vrd = k_d*tau_nom*d
        return vrd
    if code == "EC":
        raise ValueError("VRD for EC is not implemented")
    else:
        raise ValueError("code is not defined")


# Beiwert zur Bestimmung der Betonfestigkeit 
def kc(Fall,code,fc_k):
    
    if code == "sia":                                       # SIA 262 4.2.1.7
        if Fall == 1 or Fall == 2 or Fall ==4:
            kc = 0.55
            return kc
        elif Fall == 3:
            kc = 1.0
            return kc
    elif code == "EC":                                      # EN 1992-1-1:2004 6.5.2
        if Fall == 1 or Fall == 2 or Fall ==4:
            v_strich = 1.0-fc_k/250.0
            kc = 0.6*v_strich
            return kc
        elif Fall == 3:
            kc = 1.0
            return kc
        else:
            raise ValueError("code is not defined")


