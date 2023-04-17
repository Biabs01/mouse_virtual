import cv2
import math
import mediapipe as mp
from pynput.mouse import Button, Controller
import pyautogui

mouse = Controller()

cap = cv2.VideoCapture(0)

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

(screen_width, screen_height) = pyautogui.size()

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5)

tipIds = [4, 8, 12, 16, 20]

pinch = False

def countFingers(image, hand_landmarks, handNo=0):

    global pinch

    if hand_landmarks:
        landmarks = hand_landmarks[handNo].landmark
        print(landmarks)

        fingers = []

        for lm_index in tipIds:
            finger_tip_y = landmarks[lm_index].y
            finger_bottom_y = landmarks[lm_index - 2].y

            if lm_index != 4:
                if finger_tip_y < finger_bottom_y:
                    fingers.append(1)
                    print("Dedo com id ", lm_index, "está aberto")

                if finger_tip_y > finger_bottom_y:
                    fingers.append(0)
                    print("Dedo com id ", lm_index, "está fechado")

        totalFingers = fingers.count(1)

        #PINÇA 

        #desenhar a linha do indicador ao dedão
        finger_tip_x = int((landmarks[8].x)*width)
        finger_tip_y = int((landmarks[8].y)*height)

        thumb_tip_x = int((landmarks[4].x)*width)
        thumb_tip_y = int((landmarks[4].y)*height)

        cv2.line(image, (finger_tip_x, finger_tip_y), (thumb_tip_x, thumb_tip_y), (255, 0, 0), 2)

        #desenhar o ponto central da linha

        center_x = int((finger_tip_x + thumb_tip_x)/2)
        center_y = int((finger_tip_y + thumb_tip_y)/2)

        cv2.circle (image, (center_x, center_y) (0, 0, 255), 2)

        text = f'Dedos: {totalFingers}'

        cv2.putText(image, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

def drawHandLandmarks(image, hand_landmarks):
    if hand_landmarks:

        for landmarks in hand_landmarks:

            mp_drawing.draw_landmarks(image, landmarks, mp_hands.HAND_CONNECTIONS)

while True:
    success, image = cap.read()

    image = cv2.flip(image, 1)

    results = hands.process(image)

    hand_landmarks = results.multi_hand_landmarks

    drawHandLandmarks(image, hand_landmarks)

    countFingers(image, hand_landmarks)

    cv2.imshow("Controlador de Midia", image)

    key = cv2.waitKey(1)
    if key == 32:
        break

cv2.destroyAllWindows()

