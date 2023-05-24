import numpy as np
import time
import cv2 as cv
from defaults import ob_color

#Read Image
def read_image(img_path):
    return cv2.imread(img_path,cv2.IMREAD_COLOR)

def get_start_end(img,start_color,end_color):
    #Find start point and end point
    start = np.where(np.any(img==start_color,axis=2))
    end = np.where(np.any(img==end_color,axis=2))
    return start,end

def calcSlope(point1,point2):
    return (point2[1]-point1[1])/(point2[0]-point1[0])

def chk_colinear(start,end,p):
    try:
        a=start[1]-end[1]
        b=end[0]-start[0]
        c=start[0]*end[1]-start[1]*end[0]
        return a*point1[0]+b*point1[1]+c
    except:
        raise Exception("startpt and endpt must be indexable and cannot be None ")

def is_end_pt

#check for navigation path
def isinrange(img,position):
    '''
    Returns False if given node is not accessible
    \nElse returns True
    '''
    x,y = position
    if(x>=0 and x<img.shape[0] and y >=0 and y<img.shape[1]):
        return not np.equal(img[x,y],ob_color).all()
    return False

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
    TO DO
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


class Timer(object):
    def __init__(self):
        pass
    def begin(self):
        self.beg = time.begin()
    def finish(self):
        self.fin = time.finish()
    def _print(self):
        print("")