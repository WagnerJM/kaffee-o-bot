import os
from celery import Celery

REDIS_URL = 'redis://:{pw}@redis:6379/0'.format(pw=os.getenv('REDIS_PW'))
BROKER_URL = 'redis://:{pw}@redis:6379/1'.format(pw=os.getenv('REDIS_PW'))


app = Celery('kaffee-o-bot', backend=REDIS_URL, broker=BROKER_URL)
