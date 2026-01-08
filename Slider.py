from PyQt5.QtWidgets import QSlider
from PyQt5.QtCore import Qt


class Slider(QSlider):
    def __init__(self, orientation=Qt.Horizontal, parent =None):
        super().__init__(orientation, parent)

        self.setRange(1, 10)
        self.setValue(3)

        self.setTickPosition(QSlider.NoTicks)
        self.setTickInterval(1)

        self.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 1px solid #999999;
                height: 10px;
            }

            QSlider::handle:horizontal {
                background: #fff;
                width: 10px;
                margin: -1px -1px;
                border: 1px solid #5555ff;
            }

            QSlider::handle:hover {
                background: #000;
                border-color: #000;
            }

            QSlider::sub-page:horizontal {
                background: #5555ff;
            }

            QSlider::add-page:horizontal {
                background: #c4c4c4;
            }

            QSlider::tick-mark:horizontal {
                background: #333;
                width: 1px;
                height: 6px;
            }

            QSlider::tick-mark:horizontal:below {
                margin-top: 8px;
            }
        """)

