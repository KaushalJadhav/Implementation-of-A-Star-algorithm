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


#Calculate image size before search
h,w,c = img.shape



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