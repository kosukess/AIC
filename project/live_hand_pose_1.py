import os
import json
import trt_pose.coco
import torch
 
 
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 
 
with open('preprocess/hand_pose.json', 'r') as f:
    hand_pose = json.load(f)
 
topology = trt_pose.coco.coco_category_to_topology(hand_pose)
import trt_pose.models
 
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++
num_parts = len(hand_pose['keypoints'])
num_links = len(hand_pose['skeleton'])
 
model = trt_pose.models.resnet18_baseline_att(num_parts, 2 * num_links).cuda().eval()
 
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 
WIDTH = 224
HEIGHT = 224
data = torch.zeros((1, 3, HEIGHT, WIDTH)).cuda()
 
MODEL_WEIGHTS = 'model/hand_pose_resnet18_att_244_244.pth'
model.load_state_dict(torch.load(MODEL_WEIGHTS))
import torch2trt
model_trt = torch2trt.torch2trt(model, [data], fp16_mode=True, max_workspace_size=1<<25)
OPTIMIZED_MODEL = 'model/hand_pose_resnet18_att_244_244_trt.pth'
torch.save(model_trt.state_dict(), OPTIMIZED_MODEL)