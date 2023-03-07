

import rhinoscriptsyntax as rs
import Rhino
import scriptcontext
import System.Guid, System.Drawing.Color

from compas_fea.cad import rhino
from compas_fea.structure import ShellSection
from compas_fea.structure import Structure


#Allgemein
name = 'Rahmen'
path = 'C:/Temp/'

# Structure

mdl = Structure(name=name, path=path)

# Elements

rhino.add_nodes_elements_from_layers(mdl, mesh_type='ShellElement', layers=['elset_deck','elset_wall_left','elset_wall_right'])



# Add this block
def AddLayer():

    # Add a new layer to the document
    layer_index = scriptcontext.doc.Layers.Add('Node_numbers', System.Drawing.Color.Black)
    return Rhino.Commands.Result.Success

if __name__=="__main__":
    AddLayer()
    rs.CurrentLayer("Node_numbers")

# show Element numbers
xyz=mdl.nodes_xyz()  # return the x,y,z coor
xyz_len=len(xyz)


# show Element numbers
for ii in range(0, xyz_len):
    rs.AddTextDot(ii+1, xyz[ii])
