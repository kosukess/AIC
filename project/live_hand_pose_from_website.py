
# -*- coding: utf-8 -*-
print("preparing...")

import tkinter as tk
import cv2
from PIL import Image,ImageTk
import numpy as np

root=tk.Tk()
root.title("camera")
root.geometry("224x224")
root.resizable(width=False, height=False)
canvas=tk.Canvas(root, width=224, height=224, bg="white")
canvas.pack()


#-------------------------------------
import os
os.environ['MPLCONFIGDIR'] = "/tmp"

import json
import matplotlib.pyplot as plt
import matplotlib.image as mpimg 
import trt_pose.coco
import math
import traitlets
import pickle
import torch

with open('preprocess/hand_pose.json', 'r') as f:
    hand_pose = json.load(f)

topology = trt_pose.coco.coco_category_to_topology(hand_pose)


num_parts = len(hand_pose['keypoints'])

WIDTH = 224
HEIGHT = 224
data = torch.zeros((1, 3, HEIGHT, WIDTH)).cuda()

print("weight loading...")

OPTIMIZED_MODEL = 'model/hand_pose_resnet18_att_244_244_trt.pth'
from torch2trt import TRTModule

model_trt = TRTModule()
model_trt.load_state_dict(torch.load(OPTIMIZED_MODEL))



from trt_pose.draw_objects import DrawObjects
from trt_pose.parse_objects import ParseObjects

parse_objects = ParseObjects(topology,cmap_threshold=0.15, link_threshold=0.15)
draw_objects = DrawObjects(topology)

import torchvision.transforms as transforms
import PIL.Image

mean = torch.Tensor([0.485, 0.456, 0.406]).cuda()
std = torch.Tensor([0.229, 0.224, 0.225]).cuda()
device = torch.device('cuda')

def preprocess(image):
    global device
    device = torch.device('cuda')
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = PIL.Image.fromarray(image)
    image = transforms.functional.to_tensor(image).to(device)
    image.sub_(mean[:, None, None]).div_(std[:, None, None])
    return image[None, ...]


from preprocessdata import preprocessdata
preprocessdata = preprocessdata(topology, num_parts)

print("svm model loading...")

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
clf = make_pipeline(StandardScaler(), SVC(gamma='auto', kernel='rbf'))
filename = 'svmmodel.sav'
clf = pickle.load(open(filename, 'rb'))


with open('preprocess/gesture.json', 'r') as f:
    gesture = json.load(f)

gesture_type = gesture["classes"]


def draw_joints(image, joints):
    count = 0
    for i in joints:
        if i==[0,0]:
            count+=1
    if count>= 7:
        return 
    for i in joints:
        cv2.circle(image, (i[0],i[1]), 2, (0,0,255), 1)
    cv2.circle(image, (joints[0][0],joints[0][1]), 2, (255,0,255), 1)
    for i in hand_pose['skeleton']:
        if joints[i[0]-1][0]==0 or joints[i[1]-1][0] == 0:
            break
        cv2.line(image, (joints[i[0]-1][0],joints[i[0]-1][1]), (joints[i[1]-1][0],joints[i[1]-1][1]), (0,255,0), 1)



def execute(change):
    image = change['new']
    image = cv2.flip(image,1)
    data = preprocess(image)
    cmap, paf = model_trt(data)
    cmap, paf = cmap.detach().cpu(), paf.detach().cpu()
    counts, objects, peaks = parse_objects(cmap, paf)
    joints = preprocessdata.joints_inference(image, counts, objects, peaks)
    draw_joints(image, joints)
    
    dist_bn_joints = preprocessdata.find_distance(joints)
    gesture = clf.predict([dist_bn_joints,[0]*num_parts*num_parts])
    gesture_joints = gesture[0]
    preprocessdata.prev_queue.append(gesture_joints)
    preprocessdata.prev_queue.pop(0)
    preprocessdata.print_label(image, preprocessdata.prev_queue, gesture_type)

    return image

#-------------------------------------

def capStart():
    print('camera-start')
    try:
        global c, w, h, img
        c=cv2.VideoCapture(0)
        w, h= c.get(cv2.CAP_PROP_FRAME_WIDTH), c.get(cv2.CAP_PROP_FRAME_HEIGHT)
        print('width:'+str(w)+'px/height:'+str(h)+'px')
    except:
        import sys
        print("error")
        print(sys.exec_info()[0])
        print(sys.exec_info()[1])
        c.release()
        cv2.destroyAllWindows()

    return int(w), int(h)

def up(width, height):#change update
    edge = 0
    if width > height:
        edge = height
    else:
        edge = width
    global img
    ret, frame = c.read()
    if ret:
        frame = frame[0:edge, 0:edge]
        size = (224,224)
        frame = cv2.resize(frame,size)
        
        frame = execute({'new': frame})
        
        img = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
        canvas.create_image(0,0,image=img,anchor="nw")
    else:
        print("up failed")
    root.after(1,up)

w,h = capStart()
up(w,h)
root.mainloop()