import rhinoscriptsyntax as rs
from compas_fea.structure import Structure
from compas_fea.cad import rhino
import Rhino
import scriptcontext
import System.Guid, System.Drawing.Color


def plot_nr_nodes(mdl):
    # Basics
    layer_new = "Node_numbers"
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

    # show Node numbers
    xyz = mdl.nodes_xyz()  # return the x,y,z coor
    xyz_len = len(xyz)

    for ii in range(0, xyz_len):
        rs.AddTextDot(ii + 1, xyz[ii])
