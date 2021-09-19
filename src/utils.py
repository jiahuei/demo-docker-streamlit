# -*- coding: utf-8 -*-
import os
import json
import requests
from functools import lru_cache
from PIL import Image
from io import BytesIO


@lru_cache(1)
def load_imagenet_labels_1k():
    with open(os.path.join("resources", "imagenet_labels_1k.json"), "r") as f:
        return json.load(f)


def imagenet_idx_to_label(idx):
    return load_imagenet_labels_1k()[idx]


def load_pil_image_from_url(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img
