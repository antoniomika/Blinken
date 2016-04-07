import io
import time
from picamera

lastFrame = ""


def start():
    global lastFrame

    with picamera.PiCamera() as camera:
        camera.resolution = (1080, 720)
        camera.framerate = 20

        time.sleep(2)

        stream = io.BytesIO()
        for frame in camera.capture_continuous(stream, format="jpeg",
                                               use_video_port=True):

            stream.seek(0)
            lastFrame = stream.read()

            stream.seek(0)
            stream.truncate()
