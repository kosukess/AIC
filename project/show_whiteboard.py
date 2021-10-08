import numpy as np
import cv2


size = [hight, width, 3]

img_white = np.full(size, fill_values = 255, dtype ='uint8')

cv2.namedWindow('white board', cv2.WINDOW_NORMAL)
cv2.imshow('white board', img_white)
cv2.waitKey(0)
cv2.destroyAllWindows()