import numpy as np
from utils import chk_colinear

def subtract_tup(point1,point2):
    return (point2[0]-point1[0],point2[1]-point1[1])

def calcHeuristic(heuristic=1,point1,point2=None,startpt=None,endpt=None,in_favour_cost=-10):

    '''
 Calculates Heuristic Function according to the value set in heuristic.\n
 Calculates the Heuristic between points point1 and point2

 choice==1 Diagonal Distance\n
 returns max(abs(point1[0] - point2[0]),abs(point1[1] - point2[1]))\n
 choice==2 Dijkstra\n
 returns 0 (No Heuristic)\n
 Choice==3 Euclidean=3\n
 returns ((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)**0.5\n
 Can delete **0.5 according to need\n
 Choice==4 H1   ...A non-admissible Heuristic.\n
 H1 is a non-Admissible Heuristic.\n Based on distance between point and a line.\nWorks well with no obstacles\n
 Choice==5 Manhattan\n
 returns abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])\n
 @param startpt and endpt required for H1\n
 @param in_favour_cost (default=-10). Specifies the cost returned if point1 lies on the line joining start point and end point\n
    '''
    if(heuristic==1):
        return np.max(np.abs(subtract_tup(point1,point2)))

    if(heuristic==2):
        return 0.0

    if(heuristic==3):
        return np.linalg.norm(subtract_tup(point1,point2))

    if(heuristic==4):
        '''
        Here minimum cost is assigned to points on the line joining start point and end point.
        For non-colinear points, their distance from the line used.
        '''
        cost = chk_colinear(startpt,endpt,point1)
        if(cost==0): return in_favour_cost
        return np.abs(cost)

    if(heuristic==5):
        return np.sum(np.abs(subtract_tup(point1,point2)))