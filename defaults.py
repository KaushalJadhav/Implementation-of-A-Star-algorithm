import os
import numpy as np

# Constants Appendix
pi = np.pi 
inf = np.inf
unit_measure = 1.0
inv_pi = np.reciprocal(pi)
sqrt2=1.41421356237 

#Choice Appendix:
heuristic=1
''' 
Indicates type of Heuristic-
Heuristic=1 Diagonal Distance
Heuristic=2 Dijkstra
Heuristic=3 Euclidean
Heuristic=4 H1
Heuristic=5 Manhattan
'''
heuristic_dict={1:'Diagonal Distance',2:'Dijkstra',3:'Euclidean',4:'H1',5:'Manhattan'}
heuristic_name = heuristic_dict[heuristic]

diag=False # Travel_selection
''' 
Diag = True allows diagonal movement
Choice2=2 prevents diagonal movement
'''

cost='Norm'  # Cost_selection
'''
Cost = 'Norm'/'Normal' for normal given cost
Cost = 'Rot'/'Rotational' for normal given cost
It is a cost method developed assuming that a bot takes some time to turn.
It is designed so that the bot will prefer to go straight (According to the path along which it has entered the current node)
'''

default_cost = inf
unit_cost = unit_measure
rot_factor_180 = 2.0

rot_cost_180 = rot_factor_180*unit_cost
rot_cost_90 = rot_cost_180/2
rot_cost_45 = rot_cost_180/4
rot_cost_135 = rot_cost_45*3
rot_cost_rad = rot_cost_180*inv_pi
rot_cost_deg = rot_cost_180/180

#Color parameters
start_color = [113,204,45]
end_color = [60,76,231]
ob_color = [255,255,255]        # Colour code for obstacles
np_color =[0,0,0]               # Colour code for navigable path
visited_color=[100,0,100]       # Colour code to mark visited pixels
path_pointer=[0,255,0]          # Colour code to mark the final path traversed

#Read Image Path
img_path=r'/home/kaushal/python_work/extr work/Task_1_Low.png'

#For documentation
write_dir = r'/home/kaushal/python_work/extr work'
write_path=os.path.join(write_dir,'astar.txt')

#Write Image Path
img_format = '.png'
img_write_path=f'AStar_{heuristic_name}_Diag_{diag}_Cost_{cost}'+img_format
img_write_path=os.path.join(write_dir,img_write_path)

wait=10000