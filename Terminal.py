from PyQt5.QtWidgets import QPlainTextEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCursor

class Terminal(QPlainTextEdit):

    def __init__(self, parent = None) -> None:
        super().__init__(parent=parent)

        self.setReadOnly(False)  
        
        # Historique des commandes
        self.command_history = []
        self.history_index = -1
        
        # Position protégée du curseur
        self.protected_position = 0
        
        # CSS
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
        self.updateProtectedPosition()

    def write(self, text : str) -> None:
        self.appendPlainText(text)
        self.updateProtectedPosition()
    
    def updateProtectedPosition(self) -> None:
        """Met à jour la position jusqu'où on ne peut pas supprimer"""
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.protected_position = cursor.position()
    
    def keyPressEvent(self, event):
        cursor = self.textCursor()
        
        # Empêcher la suppression avant la position protégée
        if event.key() == Qt.Key_Backspace:
            if cursor.position() <= self.protected_position:
                return
        
        elif event.key() == Qt.Key_Delete:
            if cursor.position() < self.protected_position:
                return
        
        # Empêcher de déplacer le curseur avant la position protégée
        elif event.key() == Qt.Key_Left or event.key() == Qt.Key_Home:
            if cursor.position() <= self.protected_position and event.key() == Qt.Key_Left:
                return
        
        # Gérer la flèche haut
        if event.key() == Qt.Key_Up:
            if self.command_history and self.history_index < len(self.command_history) - 1:
                self.history_index += 1
                self.replaceCurrentLine(self.command_history[-(self.history_index + 1)])
            return
        
        # Gérer la flèche  bas
        elif event.key() == Qt.Key_Down:
            if self.history_index > 0:
                self.history_index -= 1
                self.replaceCurrentLine(self.command_history[-(self.history_index + 1)])
            elif self.history_index == 0:
                self.history_index = -1
                self.replaceCurrentLine("")
            return
        
        # Gérer la touche Entrée 
        elif event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            # Récupérer le texte de la dernière ligne
            cursor = self.textCursor()
            cursor.select(QTextCursor.LineUnderCursor)
            command = cursor.selectedText().strip()
            
            if command.startswith(">"):
                command = command[1:].strip()
            
            # Traiter la commande
            if command:
                # Ajouter à l'historique
                self.command_history.append(command)
                self.history_index = -1
                
                self.executeCommand(command)
            
            self.appendPlainText(">")
            self.updateProtectedPosition()
        else:
            super().keyPressEvent(event)
    
    def replaceCurrentLine(self, text: str) -> None:
        """Remplace le texte de la ligne actuelle après le prompt >"""
        cursor = self.textCursor()
        cursor.select(QTextCursor.LineUnderCursor)
        line = cursor.selectedText()
        
        cursor.removeSelectedText()
        cursor.insertText(f"> {text}")
        self.setTextCursor(cursor)
    
    def executeCommand(self, command: str) -> None:
        if command.lower() == "clear":
            self.clear()
            self.write("Bienvenue dans le terminal")
            self.appendPlainText(">")
            self.updateProtectedPosition()
        elif command.lower() == "help":
            self.write("Commandes disponibles:")
            self.write("  clear - Effacer le terminal")
            self.write("  help  - Afficher cette aide")
        else:
            self.write(f"Commande inconnue: {command}")