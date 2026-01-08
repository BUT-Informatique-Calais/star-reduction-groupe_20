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

        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(1)  # très serré

        self.labelText = QLabel(textLabel)
        self.labelText.setFixedHeight(14)
        self.labelText.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.labelText.setStyleSheet("""
            QLabel {
                font-size: 11px;
                margin: 0px;
                padding: 0px;
            }
        """)

        self.slider = Slider(Qt.Horizontal)
        self.slider.setRange(min_value, max_value)
        self.slider.setValue(default_value)

        self.addWidget(self.labelText)
        self.addWidget(self.slider)

