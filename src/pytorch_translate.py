# -*- coding: utf-8 -*-
from transformers import pipeline

translate = pipeline("translation_en_to_zh", "Helsinki-NLP/opus-mt-en-zh")

translate("My name is Wolfgang and I live in Berlin")
