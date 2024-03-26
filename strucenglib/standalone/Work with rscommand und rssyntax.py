 
import rhinoscriptsyntax as rs

import Rhino
import scriptcontext
import System.Guid, System.Drawing.Color
import math

# Bestimmen der Eckpunkte
meshes=rs.Command('_Selmesh _Enter')
selectmeshes = rs.ObjectsByType(rs.filter.mesh)
vertices = rs.MeshVertices(selectmeshes)

# AUfbau Kurve

    for i in selectpt:

        insidept = rs.PointInPlanarClosedCurve(i,rec, plane=rs.CurvePlane(rec), tolerance=10) 
insidept = rs.PointInPlanarClosedCurve(i,rec, plane=rs.CurvePlane(rec), tolerance=10) 

print(vertices)