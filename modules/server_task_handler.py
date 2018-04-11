import threading


class ServerTaskHandler(object):
    def __init__(self):
        self.tasks = []

        self.thread = threading.Thread(self.start())

    def start(self):
        while True:
            for task in self.tasks:
                task()
