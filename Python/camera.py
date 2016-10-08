import io
import os
import sys
import time
import json
import fcntl
import base64
import picamera
import fileinput

"""
import server
import threading
import websocket

def sendData():
    ws = create_connection("ws://" + sys.argv[1] + "/ws/stream")
    while True:
        if server.lastFrame is not None:
            ws.send(base64.b64encode(server.lastFrame))
            ws.recv()

lastFrame = ""

webserverThread = threading.Thread(target=server.app.run,
                                   kwargs=dict(threaded=True, host="0.0.0.0",
                                               port=9090))
webserverThread.start()

wsThread = threading.Thread(target=sendData)
wsThread.start()

ws = create_connection("ws://" + sys.argv[1] + "/ws/stream")

ws = websocket.WebSocketApp("ws://" + sys.argv[1] + "/ws/stream")
wst = threading.Thread(target=ws.run_forever)
wst.daemon = True
wst.start()"""

fd = sys.stdin.fileno()
fl = fcntl.fcntl(fd, fcntl.F_GETFL)
fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)

with picamera.PiCamera() as camera:
    camera.resolution = (640, 360)
    # camera.resolution = (1920, 1080)
    camera.framerate = 20
    camera.awb_mode = "auto"

    time.sleep(2)

    stream = io.BytesIO()
    for frame in camera.capture_continuous(stream, format="jpeg",
                                           use_video_port=True, quality=25,
                                           thumbnail=None, bayer=None):
        stream.seek(0)
        data = stream.read()
        print base64.b64encode(data)

        stream.seek(0)
        stream.truncate()

        try:
            line = sys.stdin.readline()
            loaded = json.loads(line)
            if loaded["type"] == "awb_mode":
                camera.awb_mode = loaded["set"]
            elif loaded["type"] == "saturation":
                camera.saturation = loaded["set"]
            elif loaded["type"] == "awb_gains":
                camera.awb_gains = (loaded["set"][0], loaded["set"][1])
            elif loaded["type"] == "brightness":
                camera.brightness = loaded["set"]
            elif loaded["type"] == "contrast":
                camera.contrast = loaded["set"]
        except:
            pass
