from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from Slider import Slider


class LayoutSetting(QVBoxLayout):

    def __init__(
        self,
        textLabel: str,
        min_value: int = 1,
        max_value: int = 10,
        default_value: int = 3,
        parent: QWidget | None = None
    ) -> None:
        super().__init__()

        self.setContentsMargins(0, 0, 0, 5)
        self.setSpacing(5)

        self.labelText = QLabel(textLabel)
        self.labelText.setFixedHeight(25)
        self.labelText.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.labelText.setStyleSheet("""
            QLabel {
                color: white;
                background-color: #22283A;
                font-weight: bold;
                font-size: 14px;
                padding: 5px;
                border-radius: 3px;
                margin: 0px;
            }
        """)

        self.slider = Slider(Qt.Horizontal)
        self.slider.setRange(min_value, max_value)
        self.slider.setValue(default_value)
        self.slider.setMinimumHeight(40)  

        self.addWidget(self.labelText)
        self.addWidget(self.slider)