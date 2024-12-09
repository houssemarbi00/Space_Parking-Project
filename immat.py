import cv2
from matplotlib import pyplot as plt
import numpy as np
import imutils
import easyocr


def immat(x):


        img = cv2.imread(x)
        img = cv2.resize(img, (620,480) )
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        
        #plt.imshow(gray)
        #plt.show()alias
        
        bfilter = cv2.bilateralFilter(gray, 11, 17, 17) 
        edged = cv2.Canny(bfilter, 30, 200) 
        #plt.imshow(edged)
        #plt.show()
        
        keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(keypoints)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
        
        #new_image = cv2.drawContours(img, contours, -1,255, 2)
        #plt.imshow(new_image)
        #plt.show()
        
        location = None
        for contour in contours:
            peri = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.018*peri, True)
            if len(approx) == 4:
                location = approx
                break
        
        mask = np.zeros(gray.shape, np.uint8)
        new_image = cv2.drawContours(mask, [location], -1,255, -1)
        new_image = cv2.bitwise_and(img, img, mask=mask)
        #plt.imshow(new_image)
        #plt.show()
        
        (x,y) = np.where(mask==255)
        (x1, y1) = (np.min(x), np.min(y))
        (x2, y2) = (np.max(x), np.max(y))
        cropped_image = gray[x1:x2+1, y1:y2+1]
        #plt.imshow(cropped_image)
        #plt.show()
        
        reader = easyocr.Reader(["en","ar"])
        result = reader.readtext(cropped_image)
        #print(result)
        
        
        text = result[0][-2]
        text1=text[-3:]
        text2=text[0:5]
        hourouf="ءآأؤإئااًبةتثجحخدذرزسشصضطظعغفقكلمنهوىيًٌٍَُِّْٰٓٔٱٹپچڈڑژکڭگںھۀہۂۃۆۇۈۋیېےۓ"
        
        for alphabet in hourouf :
            try:
                if (text[7]==alphabet ):
                    txt=f"'{text1}تونس{text2}'"
                    break
                else :
                    txt=text 
            except IndexError :    
                txt=result
        
        #print(txt)
        with open ('D:\PROJET\Python projects\SpaceParkink\immat.txt','a+',encoding='utf-8') as fichier  :
            fichier.write(txt+"\n")
        
        
        font=cv2.FONT_HERSHEY_SIMPLEX
        res = cv2.putText(img, text=text, org=(approx[0][0][0], approx[1][0][1]+60), fontFace=font,
                               fontScale=1, color=(0,255,0), thickness=2, lineType=cv2.LINE_AA)
        res = cv2.rectangle(img, tuple(approx[0][0]), tuple(approx[2][0]), (0,255,0),3)
        plt.imshow(cv2.cvtColor(res, cv2.COLOR_BGR2RGB))
        plt.show()
    
        