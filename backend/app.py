import os
import time
import json
from threading import Thread
from flask import Flask, jsonify, request
from flask_socketio import SocketIO, emit
import redis
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
REDIS_CHANNEL = os.getenv('REDIS_CHANNEL', 'metrics_channel')
RECENT_KEY = os.getenv('RECENT_KEY', 'metrics:recent')
RECENT_MAX = int(os.getenv('RECENT_MAX', '500'))

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret')
socketio = SocketIO(app, cors_allowed_origins='*', message_queue=REDIS_URL, async_mode='eventlet')

r = redis.Redis.from_url(REDIS_URL, decode_responses=True)

@app.route('/api/health')
def health():
    return jsonify({'status':'ok', 'time': datetime.utcnow().isoformat()})

@app.route('/api/metrics/recent')
def recent_metrics():
    items = r.lrange(RECENT_KEY, 0, RECENT_MAX-1)
    parsed = [json.loads(i) for i in items]
    return jsonify({'count': len(parsed), 'metrics': parsed})

@app.route('/api/metrics/aggregate')
def aggregate():
    window = int(request.args.get('window', '60'))
    cutoff = datetime.utcnow() - timedelta(seconds=window)
    items = r.lrange(RECENT_KEY, 0, RECENT_MAX-1)
    parsed = [json.loads(i) for i in items]
    agg = {}
    for p in parsed:
        t = datetime.fromisoformat(p['ts'])
        if t >= cutoff:
            key = p.get('metric', 'unknown')
            agg[key] = agg.get(key, 0) + 1
    return jsonify({'window_seconds': window, 'aggregate': agg})

@socketio.on('connect')
def on_connect():
    print('Client connected')
    emit('connected', {'msg':'connected'})

@socketio.on('disconnect')
def on_disconnect():
    print('Client disconnected')

def redis_listener():
    pubsub = r.pubsub()
    pubsub.subscribe(REDIS_CHANNEL)
    print('Redis listener started, subscribed to', REDIS_CHANNEL)
    for message in pubsub.listen():
        if message and message['type'] == 'message':
            data = message['data']
            try:
                payload = json.loads(data)
            except Exception:
                payload = {'raw': data}
            socketio.emit('metric', payload)
            r.lpush(RECENT_KEY, json.dumps(payload))
            r.ltrim(RECENT_KEY, 0, RECENT_MAX-1)

def start_listener():
    t = Thread(target=redis_listener, daemon=True)
    t.start()

if __name__ == '__main__':
    start_listener()
    if os.getenv('START_GENERATOR', '1') == '1':
        from generator import start_generator
        gen_thread = Thread(target=start_generator, daemon=True)
        gen_thread.start()
    socketio.run(app, host='0.0.0.0', port=5000)
