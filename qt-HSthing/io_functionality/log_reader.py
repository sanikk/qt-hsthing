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

    def read_log_file(self, filepath: str):
        path = Path(filepath)
        # print(f"read_log {filepath=}")
        with open(filepath) as f:
            content = f.read()
            print(f"readlog {content=}")
        with open(filepath, 'w') as f:
            f.write('')
        return content
