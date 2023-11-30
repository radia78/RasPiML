from utils import load_jit_model, predict
import cv2
import numpy as np
from PIL import Image

def draw_boxes(boxes, classes, labels, image):
    """
    Draws the bounding box around a detected object.
    """
    image = cv2.cvtColor(np.asarray(image), cv2.COLOR_BGR2RGB)
    for i, box in enumerate(boxes):
        color = 255
        cv2.rectangle(
            image,
            (int(box[0]), int(box[1])),
            (int(box[2]), int(box[3])),
            color, 2
        )
        cv2.putText(image, 'Person', (int(box[0]), int(box[1]-5)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2, 
                    lineType=cv2.LINE_AA)
    return image
  

img = Image.open("test_img.jpg")
model = load_jit_model()

outputs = predict(img, model, 0.7)
print(outputs)