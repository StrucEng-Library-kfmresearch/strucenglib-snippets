 
import rhinoscriptsyntax as rs
from compas_fea.structure import Structure
from compas_fea.cad import rhino
from compas.geometry import scale_vector
from compas.geometry import add_vectors
import Rhino
import scriptcontext
import System.Guid, System.Drawing.Color



def area_load_generator(mdl, layer, assoc_load_layer=None, fx=0, fy=0, fz=0, mx=0, my=0, mz=0, scale=1.0):
    
    numbers_of_loaded_nodes=0

    # Preapre for grafical oputput

    v = scale_vector([fx, fy, fz], -scale * 0.001)
    
    # check associated layer  (Ein Layer von mehrer in einer ebene liegende Layer genuegt)
   
    guid_assoc_load_layer= rs.ObjectsByLayer(assoc_load_layer)
    vertices = rs.MeshVertices(guid_assoc_load_layer)
    vertice_lauf=-1
    vertice_save=[]
    for vertice in vertices:
        vertice_save.append(vertice[2])
    
    if vertice_lauf>0:
        if vertice_save[vertice_lauf-1]==vertice_save[vertice_lauf]:
            pass
        else:
            print('load generator for inclined meshes or meshes in x,y plane is not implemented')

    vertice_check=vertice_save[0]
    R_tol=10

    # Layer with curve which define the loaded area
    load_layer=layer 
    
    # Create layername with loaded nodes
    load_layer_nodes=load_layer+'_loaded_nodes'
    load_layer_nodes_arrows=load_layer+'_loaded_nodes_arrows'
    # extract all points from all associated layers
    rs.Command('_ExtractPt _Selmesh _Enter')

    # set current layer to load_layewr
    rs.CurrentLayer(load_layer)

    # Select layer with polycon
    rec=rs.ObjectsByLayer(load_layer)
    
    # Definition of the new layer with arrows
    if rs.IsLayer(load_layer_nodes_arrows):
        rs.PurgeLayer(load_layer_nodes_arrows)
        scriptcontext.doc.Layers.Add(load_layer_nodes_arrows, System.Drawing.Color.Black)
        rs.CurrentLayer(load_layer_nodes_arrows)
    else:
        scriptcontext.doc.Layers.Add(load_layer_nodes_arrows, System.Drawing.Color.Black)
        rs.CurrentLayer(load_layer_nodes_arrows)    

    # Definition of the new layer with the loaded nodes
    if rs.IsLayer(load_layer_nodes):
        rs.PurgeLayer(load_layer_nodes)
        scriptcontext.doc.Layers.Add(load_layer_nodes, System.Drawing.Color.Black)
        rs.CurrentLayer(load_layer_nodes)
    else:
        scriptcontext.doc.Layers.Add(load_layer_nodes, System.Drawing.Color.Black)
        rs.CurrentLayer(load_layer_nodes)

    

    # Filter and save all control points inside polycon
    points=[]
    coor_x=[]
    coor_y=[]
    coor_z=[]
    selectpt = rs.ObjectsByType(rs.filter.point)

    i_lauf=-1
    test_lauf=0
    for i in selectpt:
        points.append(i)
        i_lauf=i_lauf+1

        insidept = rs.PointInPlanarClosedCurve(points[i_lauf],rec, plane=None, tolerance=10)
        if insidept==0:
            #print("The point is NOT inside the closed surve") 
            pass
        else: 
            #print ("The point is on the closed curve.")
            #test_lauf=test_lauf+1
            coor=rs.PointCoordinates(i)
            # if coor[0] in coor_x and coor[1] in coor_y and coor[2] in coor_z
               # print("The object already exists.")
               # pass            
            #else:
            if vertice_check>=coor[2]-R_tol and vertice_check<coor[2]+R_tol:
                #print("The object does not exist.")
                numbers_of_loaded_nodes=numbers_of_loaded_nodes+1
                rs.CurrentLayer(load_layer_nodes)    
                coor_x.append(coor[0])
                coor_y.append(coor[1])
                coor_z.append(coor[2])
                coorx=coor[0]
                coory=coor[1]
                coorz=coor[2]
                xyz=[coorx, coory, coorz]
                rs.AddPoint( (coorx,coory,coorz) )
                   
                rs.CurrentLayer(load_layer_nodes_arrows) 
                line = rs.AddLine(xyz, add_vectors(xyz, v))
                rs.CurveArrows(line, 1)
                rs.CurrentLayer(load_layer_nodes) 
            else:
                pass
                
                            
    rs.Command('_Delete') # Del selected control point
    
    return load_layer_nodes, numbers_of_loaded_nodes