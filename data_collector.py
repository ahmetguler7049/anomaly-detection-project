import cv2
import time

cam = cv2.VideoCapture(1)
sampleNum = 0

while sampleNum < 50:
    ret, img = cam.read()
    cv2.imshow("Data Collector", img)

    sampleNum = sampleNum + 1
    cv2.imwrite("dataset/lion/p/anomaly_sample_" + str(sampleNum) + ".jpg", img)
    print(str(sampleNum) + " tane resim cekildi")
    time.sleep(2)
    if cv2.waitKey(100) & 0xFF == ord('q'):
        break


cam.release()
cv2.destroyAllWindows()

