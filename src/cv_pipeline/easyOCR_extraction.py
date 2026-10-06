import cv2 as cv
import numpy as np
import easyocr
import torch
import logging
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

def easyocr_text_extraction(frame : np.ndarray):
    logging.getLogger('easyocr').setLevel(logging.ERROR)

    has_gpu = torch.cuda.is_available()
    reader = easyocr.Reader(['en'], gpu=has_gpu)

    result = reader.readtext(frame)
    text_list = []

    for detection in result:
        text = detection[1]
        text_list.append(text)

    return " ".join(text_list)