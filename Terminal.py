from PyQt5.QtWidgets import QPlainTextEdit, QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCursor

import sys
import os
from Logique.reduce_stars import reduce_stars
from Logique.saveImage import saveImage
from Logique.ligneCommande import verifieFitsFolder

class Terminal(QPlainTextEdit):

    def __init__(self, parent = None) -> None:
        super().__init__(parent=parent)

        self.setReadOnly(False)  
        
        # Historique des commandes (gardé pour compatibilité mais moins utile ici)
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
        
        # State management for the interactive process
        self.state = "INIT"
        self.params = {}
        
        self.start_bash_interface()

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
        
        # Gérer la touche Entrée 
        elif event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            # Récupérer l'input utilisateur
            all_text = self.toPlainText()
            user_input = all_text[self.protected_position:].strip()
            
            # S'assurer que le curseur est à la fin
            cursor.movePosition(QTextCursor.End)
            self.setTextCursor(cursor)
            
            self.process_input(user_input)
            return

        super().keyPressEvent(event)
    
    def start_bash_interface(self):
        self.clear()
        # Affichage du logo comme dans mainBash
        logo = "                               ..                 ___ _                         \n                             .. .                / __| |_ __ _ _ _ ___          \n                .-==++++++++.   ..               \\__ \\  _/ _` | '_(_-<          \n             .=======++++++++++- .=+###*=:.       |___/\\__\\__,_|_| /__/          \n           .===========+++++++++++  -#######-     | _ \\___ __| |_  _ __ ___ _ _  \n          ==============+++++++++++  *#######     |   / -_) _` | || / _/ -_) '_| \n         =================+++++++++ .#######*     |_|_\\___\\__,_|\\_,_\\__\\___|_|   \n        ===================+++++++..#######*     \n       .=====================+++: ########:      \n       :======================..########=       \n     . :===================:.*########-         \n   +#  .------=========: -#########*+=          \n .###*   .-------:. .+###########+=++.          \n:########*+==**##############+======.           \n#########################+---------.            \n#####################-------------              \n .############+----------------:                \n                .:----------.                   \n\n"
        self.appendPlainText(logo)
        self.write("Entrez le chemin du dossier source [obligatoire] : ")
        self.state = "FITS_FOLDER"
        
    def prompt_restart(self):
        self.write("Appuilez sur une touche pour redémarer")
        self.state = "WAITING_RESTART"

    def process_input(self, user_input):
        # Afficher la réponse de l'utilisateur sur une nouvelle ligne (visuellement)
        self.appendPlainText("") 
        
        if self.state == "WAITING_RESTART":
            self.start_bash_interface()
            return
            
        try:
            if self.state == "FITS_FOLDER":
                verifieFitsFolder(user_input)
                self.params['fitsFolder'] = user_input
                self.write("Entrez le chemin du dossier de destination (par defaut : ./results) : ")
                self.state = "DESTINATION"
                
            elif self.state == "DESTINATION":
                self.params['folderDestination'] = user_input if user_input else "./results"
                self.write("Entrez la valeur de fwhm (par defaut : 3.0) : ")
                self.state = "FWHM"
            
            elif self.state == "FWHM":
                val = 3.0
                if user_input:
                    try: val = float(user_input)
                    except: raise ValueError
                if val <= 0: raise ValueError
                self.params['fwhm'] = val
                self.write("Entrez la valeur de threshold (par defaut : 1.0) : ")
                self.state = "THRESHOLD"
                
            elif self.state == "THRESHOLD":
                val = 1.0
                if user_input:
                    try: val = float(user_input)
                    except: raise ValueError
                if val <= 0: raise ValueError
                self.params['threshold'] = val
                self.write("Entrez la valeur de kernelSize (par defaut : 3) : ")
                self.state = "KERNEL_SIZE"

            elif self.state == "KERNEL_SIZE":
                val = 3
                if user_input:
                    try: val = int(user_input)
                    except: raise ValueError
                if val <= 0: raise ValueError
                self.params['kernelSize'] = val
                self.write("Entrez la valeur de ksize (par defaut : 3) : ")
                self.state = "KSIZE"

            elif self.state == "KSIZE":
                val = 3
                if user_input:
                    try: val = int(user_input)
                    except: raise ValueError
                if val <= 0: raise ValueError
                self.params['ksize'] = val
                self.write("Entrez la valeur de sigmaX (par defaut : 1.5) : ")
                self.state = "SIGMAX"
                
            elif self.state == "SIGMAX":
                val = 1.5
                if user_input:
                    try: val = float(user_input)
                    except: raise ValueError
                if val <= 0: raise ValueError
                self.params['sigmaX'] = val
                
                self.run_processing()

        except ValueError as e:
            # Replicating error messages from chargementParametresInteractif
            msg = str(e)
            if not msg:
                if self.state == "FWHM": msg = f"ERREUR : La valeur de fwhm doit être un nombre strictement positif (float). Valeur reçue : \"{user_input}\""
                elif self.state == "THRESHOLD": msg = f"ERREUR : La valeur de threshold doit être un nombre strictement positif (float). Valeur reçue : \"{user_input}\""
                elif self.state == "KERNEL_SIZE": msg = f"ERREUR : La valeur de kernelSize doit être un entier strictement positif (int). Valeur reçue : \"{user_input}\""
                elif self.state == "KSIZE": msg = f"ERREUR : La valeur de ksize doit être un entier strictement positif (int). Valeur reçue : \"{user_input}\""
                elif self.state == "SIGMAX": msg = f"ERREUR : La valeur de sigmaX doit être un nombre strictement positif (float). Valeur reçue : \"{user_input}\""
            
            self.write(msg)
            self.prompt_restart()

    def run_processing(self):
        self.appendPlainText("\n\n")
        self.write("Chargement...\n")
        
        QApplication.processEvents()
        
        fitsFolder = self.params['fitsFolder']
        folderDestination = self.params['folderDestination']
        
        try:
            os.makedirs(folderDestination, exist_ok=True)
            
            for file in os.listdir(fitsFolder):
                if file.endswith(".fits"):
                    fitsFile = os.path.join(fitsFolder, file)
                    fileName = fitsFile.split("/")[-1].removesuffix(".fits")
                    fileName += "_star_reduced"
                    
                    try:
                        res = reduce_stars(
                            fitsFile, 
                            self.params['fwhm'], 
                            self.params['threshold'], 
                            self.params['kernelSize'], 
                            self.params['ksize'], 
                            self.params['sigmaX']
                        )
                        saveImage(res, fileName, folderDestination)
                        self.write(f"{fitsFile} traité et enregistrer dans {folderDestination}")
                    except Exception as e:
                        self.write(f"Erreur lors du traitement de {file}: {e}")
                    
                    QApplication.processEvents()

            self.write("Traitement terminé")
            
        except Exception as e:
            self.write(f"Une erreur inattendue est survenue: {e}")
            
        self.prompt_restart()
