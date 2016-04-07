import io
import sys
import time
import base64
import picamera

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
with picamera.PiCamera() as camera:
    camera.resolution = (378, 252)
    # camera.resolution = (1920, 1080)
    camera.framerate = 20

    time.sleep(2)

    stream = io.BytesIO()
    for frame in camera.capture_continuous(stream, format="jpeg",
                                           use_video_port=True):
        stream.seek(0)
        data = stream.read()
        print base64.b64encode(data)

        stream.seek(0)
        stream.truncate()
