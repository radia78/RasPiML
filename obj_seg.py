import torch
from torchvision import transforms
import numpy as np
import cv2
from labels import COCO_INSTANCE_CATEGORY_NAMES as coco_names

# create colors for each class
# values between 0-225 for each of the three channels
COLORS = np.random.uniform(0, 255, size=(len(coco_names), 3))

# preprocessing the image
transform = transforms.Compose([
    transforms.ToTensor()
])

# the predict function
# NEED TO CHANGE THIS TO ONLY DETECTING PEOPLE
def predict(image, model, detection_threshold):
    # transform the image to tensor
    image = transform(image)
    # add a batch dimension
    image = image.unsqueeze(0)
    # get the prediction result
    with torch.no_grad():
        outputs = model(image)
    
    # get score for a person
    pred_scores = outputs[0]['scores']
    # get the boundary boxes
    pred_boxes = outputs[0]['boxes']
    boxes = pred_boxes[pred_scores > detection_threshold]
    # only take labels of those higher than the threshold
    labels = outputs[0]['labels'][:len(boxes)]
    # get the names of the labels
    pred_classes = [coco_names[i] for i in labels]

    return boxes, pred_classes, labels

# helper function to draw boxes
def draw_boxes(boxes, classes, labels, image):
    image = cv2.cvtColor(np.asarray(image), cv2.COLOR_BGR2RGB)
    for i, box in enumerate(boxes):
        color = COLORS(labels[i])
        # draw the rectangle boxes
        cv2.rectangle(
            image,
            (int(box[0]), int(box[1])),
            (int(box[2]), int(box[2])),
            color, 2
        )
        # put the name of the boxes
        cv2.putText(
            image, classes[i], (int(box[0]), int(box[1]-5)),
            cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2, 
            lineType=cv2.LINE_AA
        )

    return image