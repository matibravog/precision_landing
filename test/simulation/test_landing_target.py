from pymavlink import mavutil
import time

master = mavutil.mavlink_connection('/dev/serial0', baud=57600)

print("Esperando heartbeat...")
master.wait_heartbeat()
print("Conectado!")

# Loop enviando target centrado
while True:
    master.mav.landing_target_send(
        int(time.time() * 1e6),  # timestamp
        0,                       # target num
        mavutil.mavlink.MAV_FRAME_BODY_NED,
        0.0,                     # x offset (rad)
        0.0,                     # y offset (rad)
        2.0,                     # distancia (m)
        0, 0
    )

    print("Enviando target centrado")
    time.sleep(0.05)
