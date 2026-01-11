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
import cv2

class MainWindow(QMainWindow):

    def __init__(self) -> None:
        super().__init__()

        # Fenêtre principale
        self.setWindowTitle("Editeur image FITS")
        self.setWindowIcon(QIcon("./assets/logo.webp"))
        self.setFixedSize(1200, 900)

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
        main_layout : QVBoxLayout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        central_widget.setLayout(main_layout)

        # Créer un QTabWidget
        self.tabs : QTabWidget = QTabWidget()
        main_layout.addWidget(self.tabs)

        # Créer les onglets
        self.interface : Interface = Interface(parent=self)
        self.tab2 : QWidget = QWidget()

        # Ajouter les onglets au QTabWidget
        self.tabs.addTab(self.interface, "Interface")
        self.tabs.addTab(self.tab2, "Terminal")
        
        self.original_pixmap = None
        self.original_image = None   
        self.processed_image = None   

        self.current_fits_path = None

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

    def openImage(self, file_path=None):
        if file_path is None:
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Ouvrir une image",
                "",
                "Images (*.png *.jpg *.jpeg *.bmp *.fits)"
            )

        if not file_path:
            return

        if file_path.lower().endswith('.fits'):
            self.current_fits_path = file_path
            # Convertir en PNG pour affichage
            from Logique.original import fits_to_png
            file_path = fits_to_png(file_path)
        
        self.original_image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)

        if self.original_image is None:
            QMessageBox.critical(self, "Erreur", "Impossible d'ouvrir l'image")
            return

        self.updateImageFromSliders()

    def updateImageDisplay(self):
        if self.original_pixmap is None:
            return

        zoom_factor = self.interface.zoom_slider.value() / 100.0

        scaled_pixmap = self.original_pixmap.scaled(
            int(self.original_pixmap.width() * zoom_factor),
            int(self.original_pixmap.height() * zoom_factor),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )


        self.interface.labelImage.setPixmap(scaled_pixmap)



    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.updateImageDisplay()

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


    def updateImageFromSliders(self):
        if self.original_image is None:
            return
        if self.current_fits_path is not None:
            # Récupérer les valeurs des sliders
            fwhm = float(self.interface.settings[0].slider.value())
            threshold = float(self.interface.settings[1].slider.value())
            kernelSize = int(self.interface.settings[2].slider.value())
            ksize = int(self.interface.settings[3].slider.value())
            sigmaX = float(self.interface.settings[4].slider.value())

            from Logique.reduce_stars import reduce_stars
            
            try:
                self.processed_image = reduce_stars(
                    self.current_fits_path,
                    fwhm=fwhm,
                    threshold=threshold,
                    kernelSize=kernelSize,
                    ksize=ksize,
                    sigmaX=sigmaX
                )
                self.displayImage(self.processed_image)
                self.terminal.write(f"✓ Image traitée (fwhm={fwhm}, threshold={threshold})")
            except Exception as e:
                self.terminal.write(f"✗ Erreur: {e}")
                QMessageBox.warning(self, "Erreur", f"Erreur de traitement:\n{e}")
        else:
            img = self.original_image.copy()

            fwhm = self.interface.settings[0].slider.value()
            threshold = self.interface.settings[1].slider.value()

            _, img = cv2.threshold(img, threshold * 20, 255, cv2.THRESH_BINARY)
            ksize = max(1, fwhm * 2 + 1)
            img = cv2.GaussianBlur(img, (ksize, ksize), 0)

            self.processed_image = img
            self.displayImage(img)

    def displayImage(self, img):
        if len(img.shape) == 3:  # Image couleur (H, W, 3)
            h, w, c = img.shape
            bytes_per_line = 3 * w
            
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            qimg = QImage(
                img_rgb.data,
                w,
                h,
                bytes_per_line,
                QImage.Format_RGB888
            )
        else:  # Image en niveaux de gris (H, W)
            h, w = img.shape
            qimg = QImage(
                img.data,
                w,
                h,
                w,
                QImage.Format_Grayscale8
            )

        pixmap = QPixmap.fromImage(qimg)

        # Appliquer le zoom
        zoom = self.interface.zoom_slider.value() / 100
        pixmap = pixmap.scaled(
            int(w * zoom),
            int(h * zoom),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        self.interface.labelImage.setPixmap(pixmap)