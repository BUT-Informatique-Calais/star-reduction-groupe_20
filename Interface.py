from PyQt5.QtWidgets import QWidget, QSizePolicy, QListWidget, QListWidgetItem, QSlider, QScrollArea
import os
from PyQt5.QtCore import Qt
from Buttons import Buttons
from Layout import Layout
from LayoutSetting import LayoutSetting
from Label import Label
import original

class Interface(QWidget):

    def __init__(self, parent = None) -> None:
        super().__init__(parent=parent)
        self.parent = parent
        self.mainLayout : Layout = Layout(Qt.Horizontal)
        self.zoom_factor = 1.0 

        #############################
        # CREATION DU LAYOUT GAUCHE #
        #############################
        leftLayout : Layout = Layout()
        leftLayout.setContentsMargins(0,0,0,0)  # enlève les marges autour du layout

        # Layout paramètres de l'image
        left_top_layout : Layout = Layout()
        left_top_layout.setSpacing(2)    

        setting_fwhm : LayoutSetting = LayoutSetting("fwhm", parent=self)
        setting_threshold : LayoutSetting = LayoutSetting("Threshold", default_value=1, parent=self)
        setting_kernel : LayoutSetting = LayoutSetting("Kernel size", parent=self)
        setting_ksize : LayoutSetting = LayoutSetting("Blurry kernel gaussien size", parent=self)
        setting_sigmax : LayoutSetting = LayoutSetting("SigmaX", default_value=1, parent=self)

        left_top_layout.addLayout(setting_fwhm)
        left_top_layout.addLayout(setting_threshold)
        left_top_layout.addLayout(setting_kernel)
        left_top_layout.addLayout(setting_ksize)
        left_top_layout.addLayout(setting_sigmax)

        # Layout chemin images possibles
        left_bottom_layout : Layout = Layout()

        self.fits_list = QListWidget()
        self.fits_list.setStyleSheet("background-color: #22283A; color: white;")
        self.fits_list.setMaximumHeight(300)  # ou autre taille
        self.fits_list.itemClicked.connect(self.openSelectedFits)

        left_bottom_layout.addWidget(self.fits_list)

        # Remplir la liste avec les fichiers FITS
        self.loadFitsList()

        leftLayout.addLayout(left_top_layout)
        leftLayout.addLayout(left_bottom_layout)

        ############################
        # CREATION DU LAYOUT DROIT #
        ############################
        rightLayout : Layout = Layout()
        
        # Layout haut droit
        right_top_layout : Layout = Layout(full_size=False)

        # Créer le scroll area pour contenir le QLabel
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)  # important
        self.scroll_area.setMinimumSize(400, 400)

        # Label qui affichera l'image
        self.labelImage = Label()
        self.labelImage.setAlignment(Qt.AlignCenter)
        self.labelImage.setScaledContents(False)
        self.scroll_area.setWidget(self.labelImage)  # IMPORTANT : label dans scroll

        # Ajouter le scroll area au layout
        right_top_layout.addWidget(self.scroll_area)

        # Slider de zoom
        self.zoom_slider = QSlider(Qt.Horizontal)
        self.zoom_slider.setMinimum(10)
        self.zoom_slider.setMaximum(400)  # jusqu'à 400%
        self.zoom_slider.setValue(100)
        self.zoom_slider.setTickInterval(10)
        self.zoom_slider.setTickPosition(QSlider.TicksBelow)
        self.zoom_slider.valueChanged.connect(self.updateZoom)

        # Ajouter le slider sous l'image
        rightLayout.addLayout(right_top_layout)
        rightLayout.addWidget(self.zoom_slider)  # slider en dessous du scroll area

        rightLayout.addLayout(right_top_layout)
        
        # Layout bas droit
        self.right_down_layout : Layout = Layout(Qt.Horizontal, full_size=False)
        

        self.open_button : Buttons = Buttons("Open file", self)
        self.open_button.clicked.connect(self.parent.openImage)

        self.save_button : Buttons = Buttons("Save file", self)
        self.save_button.clicked.connect(self.parent.saveImage)

        self.right_down_layout.addWidget(self.open_button)
        self.right_down_layout.addWidget(self.save_button)

        rightLayout.addLayout(self.right_down_layout)

        self.mainLayout.addLayout(leftLayout, 1)
        self.mainLayout.addLayout(rightLayout, 1)

        self.setLayout(self.mainLayout)

    def updateZoom(self):
        if self.parent:
            self.parent.updateImageDisplay()

    def loadFitsList(self):
        """Charge tous les fichiers .fits du dossier ./imagesFits"""
        self.fits_list.clear()
        folder = "./imagesFits"
        if os.path.exists(folder):
            for filename in os.listdir(folder):
                if filename.lower().endswith(".fits"):
                    item = QListWidgetItem(filename)
                    self.fits_list.addItem(item)

    def openSelectedFits(self, item):
        """Ouvre l'image FITS sélectionnée depuis la liste."""
        fits_path = os.path.join("./imagesFits", item.text())
        
        # Convertir en PNG
        png_path = original.fits_to_png(fits_path)

        # Utiliser ton openImage pour afficher le PNG
        self.parent.openImage(png_path)