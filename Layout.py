from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt


class Layout:
    def __new__(
        cls,
        orientation=Qt.Vertical,
        margins=(10, 10, 10, 10),
        spacing=10,
        full_size=True
    ):
        if orientation == Qt.Horizontal:
            layout = QHBoxLayout()
        else:
            layout = QVBoxLayout()

        # Marges
        layout.setContentsMargins(*margins)

        # Espacement entre widgets
        layout.setSpacing(spacing)

        # Prend toute la fenêtre
        if full_size:
            layout.setStretch(0, 1)

        return layout
