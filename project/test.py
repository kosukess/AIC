import cv2
import time
from jetcam.usb_camera import USBCamera
from jetcam.utils import bgr8_to_jpeg

WIDTH = 224
HEIGHT = 224
camera = USBCamera(capture_fps=30, capture_device=0)

while(True):
    before = time.time()
    frame = camera.read()
    #frame = frame[0:edge, 0:edge]
    #size = (224,224)
    #frame = cv2.resize(frame,size)
    cv2.imshow("image", frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    after = time.time()
    print("fps: ", 1 / (after-before))