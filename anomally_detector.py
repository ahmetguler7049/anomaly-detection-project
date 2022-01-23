import serial
import time
import cv2
import numpy as np

frameWidth = 640
frameHeight = 480
cam = cv2.VideoCapture(1)
cam.set(3, frameWidth)
cam.set(4, frameHeight)

arduino = serial.Serial(port='COM3', baudrate=9600, timeout=.1)
time.sleep(1)

car_front_cascadePath = "dataset/car_front/car_front_cascade.xml"
car_frontCascade = cv2.CascadeClassifier(car_front_cascadePath)
lion_cascadePath = "dataset/lion/classifier/lion_cascade.xml"
lionCascade = cv2.CascadeClassifier(lion_cascadePath)


def send_data(data, ard):
    ard.write(bytes(data, 'utf-8'))
    time.sleep(0.05)
    data_write = ard.readline()
    return data_write


def stackImages(scale, imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range(0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]),
                                                None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y] = cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank] * rows
        hor_con = [imageBlank] * rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None, scale,
                                         scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        ver = hor
    return ver


def getContours(img, imgContour):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 5500:
            send_data("1", arduino)
            cv2.drawContours(imgContour, cnt, -1, (255, 0, 255), 7)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            print(len(approx))
            x, y, w, h = cv2.boundingRect(approx)
            cv2.rectangle(imgContour, (x, y), (x + w, y + h), (0, 255, 0), 5)

            cv2.putText(imgContour, "Points: " + str(len(approx)), (x + w + 20, y + 20), cv2.FONT_HERSHEY_COMPLEX,
                        .7,
                        (0, 255, 0), 2)
            cv2.putText(imgContour, "Area: " + str(int(area)), (x + w + 20, y + 45), cv2.FONT_HERSHEY_COMPLEX, 0.7,
                        (0, 255, 0), 2)


while True:
    success, frame = cam.read()
    imgContour = frame.copy()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lh = 5
    ls = 15
    lv = 0
    uh = 22
    us = 255
    uv = 255
    lower_color = np.array([lh, ls, lv])
    upper_color = np.array([uh, us, uv])

    mask = cv2.inRange(frame, lower_color, upper_color)
    img = cv2.bitwise_and(frame, frame, mask=mask)

    imgBlur = cv2.GaussianBlur(img, (7, 7), 1)
    imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)
    threshold1 = 119
    threshold2 = 117
    imgCanny = cv2.Canny(imgGray, threshold1, threshold2)
    kernel = np.ones((5, 5))
    imgDil = cv2.dilate(imgCanny, kernel, iterations=1)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    lion_detected = lionCascade.detectMultiScale(gray, 1.05, 3)
    car_front_detected = car_frontCascade.detectMultiScale(gray, 1.05, 3)

    if len(lion_detected) != 0:
        for (x, y, w, h) in lion_detected:
            cv2.rectangle(imgContour, (x, y), (x + w, y + h), (225, 0, 0), 2)
            print("Vahşi Hayvan")
            send_data("2", arduino)

    elif len(car_front_detected) != 0:
        for (x, y, w, h) in car_front_detected:
            cv2.rectangle(imgContour, (x, y), (x + w, y + h), (225, 0, 0), 2)
            print("Ters Yön")
            send_data("3", arduino)

    elif len(lion_detected) == 0 and len(car_front_detected) == 0:
        getContours(imgDil, imgContour)

    else:
        send_data("0", arduino)

    imgStack = stackImages(0.8, ([img, imgCanny],
                                 [imgDil, imgContour]))
    cv2.imshow("Result", imgStack)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
