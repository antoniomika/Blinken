import io
import sys
import time
import base64
import server
import picamera
import threading
from websocket import create_connection

lastFrame = ""

webserverThread = threading.Thread(target=server.app.run,
                                   kwargs=dict(threaded=True, host="0.0.0.0",
                                               port=8080))
webserverThread.start()

wsThread = threading.Thread(target=sendData)
wsThread.start()

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


def sendData():
    ws = create_connection("ws://" + sys.argv[1] + "/ws/stream")
    while True:
        if server.lastFrame is not None:
            ws.send(base64.b64encode(server.lastFrame))
