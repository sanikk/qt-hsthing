from PyQt6.QtCore import pyqtSignal, pyqtSlot, QObject

from log_io.dir_monitor import DirMonitor
# from dir_monitor import DirMonitor
from log_io.log_reader import LogReader
from log_io.qfilesystemeventhandler import QFileSystemEventHandler
# from qfilesystemeventhandler import QFileSystemEventHandler


class LogService(QObject):

    content_ready = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.dir_monitor = None
        self.log_reader = None
        self.filenames = ['Achievements.log', 'Gameplay.log', 'Power.log']
        # convenience variable to store path with pyqtSlot-connected setter
        self.fetch_path = None

    def start_reading(self, subdir_path: str = None):
        if not subdir_path:
            return
        # we make this here for ez connects
        event_handler = QFileSystemEventHandler(filenames=self.filenames)
        event_handler.path_has_content.connect(self.set_fetch_path)
        event_handler.path_has_content.connect(self.content_ready)

        self.log_reader = LogReader(subdir_path)
        self.dir_monitor = DirMonitor(subdir_path, event_handler=event_handler)
        self.dir_monitor.run()

    def stop_reading(self):
        if self.dir_monitor:
            self.dir_monitor.stop_reading()
        self.deleteLater()

    # TODO rm this, just checking for connection
    @pyqtSlot(str)
    def testeri(self, filepath: str):
        print(f"log_service {filepath=}")

    @pyqtSlot(str)
    def set_fetch_path(self, path):
        self.fetch_path = path

    def fetch(self):
        # saved here for nostalgic reasons, nvm
        # return 'supreme data'
        return self.log_reader.read_log_file(self.fetch_path)


if __name__ == '__main__':
    import PyQt6.QtWidgets as QtW
    import PyQt6.QtCore as QtC

    app = QtW.QApplication([])

    logservice = LogService()
    logservice.start_reading('.')

    cunt = QtW.QMainWindow()
    container = QtW.QWidget()
    layout = QtW.QHBoxLayout()

    button1 = QtW.QPushButton('Push me!')
    button2 = QtW.QPushButton('Push me!')
    button3 = QtW.QPushButton('Push me!')
    button4 = QtW.QPushButton('Push me!')

    layout.addWidget(button1)
    layout.addWidget(button2)
    layout.addWidget(button3)
    layout.addWidget(button4)

    container.setLayout(layout)
    cunt.setCentralWidget(container)

    def empty_fun():
        return

    button1.clicked.connect(empty_fun)
    button2.clicked.connect(empty_fun)
    button3.clicked.connect(empty_fun)
    button4.clicked.connect(empty_fun)
    cunt.show()

    app.exec()
    exit()
