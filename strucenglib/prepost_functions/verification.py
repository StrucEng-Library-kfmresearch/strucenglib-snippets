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
       
    # Layer with curve which define the Nachweisschnitt
    NS_layer_V=layer 
    
    # Create layername with elements inside Nachweisschnitt
    NS_layer_ele_centroids=NS_layer_V+'_Elementmittelpunkte'
    NS_layer_ele_centroids_temp='temp'
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
            
            rs.CurrentLayer(NS_layer_ele_centroids)
            rs.AddPoint( (coorx,coory,coorz) ) 
            xyz_coor_NS_centroid_points.append([coorx,coory,coorz])


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
                