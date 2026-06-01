from picamera2 import Picamera2
import cv2
import cv2.aruco as aruco
import numpy as np
import time
import math

# ---------------- CONFIGURACIÓN DE CALIBRACIÓN ----------------
# Matriz intrínseca (K) y coeficientes de distorsión proporcionados
camera_matrix = np.array([[714.23, 0.0, 305.37], 
                          [0.0, 716.09, 249.52], 
                          [0.0, 0.0, 1.0]], dtype=np.float32)

dist_coeffs = np.array([-0.490, 0.324, 0.0013, -0.00086, -0.625], dtype=np.float32)

# Parámetros del marcador
MARKER_SIZE = 0.16  # 16cm en metros
ARUCO_DICT = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
ARUCO_PARAMS = aruco.DetectorParameters()

# ---------------- CONFIGURACIÓN DE CÁMARA ----------------
picam2 = Picamera2()
config = picam2.create_video_configuration(main={"format": "RGB888", "size": (640, 480)})
picam2.configure(config)
picam2.start()

def get_full_6dof(rvec, tvec):
    """
    Calcula la posición y los ángulos de Euler corregidos.
    """
    # Traslación directa
    x, y, z = tvec[0]

    # Convertir vector de rotación a matriz
    rmat, _ = cv2.Rodrigues(rvec)
    
    # Extraer ángulos de Euler
    # Usamos la descomposición para obtener Roll, Pitch, Yaw
    sy = math.sqrt(rmat[0,0] * rmat[0,0] +  rmat[1,0] * rmat[1,0])
    singular = sy < 1e-6

    if not singular:
        roll_raw = math.atan2(rmat[2,1] , rmat[2,2])
        pitch_raw = math.atan2(-rmat[2,0], sy)
        yaw_raw = math.atan2(rmat[1,0], rmat[0,0])
    else:
        roll_raw = math.atan2(-rmat[1,2], rmat[1,1])
        pitch_raw = math.atan2(-rmat[2,0], sy)
        yaw_raw = 0

    roll = math.degrees(roll_raw)
    pitch = math.degrees(pitch_raw)
    yaw = math.degrees(yaw_raw)

    # --- CORRECCIÓN DEL SALTO DE 180° ---
    # OpenCV asume que el eje Z de la cámara y del marcador están enfrentados.
    # Si detectamos que el Roll está invertido (cerca de 180), lo normalizamos.
    if roll > 90:
        roll -= 180
    elif roll < -90:
        roll += 180
    
    # Invertir Pitch si es necesario según la orientación física de tu montaje
    # pitch = -pitch 

    return x, y, z, roll, pitch, yaw

print("--- Iniciando Rastreo 6DoF Corregido ---")

try:
    while True:
        frame = picam2.capture_array()
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        corners, ids, _ = aruco.detectMarkers(gray, ARUCO_DICT, parameters=ARUCO_PARAMS)

        if ids is not None:
            rvecs, tvecs, _ = aruco.estimatePoseSingleMarkers(
                corners, MARKER_SIZE, camera_matrix, dist_coeffs
            )

            for i in range(len(ids)):
                # Obtener datos 6DoF procesados
                pos_x, pos_y, pos_z, ang_roll, ang_pitch, ang_yaw = get_full_6dof(rvecs[i], tvecs[i])

                # Limpiar pantalla de consola para lectura fácil
                print("\033[H\033[J") 
                print(f"ID: {ids[i][0]} | Marcador: {MARKER_SIZE*100}cm")
                print("-" * 40)
                print(f"POSICIÓN (Metros):")
                print(f"  X (Lateral):      {pos_x:7.3f}")
                print(f"  Y (Longitudinal): {pos_y:7.3f}")
                print(f"  Z (Altura/Dist):  {pos_z:7.3f}")
                print("-" * 40)
                print(f"ORIENTACIÓN (Grados):")
                print(f"  Roll (Alabeo):    {ang_roll:7.2f}°")
                print(f"  Pitch (Cabeceo):  {ang_pitch:7.2f}°")
                print(f"  Yaw (Guiñada):    {ang_yaw:7.2f}°")
                print("-" * 40)
                
                # Visualización opcional (Dibuja los ejes en el frame si tuvieras pantalla)
                # cv2.drawFrameAxes(frame, camera_matrix, dist_coeffs, rvecs[i], tvecs[i], 0.1)

        time.sleep(0.02) # ~50Hz de refresco máximo

except KeyboardInterrupt:
    print("\nDeteniendo...")
finally:
    picam2.stop()
