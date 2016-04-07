import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray

lastFrame = ""


def start():
    global lastFrame

    camera = PiCamera()
    camera.resolution = (1920, 1080)
    camera.framerate = 32
    rawCapture = PiRGBArray(camera, size=(1920, 1080))

    for frame in camera.capture_continuous(rawCapture, format="bgr",
                                           use_video_port=True):

        image = frame.array

        ret, jpeg = cv2.imencode('.jpg', image)
        lastFrame = jpeg.tostring()

        rawCapture.truncate(0)
