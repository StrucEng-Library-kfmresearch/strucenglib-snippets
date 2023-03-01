import rhinoscriptsyntax as rs
from compas_fea.structure import Structure
from compas_fea.cad import rhino
import Rhino
import scriptcontext
import System.Guid, System.Drawing.Color


def plot_nr_elem(mdl):
    # Basics
    layer_new = "Element_numbers"
    rs.CurrentLayer(layer="Default")

    def AddLayer():
        layer_index = scriptcontext.doc.Layers.Add(layer_new, System.Drawing.Color.Black)
        return Rhino.Commands.Result.Success

    # check if layer already exist and Add a new layer to the document
    if rs.IsLayer(layer_new):
        rs.PurgeLayer(layer_new)
        AddLayer()
        rs.CurrentLayer(layer_new)
    else:
        AddLayer()
        rs.CurrentLayer(layer_new)

    # show Element numbers
    for element_num, element in mdl.elements.items():
        xyz = mdl.element_centroid(element=element_num)  # return the centroid of element
        elemen_num_backend = element_num + 1
        rs.AddTextDot(str(elemen_num_backend), xyz)
