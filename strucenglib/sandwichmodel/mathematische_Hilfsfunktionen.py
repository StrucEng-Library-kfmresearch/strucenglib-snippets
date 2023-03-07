#----------------------------------------------------------------------------------------------------------------------------------
#Mathematische Hilfsfunktionen
#----------------------------------------------------------------------------------------------------------------------------------
import math

# Winkelfunktionen fuer Winkel zwischen 0 und 90 in Grad:
def angle_check(x):
    if 0<x<=180:
        return x
    else:
        raise ValueError("angle is out of range")  

def sin(x):
    if x == 90:
        return 1.0
    elif x == 0:
        return 0.0
    else:
        return math.sin(math.radians(x))

def cos(x):
    if x == 90:
        return 0.0
    elif x == 0:
        return 1.0
    else:
        return math.cos(math.radians(x))

def tan(x):
    if x == 90:
        raise ValueError("tan(90) is not defined")
    elif x == 0:
        return 0.0
    elif x == 45:
        return 1.0
    else:
        return math.tan(math.radians(x))

def cot(x):
    if x == 90:
        return 0.0
    elif x == 45:
        return 1.0
    elif x == 0:
        raise ValueError("cot(0) is not defined")
    else:
        return 1/math.tan(math.radians(x))

def arccot(x):
    if x == 0.0:
        return 90
    else:
        return math.degrees(math.atan(1/x))


def e_xi(ex,ey,ez,alpha): # gibt Bewehrungsrichtung in globalen koordinaten wieder M*e_xi_lokal
    e_xi_x = ex[0]*cos(alpha)+ey[0]*sin(alpha)+ez[0]*0
    e_xi_y = ex[1]*cos(alpha)+ey[1]*sin(alpha)+ez[1]*0
    e_xi_z = ex[2]*cos(alpha)+ey[2]*sin(alpha)+ez[2]*0
    e_xi = [e_xi_x, e_xi_y, e_xi_z]
    return e_xi

