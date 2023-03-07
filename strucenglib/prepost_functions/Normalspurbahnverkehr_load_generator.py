 
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

def Normalspurbahnverkehr_load_generator(mdl, name=None, l_Pl=None, h_Pl=None, s=None, beta=None, q_Gl=4.8, b_Bs=2500, h_Strich=None, Q_k=225*1000, y_A=200):
    
    # Allgemeine Berechnunge/Definitionen
    #-------------------------------------------------------
    #-------------------------------------------------------
    #-------------------------------------------------------

    # Winkeldefinition
    beta_rad=math.radians(beta)
    alfa_rec=beta_rad        
    plane = rs.WorldXYPlane()

    # Aufbau Liste fur Layer Namen
    Lasten_aus_Normalspurverkehr=[]

    # Generierung der Mittelachse aus s und beta falls Gleis Layer nicht schon vorhanden
    #-------------------------------------------------------
    #-------------------------------------------------------
    #-------------------------------------------------------

    # Create layername
    Gleis_Mittelachse=name+'_Mittelachse'

    # Definition eines neuen Layers
    if rs.IsLayer(Gleis_Mittelachse):
        rs.PurgeLayer(Gleis_Mittelachse)
        scriptcontext.doc.Layers.Add(Gleis_Mittelachse, System.Drawing.Color.Red)
    else:
        scriptcontext.doc.Layers.Add(Gleis_Mittelachse, System.Drawing.Color.Red)
    
    rs.CurrentLayer(Gleis_Mittelachse)

    point_start_x=s
    point_start_y=0

    point_end_x=s+math.tan(beta_rad)*l_Pl
    point_end_y=l_Pl

    rs.AddCurve([(point_start_x,point_start_y,0),(point_end_x,point_end_y,0)])
       
    selectcurve = rs.ObjectsByLayer(Gleis_Mittelachse)
    
    # Calculate End and Startpoints
    point_start = rs.CurveStartPoint(selectcurve)
    point_end = rs.CurveEndPoint(selectcurve)
    
    # check in welcher Ebene (xy, xz oder yz) - ONLY SUPPORTED FOR XY PLANES
    if point_start[0] == point_end[0]:
        raise NotImplementedError
    elif point_start[1] == point_end[1]:
        raise NotImplementedError
    elif point_start[2] == point_end[2]:
        pass
        
    # Lastgenerator fur Eigengeiwchte Gleise/Schwellen
    #-------------------------------------------------------
    #-------------------------------------------------------
    #------------------------------------------------------- 

    # Create layername with load area
    Gleis_Eigengewichte_Schiene=name+'_EIGENGEWICHTE_SCHIENE_Lasteinzug'

    # Definition eines neues Layers fur alle belasteten Elementmittelpunkte 
    if rs.IsLayer(Gleis_Eigengewichte_Schiene):
        rs.PurgeLayer(Gleis_Eigengewichte_Schiene)
        scriptcontext.doc.Layers.Add(Gleis_Eigengewichte_Schiene, System.Drawing.Color.Green)
    else:
        scriptcontext.doc.Layers.Add(Gleis_Eigengewichte_Schiene, System.Drawing.Color.Green)

    rs.CurrentLayer(Gleis_Eigengewichte_Schiene)

    # Geometrische Berechnung der Lastflachen
    # ---------------------------------------------------------------------------------
    # Berechnung b_Gl
    b_Gl=(b_Bs/2+h_Strich/4+h_Pl/2)*2

    # Berechnung b_strich_Gl
    b_Strich_Gl=b_Gl/math.sin(beta_rad)

    # Berechnung der vier Eckpunkte der Lastflache
    # ---------------------------------------------------------------------------------
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
    # ---------------------------------------------------------------------------------
    rs.CurrentLayer(Gleis_Eigengewichte_Schiene)
    rs.AddPolyline([(P_A_x,P_A_y,P_A_z),(P_B_x,P_B_y,P_B_z),(P_C_x,P_C_y,P_C_z),(P_D_x,P_D_y,P_D_z),(P_A_x,P_A_y,P_A_z)])

    # Berechnung der verteilten Belastung q_k_Gl der Gleise
    q_k_Gl=q_Gl/b_Gl

    # Berechnung der belasteten Elemente
    # ---------------------------------------------------------------------------------
    loaded_element_numbers=area_load_generator_elements(mdl,Gleis_Eigengewichte_Schiene) # Calculate Element numbers within the area load curve
    
    # Hinzufugen der belasteten Elemente
    mdl.add(AreaLoad(Gleis_Eigengewichte_Schiene, elements=loaded_element_numbers,x=0,y=0,z=q_k_Gl)) # Add new element set
    # Bemerkung: Naming Gleis_Eigengewichte_Schiene gibt es pro Schiene (d.h. pro Funktionsaufruf) nur einmal
    Lasten_aus_Normalspurverkehr.append(Gleis_Eigengewichte_Schiene)  

    # Lastgenerator fur Bahnlasten
    #-------------------------------------------------------
    #-------------------------------------------------------
    #------------------------------------------------------- 
  

    # Step 1: Allgemeine Definitionen
    #--------------------------------------------------------------------------        
        
    # Berechnung der x_A Koordinante aus y_A
    x_A=math.tan(beta_rad)*y_A+s 
    #rs.AddPoint((x_A,y_A))     
    
    
    # Schleife uber neg und pos richtung ausgehend von x_A, y_A
    for LB_VZ in xrange(1,3):

        # Liste mit Abstanden L_i
        if LB_VZ==1:  # in positive Richtung
            L_i_list=[0,3000,3000+1800,3000+1800+4500,3000+1800+4500+1800]
        else: # in negative Richtung
            L_i_list=[-1800,-1800-4500,-1800-4500-1800]

        # Lastausbreitung in Langsrichtung und QUerrichtung
        l_Bl=(h_Strich/4+h_Pl/2)*2
        b_Bl=b_Gl
        lauf_LB=0

        for L_i in L_i_list: # Schleife uber alle Lastblocke
            
            # Anzahl der Durchlaufe for naming
            if LB_VZ==1:  
                lauf_LB=lauf_LB+1
            else:
                lauf_LB=lauf_LB-1
                


            #print(lauf_LB)    
            
            # Step 2: Mittelkoordinanten des Lastpunktes
            #--------------------------------------------------------------------------   

            # Create layername with load area
            Bahnlasten_Einzellasten=name+'_BAHNLASTEN_Einzellasten'+'_Lastblock_'+str(lauf_LB)

            # Definition eines neues Layers fur alle belasteten Elementmittelpunkte 
            if rs.IsLayer(Bahnlasten_Einzellasten):
                rs.PurgeLayer(Bahnlasten_Einzellasten)
                scriptcontext.doc.Layers.Add(Bahnlasten_Einzellasten, System.Drawing.Color.Green)
            else:
                scriptcontext.doc.Layers.Add(Bahnlasten_Einzellasten, System.Drawing.Color.Green)

            rs.CurrentLayer(Bahnlasten_Einzellasten)

            d_x=L_i*math.sin(beta_rad)
            d_y=L_i*math.cos(beta_rad)
            x_point=x_A+d_x
            y_point=y_A+d_y

            rs.AddPoint((x_point,y_point))

            # Step 3: Lastpolygone berechnen
            #--------------------------------------------------------------------------   

            # Koordianten der Eckpunkte der Lastflache bestimmen

            # Punkt A_strich        
            x_P_A_strich=-b_Bl/2
            y_P_A_strich=l_Bl/2
            # Punkt B_strich
            x_P_B_strich=-b_Bl/2
            y_P_B_strich=-l_Bl/2
            # Punkt C_strich
            x_P_C_strich=b_Bl/2
            y_P_C_strich=-l_Bl/2
            # Punkt D_strich
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
            Bahnlasten_Lasteinzug=name+'_BAHNLASTEN_Lasteinzug'+'_Lastblock_'+str(lauf_LB)

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

            # Step 4: Kontrolle ob Lastpolygone Elemente beinhaltet
            #--------------------------------------------------------------------------   
            loaded_element_numbers=area_load_generator_elements(mdl,Bahnlasten_Lasteinzug) # Calculate Element numbers within the area load curve
            
                   
            if not loaded_element_numbers:  # Zudem Bedingung dass Lastrflache nicht in area liegt                  
                rs.CurrentLayer(Gleis_Mittelachse)
                rs.PurgeLayer(Bahnlasten_Einzellasten)
                rs.PurgeLayer(Bahnlasten_Lasteinzug)  
                load_layer_ele_centroids_loaded=Bahnlasten_Lasteinzug+'_Elementmittelpunkte_belastet'         
                rs.PurgeLayer(load_layer_ele_centroids_loaded)
                break
                
            else:                       
                # Abspeichern der Namen fur die Bahnlasten_Lasteinzug                         
                Lasten_aus_Normalspurverkehr.append(Bahnlasten_Lasteinzug)
                # Berechnung der Flachenlast
                selectloadedarea = rs.ObjectsByLayer(Bahnlasten_Lasteinzug)
                area=rs.Area(selectloadedarea)
                q_k_Bl=(Q_k/4)/area

                # Hinzufugen der belasten Elemente zu Struktur                
                mdl.add(AreaLoad(Bahnlasten_Lasteinzug, elements=loaded_element_numbers,x=0,y=0,z=q_k_Bl)) # Add new element set
                

    return Lasten_aus_Normalspurverkehr