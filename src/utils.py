# -*- coding: utf-8 -*-
import os
import json
import urllib.request
import streamlit as st
from functools import lru_cache
from PIL import Image
from io import BytesIO

METRICS = [
    "Bleu_1",
    "Bleu_2",
    "Bleu_3",
    "Bleu_4",
    "METEOR",
    "ROUGE_L",
    "CIDEr",
    "SPICE",
]


def dict_filter(dict_obj, key_list):
    return {k: v for k, v in dict_obj.items() if k in key_list}


@lru_cache(1)
def load_imagenet_labels_1k():
    with open(os.path.join("resources", "imagenet_labels_1k.json"), "r") as f:
        return json.load(f)


def imagenet_idx_to_label(idx):
    return load_imagenet_labels_1k()[idx]


def load_image_from_url(url):
    with urllib.request.urlopen(url) as response:
        img = Image.open(BytesIO(response.read()))
    return img


@st.cache(show_spinner=True)
def load_image_from_url_streamlit(url):
    with urllib.request.urlopen(url) as response:
        img = Image.open(BytesIO(response.read()))
    return img
