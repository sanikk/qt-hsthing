from pathlib import Path


class LogReader:
    """
    Tämä toimii koska se ei varaa tuota tiedostoa.

    :param logfile_path:
    :return:
    """

    def __init__(self, sub_dir_path: str = None):
        """
        :param logfile_path: directory containing logfile as Path object.
        :param logfile_name:  name of logfile to watch, shouldnt change. Should accept Path or string.
        """
        self.sub_dir_path = sub_dir_path
        self._tuples = None
        self._make_lists_and_dicts()

    def _make_lists_and_dicts(self):
        files = ['Achievements.log', 'Gameplay.log', 'Power.log']
        # kas gameplay.logia ei ole ennen kuin käynnistää pelin
        self.paths = [Path(self.sub_dir_path, file) for file in files]
        self.last_positions = {path: path.stat().st_size if path.exists() else 0 for path in self.paths}

    def read_log(self, path):
        pathed = Path(path)
        if pathed not in self.paths:
            print(f"{pathed} was filtered")
            return None
        with open(path, 'r') as logfile:
            last_pos = self.last_positions[path]
            size_now = path.stat().st_size
            if size_now != last_pos:
                logfile.seek(last_pos)
                content = logfile.read().splitlines()

                self.last_positions[path] = size_now
                if content:
                    return path, [f"{line}\n" for line in content if line.startswith('E')]
