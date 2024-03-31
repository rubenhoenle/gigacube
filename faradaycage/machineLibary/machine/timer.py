import time
import threading

class Timer:
    ONE_SHOT = 0
    PERIODIC = 1

    def __init__(self, id=-1):
        self.id = id
        self.period = None
        self.callback = None
        self.semaphore = threading.Semaphore(value=1)
        self.mode = None
        self.running = False
        self.thread = None

    def init(self, period=None, mode=None, callback=None):
        self.period = period/1000
        self.mode = mode
        self.callback = callback
        self.running = True
        run_treahd = threading.Thread(target=self.call)
        run_treahd.start()

    def deinit(self):
        self.running = False

    def _timer_func(self):
        while self.running:
            self.semaphore.acquire()
            time.sleep(self.period)
            if self.running:
                self.callback(self)
            self.semaphore.release()

    def call(self):
        if self.period is None or self.mode is None or self.callback is None:
            raise ValueError("Timer not initialized properly")
        
        self.callback(self)
        
        threading.Timer(self.period, self.call).start()