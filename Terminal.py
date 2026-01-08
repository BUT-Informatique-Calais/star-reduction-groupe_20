from PyQt5.QtWidgets import QPlainTextEdit
from PyQt5.QtCore import Qt

class Terminal(QPlainTextEdit):

    def __init__(self, parent = None) -> None:
        super().__init__(parent=parent)

        self.setReadOnly(False) 
        
        # css
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
        self.appendPlainText(">")

    def write(self, text : str) -> None:
        self.appendPlainText(text)
    
    def keyPressEvent(self, event):
        # Gérer la touche Entrée pour exécuter des commandes
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            # Récupérer le texte de la dernière ligne
            cursor = self.textCursor()
            cursor.select(cursor.LineUnderCursor)
            command = cursor.selectedText().strip()
            
            if command.startswith(">"):
                command = command[1:].strip()
            
            if command:
                self.executeCommand(command)
            
            self.appendPlainText(">")
        else:
            super().keyPressEvent(event)
    
    def executeCommand(self, command: str) -> None:

        if command.lower() == "clear":
            self.clear()
            self.write("Bienvenue dans le terminal")
        elif command.lower() == "help":
            self.write("Commandes disponibles:")
            self.write("  clear - Effacer le terminal")
            self.write("  help  - Afficher cette aide")
        else:
            self.write(f"Commande inconnue: {command}")