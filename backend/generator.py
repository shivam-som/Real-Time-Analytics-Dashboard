import os, time, json, random
import redis
from datetime import datetime
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
REDIS_CHANNEL = os.getenv('REDIS_CHANNEL', 'metrics_channel')
r = redis.Redis.from_url(REDIS_URL, decode_responses=True)

METRIC_TYPES = ['orders', 'page_views', 'signups', 'errors', 'latency']

def generate_metric():
    m = random.choice(METRIC_TYPES)
    value = None
    if m == 'orders':
        value = {'amount': round(random.random()*500,2), 'status': random.choice(['completed','pending'])}
    if m == 'page_views':
        value = {'count': random.randint(1,50)}
    if m == 'signups':
        value = {'plan': random.choice(['free','pro','enterprise'])}
    if m == 'errors':
        value = {'code': random.choice([500,502,504,400]), 'msg': 'simulated'}
    if m == 'latency':
        value = {'ms': random.randint(10,800)}
    payload = {
        'metric': m,
        'value': value,
        'ts': datetime.utcnow().isoformat()
    }
    return payload

def start_generator(rate_per_sec=50):
    interval = 1.0 / max(1, rate_per_sec)
    print(f"Generator started at ~{rate_per_sec} events/sec (interval {interval}s)")
    while True:
        payload = generate_metric()
        r.publish(REDIS_CHANNEL, json.dumps(payload))
        time.sleep(interval)
