import mediapipe as mp
import cv2
import time
import utils
import pyautogui as pag

from utils import get_distance

mpHands = mp.solutions.hands
hands = mpHands.Hands(False,min_detection_confidence=0.7,min_tracking_confidence=0.5,max_num_hands=1)

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
mpDraw = mp.solutions.drawing_utils

try:
    while cap.isOpened():
        success, img = cap.read()

        if not success:
            break
        img = cv2.flip(img, 1)
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)

        landmarkList = [(0,0)]*21

        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            mpDraw.draw_landmarks(img, hand_landmarks, mpHands.HAND_CONNECTIONS)

            for id, lm in enumerate(hand_landmarks.landmark):
                for i in range(0, 21):
                    if id == i:
                        h, w, c = img.shape
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        landmarkList[i]=(cx, cy)

            x, y = pag.size()
            if int(landmarkList[8][0] * (x/550)) < x and int(landmarkList[8][1] * (x/400)) < y:
                pag.moveTo(int(landmarkList[12][0] * (x/550)), int(landmarkList[12][1] * (y/400)))

                if utils.get_distance(landmarkList,8,12)<40:
                    pag.click()


        #print(is_down(landmarkList,1),is_down(landmarkList,2),is_down(landmarkList,3),is_down(landmarkList,4),is_down(landmarkList,5))
        cv2.putText(img, str(get_distance(landmarkList,8,12)), (10, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 1)

        cv2.imshow("image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
