#import library
import json
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg 
import trt_pose.coco
import math
import os
import sys
import numpy as np
import traitlets
import pickle 
import trt_pose.models
import torch
import torch2trt
import socket
import signal
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
from frame import Frame


class Project:
    def __init__(self, h=224, w=224):
        
        # model load
        with open('preprocess/hand_pose.json', 'r') as f:
            self.hand_pose = json.load(f)
        topology = trt_pose.coco.coco_category_to_topology(self.hand_pose)
        self.num_parts = len(self.hand_pose['keypoints'])
        num_links = len(self.hand_pose['skeleton'])
        model = trt_pose.models.resnet18_baseline_att(self.num_parts, 2 * num_links).cuda().eval() 
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

        # parse
        self.parse_objects = ParseObjects(topology,cmap_threshold=0.12, link_threshold=0.15)
        draw_objects = DrawObjects(topology)
        self.mean = torch.Tensor([0.485, 0.456, 0.406]).cuda()
        self.std = torch.Tensor([0.229, 0.224, 0.225]).cuda()
        self.device = torch.device('cuda')

        # classify
        self.clf = make_pipeline(StandardScaler(), SVC(gamma='auto', kernel='rbf'))
        self.preprocessdata = preprocessdata(topology, self.num_parts)
        filename = 'svmmodel.sav'
        self.clf = pickle.load(open(filename, 'rb'))
        with open('preprocess/gesture.json', 'r') as f:
            gesture = json.load(f)
        self.gesture_type = gesture["classes"]

        # usb camera
        WIDTH = 224
        HEIGHT = 224
        self.camera = USBCamera(width=WIDTH, height=HEIGHT, capture_fps=30, capture_device=0)
        #camera = CSICamera(width=WIDTH, height=HEIGHT, capture_fps=30)
        self.camera.running = True

        # hand tracking
        self.pre_frame = None
        self.cursor_joint = 8
        self.dif_threshold = 15
        self.num_frames = 4
        self.abs_dif_threshold = self.dif_threshold * np.sqrt(2)

        # params for ShiTomasi corner detection
        self.feature_params = dict( maxCorners = 100,
                            qualityLevel = 0.3,
                            minDistance = 7,
                            blockSize = 7 )

        # Parameters for lucas kanade optical flow
        self.lk_params = dict( winSize  = (15,15),
                        maxLevel = 2,
                        criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

        # socket parameter
        self.M_SIZE = 1024
        self.server_address = ('192.168.55.100', 30000)
        client_address = ('192.168.55.1', 30000)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(client_address)
        signal.signal(signal.SIGINT, self.handler)


    def handler(self, signum, frame):
        self.sock.close()
        print("\npushed Ctrl-C")
        sys.exit(0)


    def send_data(self, cursor, gesture_class):
        data = [cursor, gesture_class]
        send_len = self.sock.sendto(pickle.dumps(data), self.server_address)


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


    def classify_gesture(self, hand_pose_image, hand_pose_joints):
        dist_bn_joints = self.preprocessdata.find_distance(hand_pose_joints)
        gesture = self.clf.predict([dist_bn_joints,[0]*self.num_parts*self.num_parts])
        gesture_joints = gesture[0]
        self.preprocessdata.prev_queue.append(gesture_joints)
        self.preprocessdata.prev_queue.pop(0)
        gesture = self.gesture_class()
        return hand_pose_image, gesture


    def estimate_hand_pose(self, image):
        data = self.preprocess(image)
        cmap, paf = self.model_trt(data)
        cmap, paf = cmap.detach().cpu(), paf.detach().cpu()
        counts, objects, peaks = self.parse_objects(cmap, paf)
        joints = self.preprocessdata.joints_inference(image, counts, objects, peaks)
        self.draw_joints(image, joints)
        return image, joints


    def gesture_class(self):
        if self.preprocessdata.prev_queue == [1]* self.num_frames:
            return self.gesture_type[0]
        elif self.preprocessdata.prev_queue == [2]* self.num_frames:
            return self.gesture_type[1]
        elif self.preprocessdata.prev_queue == [3]* self.num_frames:
            return self.gesture_type[2]
        elif self.preprocessdata.prev_queue == [4]* self.num_frames:
            return self.gesture_type[3]
        elif self.preprocessdata.prev_queue == [5]* self.num_frames:
            return self.gesture_type[4]
        elif self.preprocessdata.prev_queue == [6]* self.num_frames:
            return self.gesture_type[5]
        elif self.preprocessdata.prev_queue == [7]*self.num_frames:
            return self.gesture_type[6]


    def calcAbs(self, difvec):
        return np.sqrt(difvec[0]**2+difvec[1]**2)


    def kltTracker(self, current_frame, pre_frame):
        p1, st, err = cv2.calcOpticalFlowPyrLK(pre_frame.img, current_frame.img, np.array([[pre_frame.hand_position]]), None, **self.lk_params)
        p0_inv, st_inv, err_inv = cv2.calcOpticalFlowPyrLK(current_frame.img, pre_frame.img, p1, None, **self.lk_params)
        dif = pre_frame.hand_position - p0_inv[0][0]
        abs_dif = self.calcAbs(dif)
        if abs_dif > self.abs_dif_threshold:
            return np.array([0, 0])
        else:
            return p1[0][0]


    def execute(self, change):
        image = change['new']
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        hand_pose_image, hand_pose_joints = self.estimate_hand_pose(image)
        hand_pose_image, current_gesture = self.classify_gesture(hand_pose_image, hand_pose_joints)
        current_hand_position = np.array(hand_pose_joints[self.cursor_joint], dtype=np.float32)

        # frameの作成
        current_frame = Frame(gray, current_hand_position, current_gesture)

        # hand_poseが失敗していたらKLTtracker
        print("\ncurrent_frame position: ", current_frame.hand_position)
        print("current gesture: ", current_gesture)
        if self.pre_frame is not None:
            if self.pre_frame.hand_position[0] != 0 or self.pre_frame.hand_position[1] != 0:
                dif = current_frame.hand_position - self.pre_frame.hand_position
                abs_dif = self.calcAbs(dif)
                if abs_dif <= self.abs_dif_threshold:
                    print("execute KLT tracker")
                    current_hand_position = self.kltTracker(current_frame, self.pre_frame)
                    current_frame.update_hand_position(current_hand_position)
        self.send_data(current_hand_position, current_gesture)
        self.pre_frame = current_frame
        

    def start(self):
        self.camera.observe(self.execute, names='value')


    def end(self):
        self.camera.unobserve_all()
    
    #camera.running = False