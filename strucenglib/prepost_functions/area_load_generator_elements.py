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
       
    # Layer with curve which define the loaded area
    load_layer=layer 
    
    # Create layername for saving the centroids of all elements
    load_layer_ele_centroids=load_layer+'_Elementmittelpunkt'

    # Create layername for savin only the centroids of the loaded elements
    load_layer_ele_centroids_loaded=load_layer+'_Elementmittelpunkte_belastet'


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
            
            # Bestimmung Koordinaten des Punktes und Abspeichern im Layer fur alle belastetne Elemente 
            coor=rs.PointCoordinates(i)
            coorx=coor[0]
            coory=coor[1]
            coorz=coor[2]          
            
            rs.CurrentLayer(load_layer_ele_centroids_loaded)
            rs.AddPoint( (coorx,coory,coorz) ) 
            xyz_coor_loaded_centroid_points.append([coorx,coory,coorz])


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
                