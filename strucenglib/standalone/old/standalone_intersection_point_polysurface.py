from Geometry3D import *


# node a as an input
a = Point(0.1,0,-0.000000000000000000001)

a1 = Point(0,0,0)
b1 = Point(1,0,0)
c1 = Point(1,1,0)
d1 = Point(0,1,0)
plane2 = ConvexPolygon((a1,b1,c1,d1))

inter = intersection(a,plane2)
print(inter) # results I needed

# Check result points, which correspond to the nodes coordinates


# visualize planes 
r = Renderer()
r.add((plane2,'b',2),normal_length = 0)
r.show()

