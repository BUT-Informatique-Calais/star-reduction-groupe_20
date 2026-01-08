from PyQt5.QtWidgets import (
    QMainWindow,
    QMessageBox,
    QFileDialog,
    QLabel,
    QVBoxLayout,
    QWidget,
    QTabWidget,
    QHBoxLayout
)
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtCore import Qt

from MenuBar import MenuBar
from Terminal import Terminal
from Interface import Interface

import numpy as np
from astropy.io import fits


class MainWindow(QMainWindow):

    def __init__(self) -> None:
        super().__init__()

        # Fenêtre principale
        self.setWindowTitle("Editeur image FITS")
        self.setWindowIcon(QIcon("./assets/icons/planete-terre.png"))
        self.setGeometry(100, 100, 1000, 700)

        # Appliquer le style CSS
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1A1F2E;
            }
            QMenuBar {
                background-color: #22283A;
                color: white;
                padding: 5px;
            }
            QMenuBar::item {
                background-color: #6CA1DB;
                color: white;
                padding: 5px 10px;
            }
            QMenuBar::item:selected {
                background-color: #5A91CB;
            }
            QTabWidget::pane {
                border: 1px solid black;
                background-color: #1A1F2E;
            }
            QTabBar::tab {
                background-color: #1A1F2E;
                color: white;
                border: 1px solid black;
                padding: 8px 20px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: #1A1F2E;
                border-bottom: 2px solid #6CA1DB;
            }
            QTabBar::tab:hover {
                background-color: #22283A;
            }
            QWidget {
                background-color: #1A1F2E;
                color: white;
            }
        """)

        # Créer un widget personnalisé pour la barre de menu avec le logo
        menu_widget = QWidget()
        menu_widget.setStyleSheet("background-color: #22283A;")
        menu_layout = QHBoxLayout()
        menu_layout.setContentsMargins(10, 5, 10, 5)
        menu_layout.setSpacing(10)
        menu_widget.setLayout(menu_layout)

        # Ajouter le logo dans la barre de menu
        logo_label = QLabel()
        logo_pixmap = QPixmap("assets/logo.webp")  
        logo_pixmap = logo_pixmap.scaled(30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(logo_pixmap)
        logo_label.setAlignment(Qt.AlignCenter)  
        logo_label.setContentsMargins(0, 10, 0, 10)
        menu_layout.addWidget(logo_label)

        # Menu
        self.menuBar = MenuBar(self)
        menu_layout.addWidget(self.menuBar)

        # Ajouter le widget de menu comme corner widget
        self.setMenuWidget(menu_widget)

        # Créer un widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Créer le layout principal
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        central_widget.setLayout(main_layout)

        # Créer un QTabWidget
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        # Créer les onglets
        self.interface = Interface(parent=self)
        self.tab2 = QWidget()

        # Ajouter les onglets au QTabWidget
        self.tabs.addTab(self.interface, "Interface")
        self.tabs.addTab(self.tab2, "Terminal")
        

        # Contenu du deuxième onglet - Terminal
        tab2_layout = QVBoxLayout()
        tab2_layout.setContentsMargins(20, 20, 20, 20)
        
        # Créer l'instance du Terminal
        self.terminal = Terminal()
        tab2_layout.addWidget(self.terminal)
        
        self.tab2.setLayout(tab2_layout)

    def newWindow(self) -> None:
        self.nouvelle_fenetre = MainWindow()
        self.nouvelle_fenetre.show()
        self.close()

    def openImage(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Ouvrir une image FITS",
            "",
            "FITS (*.fits *.fit *.fts)"
        )

        if not file_path:
            return

        try:
            # Lecture FITS
            with fits.open(file_path) as hdul:
                data = hdul[0].data

            if data is None:
                raise ValueError("Fichier FITS invalide")

            # Conversion en image affichable
            data = data.astype(float)
            data -= data.min()
            data /= data.max()
            data *= 255
            data = data.astype(np.uint8)

            height, width = data.shape

            image = QImage(
                data.data,
                width,
                height,
                width,
                QImage.Format_Grayscale8
            )

            pixmap = QPixmap.fromImage(image)

            scaled_pixmap = pixmap.scaled(
                self.interface.labelImage.size(),  # taille actuelle du label
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )

            self.interface.labelImage.setPixmap(scaled_pixmap)
                        
        except Exception as e:
            QMessageBox.critical(
                self,
                "Erreur",
                f"Impossible d'ouvrir le fichier FITS\n\n{e}"
            )

    def saveImage(self) -> None:
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Enregistrer l'image",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp)"
        )

        if not file_path:
            return

        try:
            pixmap = self.interface.labelImage.pixmap()

            if pixmap and not pixmap.isNull():
                pixmap.save(file_path)
                self.terminal.write(f"Image enregistrée : {file_path}")
                QMessageBox.information(
                    self,
                    "Succès",
                    "Image enregistrée avec succès !"
                )
            else:
                raise ValueError("Aucune image à enregistrer")

        except Exception as e:
            QMessageBox.critical(
                self,
                "Erreur",
                f"Impossible d'enregistrer l'image\n\n{e}"
            )
            self.terminal.write(f"Erreur : {e}")

    def closeEvent(self, event) -> None:
        reponse = QMessageBox.question(
            self,
            "Quitter",
            "Voulez-vous vraiment quitter ?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reponse == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()