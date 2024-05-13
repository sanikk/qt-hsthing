from pathlib import Path
import json

from config import LOG_PATH


class PathService:
    def __init__(self, log_path=None, log_service=None):
        self._log_service = log_service

        # store all as path
        # ~/..../Logs/
        self._log_path = log_path or LOG_PATH
        # folder Hearthstone-date-time
        self._log_subdir = None
        self._log_file = None

        self.set_subdir()

    def set_subdir(self):
        if not self._log_path or not self._log_path.is_dir():
            return False
        self._log_subdir = Path(str(sorted(self._log_path.iterdir())[-1]).split('Hearthstone/Logs/')[1])
        self._log_service.start_monitor(subdir_path=self.get_subdir_path())
        return True

    def get_subdir_path(self):
        return Path(self._log_path, self._log_subdir)

    def get_subdir_name(self):
        return self._log_subdir

    def set_log_path(self, new_path: str = None):
        self._log_path = Path(new_path)
        return self.set_subdir()

    def get_log_path(self):
        return self._log_path

    def save_log_path(self):
        if self._log_path:
            with open('settings.ini', 'w') as f:
                f.write(json.dumps({'LOG_PATH': str(self._log_path)}))
            return True
        return False

    def _set_file(self):
        # not used right now
        if not self._log_subdir:
            return
        self._log_file = Path(self._log_subdir, 'Hearthstone.log')
