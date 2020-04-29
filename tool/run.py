import time
import traceback
import os

from data_handler import Handler

if __name__ == "__main__":
    """Startup script that listens to a Redis queue."""

    while True:
        try:
            print("Booting (handler) worker")
            indexer = Handler(os.environ.get('REDIS_QUEUE'))
            indexer.work()
        except Exception:
            traceback.print_exc()
            print("Something went wrong. Restarting worker in a second.")
            time.sleep(1)