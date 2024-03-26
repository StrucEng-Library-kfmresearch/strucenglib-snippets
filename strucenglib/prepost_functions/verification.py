# Author(s): Marius  Weber (ETHZ, HSLU T&A)

import rhinoscriptsyntax as rs
from compas_fea.structure import Structure
from compas_fea.cad import rhino
from compas.geometry import scale_vector
from compas.geometry import add_vectors
import Rhino
import scriptcontext
import System.Guid, System.Drawing.Color

def verification(mdl, layer, check=None):
    
    # Basic definitions
    #-------------------------------------------------------
    # Tolerance for the plane check  
    R_tol=5    
    
    # Layer with curve which define the Nachweisschnitt
    NS_layer_V=layer 
    
    # Create layername with elements inside Nachweisschnitt
    NS_layer_ele_centroids=NS_layer_V+'_Elementmittelpunkte'
    NS_layer_ele_centroids_temp='temp'


    # Aufstellung der Grundlagen fur die Ebenengleichung
    # ---------------------------------------------------------------------------------
    # Extract Point coor from the curve in load_layer
    x_coor_all=[]
    y_coor_all=[]
    z_coor_all=[]

    curve=rs.ObjectsByLayer(NS_layer_V)
    if rs.IsCurve(curve):
        points=rs.CurvePoints(curve)
    
    # Determine three points of the curve
    for i in range(0,3):
        
        x_coor=points[i][0]
        y_coor=points[i][1]
        z_coor=points[i][2]
        x_coor_all.append(x_coor)
        y_coor_all.append(y_coor)
        z_coor_all.append(z_coor)
    
    # Define the three points A=x_A,y_A,z_A; B=x_B,y_B,z_B; C=x_C,y_C,z_C
    x_A=x_coor_all[0]
    y_A=y_coor_all[0]
    z_A=z_coor_all[0]
    
    x_B=x_coor_all[1]
    y_B=y_coor_all[1]
    z_B=z_coor_all[1]

    x_C=x_coor_all[2]
    y_C=y_coor_all[2]
    z_C=z_coor_all[2]

    # Vectors AB=[AB_x, AB_y, AB_z] and AC=[AC_x, AC_y, AC_z]
    AB_x=x_B-x_A
    AB_y=y_B-y_A
    AB_z=z_B-z_A

    AC_x=x_C-x_A
    AC_y=y_C-y_A
    AC_z=z_C-z_A 


    # Normalvektor via corrsproduct (N=AB x AC)
    N_x=AB_y*AC_z-AB_z*AC_y
    N_y=AB_z*AC_x-AB_x*AC_z
    N_z=AB_x*AC_y-AB_y*AC_x
    AN=x_A*N_x + y_A*N_y + z_A*N_z    
    
    
    # Create points at centroid of the elements
    # ---------------------------------------------------------------------------------
    
    # Definition eines neues Layers fur die Elementmittelpunkte innerhalb des Nachweisschnittes
    if rs.IsLayer(NS_layer_ele_centroids):
        rs.PurgeLayer(NS_layer_ele_centroids)
        scriptcontext.doc.Layers.Add(NS_layer_ele_centroids, System.Drawing.Color.Green)
    else:
        scriptcontext.doc.Layers.Add(NS_layer_ele_centroids, System.Drawing.Color.Green)

    # Definition eines neues Layers temporar (wird wieder geloscht)
    if rs.IsLayer(NS_layer_ele_centroids_temp):
        rs.PurgeLayer(NS_layer_ele_centroids_temp)
        scriptcontext.doc.Layers.Add(NS_layer_ele_centroids_temp, System.Drawing.Color.Green)
    else:
        scriptcontext.doc.Layers.Add(NS_layer_ele_centroids_temp, System.Drawing.Color.Green)

    # Bestimmung der Elementmittelpunkte
    for element_num, element in mdl.elements.items(): # fangt bei elemntnummer 0 an
        
        xyz=mdl.element_centroid(element=element_num)  # return the centroid of element
        elemen_num_backend=element_num+1 # return element number
        rs.CurrentLayer(NS_layer_ele_centroids_temp)
        rs.AddPoint( (xyz[0],xyz[1],xyz[2]) )
        

    # Extract points at element centroid and extract curve layer
    # ---------------------------------------------------------------------------------
    selectpt = rs.ObjectsByLayer(NS_layer_ele_centroids_temp)
    rec=rs.ObjectsByLayer(NS_layer_V)
    xyz_coor_NS_centroid_points=[]
    
    
     # Checks Punkt innerhalb des Nachweisschnittes
    # ---------------------------------------------------------------------------------
   
    for i in selectpt:
    
        # Check 1: Point is inside aufgespannter area_load Kurve 
        insidept = rs.PointInPlanarClosedCurve(i,rec, plane=rs.CurvePlane(rec), tolerance=10) 
        
        if insidept==0: # The point is NOT inside the closed surve
            pass
        else: # The point IS inside the closed surve
            # Koordinaten des Punktes 
            coor=rs.PointCoordinates(i)
            coorx=coor[0]
            coory=coor[1]
            coorz=coor[2]          
            
            # Check if point is inside curve-plane (mit Ebenegleichung)

            # Koordiantenform (XN= AN ----> N_x*coorx + N_y*coor_y + N_z*coor_z = x_A*N_x + y_A*N_y + z_A*N_z)
            XN=N_x*coorx+N_y*coory+N_z*coorz 

            if XN >= AN-R_tol and XN < AN+R_tol: 
                # Abspeichern im Layer fur alle belastetne Elemente 
                rs.CurrentLayer(NS_layer_ele_centroids)
                rs.AddPoint( (coorx,coory,coorz) ) 
                xyz_coor_NS_centroid_points.append([coorx,coory,coorz])
            else:
                pass


    # Bestimmung der Nummern der Elemente welche belastet sind
    NS_element_numbers=[]
    for element_num, element in mdl.elements.items():
        
        xyz=mdl.element_centroid(element=element_num)  # return the centroid of element        
        if [xyz[0],xyz[1],xyz[2]] in xyz_coor_NS_centroid_points:
            NS_element_numbers.append(element_num+1)
            
        else:
            pass
    rs.CurrentLayer(NS_layer_ele_centroids)   
    rs.PurgeLayer(NS_layer_ele_centroids_temp)

    
    # add elements to the structure using add_set
    if check == 'V':
        name_type='Nachweisschnitt_'+check
        mdl.add_set(name=NS_layer_V, type=name_type, selection=NS_element_numbers)  # add an element set 'elset_shell'
    else:
        pass

    return NS_element_numbers
                