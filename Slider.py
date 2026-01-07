from PyQt5.QtWidgets import QSlider
from PyQt5.QtCore import Qt

class Slider(QSlider):
    def __init__(self, orientation=Qt.Horizontal, parent=None):
        super().__init__(orientation, parent)

        self.setMinimum(0)
        self.setMaximum(100)
        self.setValue(50)
