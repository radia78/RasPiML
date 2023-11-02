import torch
from torchvision import transforms
import numpy as np
import cv2

def load_model():
    model = torch.jit.load('qt_model.pth')
    model.eval()
    return model

# preprocessing the image
transform = transforms.Compose([
    transforms.ToTensor()
])

# the predict function
def predict(image, model, detection_threshold):
    # transform the image to tensor
    image = transform(image)
    # add a batch dimension
    image = image
    # get the prediction result
    with torch.no_grad():
        outputs = model(image)

    # get score for a person
    pred_scores = outputs[0]['scores'][0]
    if pred_scores > detection_threshold:

        # get the boundary boxes
        pred_box = outputs[0]['boxes'][0]

        return pred_box
    else:
        return None

# helper function to draw boxes
def draw_boxes(box, image):
    image = cv2.cvtColor(np.asarray(image), cv2.COLOR_BGR2RGB)
    
    if box != None:
        # draw the rectangle boxes
        cv2.rectangle(
            image,
            (int(box[0]), int(box[1])),
            (int(box[2]), int(box[2])),
            (255, 0, 0), 2
        )
        # put the name of the boxes
        cv2.putText(
            image, "Person", (int(box[0]), int(box[1]-5)),
            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2, 
            lineType=cv2.LINE_AA
        )

    return image