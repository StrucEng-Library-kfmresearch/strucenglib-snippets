 
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
       
    # Preapre for grafical oputput
    # v = scale_vector([fx, fy, fz], -scale * 0.001)
    
    R_tol=5 # Tolerance for the plane check

    # Layer with curve which define the loaded area
    load_layer=layer 
    
    # Create layername with loaded nodes
    load_layer_ele_centroids=load_layer+'_ele_centroids'
    load_layer_ele_centroids_loaded=load_layer+'_ele_centroids_loaded'

    # Berechnung Ebenengleichung der aufgespannten area_load Kurve
    # ---------------------------------------------------------------------------------
    # Bestimmung der Eckpunkte der Kurve
    curve=rs.ObjectsByLayer(load_layer)
    if rs.IsCurve(curve):
        points_curve=rs.CurvePoints(curve)

    x_coor_curve=[]
    y_coor_curve=[]
    z_coor_curve=[]
    
    # Bestimmung von drei punkten auf der area_load Kurve
    for i in range(0,3):
        x_coor=points_curve[i][0]
        y_coor=points_curve[i][1]
        z_coor=points_curve[i][2]
        x_coor_curve.append(x_coor)
        y_coor_curve.append(y_coor)
        z_coor_curve.append(z_coor)
    
    x_A=x_coor_curve[0]
    y_A=y_coor_curve[0]
    z_A=z_coor_curve[0]
    x_B=x_coor_curve[1]
    y_B=y_coor_curve[1]
    z_B=z_coor_curve[1]
    x_C=x_coor_curve[2]
    y_C=y_coor_curve[2]
    z_C=z_coor_curve[2]

    # Vektoren AB=[AB_x, AB_y, AB_z] und AC=[AC_x, AC_y, AC_z] bestimmen
    AB_x=x_B-x_A
    AB_y=y_B-y_A
    AB_z=z_B-z_A

    AC_x=x_C-x_A
    AC_y=y_C-y_A
    AC_z=z_C-z_A 

    # Normalvektoren via Vektorprodukt (N=AB x AC)
    N_x=AB_y*AC_z-AB_z*AC_y
    N_y=AB_z*AC_x-AB_x*AC_z
    N_z=AB_x*AC_y-AB_y*AC_x
    AN=x_A*N_x + y_A*N_y + z_A*N_z

    # Create points at centroid of the elements
    # ---------------------------------------------------------------------------------
    
    # Definition eines neues Layers fur alle belasteten Elementmittelpunkte 
    if rs.IsLayer(load_layer_ele_centroids_loaded):
        rs.PurgeLayer(load_layer_ele_centroids_loaded)
        scriptcontext.doc.Layers.Add(load_layer_ele_centroids_loaded, System.Drawing.Color.Black)
    else:
        scriptcontext.doc.Layers.Add(load_layer_ele_centroids_loaded, System.Drawing.Color.Black)

    # Definition eines neues Layers fur alle Elementmittelpunkte 
    if rs.IsLayer(load_layer_ele_centroids):
        rs.PurgeLayer(load_layer_ele_centroids)
        scriptcontext.doc.Layers.Add(load_layer_ele_centroids, System.Drawing.Color.Black)
    else:
        scriptcontext.doc.Layers.Add(load_layer_ele_centroids, System.Drawing.Color.Black)
        
    # Bestimmung der Elementmittelpunkte
    for element_num, element in mdl.elements.items():
        xyz=mdl.element_centroid(element=element_num)  # return the centroid of element
        elemen_num_backend=element_num+1 # return element number
        rs.CurrentLayer(load_layer_ele_centroids)
        rs.AddPoint( (xyz[0],xyz[1],xyz[2]) )
        

    # Extract points at element centroid and extract curve layer
    # ---------------------------------------------------------------------------------
    selectpt = rs.ObjectsByLayer(load_layer_ele_centroids)
    rec=rs.ObjectsByLayer(load_layer)
    xyz_coor_loaded_centroid_points=[]
    
    
     # Checks Punkt innerhalb der Lastarea
    # ---------------------------------------------------------------------------------
    
    for i in selectpt:
    
        # Check 1: Point is inside aufgespannter area_load Kurve 
        insidept = rs.PointInPlanarClosedCurve(i,rec, plane=None, tolerance=10) 
        
        if insidept==0: # The point is NOT inside the closed surve
            pass
        else: # The point IS inside the closed surve
            # Koordinaten des Punktes 
            coor=rs.PointCoordinates(i)
            #print(coor)
            coorx=coor[0]
            coory=coor[1]
            coorz=coor[2]          
            # Koordiantenform des Punktes berechnen 
            XN=N_x*coorx+N_y*coory+N_z*coorz 
            # Check 2: Point is inside aufgespannter area_load Kurve (if XN=AN -> true)   
            if XN >= AN-R_tol and XN < AN+R_tol: # 2. check point if is in curve-plane                          
                rs.CurrentLayer(load_layer_ele_centroids_loaded)
                rs.AddPoint( (coorx,coory,coorz) )     
                xyz_coor_loaded_centroid_points.append([coorx,coory,coorz])         
            else:
                pass

    # Bestimmung der Nummern der Elemente welche belastet sind
    loaded_element_numbers=[]
    for element_num, element in mdl.elements.items():
        xyz=mdl.element_centroid(element=element_num)  # return the centroid of element        
        if [xyz[0],xyz[1],xyz[2]] in xyz_coor_loaded_centroid_points:
            loaded_element_numbers.append(element_num+1)
        else:
            pass
    rs.PurgeLayer(load_layer_ele_centroids)

    return loaded_element_numbers
                