import picamera
import time

camera = picamera.PiCamera()

time.sleep(2)

camera.capture('captured_picture.jpeg')