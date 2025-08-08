import mediapipe as mp
import cv2
import time

cap = cv2.VideoCapture(0)

mpFaceDetection = mp.solutions.face_detection
face = mpFaceDetection.FaceDetection()
mpDraw=mp.solutions.drawing_utils

pTime = 0
cTime = 0

while True:

    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.flip(img,1)

    results = face.process(img)

    if results.detections:
        for id, detection in enumerate(results.detections):
            mpDraw.draw_detection(img, detection)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 1)

    cv2.imshow("image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


