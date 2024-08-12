 
import rhinoscriptsyntax as rs
from compas_fea.structure import Structure
from compas_fea.cad import rhino
from compas.geometry import scale_vector
from compas.geometry import add_vectors
import Rhino
import scriptcontext
import System.Guid, System.Drawing.Color
import math


def Normalspurbahnverkehr_load_generator(name=None, origin=[None,None,None], l_Pl=None, h_Pl=None, s=None, beta=None, q_Gl=4.8, b_Bs=2500, h_Strich=None, Q_k=225*1000, pos_bahnlast_1=None, a=None):
    

    # Winkeldefinition
    beta_rad=math.radians(beta)
            
    plane = rs.WorldXYPlane()
    if beta_rad >= math.pi/2:
        alfa_rec=beta_rad-math.pi/2            
    elif beta_rad < math.pi/2:
        alfa_rec=beta_rad 

    
    # Generierung der Mittelachse aus s und beta falls Gleis_1 Layer nicht schon vorhanden
    #-------------------------------------------------------
    #-------------------------------------------------------
    #-------------------------------------------------------

    
    if rs.IsLayer(name): 
        rs.PurgeLayer(name)
        scriptcontext.doc.Layers.Add(name, System.Drawing.Color.Red)
        rs.CurrentLayer(name)
    else:
        scriptcontext.doc.Layers.Add(name, System.Drawing.Color.Red)
        rs.CurrentLayer(name)
    
    # Berechnung der Gleismittelachse
    # ---------------------------------------------------------------------------------    
    point_start_x=origin[0]+s
    if beta_rad >= math.pi/2:
        point_end_x=l_Pl/(math.tan(math.pi-beta_rad))
        rs.AddCurve([(point_start_x,origin[1],origin[2]),(point_start_x-point_end_x,origin[1]+l_Pl,origin[2])])
    elif beta_rad < math.pi/2:
        point_end_x=l_Pl/(math.tan(beta_rad))        
        rs.AddCurve([(point_start_x,origin[1],origin[2]),(point_start_x+point_end_x,origin[1]+l_Pl,origin[2])])
        
    selectcurve = rs.ObjectsByLayer(name)
    
    # Calculate End and Startpoints
    point_start = rs.CurveStartPoint(selectcurve)
    point_end = rs.CurveEndPoint(selectcurve)

    
    # check in welcher Ebene (xy, xz oder yz) - ONLY SUPPORTED FOR XY PLANES
    if point_start[0] == point_end[0]:
        raise NotImplementedError
    elif point_start[1] == point_end[1]:
        raise NotImplementedError
    elif point_start[2] == point_end[2]:

        # Lastgenerator fur Gleise/Schwellen Lasten
        #-------------------------------------------------------
        #-------------------------------------------------------
        #------------------------------------------------------- 
        
        # Create layername with load area
        area_load_layer_Schwellen_Gleis_Last=name+'_Schwellen_Gleis_Last'

        # Definition eines neues Layers fur alle belasteten Elementmittelpunkte 
        if rs.IsLayer(area_load_layer_Schwellen_Gleis_Last):
            rs.PurgeLayer(area_load_layer_Schwellen_Gleis_Last)
            scriptcontext.doc.Layers.Add(area_load_layer_Schwellen_Gleis_Last, System.Drawing.Color.Green)
        else:
            scriptcontext.doc.Layers.Add(area_load_layer_Schwellen_Gleis_Last, System.Drawing.Color.Green)

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
        rs.CurrentLayer(area_load_layer_Schwellen_Gleis_Last)
        rs.AddPolyline([(P_A_x,P_A_y,P_A_z),(P_B_x,P_B_y,P_B_z),(P_C_x,P_C_y,P_C_z),(P_D_x,P_D_y,P_D_z),(P_A_x,P_A_y,P_A_z)])

        # Berechnung der Belastung q_k_Gl der Gleise
        q_k_Gl=q_Gl/b_Gl
                        
        
        
        
        # Lastgenerator fur Bahnverkehrslasten Nr. 1 Lastzug A
        #-------------------------------------------------------
        #-------------------------------------------------------
        #-------------------------------------------------------
        
        # Lastausbreitung in Langsrichtung
        l_Bl=(h_Strich/4+h_Pl/2)*2

        
        # Setzen der angegeben Last 1 und der Lasten 1A, 1B, 1C
        #-------------------------------------------------------
        y_load_1=pos_bahnlast_1
        

        # Create layername with load area
        load_name_1=name+'_Bahnlast_1'
        load_name_1A=name+'_Bahnlast_1A'
        load_name_1B=name+'_Bahnlast_1B'
        load_name_1C=name+'_Bahnlast_1C'
        load_name_1A_rect=name+'_Bahnlast_1A_rect'
        load_name_1B_rect=name+'_Bahnlast_1B_rect'
        load_name_1C_rect=name+'_Bahnlast_1C_rect'

        # Definition eines neues Layers fur Bahnlast 1
        if rs.IsLayer(load_name_1):
            rs.PurgeLayer(load_name_1)
            scriptcontext.doc.Layers.Add(load_name_1, System.Drawing.Color.Red)
        else:
            scriptcontext.doc.Layers.Add(load_name_1, System.Drawing.Color.Red)
        
        rs.CurrentLayer(load_name_1)
        
        # Position Last 1 
        if beta_rad >= math.pi/2:
            delta_x_load_1=y_load_1/(math.tan(math.pi-beta_rad))
            x_load_1=point_start[0]-delta_x_load_1
            rs.AddPoint((x_load_1,y_load_1))
        elif beta_rad < math.pi/2:
            delta_x_load_1=y_load_1/(math.tan(beta_rad))
            x_load_1=point_start[0]+delta_x_load_1
            rs.AddPoint((x_load_1,y_load_1))


        # Definition eines neues Layers fur Bahnlast 1A
        if rs.IsLayer(load_name_1A):
            rs.PurgeLayer(load_name_1A)
            scriptcontext.doc.Layers.Add(load_name_1A, System.Drawing.Color.Red)
        else:
            scriptcontext.doc.Layers.Add(load_name_1A, System.Drawing.Color.Red)
        
        rs.CurrentLayer(load_name_1A)
        
        # Position Last 1A
        if beta_rad >= math.pi/2:
            delta_x_load_1A=a*math.cos(math.pi-beta_rad)
            delta_y_load_1A=a*math.sin(math.pi-beta_rad)
            x_load_1A=x_load_1+delta_x_load_1A
            y_load_1A=y_load_1-delta_y_load_1A
            rs.AddPoint((x_load_1A,y_load_1A))
        elif beta_rad < math.pi/2:
            delta_x_load_1A=a*math.cos(beta_rad)
            delta_y_load_1A=a*math.sin(beta_rad)
            x_load_1A=x_load_1-delta_x_load_1A
            y_load_1A=y_load_1-delta_y_load_1A
            rs.AddPoint((x_load_1A,y_load_1A))




        # Definition eines neues Layers fur Bahnlast 1B
        if rs.IsLayer(load_name_1B):
            rs.PurgeLayer(load_name_1B)
            scriptcontext.doc.Layers.Add(load_name_1B, System.Drawing.Color.Red)
        else:
            scriptcontext.doc.Layers.Add(load_name_1B, System.Drawing.Color.Red)
        
        rs.CurrentLayer(load_name_1B)
        
        # Position Last 1B = Position Last 1
        x_load_1B=x_load_1
        y_load_1B=y_load_1
        rs.AddPoint((x_load_1B,y_load_1B))
           



        # Definition eines neues Layers fur Bahnlast 1C
        if rs.IsLayer(load_name_1C):
            rs.PurgeLayer(load_name_1C)
            scriptcontext.doc.Layers.Add(load_name_1C, System.Drawing.Color.Red)
        else:
            scriptcontext.doc.Layers.Add(load_name_1C, System.Drawing.Color.Red)
        
        rs.CurrentLayer(load_name_1C)
               
        # Position Last 1C
        if beta_rad >= math.pi/2:
            delta_x_load_1C=a*math.cos(math.pi-beta_rad)
            delta_y_load_1C=a*math.sin(math.pi-beta_rad)
            x_load_1C=x_load_1-delta_x_load_1C
            y_load_1C=y_load_1+delta_y_load_1C
            rs.AddPoint((x_load_1C,y_load_1C))
        elif beta_rad < math.pi/2:
            delta_x_load_1C=a*math.cos(beta_rad)
            delta_y_load_1C=a*math.sin(beta_rad)
            x_load_1C=x_load_1+delta_x_load_1C
            y_load_1C=y_load_1+delta_y_load_1C
            rs.AddPoint((x_load_1C,y_load_1C))     

        

        # Definition eines neues Layers fur Rectnalge 1A
        if rs.IsLayer(load_name_1A_rect):
            rs.PurgeLayer(load_name_1A_rect)
            scriptcontext.doc.Layers.Add(load_name_1A_rect, System.Drawing.Color.Red)
        else:
            scriptcontext.doc.Layers.Add(load_name_1A_rect, System.Drawing.Color.Red)
        
        rs.CurrentLayer(load_name_1A_rect)

        # Build rectangle fro load Area 1A
        plane1A = rs.RotatePlane(plane, math.degrees(alfa_rec), [0,0,1])
        rs.AddRectangle( plane1A, l_Bl, b_Gl )
        selectrect_1A = rs.ObjectsByLayer(load_name_1A_rect)
        rect_1A_corner_points=rs.CurvePoints(selectrect_1A)
        mid_point_rect_1A_x=(rect_1A_corner_points[0][0]+rect_1A_corner_points[2][0])/2
        mid_point_rect_1A_y=(rect_1A_corner_points[0][1]+rect_1A_corner_points[2][1])/2
        translation_start_rect=[mid_point_rect_1A_x, mid_point_rect_1A_y, 0]
        translation_end_rect=[x_load_1A,y_load_1A,0]
        translation_rect=[translation_end_rect[0]-translation_start_rect[0],translation_end_rect[1]-translation_start_rect[1],translation_end_rect[2]-translation_start_rect[2]]
        rs.MoveObject(selectrect_1A, translation_rect)
        



        # Definition eines neues Layers fur Rectnalge 1B
        if rs.IsLayer(load_name_1B_rect):
            rs.PurgeLayer(load_name_1B_rect)
            scriptcontext.doc.Layers.Add(load_name_1B_rect, System.Drawing.Color.Red)
        else:
            scriptcontext.doc.Layers.Add(load_name_1B_rect, System.Drawing.Color.Red)
        
        rs.CurrentLayer(load_name_1B_rect)

        # Build rectangle fro load Area 1B
        plane1B = rs.RotatePlane(plane, math.degrees(alfa_rec), [0,0,1])
        rs.AddRectangle( plane1B, l_Bl, b_Gl )
        selectrect_1B = rs.ObjectsByLayer(load_name_1B_rect)
        rect_1B_corner_points=rs.CurvePoints(selectrect_1B)
        mid_point_rect_1B_x=(rect_1B_corner_points[0][0]+rect_1B_corner_points[2][0])/2
        mid_point_rect_1B_y=(rect_1B_corner_points[0][1]+rect_1B_corner_points[2][1])/2
        translation_start_rect=[mid_point_rect_1B_x, mid_point_rect_1B_y, 0]
        translation_end_rect=[x_load_1B,y_load_1B,0]
        translation_rect=[translation_end_rect[0]-translation_start_rect[0],translation_end_rect[1]-translation_start_rect[1],translation_end_rect[2]-translation_start_rect[2]]
        rs.MoveObject(selectrect_1B, translation_rect)




        # Definition eines neues Layers fur Rectnalge 1C
        if rs.IsLayer(load_name_1C_rect):
            rs.PurgeLayer(load_name_1C_rect)
            scriptcontext.doc.Layers.Add(load_name_1C_rect, System.Drawing.Color.Red)
        else:
            scriptcontext.doc.Layers.Add(load_name_1C_rect, System.Drawing.Color.Red)
        
        rs.CurrentLayer(load_name_1C_rect)

        # Build rectangle fro load Area 1C
        plane1C = rs.RotatePlane(plane, math.degrees(alfa_rec), [0,0,1])
        rs.AddRectangle( plane1C, l_Bl, b_Gl )
        selectrect_1C = rs.ObjectsByLayer(load_name_1C_rect)
        rect_1C_corner_points=rs.CurvePoints(selectrect_1C)
        mid_point_rect_1C_x=(rect_1C_corner_points[0][0]+rect_1C_corner_points[2][0])/2
        mid_point_rect_1C_y=(rect_1C_corner_points[0][1]+rect_1C_corner_points[2][1])/2
        translation_start_rect=[mid_point_rect_1C_x, mid_point_rect_1C_y, 0]
        translation_end_rect=[x_load_1C,y_load_1C,0]
        translation_rect=[translation_end_rect[0]-translation_start_rect[0],translation_end_rect[1]-translation_start_rect[1],translation_end_rect[2]-translation_start_rect[2]]
        rs.MoveObject(selectrect_1C, translation_rect)
        
        # Berechnung der Flachenlasten fur A
        area_1A=rs.Area(selectrect_1A)
        q_k_Bl_A=(Q_k/4)/area_1A

        # Berechnung der Flachenlasten fur B
        area_1B=rs.Area(selectrect_1B)
        q_k_Bl_B=(Q_k/2)/area_1B

        # Berechnung der Flachenlasten fur C
        area_1C=rs.Area(selectrect_1C)
        q_k_Bl_C=(Q_k/4)/area_1C


        # Lastgenerator fur Bahnverkehrslasten >= Nr.2  Lastzug A
        #--------------------------------------------------------
        #--------------------------------------------------------
        #--------------------------------------------------------
        
        
        for lg in range(0,4): # Lastgruppen 2 (lg=0), 3(lg=1),... bis unendlich
            
            # Relative Distance
            delta_distance_load_lg_to_load_1=[]    
            delta_distance_load_lg_to_load_1.append(1800)
            delta_distance_load_lg_to_load_1.append((1800+4500))
            delta_distance_load_lg_to_load_1.append((1800+4500+1800))
            delta_distance_load_lg_to_load_1.append((1800+4500+1800+3000))
            delta_distance_load_lg_to_load_1.append((1800+4500+1800+3000+1800))
            delta_distance_load_lg_to_load_1.append((1800+4500+1800+3000+1800+4500))
            delta_distance_load_lg_to_load_1.append((1800+4500+1800+3000+1800+4500+1800))
            # Hier entsprechend erweitern fur beliebig viele lg
                        
            #  SCHLEIFE uber Einzallasten i (d.h. A (i=0), B (i=1), C(i=2)) in Lastgruppe lg
            for i in range(0,3):

                # Bestimmen neuer Layers
                if i==0:
                    load_name_i_rect=name+'_Bahnlast_'+str(lg+2)+'A'
                if i==1:
                    load_name_i_rect=name+'_Bahnlast_'+str(lg+2)+'B'
                if i==2:
                    load_name_i_rect=name+'_Bahnlast_'+str(lg+2)+'C'
                            
                if rs.IsLayer(load_name_i_rect):
                    rs.PurgeLayer(load_name_i_rect)
                    scriptcontext.doc.Layers.Add(load_name_i_rect, System.Drawing.Color.Red)
                else:
                    scriptcontext.doc.Layers.Add(load_name_i_rect, System.Drawing.Color.Red)
                

                
            
                # Calcualte relativ position and absolute positions x,y for iA, iB, iC zum Punkt 1A, 1B, 1C (iA to 1A = iB to 1B = iC to 1C) and copy rectangle
                if beta_rad >= math.pi/2:
                    delta_x_load_i_to_1=delta_distance_load_lg_to_load_1[lg]*math.cos(math.pi-beta_rad)
                    delta_y_load_i_to_1=delta_distance_load_lg_to_load_1[lg]*math.sin(math.pi-beta_rad)
                    if i==0: # d.h. iA
                        rs.CurrentLayer(load_name_i_rect)
                        x_load_iA=x_load_1A+delta_x_load_i_to_1
                        y_load_iA=y_load_1A-delta_y_load_i_to_1
                        planeiA = rs.RotatePlane(plane, math.degrees(alfa_rec), [0,0,1])
                        rs.AddRectangle( planeiA, l_Bl, b_Gl )
                        selectrect_iA = rs.ObjectsByLayer(load_name_i_rect)
                        rect_iA_corner_points=rs.CurvePoints(selectrect_iA)
                        mid_point_rect_iA_x=(rect_iA_corner_points[0][0]+rect_iA_corner_points[2][0])/2
                        mid_point_rect_iA_y=(rect_iA_corner_points[0][1]+rect_iA_corner_points[2][1])/2
                        translation_start_rect=[mid_point_rect_iA_x, mid_point_rect_iA_y, 0]
                        translation_end_rect=[x_load_iA,y_load_iA,0]
                        translation_rect=[translation_end_rect[0]-translation_start_rect[0],translation_end_rect[1]-translation_start_rect[1],translation_end_rect[2]-translation_start_rect[2]]
                        rs.MoveObject(selectrect_iA, translation_rect)
                        q_k_Bl_A
                    elif i==1: # d.h. iB
                        rs.CurrentLayer(load_name_i_rect)
                        x_load_iB=x_load_1B+delta_x_load_i_to_1
                        y_load_iB=y_load_1B-delta_y_load_i_to_1     
                        planeiB = rs.RotatePlane(plane, math.degrees(alfa_rec), [0,0,1])
                        rs.AddRectangle( planeiB, l_Bl, b_Gl )
                        selectrect_iB = rs.ObjectsByLayer(load_name_i_rect)
                        rect_iB_corner_points=rs.CurvePoints(selectrect_iB)
                        mid_point_rect_iB_x=(rect_iB_corner_points[0][0]+rect_iB_corner_points[2][0])/2
                        mid_point_rect_iB_y=(rect_iB_corner_points[0][1]+rect_iB_corner_points[2][1])/2
                        translation_start_rect=[mid_point_rect_iB_x, mid_point_rect_iB_y, 0]
                        translation_end_rect=[x_load_iB,y_load_iB,0]
                        translation_rect=[translation_end_rect[0]-translation_start_rect[0],translation_end_rect[1]-translation_start_rect[1],translation_end_rect[2]-translation_start_rect[2]]
                        rs.MoveObject(selectrect_iB, translation_rect)

                    elif i==2: # d.h. iC
                        rs.CurrentLayer(load_name_i_rect)
                        x_load_iC=x_load_1C+delta_x_load_i_to_1
                        y_load_iC=y_load_1C-delta_y_load_i_to_1                     
                        planeiC = rs.RotatePlane(plane, math.degrees(alfa_rec), [0,0,1])
                        rs.AddRectangle( planeiC, l_Bl, b_Gl )
                        selectrect_iC = rs.ObjectsByLayer(load_name_i_rect)
                        rect_iC_corner_points=rs.CurvePoints(selectrect_iC)
                        mid_point_rect_iC_x=(rect_iC_corner_points[0][0]+rect_iC_corner_points[2][0])/2
                        mid_point_rect_iC_y=(rect_iC_corner_points[0][1]+rect_iC_corner_points[2][1])/2
                        translation_start_rect=[mid_point_rect_iC_x, mid_point_rect_iC_y, 0]
                        translation_end_rect=[x_load_iC,y_load_iC,0]
                        translation_rect=[translation_end_rect[0]-translation_start_rect[0],translation_end_rect[1]-translation_start_rect[1],translation_end_rect[2]-translation_start_rect[2]]
                        rs.MoveObject(selectrect_iC, translation_rect)

                elif beta_rad < math.pi/2:
                    delta_x_load_i_to_1=delta_distance_load_lg_to_load_1[lg]*math.cos(beta_rad)
                    delta_y_load_i_to_1=delta_distance_load_lg_to_load_1[lg]*math.sin(beta_rad)
                    print(delta_distance_load_lg_to_load_1[lg])
                    if i==0: # d.h. iA
                        rs.CurrentLayer(load_name_i_rect)
                        x_load_iA=x_load_1A-delta_x_load_i_to_1
                        y_load_iA=y_load_1A-delta_y_load_i_to_1
                        planeiA = rs.RotatePlane(plane, math.degrees(alfa_rec), [0,0,1])
                        rs.AddRectangle( planeiA, l_Bl, b_Gl )
                        selectrect_iA = rs.ObjectsByLayer(load_name_i_rect)
                        rect_iA_corner_points=rs.CurvePoints(selectrect_iA)
                        mid_point_rect_iA_x=(rect_iA_corner_points[0][0]+rect_iA_corner_points[2][0])/2
                        mid_point_rect_iA_y=(rect_iA_corner_points[0][1]+rect_iA_corner_points[2][1])/2
                        translation_start_rect=[mid_point_rect_iA_x, mid_point_rect_iA_y, 0]
                        translation_end_rect=[x_load_iA,y_load_iA,0]
                        translation_rect=[translation_end_rect[0]-translation_start_rect[0],translation_end_rect[1]-translation_start_rect[1],translation_end_rect[2]-translation_start_rect[2]]
                        rs.MoveObject(selectrect_iA, translation_rect)

                    elif i==1: # d.h. iB
                        rs.CurrentLayer(load_name_i_rect)
                        x_load_iB=x_load_1B-delta_x_load_i_to_1
                        y_load_iB=y_load_1B-delta_y_load_i_to_1   
                        planeiB = rs.RotatePlane(plane, math.degrees(alfa_rec), [0,0,1])
                        rs.AddRectangle( planeiB, l_Bl, b_Gl )
                        selectrect_iB = rs.ObjectsByLayer(load_name_i_rect)
                        rect_iB_corner_points=rs.CurvePoints(selectrect_iB)
                        mid_point_rect_iB_x=(rect_iB_corner_points[0][0]+rect_iB_corner_points[2][0])/2
                        mid_point_rect_iB_y=(rect_iB_corner_points[0][1]+rect_iB_corner_points[2][1])/2
                        translation_start_rect=[mid_point_rect_iB_x, mid_point_rect_iB_y, 0]
                        translation_end_rect=[x_load_iB,y_load_iB,0]
                        translation_rect=[translation_end_rect[0]-translation_start_rect[0],translation_end_rect[1]-translation_start_rect[1],translation_end_rect[2]-translation_start_rect[2]]
                        rs.MoveObject(selectrect_iB, translation_rect)

                    elif i==2: # d.h. iC
                        rs.CurrentLayer(load_name_i_rect)
                        x_load_iC=x_load_1C-delta_x_load_i_to_1
                        y_load_iC=y_load_1C-delta_y_load_i_to_1    
                        planeiC = rs.RotatePlane(plane, math.degrees(alfa_rec), [0,0,1])
                        rs.AddRectangle( planeiC, l_Bl, b_Gl )
                        selectrect_iC = rs.ObjectsByLayer(load_name_i_rect)
                        rect_iC_corner_points=rs.CurvePoints(selectrect_iC)
                        mid_point_rect_iC_x=(rect_iC_corner_points[0][0]+rect_iC_corner_points[2][0])/2
                        mid_point_rect_iC_y=(rect_iC_corner_points[0][1]+rect_iC_corner_points[2][1])/2
                        translation_start_rect=[mid_point_rect_iC_x, mid_point_rect_iC_y, 0]
                        translation_end_rect=[x_load_iC,y_load_iC,0]
                        translation_rect=[translation_end_rect[0]-translation_start_rect[0],translation_end_rect[1]-translation_start_rect[1],translation_end_rect[2]-translation_start_rect[2]]
                        rs.MoveObject(selectrect_iC, translation_rect)
        



 

    else:
        raise NotImplementedError  
        
           
    
    return q_k_Gl, area_load_layer_Schwellen_Gleis_Last, q_k_Bl_A, load_name_1A_rect, q_k_Bl_B, load_name_1B_rect, q_k_Bl_C, load_name_1C_rect


