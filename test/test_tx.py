from pymavlink import mavutil
import time

# Conexión
master = mavutil.mavlink_connection('/dev/serial0', baud=921600)

print("Esperando heartbeat...")
master.wait_heartbeat()
print("Conectado!")

# Obtener modos disponibles
mode = 'STABILIZE'

if mode not in master.mode_mapping():
    print(f"Modo {mode} no disponible")
    exit()

mode_id = master.mode_mapping()[mode]

print(f"Cambiando a modo {mode}...")

# Enviar cambio de modo
master.mav.set_mode_send(
    master.target_system,
    mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
    mode_id
)

# Esperar confirmación
print("Esperando confirmación...")

while True:
    msg = master.recv_match(type='HEARTBEAT', blocking=True)
    
    current_mode = msg.custom_mode
    
    if current_mode == mode_id:
        print(f"Modo cambiado a {mode} ✅")
        break
