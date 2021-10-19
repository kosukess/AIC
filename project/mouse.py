#マウスの位置とジェスチャークラスを受け取る
#マウス位置＝mouse_position
#ジェスチャークラス=gesture_class
#受け取ったもので描く・消す・スイッチ
#描画したホワイトボードの表示

import numpy as np
import cv2
import socket
import pickle
import pyautogui
import time

"""[summary]

"""

class mouse():
    def __init__(self):

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

    def receive_data(self):
        """
        message[0]: cursor data [0]: x, [1]: y
        message[1]: gesture class name

        """        
        message, cli_addr = self.sock.recvfrom(self.M_SIZE)
        message = pickle.loads(message)
        return message


    def calcAbs(self, difvec):
        return np.sqrt(difvec[0]**2+difvec[1]**2)


    def control_cursor(self, mouse_position, gesture_name):

        if self.pre_gesture!="stop":
            #pyautogui.position()
            self.fixed_x = mouse_position[0]
            self.fixed_y = mouse_position[1] 
        if self.pre_gesture!="fist" and self.pre_gesture=="fist":
            pyautogui.mouseUp(((mouse_position[0])*self.screenWidth)/256, ((mouse_position[1])*self.screenHeight)/256, button= 'left')
            pyautogui.click()

        if gesture_name == "stop":
            if mouse_position!=[0,0]:
                pyautogui.mouseUp(((mouse_position[0])*self.screenWidth)/256, ((mouse_position[1])*self.screenHeight)/256, button= 'left')
                pyautogui.moveTo(((mouse_position[0])*self.screenWidth)/256, ((mouse_position[1])*self.screenHeight)/256)


        if gesture_name == "peace":   
            if mouse_position!=[0,0]:
                pyautogui.mouseUp(((mouse_position[0])*self.screenWidth)/256, ((mouse_position[1])*self.screenHeight)/256, button= 'left')#to_scroll = (mouse_position[8][1]-mouse_position[0][1])/10
                to_scroll = (self.p_sc-mouse_position[1])
                if to_scroll>0:
                    to_scroll = 1
                else:
                    to_scroll = -1
                pyautogui.scroll(int(to_scroll),x=(mouse_position[0]*self.screenWidth)/256, y=(mouse_position[1]*self.screenHeight)/256)
        
        if gesture_name == "ok":
            pyautogui.keyDown('ctrl')
            if mouse_position!=[0,0]:
                pyautogui.mouseUp(((mouse_position[0])*self.screenWidth)/256, ((mouse_position[1])*self.screenHeight)/256, button= 'left')
                
                to_scroll = (self.p_sc-mouse_position[1])
                if to_scroll>0:
                    to_scroll = 1
                else:
                    to_scroll = -1
                t1 = time.time()
                #print(t1-t0)
                if t1-self.t0>1:   
                    pyautogui.scroll(int(to_scroll),x=(mouse_position[0]*self.screenWidth)/256, y=(mouse_position[1]*self.screenHeight)/256)
                    self.t0 = time.time()
            pyautogui.keyUp('ctrl')
            
            
        if gesture_name == "xxx":    
            if mouse_position!=[0,0]:
                pyautogui.mouseDown(((mouse_position[0])*self.screenWidth)/256, ((mouse_position[1])*self.screenHeight)/256, button= 'left')
        
        self.pre_gesture = gesture_name
        self.p_sc = mouse_position[1]   
        