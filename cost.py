from defaults import default_cost,sqrt2,rot_cost_180,rot_cost_90,rot_cost_45,rot_cost_135,unit_cost

def calcCost(point1,point2):
    ''' 
    Calculates cost
    '''
    if(abs(point1[0]-point2[0])==1 and abs(point1[1]-point2[1])==0):
        return unit_cost                                                 # unit cost is 1.0
    if(abs(point1[0]-point2[0])==0 and abs(point1[1]-point2[1])==1):
        return unit_cost
    if(abs(point1[0]-point2[0])==0 and abs(point1[1]-point2[1])==0):
        return 0.0
    return default_cost        #Heavily penalized

def calcCost_diag(point1,point2):
    ''' 
    Calculates cost
    '''
    if(abs(point1[0]-point2[0])==1 and abs(point1[1]-point2[1])==0):
        return unit_cost
    if(abs(point1[0]-point2[0])==1 and abs(point1[1]-point2[1])==1):
        return sqrt2*unit_cost
    if(abs(point1[0]-point2[0])==0 and abs(point1[1]-point2[1])==1):
        return unit_cost
    if(abs(point1[0]-point2[0])==0 and abs(point1[1]-point2[1])==0):
        return 0.0
    return default_cost        #Heavily penalized

def calcCost_rot(child,current,start_point,parent=None): 
    '''
    Special cost function\n
    based on real runtime situation.\n
    Accounts time taken for turning by the bot\n

    '''
    if not current==start_point:
        assert parent is not None
        # Check whether given points- child,current and parent are colinear and whether parent and child are the same.
        # If parent and child are identical then that means the bot will have to turn through 180 degrees which should be penalized.
        if(float(current[0])==(child[0]+parent[0])/2 and float(current[1])==(child[1]+parent[1])/2 ):  
            return unit_cost
        if parent==child:
            return unit_cost+rot_cost_180 # rot_cost_180 == 2
        if child==current:
            return 0
        # Remaining case- Bot will have to turn through 90 degrees.
        if calcSlope(current,parent)*calcSlope(child,current)==-1:
            return unit_cost+rot_cost_90
        return default_cost            #Handling outliers
    
    # Start_point will not have any parent. So need separate cases.
    return calcCost(child,start_point)

def calcCost_rot_diag(child,current,start_point,parent=None): 
    '''
    Special cost function\n
    based on real runtime situation.\n
    Accounts time taken for turning by the bot\n

    '''
    if not current==start_point:
        assert parent is not None
        # Check whether given points- child,current and parent are colinear and whether parent and child are the same.
        # If parent and child are identical then that means the bot will have to turn through 180 degrees which should be penalized.
        if(float(current[0])==(child[0]+parent[0])/2 and float(current[1])==(child[1]+parent[1])/2 ):  
            return unit_cost
        if parent==child:
            return unit_cost+rot_cost_180 # rot_cost_180 == 2
        if child==current:
            return 0
        # Remaining case- Bot will have to turn through 90 degrees.
        if calcSlope(current,parent)*calcSlope(child,current)==-1:
            return unit_cost+rot_cost_90
        return default_cost            #Handling outliers
    
    # Start_point will not have any parent. So need separate cases.
    return calcCost(child,start_point)