import time
import csv
import requests
import json
from queue import Queue
from threading import Thread


NUMBER_WORKERS = 5

def process(data):
    print(data)

def put_data(queue):
    with open("./resource/clients.csv") as f:
        reader = csv.reader(f, delimiter=";")
        for line in reader:
            id_client = line[0]
            queue.put(id_client)

class Worker(Thread):

    def __init__(self, queue, process):
        Thread.__init__(self)
        self.queue = queue
        self.process = process

    def run(self):
        while True:
            # Get the work from the queue and expand the tuple
            data = self.queue.get()
            try:
                self.process(data)
            finally:
                self.queue.task_done()


def main_thread():
    # Create a queue to communicate with the worker threads
    queue = Queue()
    # Create 8 worker threads
    for x in range(NUMBER_WORKERS):
        worker = Worker(queue, process)
        # Setting daemon to True will let the main thread exit even though the workers are blocking
        worker.daemon = True
        worker.start()
    # Put the tasks into the queue as a tuple
    put_data(queue)
    # Causes the main thread to wait for the queue to finish processing all the tasks
    queue.join()


if __name__ == '__main__':
    main_thread()
