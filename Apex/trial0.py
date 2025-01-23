import cv2
import numpy as np
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

#Grayscale, double size, apply Gaussian Blur, then convert to binary format (b&w)
def preprocess_image(image):
    img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    img = cv2.GaussianBlur(img, (5, 5), 0)
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    return img


#Run OCR using only alphabetical characters
def run_ocr_alpha(image, whitelist="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", psm=7):
    config = f'--psm {psm} -c tessedit_char_whitelist="{whitelist}"'
    return pytesseract.image_to_string(image, config=config)

#Run OCR using only numerical characters
def run_ocr_numer(image, whitelist="0123456789", psm=8):
    config = f'--psm {psm} -c tessedit_char_whitelist="{whitelist}"'
    return pytesseract.image_to_string(image, config=config)


#Process Regions of Interest for alphabetical characters
def process_roi_alpha(image, x, y, w, h):
    roi = image[y:y+h, x:x+w]
    preprocessed = preprocess_image(roi)
    return run_ocr_alpha(preprocessed)


#Process Regions of Interest for numerical characters
def process_roi_numer(image, x, y, w, h):
    roi = image[y:y+h, x:x+w]
    preprocessed = preprocess_image(roi)
    return run_ocr_numer(preprocessed)

# Load image and process regions with fixed coordinates TODO: Dynamic Coords?
image = cv2.imread('Apex_Scoreboard.png')
regions = [
    {"name": "Codeword", "x": 100, "y": 50, "w": 330, "h": 50},
    {"name": "Placement", "x": 1470, "y": 120, "w": 100, "h": 75},
]

for region in regions:
    name, x, y, w, h, = region.values()
    if region["name"] == "Codeword":
        text0 = process_roi_alpha(image, x, y, w, h)
        print(f"{name}: {text0}")
    else:
        text1 = process_roi_numer(image, x, y, w, h)
        print(f"{name}: {text1}")