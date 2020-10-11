"""
Required libs:
flask
numpy
opencv-contrib-python
imutils
"""
import time
import argparse
import cv2
from imutils.video import VideoStream
from flask import Response
from flask import Flask


# initialize a flask object
app = Flask(__name__)

@app.route('/')
def index():
    return '<html><body><img src="/video"></body></html>'


@app.route('/video')
def video():
    return Response(generate(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


def generate():
    while True:
        time.sleep(1.0 / fps)
        frame = video_stream.read()
        if frame is None:
            continue

        # encode the video frame in JPEG format
        (flag, jpeg_image) = cv2.imencode('.jpg', frame)
        # ensure the frame was successfully encoded
        if not flag:
            continue

        # yield the output frame in the byte format
        yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + bytearray(jpeg_image) + b'\r\n'


if __name__ == '__main__':
    # Start video stream from given source
    video_stream = VideoStream(src=0).start()
    parser = argparse.ArgumentParser(description='Web Camera')
    parser.add_argument('--port',
                        help='Port, default is 9999',
                        type=int,
                        default=9999)
    parser.add_argument('--host',
                        help='Host IP, default is 127.0.0.1',
                        type=str,
                        default='127.0.0.1')
    parser.add_argument('--fps',
                        help='Frames per second, default is 10',
                        type=int,
                        default=10)
    args = vars(parser.parse_args())
    fps = args['fps']
    # Start flask server
    app.run(host=args['host'],
            port=args['port'],
            debug=False,
            threaded=True,
            use_reloader=False)
    # Stop VideoStream and release camera
    video_stream.stop()
