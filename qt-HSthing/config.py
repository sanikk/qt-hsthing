import json

from pathlib import Path


def read_settings_file():
    settings_file = Path('./settings.ini')
    if settings_file.exists():
        with open('settings.ini', 'r') as f:
            data = f.read()
            if data:
                return json.loads(data)


settings = read_settings_file()
LOG_PATH = None

if settings and settings['LOG_PATH']:
    LOG_PATH = Path(settings['LOG_PATH'])
