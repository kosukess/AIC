import cv2
import numpy as np

class Frame():
    def __init__(self, image, hand_position, gesture_class) -> None:
        self.img = image
        self.hand_position = hand_position
        self.gesture = gesture_class


    def update_hand_position(self, hand_pos):
        self.hand_position = hand_pos