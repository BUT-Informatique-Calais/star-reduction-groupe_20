from PyQt5.QtWidgets import QLabel

class Label(QLabel):

    def __init__(self, parent = None) -> None:
        super().__init__(parent=parent)
        self.setScaledContents(False)