from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path

from PyQt6.QtCore import QObject

from log_io.log_reader import LogReader


class DirectoryMonitor(QObject):

    def __init__(self, directory_path, log_reader=None, data_queue=None):
        super().__init__()
        self.observer = Observer()
        self.directory_path = directory_path
        self.data_queue = data_queue
        # TODO fix this. we have better logs now.
        self.log_reader = log_reader or LogReader(log_dir_path=directory_path)

    def run(self):
        self.observer.schedule(
            event_handler=Handler(log_reader=self.log_reader, data_queue=self.data_queue),
            path=self.directory_path
        )
        self.observer.start()

    def cleanup(self):
        self.observer.join()


class Handler(FileSystemEventHandler):
    def __init__(self, log_reader=None, data_queue=None):
        super().__init__()
        self.log_reader = log_reader
        self.data_queue = data_queue

    def on_modified(self, event) -> None:
        if event.is_directory:
            return None

        path, content = self.log_reader.read_log(event.src_path)
        if content:
            # this should be made sync/async and threadsafe
            # self.log_service.add_content(content=content)
            self.data_queue.put(content)


if __name__ == '__main__':
    le_path = Path('/home/karpo/hd/SteamLibrary/steamapps/common/HS/Hearthstone/Logs/Hearthstone_2024_05_09_15_07_58/')
    monitor = DirectoryMonitor(directory_path=le_path)
    monitor.run()
