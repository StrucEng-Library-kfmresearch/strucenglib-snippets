import rhinoscriptsyntax as rs
from compas_fea.structure import Structure
from compas_fea.cad import rhino
from compas.geometry import scale_vector
from compas.geometry import add_vectors
import Rhino
import scriptcontext
import System.Guid, System.Drawing.Color


def area_load_generator(mdl, layer, assoc_load_layer=None, fx=0, fy=0, fz=0, mx=0, my=0, mz=0, scale=1.0):
    load_layer = 'area_load'

    coorx = 2000
    coory = 0
    coorz = 0
    R_tol = 5

    x_coor_all = []
    y_coor_all = []
    z_coor_all = []

    curve = rs.ObjectsByLayer(load_layer)
    print(curve)
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

    # Normalvektot via corrsproduct (N=AB x AC)
    N_x = AB_y * AC_z - AB_z * AC_y
    N_y = AB_z * AC_x - AB_x * AC_z
    N_z = AB_x * AC_y - AB_y * AC_x

    # Koordiantenform (XN= AN ----> N_x*coorx + N_y*coor_y + N_z*coor_z = x_A*N_x + y_A*N_y + z_A*N_z)
    XN = N_x * coorx + N_y * coory + N_z * coorz
    AN = x_A * N_x + y_A * N_y + z_A * N_z

    # Check if Point with coorx, coory and coorz lies on the plane (if XN=AN -> true)
    if XN >= AN - R_tol and XN < AN - R_tol:
        print('yes')

    load_layer_nodes = None
    numbers_of_loaded_nodes = None
    return load_layer_nodes, numbers_of_loaded_nodes
