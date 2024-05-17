# toistaiseksi sleep/wait timestä
import time
from pathlib import Path


class LogReader:
    """
    :param log_dir_path:
    :return:
    """

    def __init__(self, sub_dir_path: Path, filenames=None):
        """
        :param logfile_path: directory containing logfile as Path object.
        :param logfile_name:  name of logfile to watch, shouldnt change. Should accept Path or string.
        """
        self.sub_dir_path = sub_dir_path
#         self.filenames = filenames
        self._tuples = None
        # self._make_tuples()

    # def _make_tuples(self):
    #     paths = [Path(self.sub_dir_path, filename) for filename in self.filenames]
    #     self.last_positions = {str(path): path.stat().st_size if path.exists() else 0 for path in paths}
    #
    # def read_log(self, path: str):
    #     pathed = Path(path)
    #     if pathed.parts[-1] not in self.filenames:
    #         print(f"{pathed} was filtered")
    #         return None
    #     with open(pathed, 'r') as logfile:
    #         last_pos = self.last_positions[path]
    #         size_now = pathed.stat().st_size
    #         if size_now != last_pos:
    #             logfile.seek(last_pos)
    #             content = logfile.read().splitlines()
    #             self.last_positions[path] = size_now
    #             if content:
    #                 return path, [f"{line}\n" for line in content]
