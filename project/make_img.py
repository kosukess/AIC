import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anm
import cv2

h = 224
w = 224
size = (h, w)

img_white = np.full(size, 255, np.uint8)
print(img_white.shape)

img_white[0:int(h/2), 0:int(w/3)]=0
img_white[0:int(h/2), int(w/3):int(2*w/3)]=40
img_white[0:int(h/2), int(2*w/3):w]=80
img_white[int(h/2):h, 0:int(w/3)]=120
img_white[int(h/2):h, int(w/3):int(2*w/3)]=160
img_white[int(h/2):h, int(2*w/3):w]=200

"""
img_white[0:112, 0:72, (1,2)]=0
print(img_white[0,71,:])
img_white[0:112, 72:144, (0, 2)]=0
print(img_white[0,143,:])
img_white[0:112, 144:224, (0, 1)]=0
print(img_white[0,223,:])

count = 2
while count > 0:
    for x in range(width):
        if x < width/3:
            img_white[0:height/2, x:x+1, (1,2)]=0
        elif x < 2*width/3:
            img_white[0:height/2, x:x+1, (0,2)]=0
        else:
            img_white[0:height/2, x:x+1, (0,2)]=0
"""
plt.tick_params(labelbottom=False, labelleft=False, labelright=False, labeltop=False)
plt.tick_params(bottom=False, left=False,right=False, top=False)

plt.imshow(img_white)
plt.show()