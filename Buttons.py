from PyQt5.QtWidgets import QPushButton

class Buttons(QPushButton):
    _next_x = 20  # position du prochain bouton

    def __init__(self, titre: str, parent=None):
        super().__init__(titre, parent)

        self.load_style()
        self.adjustSize()  # taille selon le texte

        spacing = 10
        margin_bottom = 20

        if parent:
            y = parent.height() - self.height() - margin_bottom
        else:
            y = 0

        # position automatique sans chevauchement
        self.move(Buttons._next_x, y)

        
        Buttons._next_x += self.width() + spacing

    def load_style(self):
      
        self.setStyleSheet("""
            QPushButton {
                background-color: #0b3954;
                color: white;
                border-radius: 12px;
                font-size: 14px;
                font-weight: bold;
                padding: 6px 14px;
            }
            QPushButton:hover {
                background-color: #087e8b;
            }
            QPushButton:pressed {
                background-color: #062f3a;
            }
        """)