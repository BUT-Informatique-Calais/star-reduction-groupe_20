from PyQt5.QtWidgets import (
    QMainWindow,
    QMessageBox,
    QFileDialog
)
from PyQt5.QtGui import QIcon, QPixmap, QImage

from MenuBar import MenuBar
from Label import Label
from Terminal import Terminal

import numpy as np
from astropy.io import fits


class MainWindow(QMainWindow):

    def __init__(self) -> None:
        super().__init__()

        # Fenêtre principale
        self.setWindowTitle("Editeur image FITS")
        self.setWindowIcon(QIcon("./assets/icons/planete-terre.png"))
        self.setGeometry(100, 100, 1000, 700)

        # Menu
        self.menuBar = MenuBar(self)
        self.setMenuBar(self.menuBar)

        # Zone d'affichage image
        self.imageLabel = Label(self)
        self.imageLabel.setScaledContents(True)
        self.setCentralWidget(self.imageLabel)

        self.terminal : Terminal = Terminal(self)

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

            self.imageLabel.setPixmap(QPixmap.fromImage(image))
            self.imageLabel.adjustSize()

        except Exception as e:
            QMessageBox.critical(
                self,
                "Erreur",
                f"Impossible d'ouvrir le fichier FITS\n\n{e}"
            )

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
