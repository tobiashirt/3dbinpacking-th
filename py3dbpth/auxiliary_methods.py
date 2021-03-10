#from decimal import Decimal
from .constants import Axis
import math

def rect_overlap(item1, item2, x, y):
    
    ix = 0
    iy = 0
    
    if rect_intersect(item1,item2,x,y):
        d1 = item1.get_dimension()
        d2 = item2.get_dimension()
        
        x1 = item1.position[x] + d1[x]
        y1 = item1.position[y] + d1[y]
        x2 = item2.position[x] + d2[x]
        y2 = item2.position[y] + d2[y]
    
        ix = min(x1,x2) - max(item1.position[x],item2.position[x])
        iy = min(y1,y2) - max(item1.position[y],item2.position[y])
    
        return ix * iy
    
    else:
        return -1

def rect_intersect(item1, item2, x, y):
    d1 = item1.get_dimension()
    d2 = item2.get_dimension()

    cx1 = item1.position[x] + d1[x]/2
    cy1 = item1.position[y] + d1[y]/2
    cx2 = item2.position[x] + d2[x]/2
    cy2 = item2.position[y] + d2[y]/2

    ix = max(cx1, cx2) - min(cx1, cx2)
    iy = max(cy1, cy2) - min(cy1, cy2)

    return ix < (d1[x]+d2[x])/2 and iy < (d1[y]+d2[y])/2


def intersect(item1, item2):
    return (
        rect_intersect(item1, item2, Axis.WIDTH, Axis.HEIGHT) and
        rect_intersect(item1, item2, Axis.HEIGHT, Axis.DEPTH) and
        rect_intersect(item1, item2, Axis.WIDTH, Axis.DEPTH)
    )

def distance_L2(p1, p2):
    
    d = math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2+(p1[2]-p2[2])**2)    
    
    return d
