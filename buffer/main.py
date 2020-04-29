import os
import requests
import json
import re
from redis import Redis


if __name__ == "__main__":
    """
    Calls Hospital Stream and submits each message to a Redis queue.
    Tool is gonna pick up messages from queue. 
    """

    redis = Redis(host=os.environ.get('REDIS_HOST', 'redis'), port=os.environ.get('REDIS_PORT', 6379))

    url = 'http://hospital:8080/sub'

    r = requests.get(url, stream=True)
    r.raise_for_status()

    for line in r.iter_lines():
        if line:
            if line == b': ping':
                continue
            line = re.sub('^data: ', '', str(line, 'UTF8'))
            line = json.loads(line)
            # submit to redis queue
            redis.rpush(os.environ.get('REDIS_QUEUE', 'icumessages'), json.dumps(line))
            print('message sent to queu: ', line)

