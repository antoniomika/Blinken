import io
import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray

lastFrame = ""


def start():
    global lastFrame

    camera = PiCamera()
    camera.resolution = (1080, 720)
    camera.framerate = 20
    stream = io.BytesIO()

    for frame in camera.capture_continuous(stream, format="jpeg",
                                           use_video_port=True):

        stream.seek(0)
        lastFrame = stream.read()

        stream.seek(0)
        stream.truncate()
