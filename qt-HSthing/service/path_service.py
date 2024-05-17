from pathlib import Path
import json

from config import LOG_PATH

from PyQt6.QtCore import QObject


class PathService(QObject):
    def __init__(self, log_path: str = None, log_service=None):
        super().__init__()
        self._log_service = log_service

        # store all as _string_
        # ~/..../Logs/
        self._log_path = log_path or LOG_PATH
        # folder 'Hearthstone-date-time'
        self._log_subdir = None

        self.set_subdir()

    def set_subdir(self):
        if not self._log_path:
            return False
        log_path = Path(self._log_path)
        if not log_path.is_dir():
            return False

        # take last of the files, sorted by name (includes date), and split it, to get the part we want
        self._log_subdir = str(sorted(log_path.iterdir())[-1]).split('Hearthstone/Logs/')[1]
        self._log_service.start_reading(subdir_path=self.get_full_subdir_path())
        return True

    def get_full_subdir_path(self) -> str:
        return str(Path(self._log_path, self._log_subdir))

    def get_subdir_name(self) -> str:
        return self._log_subdir

    def set_log_path(self, new_path: str = None):
        self._log_path = new_path

    def get_log_path(self) -> str:
        return self._log_path

    def save_log_path(self):
        if self._log_path:
            with open('settings.ini', 'w') as f:
                f.write(json.dumps({'LOG_PATH': self._log_path}))
            return True
        return False
