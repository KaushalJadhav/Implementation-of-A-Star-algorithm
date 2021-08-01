#Astar implementation in Python
#Contributed By Kaushal Jadhav 
#Roll No.-20EC30019
#First Year Undergraduate,Dept. of Electronics and Electrical Communication Engineering, IIT Kharagpur

#ASTAR is a further modification and more advanced than Dijkstra
#It uses Heuristics for time-efficient path planning

#import necessary libraries
import numpy as np
# Numpy module for handling matrices efficiently

import cv2
# Open-CV module to dislay, read and save image

import heapq
#To take advantage of fast and efficient heap methods

import time
#to measure time


'''
Why use heap?
The heap implementation ensures time complexity is logarithmic. Thus push/pop operations are
proportional to  the base-2 Logarithm of number of elements.
Implementation is through a binary tree (Just like a sieve!)
Heap property: Value of node is always smaller than both of its children unlike a binary search tree.
'''
'''
Why Priority Queue?
Because here we have to decide the priority of nodes. So what if we had a queue that adjusts the priority for us!
Earlier attempt was to use a list/collection of nodes and find out the minimum. But using Priority Queue saves time.
'''


#Choice Appendix:
choice1=5
''' 
Choice 1 indicates type of Heuristic-
Choice1=1 Diagonal Distance
Choice1=2 Dijkstra
Choice1=3 Euclidean
Choice1=4 H1
Choice1=5 Manhattan
'''
choice2=2 # Travel_selection
''' 
Choice2=1 means diagonal movement allowed
Choice2=2 means diagonal movement not allowed
'''
choice3=2  # Cost_selection
'''
Choice3=1 means normal given cost
Choice3=2 valid for only Choice2=2
It is a cost method developed assuming that a bot takes some time to turn.
It is designed so that the bot will prefer to go straight (According to the path along which it has entered the current node)
'''

#Read Image Path
img_path=r'/home/kaushal/python_work/extr work/Task_1_Low.png'

heuristic=['Diagonal Distance','Dijkstra','Euclidean','H1','Manhattan']
sqrt2=1.41421356237      #define square root of 2

#For documentation
write_path=r'/home/kaushal/python_work/extr work/astar.txt'
#Write Image Path
img_write_path='AStar_'+str(choice1)+'_'+heuristic[choice1-1]+'_'+'Case-'+str(choice2)
if(choice2==2 and choice3==2):
    img_write_path=img_write_path+'_2'
img_write_path=img_write_path+'.png'

wait=10000

#Define color parameters
start_color = [113,204,45]
end_color = [60,76,231]
ob_color = [255,255,255]        # Colour code for obstacles
np_color =[0,0,0]               # Colour code for navigable path
visited_color=[100,0,100]       # Colour code to mark visited pixels
path_pointer=[0,255,0]          # Colour code to mark the final path traversed

#Read Image
img = cv2.imread(img_path,cv2.IMREAD_COLOR)
#Calculate image size before search
h,w,c = img.shape

#Find start point and end point
b=False
for i in range(h):
    for j in range(w):
        if (img[i,j,0] == start_color[0] and img[i,j,1]==start_color[1] and img[i,j,2]==start_color[2]):
          start = (i,j)
        if (img[i,j,0] == end_color[0] and img[i,j,1] == end_color[1] and img[i,j,2] == end_color[2] ):
          end = (i,j)
          b=True
        if(b):
            break
    if(b):
        break

#Calculate Heuristic Func
def calcHeuristic(point1,point2=None,startpt=None,endpt=None,in_favour_cost=-10):

    '''
 Calculates Heuristic Function according to the value set in choice1.\n
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
    if(choice1==1):
        return max(abs(point1[0] - point2[0]),abs(point1[1] - point2[1]))

    if(choice1==2):
        return 0

    if(choice1==3):
        return ((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)**0.5 

    if(choice1==4):
        '''
        Here minimum cost is assigned to points on the line joining start point and end point.
        For non-colinear points, their distance from the line used.
        '''
        try:
         a=start[1]-end[1]
         b=end[0]-start[0]
         c=start[0]*end[1]-start[1]*end[0]
         if(a*point1[0]+b*point1[1]+c==0):
             return in_favour_cost
         return abs(a*point1[0]+b*point1[1]+c)
        except:
            raise Exception("startpt and endpt must be indexable and cannot be None ") 

    if(choice1==5):
        return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])




def calcCost(point1,point2):
    ''' 
    Calculates cost
    '''
    if(abs(point1[0]-point2[0])==1 and abs(point1[1]-point2[1])==0):
        return 1.0
    if(abs(point1[0]-point2[0])==1 and abs(point1[1]-point2[1])==1):
        return sqrt2
    if(abs(point1[0]-point2[0])==0 and abs(point1[1]-point2[1])==1):
        return 1.0
    if(abs(point1[0]-point2[0])==0 and abs(point1[1]-point2[1])==0):
        return 0.0
    else:
      return np.inf        #Heavily penalized




def calcCost2(child,current,start_point,parent=None): 
    '''
    Special cost function\n
    based on real runtime situation.\n
    Accounts time taken for turning by the bot\n

    '''
    point1=child.position
    point2=current.position
    start_point=start_point.position
    if not (point2[0]==start_point[0] and point2[1]==start_point[1]):
        parent_point=parent.position 
        # Check whether given points- child,current and parent are colinear and whether parent and child are the same.
        # If parent and child are identical then that means the bot will have to turn through 180 degrees which should be penalized.
        if(float(point2[0])==(point1[0]+parent_point[0])/2 and float(point2[1])==(point1[1]+parent_point[1])/2 ):  
            return 1
        if(parent_point[0]==point1[0] and parent_point[1]==point1[1]):
            return 3
        if(point1[0]==point2[0] and point1[1]==point2[1]):
            return 0
        else:
            # Remaining case- Bot will have to turn through 90 degrees.
            if(abs(parent_point[0]-point2[0])<2 and abs(parent_point[1]-point2[1])<2 and abs(point1[0]-point2[0]<2) and abs(point1[1]-point2[1]<2)):
             return 2
            return np.inf            #Handling outliers
    else:
    # Start_point will not have any parent. So need separate cases.
     if(abs(point1[0]-point2[0])==1 and abs(point1[1]-point2[1])==0):
         return 1
     if(abs(point1[0]-point2[0])==0 and abs(point1[1]-point2[1])==1):
         return 1
     if(abs(point1[0]-point2[0])==0 and abs(point1[1]-point2[1])==0):
         return 0
    return np.inf
    



#check for navigation path
def isinrange(img,position):
    '''
    Returns False if given node is not accessible
    \nElse returns True
    '''
    b=False
    x=position[0]
    y=position[1]
    ob_color = [255,255,255]
    if(x>=0 and x<img.shape[0] and y >=0 and y<img.shape[1]):
        b=True
        if(img[x,y,0] ==ob_color[0] and img[x,y,1] ==ob_color[1] and img[x,y,2] ==ob_color[2]):
           b=False
    return b



# class for handling priority queues 
class PriorityQueue :
    '''
    creates a Priority Queue Class
    '''

    def __init__(self):
        '''
        Creates a queue
        '''
        self.Queue=[]

    def isempty(self):
        '''
        Checks if given Queue is empty.
        \nReturns True if Empty
        '''
        if not self.Queue:
            return True
        else:
             return False
    
    def put(self,index):
        '''
        Puts given element onto the queue
        \nUses heapq.heappush for faster aproach.
        '''
        heapq.heappush(self.Queue,index)

    def get(self):
        '''
        Returns the smallest-in-priority element using heapq.heappop
        \n\nComparison based on __lt__ and __gt__ of node class
        '''
        return heapq.heappop(self.Queue)




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





#get neighbourhood according to choice2
def get_nbd(current):
    '''
    returns list of neighbourhood positions
    \nchoice is made based on choice2
    '''
    l=[]

    if(choice2==1):
     for i in range(-1,2):
         for j in range(-1,2):
             position=(current.position[0]+i,current.position[1]+j)
             if (isinrange(img,position)):
                 l.append(position) 

    if(choice2==2):
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
node_matrix=np.empty((h,w),dtype=object)
for i in range(h):
    for j in range(w):
        node_matrix[i,j]=node()
        node_matrix[i,j].position=(i,j)



#main function
def astar(img,startpt,endpt):
    '''
    The main traversing function\n
    returns time taken for traversing
    '''
    #create lists 
    visited=[]
    path=[]

    h,w,c=img.shape

    #create priority queue 
    pt_list=PriorityQueue()
    
    #Initialise start node
    start=node(startpt)
    start.g=0
    start.f=start.h=calcHeuristic(start.position,endpt)
    start.isvisted=True
    node_matrix[startpt]=start
    pt_list.put(start)

    #Start Traversing
    beg=time.time()


    while(not pt_list.isempty()):

        #while the list is not empty obtain the node with smallest f

        current=pt_list.get()

        #Now that current node is not in the list change the corresponding chkpts

        current.is_in_list=False
        current.is_current=True

        #Now to preserve the node use the matrix

        node_matrix[current.position]=current

        #break condition

        if(current.position==endpt):
            break

        #get the neighbourhood points

        nbd_list=get_nbd(current)

        # searching operation 

        for pos in nbd_list:

            nbd=node_matrix[pos]

            #get the temp_cost 

            if(choice2==2 and choice3==2):
                g_temp=current.g+calcCost2(nbd,current,start,current.parent)
            else:
                g_temp=current.g+calcCost(pos,current.position)
            
            # if this newly calculated cost< the stored cost-
            if(g_temp<nbd.g):

                #make note that it is visited

                nbd.isvisted=True

                #if the point is current and the new cost is less than its stored cost-
                #make the current as it's parent and put the nbd node in the pt_list. 
    
                if nbd.is_current:
                    nbd.is_current=False
                    nbd.parent=current
                    nbd.g=g_temp
                    nbd.h=calcHeuristic(nbd.position,endpt)
                    nbd.f=nbd.g+nbd.h
                    nbd.is_in_list=True
                    pt_list.put(nbd)

                # if the nbd node is not current- then put the nbd node in the pt_list (if it is not there) along with setting the chk_points.
                else:
                    nbd.parent=current
                    nbd.g=g_temp
                    nbd.h=calcHeuristic(nbd.position,endpt)
                    nbd.f=nbd.g+nbd.h
                    if(not nbd.is_in_list):
                        pt_list.put(nbd)
                    nbd.is_in_list=True
                    nbd.is_current=False

        # to display progress
        #showPath(img,current,start=start,is_end=False)
        #cv2.waitKey(1)



    # finish traversing   
    finish=time.time()
    print(round(finish-beg,3))

    # display final path
    visited,path,cost=showPath(img,current,True,start,visited,path)
    path.reverse()

    #end with saving the results in a txt document
    documentation(visited,path,finish-beg,cost,start,current,1)
    return finish-beg


def showPath(img,current,is_end:bool,start,visited_list=None,parent_list=None):
    '''
    displays current progress as image if is_end is disabled\n
    if is_end is enabled-\n
    returns visited list and parent list and calculates cost
    '''
    cost=0.0
    visited_color=[100,0,100]
    path_pointer=[0,255,0]

    # to avoid errors
    if(parent_list==None):
        parent_list=[]
    if(visited_list==None):
        visited_list=[]
    

    img2=np.copy(img)

    # display/compile visited path

    for i in range(node_matrix.shape[0]):
        for j in range(node_matrix.shape[1]):
            if(node_matrix[i,j].isvisted==True):
              img2[i,j,0]=visited_color[0]
              img2[i,j,1]=visited_color[1]
              img2[i,j,2]=visited_color[2]
              if(is_end):
                  visited_list.append((i,j))

    while(current.position!=start.position):

        #display image

        temp=current.position
        img2[temp[0],temp[1],0]=path_pointer[0]
        img2[temp[0],temp[1],1]=path_pointer[1]
        img2[temp[0],temp[1],2]=path_pointer[2]

        if(not is_end):
            current=current.position
            continue

        else:
         parent_list.append(temp)
         temp=current.parent
         
         #calculate cost

         if(choice2==2 and choice3==2):
             cost=cost+calcCost2(current,temp,start,temp.parent)
         else:
             cost=cost+calcCost(current.position,temp.position)

         current=temp
    if(is_end):
     parent_list.append(start.position)

    #imshow and imwrite 

    cv2.resize(img2,(1000,1000))    
    cv2.namedWindow('path',cv2.WINDOW_NORMAL)
    cv2.imshow('path',img2)
    if(is_end):
        cv2.imwrite(img_write_path,img2)

    #return the lists and the cost
    return (visited_list,parent_list,cost)


# display option changed according to option

def display(val,option,w=None):
    '''
    write data according to option specified
    '''
    if(option==0):
        print(val)
    else:
        w.write(val)
        w.write('\n')

# Documentation according to option

def documentation(visited_list,parent_list,val,cost,start,end,option):
    '''
    document the data
    '''

    if(option==1):
     #open desired file to write result-
     w=open(write_path,'a')
     w.write('\n')

     #write the data
    display(str(choice1)+')'+heuristic[choice1-1]+' case('+str(choice2)+') -',option,w)
    if(choice2==2 and choice3==2):
        display('Using a different cost function',option,w)
    display('cost of traversing by distance='+str(round(cost,2)),option,w)
    display('cost stored at end point='+str(round(end.f,2)),option,w)
    display('No. of nodes in path='+str(len(parent_list)),option,w)
    display('No of nodes visited='+str(len(visited_list)),option,w)
    display('start point='+str(start.position),option,w)
    display('end point='+str(end.position),option,w)
    display('Nodes in path-',option,w)
    display(str(parent_list),option,w)
    #display('Nodes visited-',option,w)
    #display(str(visited_list),option,w)
    display('time taken for traversing='+str(val),option,w)

    if(option==1):
     #close file
     w.close()


#         ************************************************* Driver Code ************************************************************************
if __name__ == "__main__":
 astar(img,start,end)
 #cv2.waitKey(wait)

#         ************************************************* END ***********************************************************************


'''
The heuristics-
diagonal distance- max(abs(point1[0] - point2[0]),abs(point1[1] - point2[1]))
So it is using max(|x1-x2|,|y1-y2|)
djikstra- Has no heuristic
euclidean- ((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)**0.5  (yes, the very old equation form the school days!)

H1 - It is a non-admissible heuristic developed by me
What it does is that it checks how far you are from the line joining start point and end point. It forces to follow the line
Based on the fact that a line is the shortest path ( in plane-geom)
Now it may not be the case when there are exceptions in the form of obstacles

    a=startpt[1]-endpt[1]   
    b=endpt[0]-startpt[0]
    c=startpt[0]*endpt[1]-startpt[1]*endpt[0]
    if(a*point[0]+b*point[1]+c==0):
        return -10
    return abs(a*point[0]+b*point[1]+c)

So as it is evident it will force to follow the line joining startpt and endpt.

Manhattan- also called city-block distance 
abs(point1[0] - point2[0]) + abs(point1[1] - point2[1]) 
or |x1-x2|+|y1-y2|

'''

'''
Note about the cost function- 
In real life a bot will take some time to turn. The actual time taken will depend on various parameters
I have assumed the change in state ( from travelling straight to the state of turning to the left/right) as taking 0-time delay
So 
if deviation=90 degrees returns 2
if deviation=0 degrees either will return 1 or 0
if deviation is 180 degrees returns 3

'''
#references-
'''
1) http://robotics.caltech.edu/wiki/images/e/e0/Astar.pdf
2) https://cs.stanford.edu/people/eroberts/courses/soco/projects/2003-04/intelligent-search/astar.html

''' 