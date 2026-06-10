from pymavlink import mavutil
import time

PORT = "/dev/serial0"
BAUD = 57600


def conectar():

    while True:

        try:

            master = mavutil.mavlink_connection(
                PORT,
                baud=BAUD
            )

            master.wait_heartbeat()

            print("Conectado")

            return master

        except Exception as e:

            print(f"Error conexión: {e}")

            time.sleep(2)


master = conectar()

ultimo_idx = -1

while True:

    try:

        msg = master.recv_match(
            type="CAMERA_FEEDBACK",
            blocking=True
        )

        if not msg:
            continue

        idx = msg.img_idx

        # evitar duplicados
        if idx == ultimo_idx:
            continue

        ultimo_idx = idx

        print(
            f"COMANDO RECIBIDO | FOTO {idx}"
        )

    except Exception as e:

        print(f"Error: {e}")

        master = conectar()
