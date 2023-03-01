import rhinoscriptsyntax as rs
import Rhino
import scriptcontext
import System.Guid, System.Drawing.Color

from compas_fea.cad import rhino
from compas_fea.structure import ShellSection
from compas_fea.structure import Structure

# Allgemein
name = 'Rahmen'
path = 'C:/Temp/'

# Structure

mdl = Structure(name=name, path=path)

# Elements

rhino.add_nodes_elements_from_layers(mdl, mesh_type='ShellElement',
                                     layers=['elset_deck', 'elset_wall_left', 'elset_wall_right'])


# Add this block
def AddLayer():
    # Add a new layer to the document
    layer_index = scriptcontext.doc.Layers.Add('Element_numbers', System.Drawing.Color.Black)
    return Rhino.Commands.Result.Success


if __name__ == "__main__":
    AddLayer()
    rs.CurrentLayer("Element_numbers")

# show Element numbers
for element_num, element in mdl.elements.items():
    xyz = mdl.element_centroid(element=element_num)  # return the centroid of element
    elemen_num_backend = element_num + 1
    rs.AddTextDot(str(elemen_num_backend), xyz)
