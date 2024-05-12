from pathlib import Path
from queue import Queue, Empty

from log_io.dir_monitor import DirectoryMonitor


class LogService:
    def __init__(self, log_path: Path = None):
        self.data_queue = Queue()
        self.monitor = None

    # DIR_MONITOR/LOG_READER
    def start_monitor(self, path: Path):
        self.monitor = DirectoryMonitor(directory_path=path, data_queue=self.data_queue)
        print("logservice starting monitor")
        self.monitor.run()

    def fetch(self):
        try:
            path, content = self.data_queue.get(block=False)
            print(f"log_service {path=}\n{content=}")
            if content:
                return content
        except Empty:
            pass

        return None
