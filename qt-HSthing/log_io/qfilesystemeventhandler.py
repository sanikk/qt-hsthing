from PyQt6.QtCore import QObject, pyqtSignal
from pathlib import Path
from watchdog.events import FileSystemEventHandler


class QFileSystemEventHandler(FileSystemEventHandler, QObject):
    """
    Event handler for watchdog, with Qt signal support.

    Sends a signal with path when one
    of the watched files is modified.

    Constructor takes an iterable of filenames(str, no checks). Quack quack.
    """

    path_has_content = pyqtSignal(str)

    def __init__(self, filenames=None, **kwargs):
        FileSystemEventHandler.__init__(self)
        QObject.__init__(self, **kwargs)
        self.filenames = filenames

    def on_modified(self, event) -> None:
        if event.is_directory or Path(event.src_path).parts[-1] not in self.filenames:
            return

        self.path_has_content.emit(event.src_path)
