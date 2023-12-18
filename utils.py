import cv2
import pickle
import torch
import numpy as np
import math
import ssl
from torchvision.models.detection import ssdlite320_mobilenet_v3_large, SSDLite320_MobileNet_V3_Large_Weights
from torchvision import transforms

def load_jit_model():
    ssl._create_default_https_context = ssl._create_unverified_context

    # load the model
    qt_model = ssdlite320_mobilenet_v3_large(weights=SSDLite320_MobileNet_V3_Large_Weights.COCO_V1)
    qt_model = qt_model.to('cpu')
    qt_model.eval()

    # jit the model
    net = torch.jit.script(qt_model)

    return net

def load_capture(vid_width, vid_height, fps):
    # create video capture object
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, vid_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, vid_height)
    cap.set(cv2.CAP_PROP_FPS, fps)

    return cap

# the predict function
def predict(image, model, detection_threshold):
    # transform the image to tensor
    image = transform(image)

    # get the prediction result
    with torch.no_grad():
        _, outputs = model([image])

    # mask of getting person detections with confidence score greater than threshold
    mask = (outputs[0]['scores'] >= detection_threshold) & (outputs[0]['labels'] == 1)

    # return the x-axis center coordinates of the boxes
    return outputs[0]['boxes'][mask].index_select(-1, idx).diff().flatten().tolist()

# preprocessing the image
transform = transforms.Compose([
    transforms.ToTensor()
])

# specific indices to choose when going over the results
idx = torch.tensor([0, 2])

# convert pixel to angle
def pixel2angle(outputs, width, hfov):

    if len(outputs) > 1 or len(outputs) == 0:
        return 0
    
    elif outputs == 1:
        pixel_rel = outputs[0]/2 - width // 2
        tan_hfov = np.tan(hfov / 2)
        return np.arctan(2 * pixel_rel * tan_hfov / (width // 2))

degrees2radians = lambda x: x * math.pi/180  
