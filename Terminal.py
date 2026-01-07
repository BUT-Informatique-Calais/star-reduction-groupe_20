from PyQt5.QtWidgets import QPlainTextEdit

class Terminal(QPlainTextEdit):

    def __init__(self, parent = None) -> None:
        super().__init__(parent=parent)

        self.setReadOnly(True)
        
        # Appliquer le style CSS au terminal
        self.setStyleSheet("""
            QPlainTextEdit {
                background-color: #1A1F2E;
                color: white;
                border: 2px solid #0E1117;
                border-radius: 5px;
                padding: 10px;
                font-family: 'Courier New', monospace;
                font-size: 12pt;
            }
        """)
        
        self.write("Bienvenue dans le terminal")

    def write(self, text : str) -> None:
        self.appendPlainText(text)