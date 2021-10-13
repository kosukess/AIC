#マウスの位置とジェスチャークラスからホワイトボードに出力
#draw_or_notを受け取るかどうか
#ボタンも


import numpy as np
import cv2

class Whiteboard():
    def __init__(self,h=224, w=224):
        self.rectangle = []
        self.h = h
        self.w = w
        self.draw_or_not = 1
        self.white_board = np.full([self.h, self.w, 3], 255, np.uint8)
        
    def draw(self, joints, gesture_class):
            if self.draw_or_not == -1:
                if gesture_class=="line":
                    if joints[5]!=[0,0]:
                        self.rectangle.append([int(joints[self.cursor_joint][0]*(self.w/224)), int(joints[self.cursor_joint][1])*(self.h/244)])

                if (len(self.rectangle)) > 0:
                    if self.rectangle[-1]!=[0,0]:
                        cv2.line(self.white_board,self.rectangle[-2], self.rectangle[-1], (0,0,0), 2)
            if self.draw_or_not == 1:
                if gesture_class=="line":
                    if joints[5]!=[0,0]:
                        self.rectangle.append([int(joints[self.cursor_joint][0]*(self.w/224)), int(joints[self.cursor_joint][1])*(self.h/244)])

                if len(self.rectangle) > 0:
                    if self.rectangle[-1]!=[0,0]:
                        cv2.line(self.white_board, self.rectangle[-2], self.rectangle[-1], (255,255,255), 5)

    def show_whiteboard(self):
        cv2.imshow('white board', self.white_board)
        key = cv2.waitKey(1)
        if  key == ord('q'):
            ggg