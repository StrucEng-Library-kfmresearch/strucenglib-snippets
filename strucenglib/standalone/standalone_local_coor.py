
import rhinoscriptsyntax as rs
from compas_fea.structure import Structure
from compas_fea.cad import rhino
from strucenglib.prepost_functions import add_loc_coor
import Rhino
import scriptcontext
import System.Guid, System.Drawing.Color

# Inputs
layer_in='elset_deck'
name = 'Rahmen'
path = 'C:/Temp/'
mdl = Structure(name=name, path=path)
axes_scale=200
# Bestimmung der Elemente
rhino.add_nodes_elements_from_layers(mdl, mesh_type='ShellElement', layers=layer_in)

# Import semi local coordinate systems (Einheitsvektoren)

semi_loc_coords=add_loc_coor(layer=layer_in, PORIG=[0,0,3120],PXAXS=[10000,0,3120]) 

e_x=semi_loc_coords[4]
e_y=semi_loc_coords[5]
e_z=semi_loc_coords[6]

# Add a new layer to the document
layer_new = "local_coor"

def AddLayer():
    layer_index = scriptcontext.doc.Layers.Add(layer_new, System.Drawing.Color.Black)
    return Rhino.Commands.Result.Success

if __name__=="__main__":
    AddLayer()
    rs.CurrentLayer(layer_new)
    
# Loop uber alle Elemente und Darstellung Koordinaten

for element_num, element in mdl.elements.items():
    
    # Centroid of the element
    xyz=mdl.element_centroid(element=element_num)  # return the centroid of element
    # Definition of point in local x direction
    
    coor_loc_x_0=xyz[0]+e_x[0]*axes_scale
    coor_loc_x_1=xyz[1]+e_x[1]*axes_scale
    coor_loc_x_2=xyz[2]+e_x[2]*axes_scale
    coor_loc_x=[coor_loc_x_0,coor_loc_x_1,coor_loc_x_2]
    
    coor_loc_y_0=xyz[0]+e_y[0]*axes_scale
    coor_loc_y_1=xyz[1]+e_y[1]*axes_scale
    coor_loc_y_2=xyz[2]+e_y[2]*axes_scale
    coor_loc_y=[coor_loc_y_0,coor_loc_y_1,coor_loc_y_2]
    
    coor_loc_z_0=xyz[0]+e_z[0]*axes_scale
    coor_loc_z_1=xyz[1]+e_z[1]*axes_scale
    coor_loc_z_2=xyz[2]+e_z[2]*axes_scale
    coor_loc_z=[coor_loc_z_0,coor_loc_z_1,coor_loc_z_2]
    
    ex = rs.AddLine(xyz, coor_loc_x)
    ey = rs.AddLine(xyz, coor_loc_y)
    ez = rs.AddLine(xyz, coor_loc_z)
        
    rs.ObjectColor(ex, [255, 0, 0]) #rot
    rs.ObjectColor(ey, [0, 255, 0]) #gruen
    rs.ObjectColor(ez, [0, 0, 255]) #blau
    rs.ObjectLayer(ex, layer_new)
    rs.ObjectLayer(ey, layer_new)
    rs.ObjectLayer(ez, layer_new)
