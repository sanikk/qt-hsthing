from io_functionality.fs_utils import read_settings_file


settings = read_settings_file()
LOG_PATH = None

if settings and settings['LOG_PATH']:
    LOG_PATH = settings['LOG_PATH']
