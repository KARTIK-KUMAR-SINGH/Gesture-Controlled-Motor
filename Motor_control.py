import cv2
import serial
import time
import mediapipe as mp
import math

# ---------- Arduino Connection ----------
board = serial.Serial('COM6', 9600)
time.sleep(2)

# ---------- MediaPipe Setup ----------
mp_hand_module = mp.solutions.hands
detector = mp_hand_module.Hands(max_num_hands=1)

drawer = mp.solutions.drawing_utils

# ---------- Camera ----------
camera = cv2.VideoCapture(0)

while True:

    ret, frame = camera.read()
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    detection = detector.process(rgb_frame)

    if detection.multi_hand_landmarks:

        for single_hand in detection.multi_hand_landmarks:

            # Different landmark appearance
            drawer.draw_landmarks(
                frame,
                single_hand,
                mp_hand_module.HAND_CONNECTIONS,
                drawer.DrawingSpec(color=(255,120,0), thickness=1),
                drawer.DrawingSpec(color=(0,200,255), thickness=2)
            )

            points = []
            height, width, _ = frame.shape

            for mark in single_hand.landmark:
                px = int(mark.x * width)
                py = int(mark.y * height)
                points.append((px, py))

            if len(points) > 8:

                thumb_tip = points[4]
                index_tip = points[8]

                # New visual indicator (rectangle instead of circles)
                cv2.rectangle(frame,
                              (thumb_tip[0]-6, thumb_tip[1]-6),
                              (thumb_tip[0]+6, thumb_tip[1]+6),
                              (255,255,0), -1)

                cv2.rectangle(frame,
                              (index_tip[0]-6, index_tip[1]-6),
                              (index_tip[0]+6, index_tip[1]+6),
                              (255,255,0), -1)

                # Different connection style
                cv2.arrowedLine(frame,
                                thumb_tip,
                                index_tip,
                                (50,255,50),
                                2)

                gap = int(math.dist(thumb_tip, index_tip))

                pwm_value = int((gap / 200) * 255)
                pwm_value = max(0, min(255, pwm_value))

                board.write((str(pwm_value) + "\n").encode())

                # Side panel display (different UI layout)
                cv2.rectangle(frame, (0,0), (180,120),
                              (20,20,20), -1)

                cv2.putText(frame,
                            "Gesture Motor",
                            (10,35),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.7,
                            (255,255,255),
                            2)

                cv2.putText(frame,
                            f"PWM : {pwm_value}",
                            (10,80),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.9,
                            (0,255,255),
                            2)

    cv2.imshow("Gesture Controller", frame)

    if cv2.waitKey(1) == 27:   # ESC to exit
        break

camera.release()
cv2.destroyAllWindows()