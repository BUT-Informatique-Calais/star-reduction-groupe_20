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

        # on prépare la place pour le bouton suivant
        Buttons._next_x += self.width() + spacing

    def load_style(self):
        with open("styles.qss", "r") as f:
            self.setStyleSheet(f.read())
