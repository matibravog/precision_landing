import time
from pymavlink import mavutil

master = mavutil.mavlink_connection('/dev/serial0', baud=57600)

master.wait_heartbeat()
print("Conectado")

while True:
    master.mav.statustext_send(3, b"PING FROM PI")

    msg = master.recv_match(type='STATUSTEXT', blocking=True, timeout=1)
    if msg:
        print("Recibido:", msg.text)

    time.sleep(1)
