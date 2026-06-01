from picamera2 import Picamera2
import cv2
import cv2.aruco as aruco
import numpy as np
import time

# ---------------- CAMERA ----------------
picam2 = Picamera2()

config = picam2.create_video_configuration(
    main={"format": "RGB888", "size": (640, 480)}
)

picam2.configure(config)
picam2.start()

time.sleep(2)

# ---------------- ARUCO ----------------
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
params = aruco.DetectorParameters()

WIDTH = 640
HEIGHT = 480
cx = WIDTH // 2
cy = HEIGHT // 2

print("Starting offset tracking...")

while True:
    frame = picam2.capture_array()
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    corners, ids, _ = aruco.detectMarkers(gray, aruco_dict, parameters=params)

    if ids is not None:
        c = corners[0][0]

        mx = int(np.mean(c[:, 0]))
        my = int(np.mean(c[:, 1]))

        x_offset = mx - cx
        y_offset = my - cy

        print(f"ID: {ids[0][0]} | X_offset: {x_offset} | Y_offset: {y_offset}")
    else:
        print("No marker detected")

    time.sleep(0.01)
