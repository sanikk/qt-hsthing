from PyQt6.QtCore import QObject, pyqtSignal, QTimer, pyqtSlot
from pathlib import Path


class SnapperShotterService(QObject):
    """
    Class that handles file/directory watchdog duties.
    Checks have to be very simple and fast.
    If the files or directory are reserved in any way the game client just routes around the dmg.
    """

    file_changed = pyqtSignal(str)
    too_many_subdirs = pyqtSignal()

    def __init__(self, filenames: list[str] = None, log_path: str = None, interval: int = None):
        """

        :param paths_to_watch: list of strings
        :param interval: int milliseconds
        """
        super().__init__()
        self.filenames = filenames or ['Achievements.log', 'Gameplay.log', 'Power.log']
        self.log_path = log_path
        self.subdir_path = None
        self.interval = interval or 100
        self.snapperstimer = None
        self.__paths_to_watch = None

    def start(self):
        if not self.__paths_to_watch and not self.change_filepaths():
            return False
        self.snapperstimer = QTimer()
        self.snapperstimer.timeout.connect(self.check_subdir)
        self.snapperstimer.timeout.connect(self.check_files)
        self.snapperstimer.start(self.interval)
        print(f"{self.__paths_to_watch=}")
        print(f"{self.log_path=}")
        print(f"{self.subdir=}")
        return True

    def change_log_path(self, log_path: str):
        """
        Tämä tehdään vain dialogin kautta, ja harvoin.
        :param log_path:
        :return:
        """
        pathed = Path(log_path)
        if pathed.exists() and pathed.parts[-1] == 'Logs' and pathed.parts[-2] == 'Hearthstone':
            self.log_path = str(pathed)
            self.change_subdir()

    def change_subdir(self, new_subdir=None):
        """
        Tämä vaihtuu käynnistäessä ja napista, ja melko usein.
        :param new_subdir:
        :return:
        """
        if not self.log_path or not new_subdir:
            return False
        pathed = Path(self.log_path, new_subdir)
        if not pathed.exists() and not pathed.is_dir():
            return False
        self.subdir = str(pathed)
        self.change_filepaths()
        return True

    def change_filepaths(self):
        if not self.log_path or (not self.subdir and not self.change_subdir()):
            print("1")
            return False
        pathed = [Path(self.log_path, self.subdir, filename) for filename in self.filenames]
        print(f"{pathed=}")
        if all([a.exists() for a in pathed]):
            print("2")
            self.__paths_to_watch = pathed
            return True
        print("3")
        return False

    @pyqtSlot()
    def check_files(self):
        try:
            for file in self.__paths_to_watch:
                if file.stat().st_size:
                    self.file_changed.emit(str(file))
                    print(f"{file} has changed!")
        except FileNotFoundError:
            self.build_new_paths()

    def check_number_of_subdirs(self):
        if not self.log_path:
            return

        if len(Path(self.log_path).iterdir()) > 1:
            self.too_many_subdirs.emit()

if __name__ == '__main__':
    from PyQt6.QtWidgets import QApplication, QWidget
    app = QApplication([])
    le_path = '/home/karpo/hd/SteamLibrary/steamapps/common/HS/Hearthstone/Logs/'
    ss = SnapperShotterService(log_path=le_path)
    window = QWidget()
    window.show()
    ss.start()
    app.exec()
