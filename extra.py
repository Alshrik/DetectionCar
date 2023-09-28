import cv2
import pytesseract
import imutils
import numpy as np

def extract_number(image):
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    #image=cv2.imread(image)
    gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    bfilter=cv2.bilateralFilter(blur,11,17,17)
    edged=cv2.Canny(bfilter,30,200) 

    keypoints=cv2.findContours(edged.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contourss=imutils.grab_contours(keypoints)
    contours=sorted(contourss,key=cv2.contourArea,reverse=True)[:10]
    len(contours)

    lacation=None
    for contour in contours:
        approx=cv2.approxPolyDP(contour,10,True)
        if len(approx)==4:
            lacation=approx
            break
        
    len(lacation)
    approx[1][0][0]

    mask=np.zeros(gray.shape,np.uint8)
    new_image =cv2.drawContours(mask,[lacation],-1,255,-1)
    new_image =cv2.bitwise_and(image,image,mask=mask)

    (x,y)=np.where(mask==255)
    (x1,y1)=(np.min(x),np.min(y))
    (x2,y2)=(np.max(x),np.max(y))
    cropped_image=gray[x1:x2+1,y1:y2+1]

        #reader=easyocr.Reader(['en'])
        #result = reader.readtext(cropped_image)
        #result=pytesseract.image_to_string(cropped_image,config='-c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ --psm 8 --oem 3 ara')
    result = pytesseract.image_to_string(cropped_image, config='-c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ --psm 8 --oem 3 ara+eng')
    # print(result)
    return result

# result = extract_number('static\images\image3.jpg')
# print(result)
