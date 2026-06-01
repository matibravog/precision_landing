from picamera2 import Picamera2
import time

print("1. creating object")
picam2 = Picamera2()

print("2. configuring")
config = picam2.create_preview_configuration(
    main={"format": "RGB888", "size": (640, 480)}
)

picam2.configure(config)

print("3. starting camera")
picam2.start()

print("4. waiting 2 seconds")
time.sleep(2)

print("5. capturing frame")
frame = picam2.capture_array()

print("6. frame received:", frame.shape)
