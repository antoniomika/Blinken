import camera
from flask import Flask, render_template, Response, request, jsonify

app = Flask(__name__)
lastFrame = None


@app.route('/')
def index():
    return render_template('index.html')


def gen():
    while True:
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + lastFrame +
               b'\r\n\r\n')


@app.route('/feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, threaded=True, debug=True)
