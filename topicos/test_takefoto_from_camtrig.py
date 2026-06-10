#!/usr/bin/env python3

from pymavlink import mavutil
from picamera2 import Picamera2
from pathlib import Path

import os
import time
from datetime import datetime


# =========================
# CONFIG
# =========================

PORT = "/dev/serial0"
BAUD = 57600

SAVE_DIR = str(
    Path.home() / "image_test"
)

os.makedirs(
    SAVE_DIR,
    exist_ok=True
)


# =========================
# MAVLINK
# =========================

def conectar():

    while True:

        try:

            print("\nConectando MAVLink...")

            master = mavutil.mavlink_connection(
                PORT,
                baud=BAUD
            )

            master.wait_heartbeat(
                timeout=15
            )

            print("MAVLink conectado")

            return master

        except Exception as e:

            print(
                f"Error conexión: {e}"
            )

            time.sleep(2)


# =========================
# CAMARA
# =========================

print("Inicializando cámara...")

cam = Picamera2()

config = cam.create_still_configuration()

cam.configure(
    config
)

cam.start()

time.sleep(2)

print("Cámara lista")


# =========================
# LOOP
# =========================

master = conectar()

ultimo_idx = -1

print("\nEsperando trigger...\n")


while True:

    try:

        msg = master.recv_match(
            type="CAMERA_FEEDBACK",
            blocking=True
        )

        if msg is None:
            continue

        idx = msg.img_idx

        # Evitar repetidos
        if idx == ultimo_idx:
            continue

        ultimo_idx = idx

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        nombre = (
            f"img_{idx}_{timestamp}.jpg"
        )

        ruta = os.path.join(
            SAVE_DIR,
            nombre
        )

        print(
            f"\nTRIGGER RECIBIDO"
        )

        print(
            f"Capturando {nombre}"
        )

        cam.capture_file(
            ruta
        )

        print(
            f"Guardado:\n{ruta}"
        )

    except KeyboardInterrupt:

        print("\nSaliendo")

        break

    except Exception as e:

        print(
            f"\nERROR: {e}"
        )

        print(
            "Reconectando..."
        )

        time.sleep(2)

        master = conectar()


cam.stop()
