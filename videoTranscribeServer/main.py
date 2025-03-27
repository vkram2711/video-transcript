import os

from flask import Flask, request, jsonify, send_from_directory, url_for, render_template
from flask_cors import CORS
from flask_sockets import Sockets
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
from werkzeug.routing import Rule

import whisper_utils
from audio_utils import slice_audio, convert_mp4_to_wav

UPLOAD_FOLDER = 'uploads'

app = Flask(__name__)
sockets = Sockets(app)
CORS(app)


@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    filename = 'video.mp4'
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)  # Save the file to the current working directory
    file_link = url_for('video', filename=filename)

    return jsonify({'video_link': file_link})


@app.route('/video/<filename>/transcribe', methods=['POST'])
def transcribe(filename):
    print('full transcript')
    text = whisper_utils.video_to_text(f'{UPLOAD_FOLDER}/{filename}')
    return jsonify({'transcript': text})


@sockets.route('/video/<filename>/transcribe')
def transcribe_socket(ws, filename):
    print(filename)
    convert_mp4_to_wav(f'{UPLOAD_FOLDER}/{filename}', 'output_audio.wav')

    fragments = slice_audio('output_audio.wav')
    whisper_utils.process_fragments(fragments, ws)
    ws.close()


@sockets.route('/echo')
def echo_socket(ws):
    print('echo')
    message = ws.receive()
    print('message:' + message)
    ws.send(message)


@app.route('/video/<filename>')
def video(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


sockets.url_map.add(Rule('/echo', endpoint=echo_socket, websocket=True))
sockets.url_map.add(Rule('/video/<filename>/transcribe', endpoint=transcribe_socket, websocket=True))

if __name__ == '__main__':
    server = pywsgi.WSGIServer(('', 5003), app, handler_class=WebSocketHandler)
    server.serve_forever()

