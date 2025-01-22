import cv2
import numpy as np
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# Read the image
image = cv2.imread('Apex_Scoreboard.png')
# Define the coordinates of the region of interest (ROI)
x, y, w, h = 100, 50, 330, 50
k, l, m, n = 1470, 120, 100, 75
aa, ab, ac, ad, ae = 200, 270, 220, 250, 475

# Crop the image
cropped_image_codeword = image[y:y+h, x:x+w]
cropped_image_placement = image[l:l+n, k:k+m]
cropped_img_p1 = image[ab:ab+ad, aa:aa+ac]
cropped_img_p2 = image[ab:ab+ad, aa+ae:aa+ac+ae]
cropped_img_p3 = image[ab:ab+ad, aa+(2*ae):aa+(2*ae)+ac+150]

cropped_image_codeword = cv2.resize(cropped_image_codeword, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
cropped_image_placement = cv2.resize(cropped_image_placement, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
cropped_img_p1 = cv2.resize(cropped_img_p1, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
cropped_img_p2 = cv2.resize(cropped_img_p2, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
cropped_img_p3 = cv2.resize(cropped_img_p3, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)


cv2.imwrite('codeword.png', cropped_image_codeword)
cv2.imwrite('placement.png', cropped_image_placement)
cv2.imwrite('p1.png', cropped_img_p1)
cv2.imwrite('p2.png', cropped_img_p2)
cv2.imwrite('p3.png', cropped_img_p3)

###COMPLETED PLACEMENT READER
img0 = cv2.imread('placement.png', cv2.IMREAD_GRAYSCALE)
img0 = cv2.resize(img0, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
# Run OCR with only digits
config = '--psm 8 -c tessedit_char_whitelist="0123456789"'
text0 = pytesseract.image_to_string(img0, config=config)
# Save Preprocessed Image and Print Text
cv2.imwrite('preprocessed_placement.png', img0)
print(f"Placement: {text0}")


###EXPERIMENTAL CODEWORD READER
img1 = cv2.imread('codeword.png', cv2.IMREAD_GRAYSCALE)
img1 = cv2.resize(img1, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
img1 = cv2.GaussianBlur(img1, (5, 5), 0)
thresh0 = cv2.adaptiveThreshold(img1, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
# Run OCR with only English Alphabet
config = '--psm 6 -c tessedit_char_whitelist="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"'
text1 = pytesseract.image_to_string(thresh0, config=config)

# Save Preprocessed Image and Print Text
cv2.imwrite('preprocessed_codeword.png', thresh0)
print(f"Codeword: {text1}")

###EXPERIMENTAL P1 READER
img2 = cv2.imread('p1.png', cv2.IMREAD_GRAYSCALE)
img2 = cv2.resize(img2, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
#img2 = cv2.GaussianBlur(img2, (5, 5), 0)
thresh1 = cv2.adaptiveThreshold(img2, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
# Run OCR with only English Alphabet
config = '--psm 6 -c tessedit_char_whitelist="0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"'
text2 = pytesseract.image_to_string(thresh1, config=config)

# Save Preprocessed Image and Print Text
cv2.imwrite('preprocessed_p1.png', thresh1)
print(f"P1: {text2}")

# Display the cropped images
'''
cv2.imshow('Cropped Image', cropped_image_codeword)
cv2.imshow('Cropped Image', cropped_image_placement)
cv2.imshow('Cropped Image', cropped_img_p1)
cv2.imshow('Cropped Image', cropped_img_p2)
cv2.imshow('Cropped Image', cropped_img_p3)


config = '--psm 7 -c tessedit_char_whitelist="abcdefghijklmnopqrstuvwxyz"'
img0 = cv2.imread('codeword.png', cv2.IMREAD_GRAYSCALE)
ret, thresh0 = cv2.threshold(img0, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
thresh0 = cv2.bitwise_not(thresh0)
print('Code: \n')
print(pytesseract.image_to_string(thresh0))


config = '--psm 8 -c tessedit_char_whitelist="0123456789"'
img1 = cv2.imread('placement.png', cv2.IMREAD_GRAYSCALE)
ret, thresh1 = cv2.threshold(img1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
thresh1 = cv2.bitwise_not(thresh1)
print('Placement \n')
print(pytesseract.image_to_string(thresh1))

img2 = cv2.imread('p1.png', cv2.IMREAD_GRAYSCALE)
ret, thresh2 = cv2.threshold(img2, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
thresh1 = cv2.bitwise_not(thresh2)
print('p1 \n')
print(pytesseract.image_to_string(thresh2))

img3 = cv2.imread('p2.png', cv2.IMREAD_GRAYSCALE)
ret, thresh3 = cv2.threshold(img3, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
thresh1 = cv2.bitwise_not(thresh3)
print('p2 \n')
print(pytesseract.image_to_string(thresh3))

img4 = cv2.imread('p3.png', cv2.IMREAD_GRAYSCALE)
ret, thresh4 = cv2.threshold(img4, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
thresh4 = cv2.bitwise_not(thresh4)
print('p3 \n')
print(pytesseract.image_to_string(thresh4))

cv2.waitKey(0)
cv2.destroyAllWindows()
'''
