import rhinoscriptsyntax as rs
from compas_fea.structure import Structure
from compas_fea.cad import rhino
from compas.geometry import scale_vector
from compas.geometry import add_vectors
import Rhino
import scriptcontext
import System.Guid, System.Drawing.Color


def area_load_generator(mdl, layer, fx=0, fy=0, fz=0, mx=0, my=0, mz=0, scale=1.0):
    numbers_of_loaded_nodes = 0

    # Preapre for grafical oputput
    v = scale_vector([fx, fy, fz], -scale * 0.001)

    R_tol = 5  # Tolerance for the plane check

    # Layer with curve which define the loaded area
    load_layer = layer

    # Create layername with loaded nodes
    load_layer_nodes = load_layer + '_loaded_nodes'
    load_layer_nodes_arrows = load_layer + '_loaded_nodes_arrows'

    # -------------------------------------------------------
    # Extract Point coor from the curve in load_layer)
    x_coor_all = []
    y_coor_all = []
    z_coor_all = []

    curve = rs.ObjectsByLayer(load_layer)
    if rs.IsCurve(curve):
        points = rs.CurvePoints(curve)

    # Determine three points of the curve
    for i in range(0, 3):
        print(i)
        x_coor = points[i][0]
        y_coor = points[i][1]
        z_coor = points[i][2]
        x_coor_all.append(x_coor)
        y_coor_all.append(y_coor)
        z_coor_all.append(z_coor)

    # Define the three points A=x_A,y_A,z_A; B=x_B,y_B,z_B; C=x_C,y_C,z_C
    x_A = x_coor_all[0]
    y_A = y_coor_all[0]
    z_A = z_coor_all[0]

    x_B = x_coor_all[1]
    y_B = y_coor_all[1]
    z_B = z_coor_all[1]

    x_C = x_coor_all[2]
    y_C = y_coor_all[2]
    z_C = z_coor_all[2]

    # Vectors AB=[AB_x, AB_y, AB_z] and AC=[AC_x, AC_y, AC_z]
    AB_x = x_B - x_A
    AB_y = y_B - y_A
    AB_z = z_B - z_A

    AC_x = x_C - x_A
    AC_y = y_C - y_A
    AC_z = z_C - z_A

    # Normalvektor via corrsproduct (N=AB x AC)
    N_x = AB_y * AC_z - AB_z * AC_y
    N_y = AB_z * AC_x - AB_x * AC_z
    N_z = AB_x * AC_y - AB_y * AC_x
    AN = x_A * N_x + y_A * N_y + z_A * N_z
    print(N_x)
    print(N_y)
    print(N_z)
    print(AN)
    # -------------------------------------------------------
    # extract all points from all associated layers
    rs.Command('_ExtractPt _Selmesh _Enter')

    # set current layer to load_layewr
    rs.CurrentLayer(load_layer)

    # Select layer with polycon
    rec = rs.ObjectsByLayer(load_layer)

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

    # MAINCALCULATION: Filter and save all control points inside polycon
    points = []
    coor_xyz = []

    selectpt = rs.ObjectsByType(rs.filter.point)

    i_lauf = -1
    test_lauf = 0
    for i in selectpt:
        points.append(i)
        i_lauf = i_lauf + 1

        insidept = rs.PointInPlanarClosedCurve(points[i_lauf], rec, plane=None,
                                               tolerance=10)  # 1. Check point if is in curve
        if insidept == 0:
            # print("The point is NOT inside the closed surve")
            pass
        else:
            # print ("The point is on the closed curve.")
            # test_lauf=test_lauf+1
            coor = rs.PointCoordinates(i)
            rs.CurrentLayer(load_layer_nodes)

            coorx = coor[0]
            coory = coor[1]
            coorz = coor[2]
            xyz = [coorx, coory, coorz]
            # Koordiantenform (XN= AN ----> N_x*coorx + N_y*coor_y + N_z*coor_z = x_A*N_x + y_A*N_y + z_A*N_z)
            XN = N_x * coorx + N_y * coory + N_z * coorz

            coor_xyz.append([coorx, coory, coorz])
            coor_xyz_red = coor_xyz[: -1]

            # print('1')
            # print(XN)
            # print(AN)
            # Check if Point with coorx, coory and coorz lies on the plane (if XN=AN -> true)
            # 3. check if the point is already checked/set (this avoid problem with angrezende Meshes wo zwei Punkte entstehen durch die extraktion)
            print(coor_xyz)

            if XN >= AN - R_tol and XN < AN + R_tol:  # 2. check point if is in curve-plane
                numbers_of_loaded_nodes = numbers_of_loaded_nodes + 1
                rs.AddPoint((coorx, coory, coorz))
                rs.CurrentLayer(load_layer_nodes_arrows)
                line = rs.AddLine(xyz, add_vectors(xyz, v))
                rs.CurveArrows(line, 1)
                rs.CurrentLayer(load_layer_nodes)
            else:
                pass

    rs.Command('_Delete')  # Del selected control point

    return load_layer_nodes, numbers_of_loaded_nodes
