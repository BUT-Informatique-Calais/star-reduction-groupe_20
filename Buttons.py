from PyQt5.QtWidgets import QPushButton

class Buttons(QPushButton):
    _next_x = 20  # position du prochain bouton

    def __init__(self, titre: str, parent =None):
        super().__init__(titre, parent)

        self.load_style()
        self.adjustSize()  # taille selon le texte
       

    def load_style(self):
        with open("styles.qss", "r") as f:
            self.setStyleSheet(f.read())
