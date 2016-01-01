#!/usr/bin/env python

from flask import Flask, render_template
from flask.ext.socketio import SocketIO, emit

HOST = "0.0.0.0"
PORT = 8000

app = Flask(__name__)
app.config['SECRET_KEY'] = 'lazers are kewl'
app.config['TEMPLATE_DIR'] = "template"
app.config['STATIC_DIR'] = "static"
app.config['STATIC_URL'] = "/static"
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('command', namespace='/control')
def control(message):
    emit('command', {'data': message['data']})

@socketio.on('connect', namespace='/control')
def test_connect():
    emit('status', {'data': 'Connected'})

@socketio.on('disconnect', namespace='/control')
def test_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, host=HOST, port=PORT, debug=True)
