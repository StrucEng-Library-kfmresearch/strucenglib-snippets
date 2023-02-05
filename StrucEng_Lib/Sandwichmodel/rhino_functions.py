
import rhinoscriptsyntax as rs
from compas.geometry import add_vectors
from compas.geometry import scale_vector

def plot_axes_BB( result_element, k, axes_scale, plot_local_axes, plot_reinf): # fuer mainfunction 
    """
    Parameter
    ----------
    result_element : dic
        Structure object.

    k : int
        Elementnumber whos axes are plotted. Furthermore, the origin of the axes are on that element.

    axes_scale : float
        scalefactor for all axes

    plot_local_axes : bool
        lokale Achsen auf jedes Element plotten?

    plot_reinf : bool
        Bewehrungsrichtungen auf jedes Element plotten?

 
    """





    # Get Coordinates and vectors
    
    xyz = result_element[12][0]
    ex = result_element[12][1]
    ey = result_element[12][2]
    ez = result_element[12][3]
    e_xi_bot= result_element[12][4]
    e_xi_top = result_element[12][5]
    e_eta_bot  = result_element[12][6]
    e_eta_top = result_element[12][7]

    # CREATE LOCAL COORDINATES
    if plot_local_axes == True:
        layer = "local_koordinaten"

        if k == 0:
            rs.CurrentLayer(rs.AddLayer(layer))
            rs.DeleteObjects(rs.ObjectsByLayer(layer))
        else:
            rs.CurrentLayer(layer)
        rs.EnableRedraw(False)

        ex = rs.AddLine(xyz, add_vectors(xyz, scale_vector(ex, axes_scale)))
        ey = rs.AddLine(xyz, add_vectors(xyz, scale_vector(ey, axes_scale)))
        ez = rs.AddLine(xyz, add_vectors(xyz, scale_vector(ez, axes_scale)))

        rs.ObjectColor(ex, [255, 0, 0]) #rot
        rs.ObjectColor(ey, [0, 255, 0]) #gruen
        rs.ObjectColor(ez, [0, 0, 255]) #blau
        rs.ObjectLayer(ex, layer)
        rs.ObjectLayer(ey, layer)
        rs.ObjectLayer(ez, layer)

        
    else:
        print("****no local_axes are plotted****")



    #CREATE BEWEHRUNGSRICHTUNGEN
    if plot_reinf == True:
        #CREATE BEWEHRUNGSRICHTUNGEN bot
        layer = "Bewehrungsrichtungen_bot"

        if k == 0:
            rs.CurrentLayer(rs.AddLayer(layer))
            rs.DeleteObjects(rs.ObjectsByLayer(layer))
        else:
            rs.CurrentLayer(layer)
        rs.EnableRedraw(False)

        e_xi_bot = rs.AddLine(xyz, add_vectors(xyz, scale_vector(e_xi_bot, axes_scale)))
        e_eta_bot = rs.AddLine(xyz, add_vectors(xyz, scale_vector(e_eta_bot, axes_scale)))


        rs.ObjectColor(e_xi_bot, [255, 0, 0]) #rot
        rs.ObjectColor(e_eta_bot, [0, 0, 255]) #blau

        rs.ObjectLayer(e_xi_bot, layer)
        rs.ObjectLayer(e_eta_bot, layer)

        #CREATE BEWEHRUNGSRICHTUNGEN top
        layer = "Bewehrungsrichtungen_top"

        if k == 0:
            rs.CurrentLayer(rs.AddLayer(layer))
            rs.DeleteObjects(rs.ObjectsByLayer(layer))
        else:
            rs.CurrentLayer(layer)
        rs.EnableRedraw(False)

        e_xi_top = rs.AddLine(xyz, add_vectors(xyz, scale_vector(e_xi_top, axes_scale)))
        e_eta_top = rs.AddLine(xyz, add_vectors(xyz, scale_vector(e_eta_top, axes_scale)))


        rs.ObjectColor(e_xi_top, [255, 0, 0]) #rot
        rs.ObjectColor(e_eta_top, [0, 0, 255]) #blau

        rs.ObjectLayer(e_xi_top, layer)
        rs.ObjectLayer(e_eta_top, layer)
        
    
    else:
        print("****no Reinforcement_axes are plotted****")

