from obj_seg import load_model
import torch

model = load_model()
x = torch.randn(1, 3, 224, 224)
with torch.no_grad():
   outputs = model(x)

print(outputs)