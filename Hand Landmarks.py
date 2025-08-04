import mediapipe as mp
import cv2
import time

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands(False)
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0

while True:

    success, img = cap.read()
    img = cv2.flip(img,1)

    results = hands.process(img)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
            for id, lm in enumerate(handLms.landmark):
                for i in range(0, 20):
                    if id == i:
                        h,w,c=img.shape
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        cv2.putText(img, str(i),(cx,cy), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0), 1)



    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 1)

    cv2.imshow("image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
