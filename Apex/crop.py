import cv2
import numpy as np
from PIL import Image
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
placements = []
codewords = []
# Read the image
for i in range(1, 7):
    print(f"Image {i}:")
    image = cv2.imread(f'Apex/Scoreboards/{i}.png')
    # Define the coordinates of the region of interest (ROI)
    x, y, w, h = 0, 50, 530, 30
    k, l, m, n = 1450, 120, 150, 75
    aa, ab, ac, ad, ae = 200, 270, 200, 250, 475

    MAX_COLOR_VAL = 255
    BLOCK_SIZE = 15
    SUBTRACT_FROM_MEAN = -2

    # Crop the image
    cropped_image_codeword = image[y:y+h, x:x+w]
    cropped_image_placement = image[l:l+n, k:k+m]
    cropped_img_p1 = image[ab:ab+ad, aa:aa+ac]
    cropped_img_p2 = image[ab:ab+ad, aa+ae:aa+ac+ae]
    cropped_img_p3 = image[ab:ab+ad, aa+(2*ae):aa+(2*ae)+ac+150]

    cv2.imwrite(f'imgs/codeword{i}.png', cropped_image_codeword)
    cv2.imwrite(f'imgs/placement{i}.png', cropped_image_placement)
    cv2.imwrite(f'imgs/p1{i}.png', cropped_img_p1)
    cv2.imwrite(f'imgs/p2{i}.png', cropped_img_p2)
    cv2.imwrite(f'imgs/p3{i}.png', cropped_img_p3)


    # Display the cropped image
    '''
    cv2.imshow('Cropped Image', cropped_image_codeword)
    cv2.imshow('Cropped Image', cropped_image_placement)
    cv2.imshow('Cropped Image', cropped_img_p1)
    cv2.imshow('Cropped Image', cropped_img_p2)
    cv2.imshow('Cropped Image', cropped_img_p3)
    '''

    config = '--psm 7 -c tessedit_char_whitelist="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789:"'
    img0 = cv2.imread(f'imgs/codeword{i}.png', cv2.IMREAD_GRAYSCALE)
    ret, thresh0 = cv2.threshold(img0, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    thresh0 = cv2.bitwise_not(thresh0)
    thresh0 = cv2.adaptiveThreshold(
        ~thresh0, 
        MAX_COLOR_VAL, 
        cv2.ADAPTIVE_THRESH_MEAN_C, 
        cv2.THRESH_BINARY, 
        BLOCK_SIZE, 
        SUBTRACT_FROM_MEAN
    )
    codewords.append(pytesseract.image_to_string(thresh0, config=config, lang='eng').split())
    print(f"Codeword: {pytesseract.image_to_string(thresh0, config=config, lang='eng')}")


    config = '--psm 8 -c tessedit_char_whitelist="0123456789#"'
    img1 = cv2.imread(f'imgs/placement{i}.png', cv2.IMREAD_GRAYSCALE)
    ret, thresh1 = cv2.threshold(img1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    thresh1 = cv2.bitwise_not(thresh1)
    thresh1 = cv2.adaptiveThreshold(
        ~thresh1, 
        MAX_COLOR_VAL, 
        cv2.ADAPTIVE_THRESH_MEAN_C, 
        cv2.THRESH_BINARY, 
        BLOCK_SIZE, 
        SUBTRACT_FROM_MEAN
    )
    placements.append(pytesseract.image_to_string(thresh1, config=config).split())
    print(f"Placement: {pytesseract.image_to_string(thresh1, config=config)}")

    config = '--psm 6 -c tessedit_char_whitelist="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/"'
    img2 = cv2.imread(f'imgs/p1{i}.png', cv2.IMREAD_GRAYSCALE)
    ret, thresh2 = cv2.threshold(img2, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    thresh2 = cv2.adaptiveThreshold(
        thresh2, 
        MAX_COLOR_VAL, 
        cv2.ADAPTIVE_THRESH_MEAN_C, 
        cv2.THRESH_BINARY, 
        BLOCK_SIZE, 
        SUBTRACT_FROM_MEAN
    )
    cv2.imwrite(f'imgs/p1_post_proc{i}.png', thresh2)
    print(f"P1: {pytesseract.image_to_string(thresh2, config=config, lang='eng')}")

    img3 = cv2.imread(f'imgs/p2{i}.png', cv2.IMREAD_GRAYSCALE)
    ret, thresh3 = cv2.threshold(img3, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    thresh3 = cv2.adaptiveThreshold(
        ~thresh3, 
        MAX_COLOR_VAL, 
        cv2.ADAPTIVE_THRESH_MEAN_C, 
        cv2.THRESH_BINARY, 
        BLOCK_SIZE, 
        SUBTRACT_FROM_MEAN
    )
    cv2.imwrite(f'imgs/p2_post_proc{i}.png', thresh3)
    print(f"P2: {pytesseract.image_to_string(thresh3, config=config, lang='eng')}")

    img4 = cv2.imread(f'imgs/p3{i}.png', cv2.IMREAD_GRAYSCALE)
    ret, thresh4 = cv2.threshold(img4, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    th2 = cv2.adaptiveThreshold(thresh4,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,11,2)
    cv2.imwrite(f'imgs/p3_post_proc{i}.png', thresh4)
    print(f"P3: {pytesseract.image_to_string(thresh4, config=config, lang='eng')}")

print(f"Codewords: {codewords}")
print(f"Placements: {placements}")
cv2.waitKey(0)
cv2.destroyAllWindows()