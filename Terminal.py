from PyQt5.QtWidgets import QPlainTextEdit

class Terminal(QPlainTextEdit):

    def __init__(self, parent = None) -> None:
        super().__init__(parent=parent)

        self.setReadOnly(True)
        self.write("Bienvenue dans le terminal")

    def write(self, text : str) -> None:
        self.appendPlainText(text)