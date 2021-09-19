# -*- coding: utf-8 -*-
import os
import torch
from torchvision import models, transforms as T
from PIL import Image
from utils import imagenet_idx_to_label

model = models.mobilenet_v3_small(pretrained=True)
model.eval()

transforms = T.Compose(
    [
        T.ToTensor(),
        T.Resize(256),
        T.CenterCrop(224),
        T.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
    ]
)


# Input image
fpath = os.path.join("resources", "n01819313_sulphur-crested_cockatoo.jpg")
img = Image.open(fpath)

# Run the net
img = transforms(img)
logits = model(img.unsqueeze(0))
cls_id = torch.argmax(logits, -1)
label = imagenet_idx_to_label(cls_id)
assert label == "sulphur-crested cockatoo"

print(f"{logits.shape = }")
print(f"Predicted label: {label}")
