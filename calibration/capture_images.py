import cv2
import numpy as np
import sys

cap = cv2.VideoCapture("pipe:0")

if not cap.isOpened():
    print("❌ no se pudo abrir pipe")
    exit()

i = 0

print("📸 Presiona 's' para guardar")

while True:
    ret, frame = cap.read()

    if not ret:
        continue

    cv2.imshow("calib", frame)

    key = cv2.waitKey(1)

    if key == ord('s'):
        cv2.imwrite(f"img_{i}.jpg", frame)
        print("guardada", i)
        i += 1

    elif key == 27:
        break

cap.release()
cv2.destroyAllWindows()
