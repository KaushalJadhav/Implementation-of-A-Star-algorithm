class node:
    '''
    class for handling nodes\n
    @param index=input default=None\nstands for position\n
    @param is_in_list and is_current are check-points\n
    @param parent=input default=None\n
    @param f,g,h=cost\n
    @param h stands for Heuristic cost\n
    @param f stands for total cost
    '''
    #constructor
    def __init__(self,index=None,parent=None):
        # Initialise params
        self.position=index  #position/location
        self.is_in_list=False  # chkpt
        self.is_current=False  #chkpt
        self.parent=parent     #parent node of the node
        '''
        f,g,h are the costs.
        f=total cost=Sum of traversal_cost and heuristic cost
        g=traversal cost that is the cost of traversing from current node to child node
        h=Heuristic cost  predicted by the Heuristic function
        '''
                                  # __
        self.f=np.inf             #   |
        self.g=np.inf             #   | initialise cost
        self.h=np.inf             # __|
        self.isvisted=False
    
    def __lt__(self,other):
        '''
        overload operator < (check parameter=cost)
        '''
        return self.f<other.f
    
    def __gt__(self,other):
        '''
        overload operator > (check parameter=cost)
        '''
        return self.f>other.f
    
    def __getitem__(self, idx):
        assert idx ==0 or idx==1
        return self.position[idx]
    
    def __setitem__(self, key, newvalue):
        assert idx ==0 or idx==1
        self.position[idx] = newvalue

#get neighbourhood according to choice2
def get_nbd(current,choice):
    '''
    returns list of neighbourhood positions
    \nchoice is made based on choice2
    '''
    l=[]

    if choice:
        for i in range(-1,2):
            for j in range(-1,2):
                position=(current.position[0]+i,current.position[1]+j)
                if isinrange(img,position):
                    l.append(position) 

    else:
        for i in range(-1,2):
            position=(current.position[0]+i,current.position[1])
            if (isinrange(img,position)):
                l.append(position)
        for j in range(-1,2):
            if(j==0): #skip repetition
                continue
            position=(current.position[0],current.position[1]+j)
            if (isinrange(img,position)):
                l.append(position) 
          
    return l

# create a matrix of objects
def init_matrix():
    node_matrix=np.empty((h,w),dtype=object)
    for i in range(h):
        for j in range(w):
            node_matrix[i,j]=node()
            node_matrix[i,j].position=(i,j)
    return node_matrix