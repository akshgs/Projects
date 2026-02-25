import cv2
import numpy as np
import mediapipe as mp

# ---------------- INITIALIZATION ----------------

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

canvas = None
px, py = 0, 0
draw_color = (255, 0, 255)
brush_thickness = 6

print("☝ Draw | ✌ Change Color | ✋ Five Fingers = Erase")

# ---------------- MAIN LOOP ----------------

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    h, w, c = frame.shape

    if canvas is None:
        canvas = np.zeros((h, w, 3), dtype=np.uint8)

    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for idx, hand_lm in enumerate(results.multi_hand_landmarks):

            lm_list = []
            for id, lm in enumerate(hand_lm.landmark):
                img_x, img_y = int(lm.x * w), int(lm.y * h)
                lm_list.append([id, img_x, img_y])

            if len(lm_list) == 0:
                continue

            x1, y1 = lm_list[8][1], lm_list[8][2]

            # ---------------- FINGER DETECTION ----------------
            fingers = []

            # Thumb (kept but not used for logic)
            fingers.append(1 if lm_list[4][1] < lm_list[3][1] else 0)

            # Other fingers
            fingers.append(1 if lm_list[8][2] < lm_list[6][2] else 0)   # Index
            fingers.append(1 if lm_list[12][2] < lm_list[10][2] else 0) # Middle
            fingers.append(1 if lm_list[16][2] < lm_list[14][2] else 0) # Ring
            fingers.append(1 if lm_list[20][2] < lm_list[18][2] else 0) # Pinky

            # ---------------- ERASE MODE ----------------
            # Index + Middle + Ring + Pinky up
            if fingers[1] and fingers[2] and fingers[3] and fingers[4]:

                cv2.putText(frame, "ERASE MODE",
                            (500, 50),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,
                            (0, 0, 255),
                            3)

                cv2.circle(canvas, (x1, y1), 70, (0, 0, 0), cv2.FILLED)
                px, py = 0, 0

            # ---------------- COLOR MODE ----------------
            # Index + Middle up only
            elif fingers[1] and fingers[2] and not fingers[3] and not fingers[4]:

                px, py = 0, 0

                cv2.putText(frame, "COLOR MODE",
                            (500, 50),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,
                            (255, 0, 0),
                            3)

                if x1 < w // 3:
                    draw_color = (255, 0, 255)  # Pink
                elif x1 < 2 * w // 3:
                    draw_color = (0, 255, 0)    # Green
                else:
                    draw_color = (0, 0, 255)    # Red

            # ---------------- DRAW MODE ----------------
            # Only Index up
            elif fingers[1] and not fingers[2]:

                cv2.putText(frame, "DRAW MODE",
                            (500, 50),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            1,
                            draw_color,
                            3)

                if px == 0 and py == 0:
                    px, py = x1, y1

                cv2.circle(frame, (x1, y1), 10, draw_color, cv2.FILLED)
                cv2.line(canvas, (px, py), (x1, y1),
                         draw_color, brush_thickness)

                px, py = x1, y1

            else:
                px, py = 0, 0

            mp_draw.draw_landmarks(frame, hand_lm,
                                   mp_hands.HAND_CONNECTIONS)

    # ---------------- MERGE CANVAS ----------------

    img_gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, img_inv = cv2.threshold(img_gray, 20, 255, cv2.THRESH_BINARY_INV)
    img_inv = cv2.cvtColor(img_inv, cv2.COLOR_GRAY2BGR)

    frame = cv2.bitwise_and(frame, img_inv)
    frame = cv2.bitwise_or(frame, canvas)

    cv2.putText(frame, "C = Clear | Q = Quit",
                (10, 50),
                cv2.FONT_HERSHEY_PLAIN,
                2,
                (0, 0, 0),
                2)

    cv2.imshow("Air Canvas", frame)

    key = cv2.waitKey(1)

    if key == ord('q'):
        break
    elif key == ord('c'):
        canvas = None

cap.release()
cv2.destroyAllWindows()