#マウスの位置とジェスチャークラスを受け取る
#マウス位置＝mouse_position
#ジェスチャークラス=gesture_class
#受け取ったもので描く・消す・スイッチ
#描画したホワイトボードの表示

import numpy as np
import cv2
import socket
import pickle

"""[summary]

"""

class Whiteboard():
    def __init__(self,h=224, w=224):
        self.pre_gesture = ""
        self.rectangle = []
        self.h = h
        self.w = w
        self.draw_or_not = 1
        self.white_board = np.full([self.h, self.w, 3], 255, np.uint8)
        self.botton_board = np.full([self.h, self.w], 255, np.uint8)
        self.botton_board[0:int(h/2), 0:int(w/3)]=0
        self.botton_board[0:int(h/2), int(w/3):int(2*w/3)]=40
        self.botton_board[0:int(h/2), int(2*w/3):w]=80
        self.botton_board[int(h/2):h, 0:int(w/3)]=120
        self.botton_board[int(h/2):h, int(w/3):int(2*w/3)]=160
        self.botton_board[int(h/2):h, int(2*w/3):w]=200

        # udp
        self.M_SIZE = 1024
        host = '192.168.55.100'
        port = 30000
        locaddr = (host, port)
        self.sock = socket.socket(socket.AF_INET, type=socket.SOCK_DGRAM)
        self.sock.bind(locaddr)
        print('create socket')

    def receive_data(self):
        """
        message[0]: cursor data [0]: x, [1]: y
        message[1]: gesture class name

        """        
        message, cli_addr = self.sock.recvfrom(self.M_SIZE)
        message = pickle.loads(message)
        return message


    def draw(self, mouse_position, gesture_class):
            if self.draw_or_not == -1:
                if gesture_class=="peace":
                    if mouse_position[0] != 0 and mouse_position[1] != 0:
                        self.rectangle.append([int(mouse_position[0]*(self.w/224)), int(mouse_position[1])*(self.h/244)])

                if (len(self.rectangle)) > 0:
                    if self.rectangle[-1]!=[0,0]:
                        cv2.line(self.white_board,self.rectangle[-2], self.rectangle[-1], (0,0,0), 2)

            if self.draw_or_not == 1:
                if gesture_class=="peace":
                    if mouse_position[0] != 0 and mouse_position[1] != 0:
                        self.rectangle.append([int(mouse_position[0]*(self.w/224)), int(mouse_position[1])*(self.h/244)])

                if len(self.rectangle) > 0:
                    if self.rectangle[-1]!=[0,0]:
                        cv2.line(self.white_board, self.rectangle[-2], self.rectangle[-1], (255,255,255), 5)
   
    def switch(self, gesture_class):
        if (gesture_class == "fist")and(self.pre_gesture == "stop"):
            x_position, y_position = int(self.mouse_position[0]*(self.w/224)), int(self.mouse_position[1]*(self.h/224))
            color = self.botton_board[x_position, y_position]
            if color == 0:
                self.draw_or_not = self.draw_or_not*-1
        self.pre_gesture = gesture_class

    def show_whiteboard(self):
        cv2.imshow('white board', self.white_board)       
        key = cv2.waitKey(1)
        return key
        