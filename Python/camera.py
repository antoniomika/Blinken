import io
import time
import server
import picamera
import threading

lastFrame = ""

webserverThread = threading.Thread(target=server.app.run,
                                   kwargs=dict(threaded=True, host="0.0.0.0",
                                               port=8080))
webserverThread.start()

with picamera.PiCamera() as camera:
    camera.resolution = (1080, 720)
    camera.framerate = 20

    time.sleep(2)

    stream = io.BytesIO()
    for frame in camera.capture_continuous(stream, format="jpeg",
                                           use_video_port=True):

        stream.seek(0)
        server.lastFrame = stream.read()

        stream.seek(0)
        stream.truncate()
