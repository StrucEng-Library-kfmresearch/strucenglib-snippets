# Author(s): Marius  Weber (ETHZ, HSLU T&A)

import math   
import rhinoscriptsyntax as rs
from compas_fea.structure import structure
from compas_fea.cad import rhino
from strucenglib.prepost_functions import calc_loc_coor
import Rhino
import scriptcontext
import System.Guid, System.Drawing.Color


def plot_loc_axes(mdl, axes_scale):




    # Basics
    layer_new = "local_coor (red=local x-direction, green=local y-direction, blue=local z-direction)"
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

    # Plot local coordiante systems
    save_element_nr = list()

    properties = mdl.element_properties
    sections = mdl.sections
    sets = mdl.sets
    #for layer in layers:
    
    # Bestimmung der Elemente
    for key in sorted(properties):
        property = properties[key]
        element_set = sets[property.elset]
        section = sections[property.section]
        stype = section.__name__

        if stype == 'ShellSection':
            loc_coor_EV_XA= section.loc_coords_EV_XA
            loc_coor_EV_YA= section.loc_coords_EV_YA
            loc_coor_EV_ZA= section.loc_coords_EV_ZA
            #print(section)

            if element_set.type != 'node':            
                selection = [i + 1 for i in sorted(element_set.selection)]    
                
                # local coordiantes           
                e_x=loc_coor_EV_XA.get('EV_XA',None)
                e_y=loc_coor_EV_YA.get('EV_YA',None)
                e_z=loc_coor_EV_ZA.get('EV_ZA',None)

                for element_num in selection:                

                    element_num=element_num-1

                    #  Centroid of the element
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

                    save_element_nr.append(element_num)
