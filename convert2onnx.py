import torch
from torchvision.models.detection.ssdlite import ssdlite320_mobilenet_v3_large, SSDLite320_MobileNet_V3_Large_Weights

# load the ssdlite model
net = ssdlite320_mobilenet_v3_large(
    weights=SSDLite320_MobileNet_V3_Large_Weights.COCO_V1, 
    trainable_backbone_layers=0    
)

# send the model to a cpu and turn on inference mode
net.to('cpu')
net.eval()

# create a random input to enforece the shape
x = torch.randn((1, 3, 320, 320)).to('cpu')

# export the model to onnx
torch.onnx.export(
    net, # model being run
    x, # model input
    "ssdlite320.onnx", # name of model
    export_params=True, # store the trained weights
    opset_version=11,
    do_constant_folding=True,
    input_names=['input'],
    output_names=['output']
)
