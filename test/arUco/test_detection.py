import cv2
import numpy as np
import socket

# ---------------- UDP ----------------
PC_IP = "192.168.1.21"   # <-- cambia esto
PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# ---------------- ARUCO ----------------
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
detector = cv2.aruco.ArucoDetector(aruco_dict)

# ---------------- CAMERA ----------------
cap = cv2.VideoCapture("pipe:0")  # o tu stream funcional

# calib (pon tus reales después)
fx, fy = 600, 600
cx, cy = 320, 240

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    corners, ids, _ = detector.detectMarkers(frame)

    if ids is not None:
        c = corners[0][0]

        u = int(np.mean(c[:,0]))
        v = int(np.mean(c[:,1]))

        angle_x = (u - cx) / fx
        angle_y = (v - cy) / fy

        msg = f"{ids[0][0]},{angle_x:.4f},{angle_y:.4f}"

        sock.sendto(msg.encode(), (PC_IP, PORT))

        print("Enviado:", msg)

    else:
        sock.sendto(b"NONE", (PC_IP, PORT))
