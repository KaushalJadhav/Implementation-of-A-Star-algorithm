import cv2
import numpy as np 
img=np.full((100,200,3),0,dtype=np.uint8)
start_color = [113,204,45]
end_color = [60,76,231]
img[0,50]=start_color
img[99,50]=end_color
for i in range (1,199):
    img[50,i]=(255,255,255)
cv2.namedWindow('sample',cv2.WINDOW_NORMAL)
cv2.imshow('sample',img)
cv2.imwrite('sample_for_Astar.png',img)
cv2.waitKey(10000)