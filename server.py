#!/usr/bin/env python

import os
import threading
import atexit
import copy
from random import randrange
from flask import Flask, render_template, request, jsonify

HOST = "0.0.0.0"
PORT = 8000
POLL_TIME = 1

current_data = {}
lock = threading.Lock()
poll_thread = None

def read_data():
    return read_data_faux()

TEMP_RANGE = 5.0
POWER_RANGE = 2.0
CURRENT_RANGE = 4.0

def read_data_faux():

    data = copy.copy(current_data)
    if not 'temp' in data:
        data['temp'] = 20.0
    if not 'power' in data:
        data['power'] = 5.0 
    if not 'current' in data:
        data['current'] = 2.0

    data['temp'] += max(0, randrange(-TEMP_RANGE, TEMP_RANGE))
    data['current'] += max(0, randrange(-CURRENT_RANGE, CURRENT_RANGE))
    data['power'] += max(0, randrange(-POWER_RANGE, POWER_RANGE))

    return data


def create_app():
    app = Flask(__name__,
                static_url_path = "/static",
                static_folder = "static",
                template_folder = "template")
    app.config['SECRET_KEY'] = 'lazers are kewl'

    def interrupt():
        global poll_thread
        if poll_thread:
            poll_thread.cancel()

    def poll_data():
        global poll_thread
        global current_data

        lock.acquire()
        current_data = read_data()
        lock.release()

        poll_thread = threading.Timer(POLL_TIME, poll_data, ())
        poll_thread.start()

    def poll_start():
        global poll_thread

        poll_thread = threading.Timer(POLL_TIME, poll_data, ())
        poll_thread.start()

    poll_start()
    atexit.register(interrupt)
    return app

app = create_app()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data')
def data():
    lock.acquire()
    data = copy.copy(current_data)
    lock.release()
    return jsonify(data)

if __name__ == '__main__':
    def cancel_thread():
        if poll_thread:
            poll_thread.cancel()

    atexit.register(cancel_thread)

    app.run(host=HOST, port=PORT, debug=False)
