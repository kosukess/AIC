#import library
import json
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg 
import trt_pose.coco
import math
import os
import numpy as np
import traitlets
import pickle 
import trt_pose.models
import torch
import torch2trt
from torch2trt import TRTModule
from preprocessdata import preprocessdata
from trt_pose.draw_objects import DrawObjects
from trt_pose.parse_objects import ParseObjects
import torchvision.transforms as transforms
import PIL.Image
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from jetcam.usb_camera import USBCamera
from jetcam.csi_camera import CSICamera
from jetcam.utils import bgr8_to_jpeg



class project:
    def __init__(self, h=224, w=224):
        
        with open('preprocess/hand_pose.json', 'r') as f:
            hand_pose = json.load(f)

        topology = trt_pose.coco.coco_category_to_topology(hand_pose)
        
        self.num_parts = len(hand_pose['keypoints'])
        num_links = len(hand_pose['skeleton'])

        model = trt_pose.models.resnet18_baseline_att(self.num_parts, 2 * num_links).cuda().eval()
        

        WIDTH = 224
        HEIGHT = 224
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

        data = torch.zeros((1, 3, HEIGHT, WIDTH)).cuda()

        if not os.path.exists('model/hand_pose_resnet18_att_244_244_trt.pth'):
            MODEL_WEIGHTS = 'model/hand_pose_resnet18_att_244_244.pth'
            model.load_state_dict(torch.load(MODEL_WEIGHTS))
            self.model_trt = torch2trt.torch2trt(model, [data], fp16_mode=True, max_workspace_size=1<<25)
            OPTIMIZED_MODEL = 'model/hand_pose_resnet18_att_244_244_trt.pth'
            torch.save(self.model_trt.state_dict(), OPTIMIZED_MODEL)

        OPTIMIZED_MODEL = 'model/hand_pose_resnet18_att_244_244_trt.pth'
        

        self.model_trt = TRTModule()
        self.model_trt.load_state_dict(torch.load(OPTIMIZED_MODEL))

        self.parse_objects = ParseObjects(topology,cmap_threshold=0.12, link_threshold=0.15)
        draw_objects = DrawObjects(topology)

        self.mean = torch.Tensor([0.485, 0.456, 0.406]).cuda()
        self.std = torch.Tensor([0.229, 0.224, 0.225]).cuda()
        self.device = torch.device('cuda')

        self.clf = make_pipeline(StandardScaler(), SVC(gamma='auto', kernel='rbf'))
        
        self.preprocessdata = preprocessdata(topology, self.num_parts)

        filename = 'svmmodel.sav'
        self.clf = pickle.load(open(filename, 'rb'))
        
        with open('preprocess/gesture.json', 'r') as f:
            gesture = json.load(f)
        self.gesture_type = gesture["classes"]


        self.camera = USBCamera(width=WIDTH, height=HEIGHT, capture_fps=30, capture_device=0)
        #camera = CSICamera(width=WIDTH, height=HEIGHT, capture_fps=30)

        self.camera.running = True



    def preprocess(self, image):
        self.device = torch.device('cuda')
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = PIL.Image.fromarray(image)
        image = transforms.functional.to_tensor(image).to(self.device)
        image.sub_(self.mean[:, None, None]).div_(self.std[:, None, None])
        return image[None, ...]
    
    def draw_joints(self, image, joints):
        count = 0
        for i in joints:
            if i==[0,0]:
                count+=1
        if count>= 3:
            return 
        for i in joints:
            cv2.circle(image, (i[0],i[1]), 2, (0,0,255), 1)
        cv2.circle(image, (joints[0][0],joints[0][1]), 2, (255,0,255), 1)
        for i in self.hand_pose['skeleton']:
            if joints[i[0]-1][0]==0 or joints[i[1]-1][0] == 0:
                break
            cv2.line(image, (joints[i[0]-1][0],joints[i[0]-1][1]), (joints[i[1]-1][0],joints[i[1]-1][1]), (0,255,0), 1)


    def classify_gesture(self, image):
        hand_pose_image, hand_pose_joints = self.hand_pose(image)
        dist_bn_joints = self.preprocessdata.find_distance(hand_pose_joints)
        gesture = self.clf.predict([dist_bn_joints,[0]*self.num_parts*self.num_parts])
        gesture_joints = gesture[0]
        self.preprocessdata.prev_queue.append(gesture_joints)
        self.preprocessdata.prev_queue.pop(0)
        gesture = self.gesture_class()
        
        return hand_pose_image, gesture


    def hand_pose(self, image):
        data = self.preprocess(image)
        cmap, paf = self.model_trt(data)
        cmap, paf = cmap.detach().cpu(), paf.detach().cpu()
        counts, objects, peaks = self.parse_objects(cmap, paf)
        joints = self.preprocessdata.joints_inference(image, counts, objects, peaks)
        self.draw_joints(image, joints)

        return image, joints


    def gesture_class(self):
        return self.preprocessdata.text

    def draw(self, image, joints):
        if self.draw_or_not == -1:
            if self.preprocessdata.text=="line":
                if joints[5]!=[0,0]:
                    self.rectangle.append((int(joints[8][0]*(self.w/224)), int(joints[8][1])*(self.h/244)))

            if (len(self.rectangle)) > 0:
                if self.rectangle[-1]!=[0,0]:
                    cv2.line(image,self.rectangle[-2], self.rectangle[-1], (0,0,0), 2)
        if self.draw_or_not == 1:
            if self.preprocessdata.text=="line":
                if joints[5]!=[0,0]:
                    self.rectangle.append([int(joints[8][0]*(self.w/224)), int(joints[8][1])*(self.h/244)])

            if (len(self.rectangle)) > 0:
                if self.rectangle[-1]!=[0,0]:
                    cv2.line(image, self.rectangle[-2], self.rectangle[-1], (255,255,255), 5)

    def switch(self, current_gesture):
        if (current_gesture == "clear")and(self.pre_gesture == "click"):
            x_position, y_position = int(joints[8][0]*(self.w/224)), int(joint[8][1]*(self.h/224))
            color = self.botton_board[x_position, y_positon]
            if color == 0:
                self.draw_or_not = self.draw_or_not*-1
        self.pre_gesture = current_gesture

    def execute(self):
        image = change['new']
        image, current_gesture = self.classify_gesture(image)
        switch(current_gesture)
        self.pre_gesture
        draw(self.white_board, joints)
        cv2.imshow('white board', self.white_board)
        #image = image[:, ::-1, :]
        cv2.imshow('screen', image)
        cv2.waitKey(1)
        
    def start(self):
        self.camera.observe(execute, names='value')

    def end(self):
        self.camera.unobserve_all()
    
    #camera.running = False