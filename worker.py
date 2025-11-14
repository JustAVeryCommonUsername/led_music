import threading
import queue
import time

class LEDWorker:
    def __init__(self, interface):
        self.event_queue = queue.Queue()
        self.interface = interface
        self.worker = threading.Thread(target=self._run)
        self.worker.daemon = True
        self.worker.start()

    def schedule(self, color, delay):
        run_time = time.time() + delay
        self.event_queue.put((run_time, color))

    def _run(self):
        while True:
            run_time, color = self.event_queue.get()
            now = time.time()
            if run_time > now:
                time.sleep(run_time - now)
            self._set_led(color)

    def _set_led(self, color):
        self.interface.send_rgb(color[0], color[1], color[2])
