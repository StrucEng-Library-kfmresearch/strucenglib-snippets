# Author(s): Marius  Weber (ETHZ, HSLU T&A)

import rhinoscriptsyntax as rs
from compas_fea.structure import Structure
from compas_fea.cad import rhino
from compas.geometry import scale_vector
from compas.geometry import add_vectors
import Rhino
import scriptcontext
import System.Guid, System.Drawing.Color

def area_load_generator_elements(mdl, layer):
    
    # Basic definitions
    #-------------------------------------------------------
    # Tolerance for the plane check  
    R_tol=5 

    # Layer with curve which define the loaded area
    load_layer=layer 
    
    # Create layername for saving the centroids of all elements
    load_layer_ele_centroids=load_layer+'_Elementmittelpunkt'

    # Create layername for savin only the centroids of the loaded elements
    load_layer_ele_centroids_loaded=load_layer+'_Elementmittelpunkte_belastet'


    # Aufstellung der Grundlagen fur die Ebenengleichung
    # ---------------------------------------------------------------------------------
    # Extract Point coor from the curve in load_layer
    x_coor_all=[]
    y_coor_all=[]
    z_coor_all=[]

    curve=rs.ObjectsByLayer(load_layer)
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


    # Create new layers 
    # ---------------------------------------------------------------------------------
    
    # For all elements
    if rs.IsLayer(load_layer_ele_centroids):
        rs.PurgeLayer(load_layer_ele_centroids)
        scriptcontext.doc.Layers.Add(load_layer_ele_centroids, System.Drawing.Color.Red)
    else:
        scriptcontext.doc.Layers.Add(load_layer_ele_centroids, System.Drawing.Color.Red)

    # For loaded elements 
    if rs.IsLayer(load_layer_ele_centroids_loaded):
        rs.PurgeLayer(load_layer_ele_centroids_loaded)
        scriptcontext.doc.Layers.Add(load_layer_ele_centroids_loaded, System.Drawing.Color.Red)
    else:
        scriptcontext.doc.Layers.Add(load_layer_ele_centroids_loaded, System.Drawing.Color.Red)

        
    # Bestimmung und speichern aller Elementmittelpunkte und speichern im Layer
    # ---------------------------------------------------------------------------------
    for element_num, element in mdl.elements.items():
        xyz=mdl.element_centroid(element=element_num)  # return the centroid of element
        rs.CurrentLayer(load_layer_ele_centroids)
        rs.AddPoint( (xyz[0],xyz[1],xyz[2]) )
        

    # Extract Kooridnaten aller Mittelpunkte aller Element
    # ---------------------------------------------------------------------------------
    selectpt = rs.ObjectsByLayer(load_layer_ele_centroids) 
    rec=rs.ObjectsByLayer(load_layer) 
    xyz_coor_loaded_centroid_points=[]
    
    # Check ob Koordianten innerhalb der Polyline (belasteten Area)
    # ---------------------------------------------------------------------------------
   
    for i in selectpt:
    
        # Check 1: Punkt innerhalb oder ausserhalb der Polylinie
        insidept = rs.PointInPlanarClosedCurve(i,rec, plane=rs.CurvePlane(rec), tolerance=10) 
        
        if insidept==0: # The point is NOT inside the closed surve
            pass
        else: # The point IS inside the closed surve

            # Bestimmung Koordinaten des Punktes und 
            coor=rs.PointCoordinates(i)
            coorx=coor[0]
            coory=coor[1]
            coorz=coor[2]   
            
            # Check if point is inside curve-plane (mit Ebenegleichung)

            # Koordiantenform (XN= AN ----> N_x*coorx + N_y*coor_y + N_z*coor_z = x_A*N_x + y_A*N_y + z_A*N_z)
            XN=N_x*coorx+N_y*coory+N_z*coorz 

            if XN >= AN-R_tol and XN < AN+R_tol: 
                # Abspeichern im Layer fur alle belastetne Elemente 
                rs.CurrentLayer(load_layer_ele_centroids_loaded)
                rs.AddPoint( (coorx,coory,coorz) ) 
                xyz_coor_loaded_centroid_points.append([coorx,coory,coorz])
            else:
                pass

            
            # Check if the z-Axis of the pont is zero (if not do no include in the set) 
            #if coorz >= 0-R_tol and coorz < 0+R_tol:
                # Abspeichern im Layer fur alle belastetne Elemente 
            #    rs.CurrentLayer(load_layer_ele_centroids_loaded)
            #    rs.AddPoint( (coorx,coory,coorz) ) 
            #    xyz_coor_loaded_centroid_points.append([coorx,coory,coorz])
            #else:
            #    pass

    # Bestimmung der Nummern der Elemente welche belastet sind
    loaded_element_numbers=[]
    for element_num, element in mdl.elements.items():
        xyz=mdl.element_centroid(element=element_num)  # return the centroid of element        
        
        if [xyz[0],xyz[1],xyz[2]] in xyz_coor_loaded_centroid_points:
            loaded_element_numbers.append(element_num+1)
            
        else:
            pass
    rs.CurrentLayer(load_layer_ele_centroids_loaded)   
    rs.PurgeLayer(load_layer_ele_centroids)

    return loaded_element_numbers
                