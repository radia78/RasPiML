from torchvision.models.detection import ssdlite320_mobilenet_v3_large as SSDLite
import ssl
import torch
from torch import nn
from typing import List, Union

class QuantizedSSDLite(nn.Module):
    def __init__(self, weights: str='DEFAULT'):
        super(QuantizedSSDLite, self).__init__()
        ssl._create_default_https_context = ssl._create_unverified_context
        self.quant = torch.ao.quantization.QuantStub()
        self.model = SSDLite(weights=weights)

    def forward(self, x: torch.Tensor):
        x = [self.quant(x)]
        x = self.model(x)
        return x[1]
    
if __name__ == "__main__":
    qt_model = QuantizedSSDLite()
    torch.jit.save(torch.jit.script(qt_model), "qt_model.pth")