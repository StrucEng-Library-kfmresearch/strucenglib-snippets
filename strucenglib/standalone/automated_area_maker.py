# Annotate the endpoints of curve objects
import rhinoscriptsyntax as rs
import scriptcontext
import System.Guid, System.Drawing.Color
import math
 
# Inputs
q_Gl=4.8 # In N/mm
b_Bs=1000
h_Strich=200
h_Pl=200
beta=110 # in Grad
layer='Gleis_1_Mittelachse'# Layer with Polyline (Mittelachse des Gleises)

# Basic definitions
#-------------------------------------------------------

# Create layername with load area
area_load_layer=layer+'_area_load'

# Definition eines neues Layers fur alle belasteten Elementmittelpunkte 
if rs.IsLayer(area_load_layer):
    rs.PurgeLayer(area_load_layer)
    scriptcontext.doc.Layers.Add(area_load_layer, System.Drawing.Color.Green)
else:
    scriptcontext.doc.Layers.Add(area_load_layer, System.Drawing.Color.Green)

# Get the curve object from the layer
# ---------------------------------------------------------------------------------
selectcurve = rs.ObjectsByLayer(layer)

# Calculate End and Startpoints
point_start = rs.CurveStartPoint(selectcurve)
point_end = rs.CurveEndPoint(selectcurve)

# Geometrische Berechnung der Lastflachen
# ---------------------------------------------------------------------------------
# Berechnung b_Gl
b_Gl=(b_Bs/2+h_Strich/4+h_Pl/2)*2

# Berechnung b_strich_Gl
b_Strich_Gl=b_Gl/math.sin(math.radians(beta))

# Berechnung der vier Eckpunkte der Lastflache
# ---------------------------------------------------------------------------------
# x Koordinanten
P_A_x=(point_start[0]-b_Strich_Gl/2)
P_B_x=(point_start[0]+b_Strich_Gl/2)
P_C_x=(point_end[0]+b_Strich_Gl/2)
P_D_x=(point_end[0]-b_Strich_Gl/2)

# y Koordinanten
P_A_y=(point_start[1])
P_B_y=(point_start[1])
P_C_y=(point_end[1])
P_D_y=(point_end[1])

# z Koordinanten
P_A_z=(point_start[2])
P_B_z=(point_start[2])
P_C_z=(point_end[2])
P_D_z=(point_end[2])

# Berechnung der vier Eckpunkte der Lastflache und Kurvne in Rhino Layer ploten
# ---------------------------------------------------------------------------------
rs.CurrentLayer(area_load_layer)
rs.AddPolyline([(P_A_x,P_A_y,P_A_z),(P_B_x,P_B_y,P_B_z),(P_C_x,P_C_y,P_C_z),(P_D_x,P_D_y,P_D_z),(P_A_x,P_A_y,P_A_z)])

# Berechnung der Belastung q_k der Gleise
q_k_Gl=q_Gl/b_Gl



