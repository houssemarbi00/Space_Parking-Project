import cv2
import datetime
import pickle
import cvzone
import numpy as np
from immat import immat


cap=cv2.VideoCapture(0)

with open('D:\PROJET\Python projects\SpaceParkink\PresenceDeVoiturePoss', 'rb') as f:
    posList = pickle.load(f)
 
width, height = 200, 400
 
 
def checkParkingSpace(imgPro):
    spaceCounter = 0

    for i,pos in enumerate(posList):
        x, y = pos
 
        imgCrop = imgPro[y:y + height, x:x + width]
        count = cv2.countNonZero(imgCrop)
 
 
        if count < 2000:
            color = (0, 255, 0)
            thickness = 5
            spaceCounter += 1
            
            
        else:
            color = (0, 0, 255)
            thickness = 2
            now=datetime.datetime.today()
            if (int(now.strftime("%S")) % 10==0) or (int(now.strftime("%S"))==59) : 
                now=now.strftime("%y-%m-%d %H-%M-%S")
                PicNoun=f'D:\PROJET\Python projects\SpaceParkink\capture_immat\{now}.jpg' 
                cv2.imwrite(PicNoun,img)
            try: 
                
                #immat(PicNoun)
                 
                font=cv2.FONT_HERSHEY_SIMPLEX
                #cv2.putText(img,"!!!!immatricule detecter!!!!",(100,500),fontFace=font,
                #           fontScale=1,color=(0,255,0),thickness=2, lineType=cv2.LINE_AA)
                
            except :
                font=cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(img,"!!!!immatricule n'est pas detecter!!!!",(100,500),fontFace=font,
                           fontScale=1,color=(0,0,255),thickness=2, lineType=cv2.LINE_AA)   
                
        
        cvzone.putTextRect(img, str(count), (x, y + height - 3), scale=1,
                           thickness=2, offset=0, colorR=color)
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
    


while True:
 
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    success, img = cap.read()
    img = cv2.resize(img, (800,600) )
    #img = cv2.flip(img,1)
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)  
    
    checkParkingSpace(imgDilate)
    
    cv2.imshow("Image", img)

    if cv2.waitKey(10) & 0xFF == ord('k'):
        break
cap.release()
cv2.destroyAllWindows()