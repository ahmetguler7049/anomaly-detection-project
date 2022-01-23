import cv2
import numpy as np

cap = cv2.VideoCapture(1)

def nothing(x):
    pass

cv2.namedWindow("Trackbar")
cv2.resizeWindow("Trackbar",500,250)

cv2.createTrackbar("Lower-H","Trackbar",0,180,nothing)
cv2.createTrackbar("Lower-S","Trackbar",0,255,nothing)
cv2.createTrackbar("Lower-V","Trackbar",0,255,nothing)

cv2.createTrackbar("Upper-H","Trackbar",0,180,nothing)
cv2.createTrackbar("Upper-S","Trackbar",0,255,nothing)
cv2.createTrackbar("Upper-V","Trackbar",0,255,nothing)

cv2.setTrackbarPos("Upper-H","Trackbar",180)
cv2.setTrackbarPos("Upper-S","Trackbar",255)
cv2.setTrackbarPos("Upper-V","Trackbar",255)

while 1:
    ret,frame = cap.read()
    frame = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    lh = cv2.getTrackbarPos("Lower-H","Trackbar")
    ls = cv2.getTrackbarPos("Lower-S","Trackbar")
    lv = cv2.getTrackbarPos("Lower-V","Trackbar")
    
    uh = cv2.getTrackbarPos("Upper-H","Trackbar")
    us = cv2.getTrackbarPos("Upper-S","Trackbar")
    uv = cv2.getTrackbarPos("Upper-V","Trackbar")

    lower_color = np.array([lh,ls,lv])
    upper_color = np.array([uh,us,uv])

    lower_blue = np.array([110,50,50])
    upper_blue = np.array([130,255,255])

    mask = cv2.inRange(hsv,lower_color,upper_color)
    # mask = cv2.erode(mask, (5, 5), iterations=2)
    # mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, (5, 5))
    # mask = cv2.dilate(mask, (5, 5), iterations=1)
    # mask_blue = cv2.inRange(hsv , lower_blue, upper_blue)

    cv2.imshow("original",frame)
    cv2.imshow("mask",mask)
    son = cv2.bitwise_and(frame,frame,mask=mask)
    cv2.imshow("son hali",son)

    if cv2.waitKey(5) & 0xFF==ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
