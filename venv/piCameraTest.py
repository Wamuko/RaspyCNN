import picamera
import time

with picamera.PiCamera() as camera:
    camera.capture('test.jpg')