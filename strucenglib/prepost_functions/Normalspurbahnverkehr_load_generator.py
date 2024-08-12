 # Author(s): Marius  Weber (ETHZ, HSLU T&A)

import os 
from datetime import datetime
import rhinoscriptsyntax as rs
from compas_fea.structure import Structure
from compas_fea.cad import rhino
from compas.geometry import scale_vector
from compas.geometry import add_vectors
import Rhino
import scriptcontext
import System.Guid, System.Drawing.Color
import math
from strucenglib.prepost_functions import area_load_generator_elements
from compas_fea.structure import AreaLoad



def Normalspurbahnverkehr_load_generator(mdl, name=None, l_Pl=None, h_Pl=None, s=None, beta=None, q_Gl=4.8+1.7, b_Bs=2500, 
                                         h_Strich=None, h_GL=160, h_w=None, Q_k=225*1000, y_A=200, m=4650, gamma_G=1, gamma_Q=1, 
                                         direction='all', verbalise=False):

    """  
    Function calculating and generating the loading resulting from a railway track. It generates the dead load of the track as
    well as the life load. The life load is applied according to SIA 269/1 11.2. The axle loads of a train is applied iteratively 
    starting from the defined starting point y_A.

    Parameters
    ----------
    mdl : structurObject
        A structure object, representing the structure to be analysed
    name : str
        Name of the track (e.g. "Track1")
    l_Pl : float
        Plate length/ Span between two walls + 2*wall Thickness [mm]
    h_Pl : float
        deck slab thickness [mm]
    s : float
        Distance between origin (0,0,0) and the track in global x-direction [mm]
    beta: float
        Angle between global y-axis and track axis [Degree], should be in range[-90,90]
    q_Gl : float
        Load form concrete sleeper(Betonschwelle, normally 4.8 N/mm)) and load from the tracks themselfs (normally 1.7 N/mm) [N/mm]
    b_Bs : float
        Width of the concrete sleeper of one track [mm] (normally 2500 mm PAIngB Page 157)
    h_Strich : float
        Height between lower level of concrete sleepers of the tracks to the upper surface of the slab deck of the bridge [mm] 
        (ca. height of gravel layer + insulation layer height)
    h_Gl:float
        Height of the tracks (normally arround 130 and 180 mm) [mm]
    Q_k : float
        axle load [N] (for D4 225*1000 N, SIA 269/1 11.2.1.1)
    y_A : float
        y-coordinate of the starting point for the live load generation iteration.
    m: int
        Distance between inner Qact (see SIA 269/1 11.2.1.1; for D4: 4650 mm) [mm]
    gamma_G: float
        Safety factor for dead load (default=1, SIA 269: 1.35 ) [-]
    gamma_Q: float
        Safety factor for live load (default=1, SIA 269: 1.45 ) [-]
    verbalise: bool
        If set to true it prints the caluclated load values. 

    Returns
    ----------
    List[str]
        A list of load names, which were generated within the function.
    """


    # Basic definitions
    #-------------------------------------------------------

    # Schreiben des Warning files zum fullen bei anfanglichen Warnungen
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    file = open('WARNINGS_in_Normalspurbahnverkehr_load_generator.txt','a')
    file.write('Warnings im Pythonfile Normalspurbahnverkehr_load_generator,'+dt_string+'\n')
    file.write('-------------------------------------------------------------------------------\n')
    file.close()

    # Winkeldefinition
    beta_rad=math.radians(beta)

    # Aufbau Liste fur Layer Namen
    Lasten_aus_Normalspurverkehr=[]


    # Generierung der Mittelachse aus s und beta 
    #-------------------------------------------------------

    # Create layername fur die Mittelachse
    Gleis_Mittelachse=name+'_Mittelachse'

    # Definition eines neuen Layers
    if rs.IsLayer(Gleis_Mittelachse):
        rs.PurgeLayer(Gleis_Mittelachse)
        scriptcontext.doc.Layers.Add(Gleis_Mittelachse, System.Drawing.Color.Red)
    else:
        scriptcontext.doc.Layers.Add(Gleis_Mittelachse, System.Drawing.Color.Red)
    
    rs.CurrentLayer(Gleis_Mittelachse)

    # Startpunkt der Mittelachse (Annahme: Globaler Nullpunkt immer bei x=0,y=0,z=0)
    point_start_x=s
    point_start_y=0

    # Endpunkt der Mittelachse
    point_end_x=s+math.tan(beta_rad)*l_Pl
    point_end_y=l_Pl

    # Hinzufugen der Linie in Layer als Polyline
    rs.AddCurve([(point_start_x,point_start_y,0),(point_end_x,point_end_y,0)])
       
    # Selektieren der Mittelachse   
    selectcurve = rs.ObjectsByLayer(Gleis_Mittelachse)
    
    # Calculate End and Startpoints der Mittelachse
    point_start = rs.CurveStartPoint(selectcurve)
    point_end = rs.CurveEndPoint(selectcurve)
    
      
    # Lastgenerator fur Eigengewichte Gleise/Schwellen
    #-------------------------------------------------------

    # Create layername
    Gleis_Eigengewichte_Schiene=name+'_EIGENGEWICHTE_SCHIENE_Lasteinzugsflache'

    # Definition eines neues Layers fur alle belasteten Elementmittelpunkte 
    if rs.IsLayer(Gleis_Eigengewichte_Schiene):
        rs.PurgeLayer(Gleis_Eigengewichte_Schiene)
        scriptcontext.doc.Layers.Add(Gleis_Eigengewichte_Schiene, System.Drawing.Color.Green)
    else:
        scriptcontext.doc.Layers.Add(Gleis_Eigengewichte_Schiene, System.Drawing.Color.Green)

    rs.CurrentLayer(Gleis_Eigengewichte_Schiene)

    # Geometrische Berechnung der Lastflachen
    # Berechnung b_Gl (Lastausbreitung in Querrichtung)
    b_Gl=(b_Bs/2+h_Strich/4+h_Pl/2)*2

    # Berechnung b_strich_Gl
    b_Strich_Gl=b_Gl/math.cos(abs(beta_rad))

    # Berechnung der vier Eckpunkte der Lastflachen
    # x Koordinanten
    P_A_x=(point_start[0]-b_Strich_Gl/2)
    P_B_x=(point_start[0]+b_Strich_Gl/2)
    P_C_x=(point_end[0]+b_Strich_Gl/2)
    P_D_x=(point_end[0]-b_Strich_Gl/2)

    # y Koordinanten
    P_A_y=(point_start[1])
    P_B_y=(point_start[1])
    P_C_y=(point_end[1])
    P_D_y=(point_end[1])

    # z Koordinanten
    P_A_z=(point_start[2])
    P_B_z=(point_start[2])
    P_C_z=(point_end[2])
    P_D_z=(point_end[2])

    # Berechnung der vier Eckpunkte der Lastflache und Kurvne in Rhino Layer ploten
    rs.CurrentLayer(Gleis_Eigengewichte_Schiene)
    rs.AddPolyline([(P_A_x,P_A_y,P_A_z),(P_B_x,P_B_y,P_B_z),(P_C_x,P_C_y,P_C_z),(P_D_x,P_D_y,P_D_z),(P_A_x,P_A_y,P_A_z)])

    # Berechnung der verteilten Belastung q_k_Gl der Gleise
    q_k_Gl=gamma_G*q_Gl/b_Gl

    # verbalise
    if verbalise:
        print('The area load resulting from concret sleeper and the tracks: ', q_k_Gl, ' N/mm2 ;',q_k_Gl*1000, ' kN/m2' )

    # Berechnung der belasteten Elemente (Gibt Nummern der belastete Elemente raus)
    loaded_element_numbers=area_load_generator_elements(mdl,Gleis_Eigengewichte_Schiene) # Calculate Element numbers within the area load curve
    
    # Hinzufugen der belasteten Elemente
    mdl.add(AreaLoad(Gleis_Eigengewichte_Schiene, elements=loaded_element_numbers,x=0,y=0,z=q_k_Gl, axes ='global')) # Add new element set

    # Hinzufugen des Namens des Layers der Lasteinzugsflache
    # Bemerkung: Naming _Lasteinzugsflaeche_der_Schienen_Eigengewichte' gibt es pro Schiene (d.h. pro Funktionsaufruf) nur einmal
    Lasten_aus_Normalspurverkehr.append(Gleis_Eigengewichte_Schiene)  

    # Lastgenerator fur Bahnlasten
    #-------------------------------------------------------
  
    # Berechnung der x_A Koordinante (Lage der Einzellast) aus y_A
    x_A=math.tan(beta_rad)*y_A+s 

    # Lastausbreitung in Langsrichtung und Querrichtung
    l_Bl=(h_GL*2+h_Strich/4+h_Pl/2)*2 #Langsrichtung
    b_Bl=b_Gl #Querrichtung

    #Berechnung Flachenlast
    #Fur Hoechstgeschwindigkeit bis 140 #TODO adapt for other Hoechstgewschwindigkeiten 125
    l_phi=(1.3*(l_Pl+(h_w+h_Pl/2)*2))/3 #[mm]
    l_phi_list=[1,2,4,6,8,10,15,20,25,30,40,50,60,70,80,100] #[m]
    dynF_list=[1.60, 1.59, 1.57, 1.54, 1.50, 1.45, 1.35, 1.32, 1.29, 1.26, 1.23, 1.20, 1.18, 1.17, 1.16, 1.14]
    index=max(i for i, num in enumerate(l_phi_list) if num <= l_phi/1000)
    dynF=dynF_list[index]
    alpha=1 # Klassifizierungsbeiwert Alpha (PAIngB S.34, =1 for evaluation of existing structures)
    area=l_Bl*b_Bl
    q_k_Bl=(Q_k*1.1*dynF*alpha)/area
    q_d_Bl=gamma_Q*q_k_Bl

    # verbalise
    if verbalise:
        print('The area load resulting from the rail traffic live load: ', q_d_Bl, ' N/mm2 ;',q_d_Bl*1000, ' kN/m2' )

       
    # Schleife uber neg und pos richtung ausgehend von x_A, y_A
    # d.h. es werden in neg. und pos Richtung weitrere Lastblocke gemass Abstand Lastmodell angeordnet
    if direction == 'positive':
        i_list=[0]
    elif direction == 'negative':
        i_list=[-1]
    elif direction in ['all', 'both']:
        i_list=range(1,3)
    else:
        raise ValueError('Invalid input for direction. Choose between "negative", "positive", and "all".')
    
    for LB_VZ in i_list: # zweimal durchlaufen - einmal pos. und einmal neg. Richtung

        # Liste mit absolunten Abstanden L_i zum Punkt x_A, y_A
        if LB_VZ==0: #in positive Richtung (y wird grosser)
            L_i_list=[0,+1800,+1800+m,1800+m+1800,+1800+m+1800+3000,+1800+m+1800+3000+1800,+1800+m+1800+3000+1800+m,+1800+m+1800+3000+1800+m+1800]
        if LB_VZ==-1: #in negative Richtung (y wird kleiner)
            L_i_list=[0,-1800,-1800-m,-1800-m-1800,-1800-m-1800-3000,-1800-m-1800-3000-1800,-1800-m-1800-3000-1800-m,-1800-m-1800-3000-1800-m-1800]
        if LB_VZ==1:  # all direction, in positive Richtung (y wird grosser)
            L_i_list=[0,3000,3000+1800,3000+1800+m,3000+1800+m+1800,3000+1800+m+1800+3000,3000+1800+m+1800+3000+1800,3000+1800+m+1800+3000+1800+m,3000+1800+m+1800+3000+1800+m+1800]            
        if LB_VZ==2: #  all direction, in negative Richtung (y wird kleiner) (with first train in negative y direction)
            L_i_list=[-1800,-1800-m,-1800-m-1800,-1800-m-1800-3000,-1800-m-1800-3000-1800,-1800-m-1800-3000-1800-m,-1800-m-1800-3000-1800-m-1800]
            

        lauf_LB=0
        List_lengh=len(L_i_list)

        for L_i in L_i_list: # Schleife uber alle Lastblocke
            
            # Anzahl der Durchlaufe fur naming der Layers
            if LB_VZ==1:  
                lauf_LB=lauf_LB+1
            else:
                lauf_LB=lauf_LB-1

            # Mittelkoordinanten des Lastpunktes

            # Create layername with load area
            Bahnlasten_Einzellasten=name+'_BAHNLASTEN_Einzellasten'+'_Lastblock_'+str(lauf_LB)

            # Definition eines neues Layers fur alle belasteten Elementmittelpunkte des Lastblockes
            if rs.IsLayer(Bahnlasten_Einzellasten):
                rs.PurgeLayer(Bahnlasten_Einzellasten)
                scriptcontext.doc.Layers.Add(Bahnlasten_Einzellasten, System.Drawing.Color.Green)
            else:
                scriptcontext.doc.Layers.Add(Bahnlasten_Einzellasten, System.Drawing.Color.Green)

            rs.CurrentLayer(Bahnlasten_Einzellasten)

            # Berechnung relativer Abstand zu Einzellast bei x_A, y_A
            d_x=L_i*math.sin(beta_rad)
            d_y=L_i*math.cos(beta_rad)

           # Berechnung Koordinaten der Einzellast zur Einzellast bei x_A, y_A
            x_point=x_A+d_x
            y_point=y_A+d_y

            rs.AddPoint((x_point,y_point))

            
            # Lastpolygone bzw. Lastausbreitung berechnen 

            # Koordinaten Punkt A_strich        
            x_P_A_strich=-b_Bl/2
            y_P_A_strich=l_Bl/2
            # Koordinaten Punkt B_strich
            x_P_B_strich=-b_Bl/2
            y_P_B_strich=-l_Bl/2
            # Koordinaten Punkt C_strich
            x_P_C_strich=b_Bl/2
            y_P_C_strich=-l_Bl/2
            # Koordinaten Punkt D_strich
            x_P_D_strich=b_Bl/2
            y_P_D_strich=l_Bl/2                

            # Berucksichtigung der Drehmatrix fur Punkte A, B, C, D
            
            # Punkt A
            x_P_A=x_P_A_strich*math.cos(-1*beta_rad)-y_P_A_strich*math.sin(-1*beta_rad)
            y_P_A=x_P_A_strich*math.sin(-1*beta_rad)+y_P_A_strich*math.cos(-1*beta_rad)
            x_def_A=x_point+x_P_A
            y_def_A=y_point+y_P_A
            # Punkt B
            x_P_B=x_P_B_strich*math.cos(-1*beta_rad)-y_P_B_strich*math.sin(-1*beta_rad)
            y_P_B=x_P_B_strich*math.sin(-1*beta_rad)+y_P_B_strich*math.cos(-1*beta_rad)
            x_def_B=x_point+x_P_B
            y_def_B=y_point+y_P_B
            # Punkt C
            x_P_C=x_P_C_strich*math.cos(-1*beta_rad)-y_P_C_strich*math.sin(-1*beta_rad)
            y_P_C=x_P_C_strich*math.sin(-1*beta_rad)+y_P_C_strich*math.cos(-1*beta_rad)
            x_def_C=x_point+x_P_C
            y_def_C=y_point+y_P_C        
            # Punkt D
            x_P_D=x_P_D_strich*math.cos(-1*beta_rad)-y_P_D_strich*math.sin(-1*beta_rad)
            y_P_D=x_P_D_strich*math.sin(-1*beta_rad)+y_P_D_strich*math.cos(-1*beta_rad)
            x_def_D=x_point+x_P_D
            y_def_D=y_point+y_P_D

            # Create layername with load area
            Bahnlasten_Lasteinzug=name+'_BAHNLASTEN_Lasteinzugsflache'+'_Lastblock_'+str(lauf_LB)

            # Definition eines neues Layers fur alle belasteten Elementmittelpunkte 
            if rs.IsLayer(Bahnlasten_Lasteinzug):
                rs.PurgeLayer(Bahnlasten_Lasteinzug)
                scriptcontext.doc.Layers.Add(Bahnlasten_Lasteinzug, System.Drawing.Color.Green)
            else:
                scriptcontext.doc.Layers.Add(Bahnlasten_Lasteinzug, System.Drawing.Color.Green)

            rs.CurrentLayer(Bahnlasten_Lasteinzug)

            # Build rectangle for load area
            points=[(x_def_A,y_def_A,0),(x_def_B,y_def_B,0),(x_def_C,y_def_C,0),(x_def_D,y_def_D,0),(x_def_A,y_def_A,0)]
            rs.AddPolyline(points)

            # Kontrolle ob Lastpolygon mindestes ein Punkt der Punkte A,B,C,D innerhalb der Fahrbahnplatte liegt
                
            # Falls alle Eckpunkte (A,B,C,D) der Lasteinzugsflache ausserhalb der Platte liegen -> Loop L_i abbrechen
            if y_def_A <= point_start_y or y_def_A >= point_end_y: # Ausserhalb der Platte
                check_lage_A=1
            else:
                check_lage_A=0

            if y_def_B <= point_start_y or y_def_B >= point_end_y: # Ausserhalb der Platte
                check_lage_B=1
            else:
                check_lage_B=0    

            if y_def_C <= point_start_y or y_def_C >= point_end_y: # Ausserhalb der Platte
                check_lage_C=1
            else:
                check_lage_C=0                             

            if y_def_D <= point_start_y or y_def_D >= point_end_y: # Ausserhalb der Platte
                check_lage_D=1
            else:
                check_lage_D=0 

            # Summe der check_lage gleich 4 dann Loop L_i abbrechen sonst (else) weiterer im L_i loop
            check_lage=check_lage_A+check_lage_B+check_lage_C+check_lage_D
            if check_lage == 4:
                rs.CurrentLayer(Gleis_Mittelachse)
                rs.PurgeLayer(Bahnlasten_Einzellasten)
                rs.PurgeLayer(Bahnlasten_Lasteinzug)  
                break
            else:
                pass
                

            # Kontrolle ob Lastpolygone Elemente beinhaltet

            # Berechnung der Elementnummern welche im oben definieren Polygon liegen
            loaded_element_numbers=area_load_generator_elements(mdl,Bahnlasten_Lasteinzug) 
            
            # 
            # Die oben definierten Polygon beinhaltet keine Elemente     
            if not loaded_element_numbers:            
                rs.CurrentLayer(Gleis_Mittelachse)
                rs.PurgeLayer(Bahnlasten_Einzellasten)
                rs.PurgeLayer(Bahnlasten_Lasteinzug)  
                load_layer_ele_centroids_loaded=Bahnlasten_Lasteinzug+'_Elementmittelpunkte_belastet' # Aus Definition in Funktion area_load_generator_elements
                rs.PurgeLayer(load_layer_ele_centroids_loaded)

                          
                warning_string='Warning: Load block ' +str(lauf_LB)+ ' inside plate, but does not contain any element -> choose smaller mesh'   
                file = open('WARNINGS_in_Normalspurbahnverkehr_load_generator.txt','a')
                file.write(warning_string+'\n')
                file.close()
               
                
            else:                       
                # Abspeichern der Namen fur die Bahnlasten_Lasteinzug                         
                Lasten_aus_Normalspurverkehr.append(Bahnlasten_Lasteinzug)

                # OLD: Berechnung der Flachenlast
                # selectloadedarea = rs.ObjectsByLayer(Bahnlasten_Lasteinzug)
                # area=rs.Area(selectloadedarea)
                # print(area,'area')
                # q_k_Bl=(Q_k/4)/area
                # print('q_k_Bl',q_k_Bl)

                # Hinzufugen der belasten Elemente zu Struktur                
                mdl.add(AreaLoad(Bahnlasten_Lasteinzug, elements=loaded_element_numbers,x=0,y=0,z=q_d_Bl, axes='global')) # postive z direction is downwards

                # Warnung, das alle vorgegeben lastblocke durchlaufen wurden und eventuell noch mehr auf der Platte platz hatten
                if L_i == L_i_list[List_lengh-1]:

                    warning_string='Warning: More load blocks could have placed on the plate -> Please adjust L_i_List in the pythonfile Normalspurbahnverkehr_load_generator'
                    file = open('WARNINGS_in_Normalspurbahnverkehr_load_generator.txt','a')
                    file.write(warning_string+'\n')
                    file.close()
  
                else:
                    pass
                

    return Lasten_aus_Normalspurverkehr  #  Beinhaltet alle Namen der Layer mit den Lasten





