import mediapipe as mp
import cv2
from ctypes import cast,POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities,IAudioEndpointVolume
from utils import get_distance

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL,None)
Volume=cast(interface,POINTER(IAudioEndpointVolume))

VolumeRange=Volume.GetVolumeRange()
Vmin,Vmax=VolumeRange[0],VolumeRange[1]
wCam,hCam= 640,480

cap=cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)

mpHands = mp.solutions.hands
hands = mpHands.Hands(False,min_detection_confidence=0.7,min_tracking_confidence=0.7)
mpDraw = mp.solutions.drawing_utils

PosList=[(0,0)]*21
dist=0
while True:
    success,img=cap.read()
    img = cv2.flip(img, 1)
    results = hands.process(img)
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
            for id, lm in enumerate(handLms.landmark):
                for i in range(0, 21):
                    if id == i:
                        h, w, c = img.shape
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        PosList[i] = (cx, cy)

        dist_for_ratio=get_distance(PosList,4,3)
        dist=get_distance(PosList,8,4)
        ratio=dist/dist_for_ratio


        if(ratio<1):
            ratio=1
        if(ratio>5):
            ratio=5

        vol= ((ratio - 1) * 100) / 4
        cv2.line(img, PosList[8], PosList[4], (0, 255 - vol * (2.55), vol * (2.55)), 2)
        cv2.putText(img,f'volume ={str(int(vol))} %', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        cv2.rectangle(img,(50,150),(85,400), (0,0,0), 2)
        cv2.rectangle(img, (50,int(400 - vol * 2.5)), (85, 400), (0, 255 - vol * (2.55), vol * (2.55)), cv2.FILLED)
        Volume.SetMasterVolumeLevel(int(((Vmin-Vmax)*(100-vol)/100)), None)

    cv2.imshow("img", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
cv2.VideoCapture(0).release()
