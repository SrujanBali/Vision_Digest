import pytesseract
import numpy as np
import cv2 as cv
from PIL import Image

def get_preprocessed_threshed(img : np.array) -> np.ndarray:
    gray_img = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (51, 51))
    background = cv.morphologyEx(gray_img, cv.MORPH_CLOSE, kernel)
    flattened_gray = cv.divide(gray_img, background, scale=255)

    height, width = flattened_gray.shape
    img_large = cv.resize(flattened_gray, (width * 2, height * 2), interpolation=cv.INTER_CUBIC)
    blur_img = cv.GaussianBlur(img_large, (3, 3), 0)
    threshed_img = cv.adaptiveThreshold(blur_img, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, blockSize=31, C=7)

    return threshed_img

def tesseract_text_extraction(filepath = r"C:\Users\Srujan Bali\Documents\Srujan\Programming\Python Projects\Vision_Digest\data\raw\Newton.png") -> str:
    img_file = Image.open(fr"{filepath}")
    img = np.array(img_file)
    processed_img = get_preprocessed_threshed(img)

    custom_config = r'--oem 3 --psm 3'
    text_extracted = pytesseract.image_to_string(processed_img, config=custom_config)

    return text_extracted