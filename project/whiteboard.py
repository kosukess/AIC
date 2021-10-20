#マウスの位置とジェスチャークラスを受け取る
#マウス位置＝mouse_position
#ジェスチャークラス=gesture_class
#受け取ったもので描く・消す・スイッチ
#描画したホワイトボードの表示

import numpy as np
import cv2
import socket
import pickle
import sys

"""[summary]

"""

class Whiteboard():
    def __init__(self,h=480, w=640):
        self.pre_gesture = ""
        self.rectangle = []
        self.h = h
        self.w = w
        self.all_w = w+80
        if self.h < 480:
            print("height of window must be larger than 480")
            sys.exit()
        self.func_width = 80
        self.white_board = np.full([self.h, self.w, 3], 255, np.uint8)
        self.draw_gesture = "draw"
        self.erase_gesture = "func"
        self.threshold = 40
        
        # zoom
        self.least_width = 50
        self.max_magni = self.w/self.least_width
        self.current_magni = 1.
        self.x_white_board = 0
        self.y_white_board = 0
        self.upper_left = (0, 0)
        self.lower_right = (self.h, self.w)
        self.white_board_magni = self.white_board.copy() # 追加

        # cursor
        self.cursor_color = (0,0,0)
        self.pre_cursor = None
        self.cursor_size = 1
        
        # button
        self.draw_state = True
        self.button_board = np.full([self.h, 80, 3], 255, np.uint8)
        self.init_button(self.button_board)
        self.button_blwh = np.full([self.h, self.all_w], 255, np.uint8)
        self.make_button_blwh(self.button_blwh)
        self.pen_size = 1
        self.max_pen_size = 50

        # udp
        self.M_SIZE = 1024
        host = '192.168.55.100'
        port = 30000
        localddr = (host, port)
        self.sock = socket.socket(socket.AF_INET, type=socket.SOCK_DGRAM)
        self.sock.bind(localddr)
        print('create socket')

    
    def __del__(self):
        self.sock.close()


    def receive_data(self):
        """
        message[0]: cursor data [0]: x, [1]: y
        message[1]: gesture class name

        """        
        message, cli_addr = self.sock.recvfrom(self.M_SIZE)
        message = pickle.loads(message)
        return message[0], message[1]


    def calcAbs(self, difvec):
        return np.sqrt(difvec[0]**2+difvec[1]**2)


    def cursor_process(self, mouse_position):
        cur_cursor = np.array([int(mouse_position[0]*(self.all_w/224)), int(mouse_position[1]*(self.h/244))])
        if cur_cursor[0] >= self.all_w:
            cur_cursor[0] = self.all_w - 1
        if cur_cursor[1] >= self.h:
            cur_cursor[1] = self.all_w - 1
          
        return cur_cursor


    def execute_function(self, cur_cursor, gesture_class):
        if cur_cursor[0] < self.w:
            self.cursor_size = self.pen_size
            self.draw(cur_cursor, gesture_class)
        else:
            self.cursor_size = 2
            self.switch(cur_cursor, gesture_class)


    def embed(self, upper_left, lower_right):
        print("embed")
        self.white_board[upper_left[1]:lower_right[1], upper_left[0]:lower_right[0]] = \
            cv2.resize(self.white_board_magni, dsize=(lower_right[0]-upper_left[0], lower_right[1]-upper_left[1]))


    def zoomin(self, cur_cursor, gesture_class):
        self.embed(self.upper_left, self.lower_right)
        if gesture_class == "zoom-in": # gesture_classが"zoom in"なら
            if self.current_magni < self.max_magni:
                if cur_cursor[0] == self.all_w and cur_cursor[1] == 0:
                    # 倍率計算
                    #while self.current_magni < self.max_magni:
                    self.current_magni *= 1.01 # 倍率を1.01倍にする
                    current_width = int(self.w/self.current_magni) # 1.01倍後の現在の幅
                    current_height = int(self.h/self.current_magni) # 1.01倍後の現在の高さ

                    # 拡大後のフレーム内での座標計算                        
                    upper_left_x = int(cur_cursor[0] / 101) # 左上のx座標
                    upper_left_y = int(cur_cursor[1] / 101) # 左上のy座標
                    upper_left = np.array([upper_left_x, upper_left_y])
                    lower_right_x = upper_left_x + current_width # 右下のx座標
                    lower_right_y = upper_left_y + current_height # 右下のx座標
                    lower_right = np.array([lower_right_x, lower_right_y])
                    self.white_board_magni = self.white_board[int(upper_left_y):int(lower_right_y), int(upper_left_x):int(lower_right_x)]

                    # 元画像内での座標計算
                    self.upper_left += upper_left/self.current_magni # 元画像での左上の座標
                    self.lower_right += lower_right/self.current_magni # 元画像での右下の座標


    def draw(self, cur_cursor, gesture_class):
        if cur_cursor[0] == self.all_w and cur_cursor[1] == 0:
            self.pre_cursor = None

        if self.pre_cursor is None:
            self.pre_cursor = cur_cursor

        elif self.calcAbs(cur_cursor - self.pre_cursor) > self.threshold:
            self.pre_cursor = None

        elif gesture_class==self.draw_gesture and self.draw_state:
            cv2.line(self.white_board_magni,self.pre_cursor, cur_cursor, (0,0,0), int(self.pen_size))
            self.pre_cursor = cur_cursor

        elif gesture_class==self.draw_gesture and not self.draw_state:
            cv2.line(self.white_board_magni,self.pre_cursor, cur_cursor, (255,255,255), int(self.pen_size))
            self.pre_cursor = cur_cursor
   

    def switch(self, cur_cursor, gesture_class):
        self.pre_cursor = cur_cursor
        if gesture_class == "func":
            # draw
            if self.button_blwh[cur_cursor[1]][cur_cursor[0]] == 0:
                print("draw pushed")
                self.draw_state = True
            # erase
            elif self.button_blwh[cur_cursor[1]][cur_cursor[0]] == 40:
                print("erase pushed")
                self.draw_state = False
            # size
            elif self.button_blwh[cur_cursor[1]][cur_cursor[0]] == 80:
                self.pen_size = (450-cur_cursor[1]) * self.max_pen_size / 180
                print("pen size changed: ", self.pen_size)


    def show_whiteboard(self, cursor):
        cursor_white_board = cv2.resize(self.white_board_magni, dsize=(self.w, self.h))
        self.update_button(self.button_board)
        show_img = cv2.hconcat([cursor_white_board, self.button_board])
        cv2.circle(show_img, cursor, int(self.cursor_size), self.cursor_color, 2)
        cv2.imshow('white board (Push \"Q\" to quit)', show_img)       
        key = cv2.waitKey(1)
        return key

    
    def loop_finish_process(self, cursor, gesture):
        self.pre_cursor = cursor
        self.pre_gesture = gesture

        
    def make_button_blwh(self, img):
        # draw = 0
        cv2.rectangle(img, (self.w+10, 50), (self.w+70, 110), 0, thickness=-1, lineType=cv2.LINE_4)

        # erase = 40
        cv2.rectangle(img, (self.w+10, 140), (self.w+70, 200), 40, thickness=-1, lineType=cv2.LINE_4)

        # size = 80
        cv2.rectangle(img, (self.w+10, 270), (self.w+70, 450), 80, thickness=-1, lineType=cv2.LINE_4)


    def init_button(self, img):
        cv2.line(img, (0, 0), (0, 480), (0, 0, 0), thickness=2, lineType=cv2.LINE_4)
        cv2.rectangle(img, (10, 50), (70, 110), (0, 0, 0), thickness=2, lineType=cv2.LINE_4)
        cv2.rectangle(img, (10, 140), (70, 200), (0, 0, 0), thickness=2, lineType=cv2.LINE_4)
        cv2.putText(img,
                    text='size',
                    org=(5, 240),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=0.5,
                    color=(0, 0, 0),
                    thickness=1,
                    lineType=cv2.LINE_4)
        cv2.putText(img,
                    text=str(self.max_pen_size),
                    org=(30, 265),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=0.5,
                    color=(0, 0, 0),
                    thickness=1,
                    lineType=cv2.LINE_4)
        cv2.rectangle(img, (30, 270), (50, 450), (0, 0, 0), thickness=1, lineType=cv2.LINE_4)
        cv2.putText(img,
                    text='0',
                    org=(35, 465),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=0.5,
                    color=(0, 0, 0),
                    thickness=1,
                    lineType=cv2.LINE_4)


    def update_button(self, img):
        if self.draw_state:
            draw_button_color = (230,230,230)
            eraser_button_color = (255,255,255)
        else:
            eraser_button_color = (230,230,230)
            draw_button_color = (255,255,255)

        # draw
        cv2.rectangle(img, (10, 50), (70, 110), draw_button_color, thickness=-1, lineType=cv2.LINE_4)
        cv2.putText(img,
                    text='pen',
                    org=(25, 85),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=0.5,
                    color=(0, 0, 0),
                    thickness=1,
                    lineType=cv2.LINE_4)

        # eraser
        cv2.rectangle(img, (10, 140), (70, 200), eraser_button_color, thickness=-1, lineType=cv2.LINE_4)
        cv2.putText(img,
                    text='eraser',
                    org=(15, 175),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=0.5,
                    color=(0, 0, 0),
                    thickness=1,
                    lineType=cv2.LINE_4)

        # size
        gray_wid = int(180 / self.max_pen_size * self.pen_size)
        cv2.rectangle(img, (30, 270), (50, 450-gray_wid), (255, 255, 255), thickness=-1, lineType=cv2.LINE_4)
        cv2.rectangle(img, (30, 450-gray_wid), (50, 450), (230, 230, 230), thickness=-1, lineType=cv2.LINE_4)