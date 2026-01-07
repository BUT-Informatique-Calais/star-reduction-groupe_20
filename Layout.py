from PyQt5.QtWidgets import QBoxLayout
from PyQt5.QtCore import Qt

class Layout(QBoxLayout):

    def __new__(cls):
        return super().__new__()