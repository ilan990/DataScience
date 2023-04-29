import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)
pTime = 0

mpDraw = mp.solutions.drawing_utils
mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh(max_num_faces=4)
drawSpec = mpDraw.DrawingSpec(thickness=1, circle_radius=1)

frameWidth = 1920
frameHeight = 1080
cap.set(3,frameWidth)
cap.set(4,frameHeight)
cap.set(10,150)

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results = faceMesh.process(imgRGB) #construit le maillage ou le visage trouvé
    if results.multi_face_landmarks:
        for faceLms in results.multi_face_landmarks: #Pour chaque maillage ou visage trouvé
            #On dessine le visage
            mpDraw.draw_landmarks(img, faceLms, mpFaceMesh.FACEMESH_TESSELATION, drawSpec, drawSpec)
    cTime = time.time() #(mili) secondes actuelle
    fps = 1 / (cTime - pTime) # fps = 1 / (secondes actuelles - secondes précedentes)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}',(20,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0),3)
    cv2.imshow('Image',img)
    if cv2.waitKey(1) == 27:
        break
cap.release()


