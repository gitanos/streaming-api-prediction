import redis
import json


class Worker(object):
    """Base class for storing and retrieving messages from the queue."""

    def __init__(self, queue_name, host='redis', port=6379):
        self.redis = redis.Redis(host=host, port=port)
        self.queue = queue_name

    def work(self):
        """Main loop, causes the worker to work perpetuously. What a life!"""
        while True:
            message = self.get()
            self.handle(message)

    def handle(self, message):
        """ Message handler that needs to be overwritten.
        """
        print("You received a message:")
        print(message)
        # Overwrite this function to do something with the message!

    def get(self, block=True, timeout=None):
        """ Remove and return a message from the queue.
        """
        if block:
            message = self.redis.blpop(self.queue, timeout=timeout)
        else:
            message = self.redis.lpop(self.queue)

        parsed_message = self.parse(message[1])
        return parsed_message

    @staticmethod
    def parse(message):
        """ Parses JSON messages to dict.
        """
        try:
            return json.loads(message)
        except TypeError:
            print("Ignoring message because it did not contain valid JSON.")
