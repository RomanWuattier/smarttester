#!/usr/bin/env python3

from flask import jsonify, request
import threading
import time

# Set key "field1": http://localhost:5000/set/field1?value=42
# Get key "field1": http://localhost:5000/get/field1
# Get all :         http://localhost:5000/get
# Clear all :       http://localhost:5000/clear

lock = threading.Lock()

d = {}
d['data'] = {}

def update_thread():
    global d
    while True:
        with lock:
            d['uptime'] = d.get('uptime', 0) + 1
        time.sleep(1.0)

def clear():
    global d
    with lock:
        d['data'] = {}
        return jsonify(d)

def get():
    with lock:
        return jsonify(d)

def get_name(name):
    with lock:
        return jsonify(d['data'].get(name, {}))

def set(name):
    global d
    with lock:
        d['data'][name] = d['data'].get(name, {})
        d['data'][name]['value'] = request.args.get('value') or float('nan')
        d['data'][name]['time'] = time.time()
        return jsonify(d)
