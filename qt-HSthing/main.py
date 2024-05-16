import sys

from PyQt6 import QtWidgets

from ui.ui import TabWindow
from service.path_service import PathService
from service.log_service import LogService


def main():
    app = QtWidgets.QApplication(sys.argv)
    # make output unbuffered
    sys.stdout.reconfigure(line_buffering=True)

    log_service = LogService()
    path_service = PathService(log_service=log_service)

    window = TabWindow(path_service=path_service, log_service=log_service)
    window.setWindowTitle('silly HS thing')

    window.show()
    return app.exec()


if __name__ == '__main__':
    main()
