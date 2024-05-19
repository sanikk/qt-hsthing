from PyQt6.QtWidgets import QTextEdit, QWidget
from PyQt6.QtCore import pyqtSlot


class LogTab(QTextEdit):
    """
    hmm
    qtextbrowser "extends QTextEdit (in read-only mode), adding some navigation functionality so that users can
    follow links in hypertext documents."

    tota vois ihmetellä jossain välissä. popuppeja avainsanoista klikkaamalla olis ilmeisin.
    ####################################
    hmm toi maksimum block count olis kätevä, eli QTextDocument jonka koko on rajoitettu,
    ja sitten täällä self.setDocument(doku). En ole varma kuinka kalliita tuon qtextdocumentim operaatiot ja
    ylläpito on.
    ###########################
    phase 1
    lisätään saadut pathit tohon tekstilaatikkoon.
    """
    def __init__(self, parent: QWidget = None, log_service=None):
        super().__init__(parent=parent)
        self._log_service = log_service

        self.setReadOnly(True)
        self.setPlaceholderText('No new log lines to show')
        self.document().setMaximumBlockCount(100)
        self._log_service.content_ready.connect(self.more_content)

    @pyqtSlot()
    def more_content(self):
        content = self._log_service.fetch()
        self.insertPlainText(content)

