if __name__ == '__main__':
    import PyQt6.QtWidgets as QtW
    import PyQt6.QtCore as QtC

    app = QtW.QApplication([])

    cunt = QtW.QMainWindow()
    container = QtW.QWidget()
    layout = QtW.QHBoxLayout()

    button1 = QtW.QPushButton('Push me!')
    button2 = QtW.QPushButton('Push me!')
    button3 = QtW.QPushButton('Push me!')
    button4 = QtW.QPushButton('Push me!')

    layout.addWidget(button1)
    layout.addWidget(button2)
    layout.addWidget(button3)
    layout.addWidget(button4)

    container.setLayout(layout)
    cunt.setCentralWidget(container)

    def empty_fun():
        return

    button1.clicked.connect(empty_fun)
    button2.clicked.connect(empty_fun)
    button3.clicked.connect(empty_fun)
    button4.clicked.connect(empty_fun)
    cunt.show()

    app.exec()
    exit()
