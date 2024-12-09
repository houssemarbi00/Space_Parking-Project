import cv2
import pickle
 
width, height = 200, 400
 
try:
    with open('D:\PROJET\Python projects\SpaceParkink\PresenceDeVoiturePoss', 'rb') as f:
        posList = pickle.load(f)
except:
    posList = []
 
def mouseClick(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x, y))
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList):
            x1, y1 = pos
            if x1 <= x <= x1 + width and y1 <= y <= y1 + height:
                posList.pop(i)
    with open('D:\PROJET\Python projects\SpaceParkink\PresenceDeVoiturePoss', 'wb') as f:
        pickle.dump(posList, f)

cap = cv2.VideoCapture(0)  
while True:
    sucess , img = cap.read()
    for pos in posList:
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)
 

    cv2.imshow("Image", img)
    cv2.setMouseCallback("Image", mouseClick)
    cv2.waitKey(1)