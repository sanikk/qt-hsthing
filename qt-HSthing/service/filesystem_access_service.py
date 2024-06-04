from config import LOG_PATH
from service.snapper_shotter import SnapperShotterService
from pathlib import Path
from PyQt6.QtCore import QObject, pyqtSignal
import json


class FileSystemAccessService(QObject):
    """
    so... we need signals:
    - content_ready for gui
    """
    content_ready = pyqtSignal()

    def __init__(self, log_service=None, log_path=None):
        self._log_service = log_service
        self.snapper_shotter = SnapperShotterService(log_path=log_path or LOG_PATH)
        # store all as _string_
        # ~/..../Logs/
        self._log_path = log_path or LOG_PATH
        # folder 'Hearthstone-date-time'

    def set_log_path(self, new_path: str = None):
        self._log_path = new_path

    def set_subdir(self):
        if not self._log_path:
            return False
        log_path = Path(self._log_path)
        if not log_path.is_dir() or not log_path.parts[-1] == 'Logs' or not log_path.parts[-2] == 'Hearthstone':
            return False
        # take last of the files, sorted by name (includes date), and split it, to get the part we want
        self._log_subdir = str(sorted(log_path.iterdir())[-1]).split('Hearthstone/Logs/')[1]
        # self._log_service.start_reading(subdir_path=self.get_full_subdir_path())
        return True

    def __remove_old_subdirs(self):
        if not self._log_path:
            return
        subdirs = sorted([Path(a) for a in self._log_path.iterdir() if Path(a).parts[-1].startswith('Hearthstone_')])
        if len(subdirs) > 1:
            (self.__handle_single_subdir(old_subdir) for old_subdir in subdirs[:-1])

    def __handle_single_subdir(self, old_subdir: Path):
        if old_subdir.parts[-2] == 'Logs' and old_subdir.parts[-1].startswith('Hearthstone_'):
            for file_path in old_subdir.iterdir():
                file_path.unlink()
            old_subdir.rmdir()

    def start_polling(self):
        self.snapper_shotter.start()

    def get_full_subdir_path(self) -> str:
        return str(Path(self._log_path, self._log_subdir))

    def get_subdir_name(self) -> str:
        return self._log_subdir

    def get_log_path(self) -> str:
        return self._log_path

    def save_log_path(self):
        """
        passthru func to keep fs operations in fs_utils
        :return:
        """
        if self._log_path:
            with open('settings.ini', 'w') as f:
                f.write(json.dumps({'LOG_PATH': self._log_path}))
            return True
        return False


if __name__ == '__main__':
    from PyQt6.QtWidgets import QApplication, QWidget
    app = QApplication([])
    le_path = '/home/karpo/hd/SteamLibrary/steamapps/common/HS/Hearthstone/Logs/'
    # ss = SnapperShotterService(log_path=le_path)
    fs_service = FileSystemAccessService()
    window = QWidget()
    window.show()
    # ss.start()
    app.exec()
