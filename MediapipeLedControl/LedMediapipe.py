import cv2
import mediapipe as mp
import requests

esp_ip = "http://192.168.4.1"  # Default IP for ESP in AP mode

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
prev_state = None

def is_hand_open(landmarks):
    fingers = []
    tips = [8, 12, 16, 20]  # Index to pinky
    for tip in tips:
        if landmarks[tip].y < landmarks[tip - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)
    return sum(fingers) >= 3  # Consider open if 3+ fingers are up

while True:
    success, img = cap.read()
    if not success:
        break

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

            if is_hand_open(handLms.landmark):
                if prev_state != "open":
                    print("Open hand – LED ON")
                    try:
                        requests.get(f"{esp_ip}/on")
                    except:
                        print("Error sending ON request")
                    prev_state = "open"
            else:
                if prev_state != "closed":
                    print("Closed hand – LED OFF")
                    try:
                        requests.get(f"{esp_ip}/off")
                    except:
                        print("Error sending OFF request")
                    prev_state = "closed"

    cv2.imshow("Hand Detection", img)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
        break

cap.release()
cv2.destroyAllWindows()
