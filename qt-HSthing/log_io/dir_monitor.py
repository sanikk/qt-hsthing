from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path

# from log_reader import LogReader
from log_io.log_reader import LogReader

from PyQt6.QtCore import pyqtSignal, QObject
from PyQt6.QtWidgets import QApplication


class DirMonitor(QObject):
    """
    paras olisi varmaan hoitaa tämä eventeillä. Joko event_handleri joka tuottaa qeventtejä,
    tai sitten jos sais määritettyä suoraan mitä eventtejä toi watchdog luo.

    Jos luodaan log_servicessä event_handler instanssi ja linkitetään se siellä.
    log_service -> dir_monitor -> observer.schedule(event_handler=event_handler)
    """

    new_content = pyqtSignal(str)

    def __init__(self, directory_path=None, filenames=None, event_handler=None):
        super().__init__()
        self.observer = Observer()
        self.directory_path = directory_path
        self.filenames = filenames
        self.event_handler = event_handler

    def run(self):
        self.observer.schedule(
            event_handler=self.event_handler,
            path=self.directory_path
        )

    def stop_reading(self):
        self.observer.stop()
        self.observer.unschedule_all()
        self.deleteLater()

    def handle_new_content(self, filepath):
        print(f"handler received: {filepath=}")
        # logfile, content = self.log_reader.read_log(filepath)
        # print(f"handle_new_content {logfile=}")
        # print(f"handle_new_content {content=}")
        # if content:
        #     for line in content:
        #         self.new_content.emit(line)


class QFileSystemEventHandler(FileSystemEventHandler, QObject):

    path_has_content = pyqtSignal(str)

    def __init__(self, filenames=None, **kwargs):
        FileSystemEventHandler.__init__(self)
        QObject.__init__(self, **kwargs)
        self.filenames = filenames

    def on_modified(self, event) -> None:
        if event.is_directory:
            return None
        filename = Path(event.src_path).parts[-1]

        if filename in self.filenames:
            # print("we have a hit!")
            self.path_has_content.emit(event.src_path)

    def notify_about_content(self, path: str):
        # tää on ny turha TODO remove
        self.path_has_content.emit(path)


if __name__ == '__main__':
    app = QApplication([])
    sub_dir_path = Path('/home/karpo/hd/SteamLibrary/steamapps/common/HS/Hearthstone/Logs/Hearthstone_2024_05_16_22_36_00/')
    filenames = ['Achievements.log', 'Gameplay.log', 'Power.log']
    log_reader = LogReader(sub_dir_path=sub_dir_path, filenames=filenames)
    # le_path = Path('/home/karpo/hd/SteamLibrary/steamapps/common/HS/Hearthstone/Logs/Hearthstone_2024_05_09_15_07_58/')
    monitor = DirMonitor(directory_path=sub_dir_path, filenames=filenames,
                         log_reader=log_reader)
    monitor.run()
    app.exec()
