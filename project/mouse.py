import numpy as np
import cv2
import socket
import pickle
import pyautogui
import time

"""[summary]

"""

class Mouse():
    def __init__(self,h=224, w=224):
        self.h = h
        self.w = w
        self.screenWidth, self.screenHeight = pyautogui.size()
        self.pre_gesture = 'none'
        self.p_sc = 0
        self.cur_x, self.cur_y = pyautogui.position()
        self.fixed_x, self.fixed_y = pyautogui.position()
        pyautogui.FAILSAFE = False
        self.t0 = time.time()

        
        self.threshold = 30

        # udp
        self.M_SIZE = 1024
        host = '192.168.55.100'
        port = 30000
        locaddr = (host, port)
        self.sock = socket.socket(socket.AF_INET, type=socket.SOCK_DGRAM)
        self.sock.bind(locaddr)
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

    def cursor_process(self, mouse_position):
        cur_cursor = np.array([mouse_position[0]*(self.screenWidth/self.w), mouse_position[1]*(self.screenHeight/self.h)]).astype(np.int32)
        if cur_cursor[0] >= self.screenWidth:
            cur_cursor[0] = self.screenWidth - 1
        if cur_cursor[1] >= self.screenHeight:
            cur_cursor[1] = self.screenHeight - 1
          
        return cur_cursor

    def control_cursor(self, cur_cursor, gesture_name):
        print(cur_cursor)
        if self.pre_gesture!="none":
            if not (cur_cursor[0] == self.screenWidth-1 and cur_cursor[1] == 0):
                print("1")
                self.fixed_x = cur_cursor[0]
                self.fixed_y = cur_cursor[1] 

        if self.pre_gesture!="func" and gesture_name=="func":
            if not (cur_cursor[0] == self.screenWidth-1 and cur_cursor[1] == 0):
                print("2")
                pyautogui.mouseUp(cur_cursor[0], cur_cursor[1], button= 'left')
                pyautogui.click()

        if gesture_name == "none":
            if not (cur_cursor[0] == self.screenWidth-1 and cur_cursor[1] == 0):
                print("3")
                pyautogui.mouseUp(cur_cursor[0], cur_cursor[1], button= 'left')
                pyautogui.moveTo(self.fixed_x, self.fixed_y)


        if gesture_name == "draw":   
            if not (cur_cursor[0] == self.screenWidth-1 and cur_cursor[1] == 0):
                print("4")
                pyautogui.mouseUp(cur_cursor[0], cur_cursor[1], button= 'left')
                to_scroll = (self.p_sc-self.fixed_y   )#to_scroll = (mouse_position[8][1]-mouse_position[0][1])/10
                if to_scroll>0:
                    to_scroll = 1
                else:
                    to_scroll = -1
                pyautogui.scroll(int(to_scroll),x=self.fixed_x, y=self.fixed_y)
        
        if self.pre_gesture!="zoom-in" and gesture_name == "zoom-in":
            if not (cur_cursor[0] == self.screenWidth-1 and cur_cursor[1] == 0):
                print("5")
                pyautogui.mouseUp(cur_cursor[0], cur_cursor[1], button= 'left')
                pyautogui.hotkey('ctrl','+')
            
            
        if self.pre_gesture!="zoom-out" and gesture_name == "zoom-out":
            if not (cur_cursor[0] == self.screenWidth-1 and cur_cursor[1] == 0):
                print("6")
                pyautogui.mouseUp(cur_cursor[0], cur_cursor[1], button= 'left')
                pyautogui.hotkey('ctrl','-')

        if self.pre_gesture=="func" and gesture_name=="func":
            if not (cur_cursor[0] == self.screenWidth-1 and cur_cursor[1] == 0):
                print("7")
                pyautogui.mouseDown(cur_cursor[0], cur_cursor[1], button= 'left')
            
        self.pre_gesture = gesture_name
        self.p_sc = cur_cursor[1]
        