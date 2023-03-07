import mechanische_Hilfsfunktionen as mechH
import mathematische_Hilfsfunktionen as mH
import genormte_Funktionen as norm

#----------------------------------------------------------------------------------------------------------------------------------
#Implementiertes Sandwichmodel
#----------------------------------------------------------------------------------------------------------------------------------

def Sandwichmodel(inp):
    """
    ----------------------------------------
    Parameters
    ----------------------------------------
    i : int
        Elementnummer

    mx : int
        mx in Nmm/mm

    my : int
        my in Nmm/mm

    mxy : int
        mxy in Nmm/mm

    vx : int
        vx in N/mm

    vy : int
        vy in N/mm

    nx : int
        nx in N/mm

    ny : int
        ny in N/mm

    nxy : int
        nxy in N/mm

    h : int
        Dicke des Elements in mm

    d_strich_bot : int
        Distanz zwischen Unterkante Element und Schwerpunkt beider unteren Bewehrungslagen in mm

    d_strich_top : int
        Distanz zwischen Oberkante Element und Schwerpunkt beider oberen Bewehrungslagen in mm

    fc_k : int
        Zylinderdruckfestigkeit Beton charakteristisch in N/mm2

    theta_grad_kern : int
        Neigung Druckfeld im Kern SIA & EC in Grad

    alpha_bot : int
        Neigung der ersten unteren Deckelbewehrung zur lokalen x-achse in Grad

    alpha_top : int
        Neigung der ersten oberen Deckelbewehrung zur lokalen x-achse in Grad

    beta_bot : int
        Neigung der zweiten unteren Deckelbewehrung zur lokalen x-achse in Grad

    beta_top : int
        Neigung der zweiten oberen Deckelbewehrung zur lokalen x-achse in Grad

    Mindestbewehrung : bool
        Mindestbewehrung beruecksichtigen?

    Druckzoneniteration : bool
        Druckzonenhoehe iterieren?

    Schubnachweis : str
        definiert ob der Schubnachweis nach sia ('sia') oder nach dem vereinfachten Verfahren ('vereinfacht') gefuehrt werden soll.
    
    code : str
        definiert ob die Betonbemessungswerte nach sia ('sia') oder Eurocode ('EC') berechnet werden sollen
    
    """
    [i,mx,my,mxy,vx,vy,v0,nx,ny,nxy,h,d_strich_bot,d_strich_top,fc_k,theta_grad_kern,fs_d, alpha_bot, alpha_top, beta_bot, beta_top, Mindestbewehrung, Druckzoneniteration, Schubnachweis, code, xyz, ex,ey,ez]=inp
    #code = ini.code
    theta_core=mH.angle_check(theta_grad_kern)
    alpha = [alpha_bot , alpha_top]
    psi=[mH.angle_check(beta_bot-alpha_bot) , mH.angle_check(beta_top-alpha_top)]
    fc_d = norm.fc_d(fc_k,code)
    fct_m = norm.fct_m(fc_k,code)
    tau_nom = norm.tau_nom(fc_k,code)

    # Startwerte:
    delta_druck = 0.01*h # Annahme
    t = [2.0*d_strich_bot, 2.0*d_strich_top]  #[mm]
    dv = h-t[0]/2.0-t[1]/2.0 #[mm]                                    
    cc = [1,1]
    m_cc = [0,0]
    #k = [abs(mH.cos(psi[0])+mH.sin(psi[0])*mH.cot(theta)),abs(mH.cos(psi[1])+mH.sin(psi[1])*mH.cot(theta))]
    k = [1,1]
    as_xi=[None , None]
    as_eta = [None , None]
    fall = [None , None]
    #theta_cover = [None , None]

    # globale xi, eta Koordinaten

    e_xi_bot = mH.e_xi(ex,ey,ez, alpha_bot)
    e_xi_top = mH.e_xi(ex,ey,ez, alpha_top)
    e_eta_bot = mH.e_xi(ex,ey,ez, beta_bot)
    e_eta_top = mH.e_xi(ex,ey,ez, beta_top)
    



 
    while cc[0] == 1 or cc[1] == 1:
        
        #Querkraftbewehrung,  Schubnachweis
        
        if Schubnachweis == 'vereinfacht':            
            if (h>=400 or v0/dv>tau_nom) and v0!=0:                 
                rho_z = v0/(fs_d*dv*mH.cot(theta_core))           #[-]
                as_z = rho_z*1000*1000#[mm2/m2]                                 #[mm^2/m2] 
                shearcrack = 1                                              #Beton gerissen, Schubbewehrung erforderlich
            else:     
                rho_z = 0                                                    #[-]
                as_z = 0                                                     #[mm^2/m2]
                shearcrack = 0                                               #Beton ungerissen, keine Schubbewehrung erforderlich

            m_shear_c = v0/(tau_nom*dv)                                         # Ausnutzungsgrad des Betons bezueglich Querkraft
        
        elif Schubnachweis == 'sia':

            d = min(h-d_strich_bot, h-d_strich_top)#? oder dv

            if v0 > norm.vrd(fc_k, fs_d, d, 'sia'):
                z = 0.9*d #sia 262 4.3.3.4.2 oder dv?
                rho_z = v0/(z*fs_d*mH.cot(theta_core))
                as_z = rho_z*1000*1000#[mm2/m2] 
                shearcrack = 1
            else:     
                rho_z = 0                                                    #[-]
                as_z = 0                                                     #[mm^2/m2]
                shearcrack = 0
            
            m_shear_c = v0/norm.vrd(fc_k, fs_d, d, 'sia')                     # Ausnutzungsgrad des Betons bezueglich Querkraft
        else: 
            raise ValueError("Schubnachweis is not defined")
        



        # Membrankraefte Schubanteil
        if shearcrack == 1:
            v_x_Term = vx**2.0*mH.cot(theta_core)/(2*v0)                  #[N/mm]
            v_y_Term = vy**2.0*mH.cot(theta_core)/(2*v0)                    #[N/mm]
            v_xy_Term = vx*vy*mH.cot(theta_core)/(2*v0)                  #[N/mm]
        elif shearcrack == 0:
            v_x_Term = 0                                                 #[N/mm]
            v_y_Term = 0                                                  #[N/mm]
            v_xy_Term = 0                                                    #[N/mm]
   
        # Membranspannungen [unterer Deckel , oberer Deckel] 
        s_x = [(nx/2+mx/dv+v_x_Term)/t[0] , (nx/2-mx/dv+v_x_Term)/t[1]]                #[N/mm2]
        s_y = [(ny/2+my/dv+v_y_Term)/t[0] , (ny/2-my/dv+v_y_Term)/t[1]]                #[N/mm2]
        s_xy = [(nxy/2+mxy/dv+v_xy_Term)/t[0] , (nxy/2-mxy/dv+v_xy_Term)/t[1]]         #[N/mm2]

        ii=0
        while ii<2:
            # Rotation der Membranspannungen, in x_stern - y_stern Koordinatensystem
            s_x_stern = mechH.s_xi(s_x[ii],s_y[ii],s_xy[ii],alpha[ii])
            s_y_stern = mechH.s_eta(s_x[ii],s_y[ii],s_xy[ii],alpha[ii])
            s_xy_stern = mechH.s_xieta(s_x[ii],s_y[ii],s_xy[ii],alpha[ii])    

            #Transformation in schiefe Spannungskomponenten, xi - eta Koordinatensystem
            s_xi = s_x_stern*mH.sin(psi[ii])+s_y_stern*mH.cos(psi[ii])*mH.cot(psi[ii])-2*s_xy_stern*mH.cos(psi[ii])            
            s_eta = s_y_stern/mH.sin(psi[ii]) 
            s_xieta = s_xy_stern-s_y_stern*mH.cot(psi[ii])
            
            #Fallunterschiedung mit k=start
             
            f_xi = round((s_xi/mH.sin(psi[ii])+k[ii]*abs(s_xieta/mH.sin(psi[ii])))/fs_d,5)
            f_eta = round((s_eta/mH.sin(psi[ii])+1/k[ii]*abs(s_xieta/mH.sin(psi[ii])))/fs_d,5)
                 
            if f_xi > 0 and f_eta <= 0: #Fall1 xi Zug, eta Druck
                fall[ii] = 1
                if round(s_eta,5) !=0:              
                    k[ii] = -abs(s_xieta)/s_eta
                    if k[ii] == 0:
                        k[ii] = 1 
                #kc = 0.55

            elif f_xi <= 0 and f_eta > 0: #Fall2 xi Druck, eta Zug
                fall[ii] = 2
                if round(s_xieta,5) !=0:              
                    k[ii] = -s_xi/abs(s_xieta)
                    if k[ii] == 0:
                        k[ii] = 1 
                #kc = 0.55

            elif f_xi <= 0 and f_eta <= 0: #Fall3 xi Druck, eta Druck
                fall[ii] = 3
                #kc = 1
                
            elif f_xi > 0 and f_eta > 0: #Fall4 xi Zug, eta Zug
                fall[ii] = 4
                #k[ii] = abs(mH.cos(psi[ii])+mH.sin(psi[ii])*mH.cot(theta))
                k[ii] = 1
                #kc = 0.55

            # Theta
            # theta_cover[ii] = mechH.theta(k[ii],psi[ii],s_xieta, alpha[ii])

            #Bewehrung
            
            rho_xi = mechH.rho(s_xi,psi[ii],k[ii],s_xieta,fs_d)
            rho_eta = mechH.rho(s_eta,psi[ii],1/k[ii],s_xieta,fs_d) #Achtung 1/k           
            as_xi[ii] = mechH.a_s(rho_xi,t[ii])
            as_eta[ii] = mechH.a_s(rho_eta,t[ii]) 

            #Betondruck
            sc_3 = (rho_xi+rho_eta)*fs_d-(s_x_stern+s_y_stern)  
            kc = norm.kc(fall[ii],code,fc_k)            
            fc = kc*fc_d
            if sc_3 <= fc:
                cc[ii]=0
                m_cc[ii] = sc_3/fc                               # Ausnutzungsgrad des Betons
            elif sc_3 > fc:
                if  t[ii] <= h/2-10 and fall[ii] == 3 and Druckzoneniteration == True:                      
                        t[ii] += delta_druck                                                                        
                        cc[ii] = 1                              # cc weiterhin vorhanden, neue Schlaufe mit dickerem t                        
                else:
                    cc[ii]=2
                    m_cc[ii] = sc_3/fc                           # Ausnutzungsgrad des Betons

            ii +=1
        dv=h-t[0]/2-t[1]/2

    # Mindest Bewehrung
    if Mindestbewehrung == True:
        rho_min = mechH.rho_min(fct_m,fs_d)
        if h >= 400:
            rho_z_min = 0.15/100 #siehe Dissertation Jaeger
        else:
            rho_z_min = 0
    else:
        rho_min=0
        rho_z_min=0

    as_z=round(max(as_z, rho_z_min*(h-d_strich_bot-d_strich_top)*1000))
    as_xi[0]=round(max(as_xi[0],rho_min*2*d_strich_bot*1000))
    as_xi[1]=round(max(as_xi[1],rho_min*2*d_strich_top*1000))
    as_eta[0]=round(max(as_eta[0],rho_min*2*d_strich_bot*1000))
    as_eta[1]=round(max(as_eta[1],rho_min*2*d_strich_top*1000))
    m_c_total = max(m_shear_c, m_cc[0], m_cc[1])

    return [i, as_xi, as_eta, as_z, fall, cc, t, k, psi, m_shear_c, m_cc, m_c_total, [xyz, ex, ey, ez, e_xi_bot, e_xi_top, e_eta_bot, e_eta_top], inp]


#Tester
#print(Sandwichmodel([1,132.46*1000,107.95*1000,0,0,0,0,0,0,0,300,40,40,30,45,435, 0, 0, 90, 90, False, True, 'vereinfacht', 'sia', [0,0,0], [0,0,0],[0,0,0],[0,0,0]]))
"""
--------------------------------------------------------------------------------
VARIABLEN UEBERSICHT
--------------------------------------------------------------------------------

i	                    int	            [-]	                Elementnummer (Zaehlvariable)
mx	                    float	        [Nmm/mm]	        Biegemoment in x-Richtung
my	                    float	        [Nmm/mm]	        Biegemoment in y-Richtung
mxy	                    float	        [Nmm/mm]	        Drillmomente (mxy = myx) bezueglich der x- und y-Richtung
vx	                    float	        [N/mm]	            Querkraft bezueglich der x-Richtung
vy	                    float	        [N/mm]	            Querkraft bezueglich der y-Richtung
v0	                    float	        [N/mm]	            Hauptquerkraft
nx	                    float	        [N/mm]	            Membrannormalkraefte in x-Richtung
ny	                    float	        [N/mm]	            Membrannormalkraefte in y-Richtung
nxy	                    float	        [N/mm]	            Membranschubkraft bezueglich der x- und y-Richtung (nxy = nyx)
h	                    float	        [mm]	            Elementdicke (Gesamtwert)
d_strich_bot	        float	        [mm]	            Distanz zwischen Unterkante Element und Schwerpunkt beider unteren Bewehrungslagen
d_strich_top	        float	        [mm]	            Distanz zwischen Oberkante Element und Schwerpunkt beider oberen Bewehrungslagen
fc_k	                float	        [N/mm2]	            Charakteristischer Wert der Zylinderdruckfestigkeit (5%-Fraktilwert)
theta_grad_kern	        float	        [Grad]	            Druckfeldneigung
fs_d	                float	        [N/mm2]	            Bemessungswert der Fliessgrenze von Betonstahl
alpha_bot	            float	        [Grad]	            Neigung der ersten unteren Deckelbewehrung zur lokalen x-Achse
alpha_top	            float	        [Grad]	            Neigung der ersten oberen Deckelbewehrung zur lokalen x-Achse
beta_bot	            float	        [Grad]	            Neigung der zweiten unteren Deckelbewehrung zur lokalen x-Achse
beta_top	            float	        [Grad]	            Neigung der zweiten oberen Deckelbewehrung zur lokalen x-Achse
Mindestbewehrung	    Bool	        [-]	                Boolvariable zur Beruecksichtigung der Mindestbewehrung
Druckzoneniteration	    Bool	        [-]	                Boolvariable zur Beruecksichtigung der Druckzoneniteration
Schubnachweis	        str	            [-]	                definiert ob der Schubnachweis nach sia ('sia') oder nach dem vereinfachten Verfahren ('vereinfacht') gefuehrt werden soll
xyz	                    list	        [-]	                Vektor mit globalen Koordinaten des Elementzentrums [x,y,z]
ex	                    list	        [-]	                Einheitsvektor fuer die x-Achse des Lokalenkoordinatensystems [exx,exy,exz]
ey	                    list	        [-]	                Einheitsvektor fuer die y-Achse des Lokalenkoordinatensystems [eyx,eyy,eyz]
ez	                    list	        [-]	                Einheitsvektor fuer die z-Achse des Lokalenkoordinatensystems [ezx,ezy,ezz]
inp	                    list	        [-]	                Inputliste fuer Sandwichmodel: [mx, my, mxy, mxy, vx, vy, v0, nx, ny, nxy, h, d'bot, d'top, fck, Theta, fsd, alphabot, alphatop, betabot, betatop, Mindestbew., Druckzonenit., Schubnachweis, xyz, ex, ey, ez]
psi	                    list	        [Grad]	            Winkel zwischen den beiden Bewehrungsrichtungen
fc_d	                float	        [N/mm2]	            Bemessungswert der Betondruckfestigkeit
fct_m	                float	        [N/mm2]	            Mittelwert der Betonzugfestigkeit
tau_nom	                float	        [N/mm2]	            Bemessungswert der Schubspannungsgrenze
delta_druck	            float	        [mm]	            Definiert wie gross der Iterationsschritt bei der Druckzoneniteration ist
t	                    list	        [mm]	            Deckeldicke
dv	                    float	        [mm]	            Abstand zwischen den beiden Deckelmittelebenen
cc	                    list	        [-]	                Wert fuer Betonbruch: 0 = kein Betonbruch; 1 = Betonbruch aber noch in in Iteration; 2 = Betonbruch (unterer Deckel)
m_cc	                list	        [-]	                Ausnuetzungsgrad fuer Betonbruch
k	                    list	        [-]	                Faktor zur Beruecksichtuigung der Drillmomente in der Bemessung
as_xi	                list	        [mm2/m]	            Absoluter Bewehrungsgehalt in xi-Richtung
as_eta	                list	        [mm2/m]	            Absoluter Bewehrungsgehalt in eta-Richtung
fall	                list	        [-]	                Fallzuordnung (siehe Kapitel 3)
e_xi_bot	            list	        [-]	                Einheitsvektor fuer die xi-Bewehrungsrichtung unterer Deckel [e_xi_x,e_xi_y,exi_z]
e_xi_top	            list	        [-]	                Einheitsvektor fuer die xi-Bewehrungsrichtung oberer Deckel [e_xi_x,e_xi_y,e_xi_z]
e_eta_bot	            list	        [-]	                Einheitsvektor fuer die eta-Bewehrungsrichtung unterer Deckel [e_eta_x,e_eta_y,e_eta_z]
e_eta_top	            list	        [-]	                Einheitsvektor fuer die eta-Bewehrungsrichtung oberer Deckel [e_eta_x,e_eta_y,e_eta_z]
rho_z	                float	        [-]	                Relativer Schubbewehrungsgehalt
as_z	                float	        [mm2/m2]	        absoluter Schubbewehrungsgehalt
shearcrack	            float	        [-]	                Wert fuer den gerissenen Kern (0 = ungerissen; 1 = gerissen)
m_shear_c	            float	        [-]	                Ausnuetzungsgrad Betonkern bezueglich Querkraft
d	                    float	        [mm]	            Statische Hoehe
z	                    float	        [mm]	            Geschaetzter innerer Hebelarm fuer Querkraftnachweis nach sia 262 4.3.3.4.2
v_x_Term	            float	        [N/mm2]	            Anteil der Querkraft an der Deckelmembrankraft in x-Richtung
v_y_Term	            float	        [N/mm2]	            Anteil der Querkraft an der Deckelmembrankraft in y-Richtung
v_xy_Term	            float	        [N/mm2]	            Anteil der Querkraft an der Deckelmembrankraft bezueglich der x- und y-Richtung
s_x	                    list	        [N/mm2]	            Normalspannung im Deckel in x-Richtung
s_y	                    list	        [N/mm2]	            Normalspannung im Deckel in y-Richtung
s_xy	                list	        [N/mm2]	            Schubspannung bezueglich der x- und y-Richtung
ii	                    list	        [-]	                Index zur Definition des oberen respektive unteren Deckels (0 = bottom=unten; 1= top=oben)
s_x_stern	            list	        [N/mm2]	            Normalspannung im Deckel in x*-Richtung
s_y_stern	            list	        [N/mm2]	            Normalspannung im Deckel in y*-Richtung
s_xy_stern	            list	        [N/mm2]	            Schubspannung bezueglich der x*- und y*-Richtung
s_xi	                list	        [N/mm2]	            Normalspannungen in schiefen Koordinaten xi
s_eta	                list	        [N/mm2]	            Normalspannungen in schiefen Koordinaten eta
s_xieta	                list	        [N/mm2]	            Schubspannungen bezueglich schiefer Koordinatenrichtungen xi und eta (s_xieta = s_etaxi)
f_xi	                float	        [-]	                Relativer Bewehrungsgehalt in xi-Richtung fuer k=1
f_eta	                float	        [-]	                Relativer Bewehrungsgehalt in eta-Richtung fuer k=1
kc	                    float	        [-]	                Beiwert zur Bestimmung der Betonfestigkeit
rho_xi	                float	        [-]	                Relativer Bewehrungsgehalt in xi-Richtung
rho_eta	                float	        [-]	                Relativer Bewehrungsgehalt in eta-Richtung
sc_3	                float	        [N/mm2]	            Maximale Betondruckspannung
fc	                    float	        [N/mm2]	            Effektive Betondruckfestigkeit
rho_min	                float	        [-]	                Minimaler relativer Laengsbewehrungsgehalt
rho_z_min	            float	        [-]	                Minimaler relativer Schubbewehrungsgehalt
"""