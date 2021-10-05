import numpy as np
import cv2


size = [hight, width, 3]

img_white = np.full(size, fill_values = 255, dtype ='unit8')

#for py
cv2.namedWindow('white board', cv2.WINDOW_NORMAL)
cv2.imshow('white board', img_white)


#for ipynb
import cv2
from google.colab.patches import cv2_imshow

cv2_imshow(img_white)