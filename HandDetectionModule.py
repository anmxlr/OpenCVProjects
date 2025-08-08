import mediapipe as mp
import cv2
import time

def capture_video(camera_number,width,height):
    cap = cv2.VideoCapture(0)
    cap.set(3,width)
    cap.set(4,height)

    return cap

def show(cap,fps=True,connections=True,PosList=[]):
    mpHands = mp.solutions.hands
    hands = mpHands.Hands(False, min_detection_confidence=0.7)
    mpDraw = mp.solutions.drawing_utils

    pTime = 0
    cTime = 0

    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)

        if fps:
            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime
            cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 1)


        PosList=[(0,0)]*21
        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                if connections:
                    mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

                for id, lm in enumerate(handLms.landmark):
                    for i in range(0, 21):
                        if id == i:

                            h, w, c = img.shape
                            cx, cy = int(lm.x * w), int(lm.y * h)
                            cv2.putText(img, str(int(i)), (cx,cy), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,0, 255), 1)
                            PosList[i] = (cx, cy)

        cv2.imshow("image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


cap=capture_video(0,640,480)
show(cap)
