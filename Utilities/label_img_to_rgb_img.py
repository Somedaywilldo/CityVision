import cv2
import numpy as np
import os
from matplotlib import pyplot as plt


color_map=[
   [128, 64, 128],  # road
   [244, 35, 232],   # sidewalk
   [70, 70, 70],     # building
   [102, 102, 156],  # wall
   [190, 153, 153],  # fence
   [153, 153, 153],  # pole
   [250, 170, 30],   # traffic light
   [220, 220, 0],    # traffic sign
   [107, 142, 35],   # vegetation
   [152, 251, 152],  # terrain
   [70, 130, 180],   # sky
   [220, 20, 60],    # person
   [255, 0, 0],      # rider
   [0, 0, 142],      # car
   [0, 0, 70],       # truck
   [0, 60, 100],     # bus
   [0, 80, 100],     # train
   [0, 0, 230],      # motorcycle
   [119, 11, 32],    # bicycle
]

def convert(label_img):
   rgb_img = label_img
   for i in range(len(rgb_img)):
      for j in range(len(rgb_img[0])):
         rgb_img[i][j]=color_map[label_img[i][j][0]]
   return rgb_img



label_img = cv2.imread('100130J91503170SCENE015_0_%s.png'%("label"))
cv2.imwrite('100130J91503170SCENE015_0_%s.png'%("rgb"),rgb_img)

