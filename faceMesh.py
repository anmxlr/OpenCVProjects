
import mediapipe as mp
import cv2
import time

from mediapipe.python.solutions.drawing_utils import DrawingSpec

cap = cv2.VideoCapture(0)
mpDraw=mp.solutions.drawing_utils
mpFaceMesh = mp.solutions.face_mesh
faceMesh= mpFaceMesh.FaceMesh(False,2,False,0.7,0.7)
drawSpec=DrawingSpec(thickness=1,circle_radius=1,color=(50,255,50))

pTime = 0
cTime = 0

while True:

    success, img = cap.read()

    img = cv2.flip(img,1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    results = faceMesh.process(imgRGB)

    if results.multi_face_landmarks:
        for faceLMS in results.multi_face_landmarks:
            mpDraw.draw_landmarks(img,faceLMS,mpFaceMesh.FACEMESH_CONTOURS,drawSpec,drawSpec )
            h, w, _ = img.shape
            for id, lm in enumerate(faceLMS.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)






    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 255), 1)

    cv2.imshow("image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


