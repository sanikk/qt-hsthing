from pathlib import Path
import json


def save_settings(path):
    if path:
        with open('settings.ini', 'w') as f:
            f.write(json.dumps({'LOG_PATH': path}))
        return True
    return False


def read_settings_file(settings_file: Path = None):
    settings_file = settings_file or Path('./settings.ini')
    if settings_file.exists():
        with open('settings.ini', 'r') as f:
            data = f.read()
            if data:
                return json.loads(data)


def cleanup(path: str, subdir: str):
    """

    :param path: full path to Logs directory
    :param subdir: just the subdir part
    :return:
    """
    print(f"fs_utils cleanup started")
    print(f"{path=}, {subdir=}")
    path = Path(path)
    subdir = Path(path, subdir)
    if path and len(_list_log_folders(path)) > 1:
        _remove_old_log_folders(path)
    if subdir:
        [_empty_file(file_path) for file_path in _list_files(subdir)]
    else:
        print("no subdir set")


def _list_log_folders(path: Path):
    # print(f"list log folders {path=}")
    if path.parts[-1] != 'Logs':
        return []
    return [Path(directory) for directory in _list_files(path)]


def _list_files(directory_path: Path):
    if 'Hearthstone' not in directory_path.parts or 'Logs' not in directory_path.parts:
        return []
    # print(f"list files {directory_path=}")
    return [Path(filepath) for filepath in sorted(directory_path.iterdir())]


def _remove_old_log_folders(path: Path):
    # print(f"clean_old {_list_log_folders(path)[:-1]=}")
    for directory_path in _list_log_folders(path)[:-1]:
        if directory_path.parts[-2] == 'Logs' and directory_path.parts[-1].startswith('Hearthstone_'):
            _remove_old_directory(directory_path)
    # (_remove_old_directory(directory_path) for directory_path in _list_log_folders(path)[:-1]
    # if directory_path.parts[-2] == 'Logs' and directory_path.parts[-1].startswith('Hearthstone_'))


def _empty_file(path: Path):
    # print(f"empty_file {path=}")
    if 'Hearthstone' not in path.parts or 'Logs' not in path.parts or not path.parts[-1].endswith('.log'):
        return
    with open(path, 'w') as f:
        f.write('')


def _remove_old_directory(directory_path: Path):
    for file_path in _list_files(directory_path):
        file_path.unlink()
    directory_path.rmdir()





