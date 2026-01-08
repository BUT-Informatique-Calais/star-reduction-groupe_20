from PyQt5.QtWidgets import QWidget, QSizePolicy
from PyQt5.QtCore import Qt
from Buttons import Buttons
from Layout import Layout
from LayoutSetting import LayoutSetting
from Label import Label

# Args:
#     fitsFile (str): Chemin du fichier FITS à traiter.
#     fwhm (float): Largeur à mi-hauteur de l'étoile PARAMETRE A AJUSTER DANS LA VUE 
#     threshold (float): Le seuil de détection PARAMETRE A AJUSTER DANS LA VUE
#     kernelSize (int): Taille du noyau de l'érosion PARAMETRE A AJUSTER DANS LA VUE
#     ksize (int): Taille du noyau du flou gaussien PARAMETRE A AJUSTER DANS LA VUE
#     sigmaX (float): Paramètre du flou gaussien PARAMETRE A AJUSTER DANS LA VUE


# fwhm: float = 3.0
# threshold: float = 1.0
# kernelSize: int = 3 
# ksize: int = 3 
# sigmaX: float = 1.5
class Interface(QWidget):

    def __init__(self, parent = None) -> None:
        super().__init__(parent=parent)
        self.parent = parent
        self.original_pixmap: QPixmap | None = None
        self.mainLayout : Layout = Layout(Qt.Horizontal)

        #############################
        # CREATION DU LAYOUT GAUCHE #
        #############################
        leftLayout : Layout = Layout()
        leftLayout.setSpacing(2)          # réduit l'espacement entre les LayoutSetting
        leftLayout.setContentsMargins(0,0,0,0)  # enlève les marges autour du layout

        setting_fwhm : LayoutSetting = LayoutSetting("fwhm", parent=self)
        setting_threshold : LayoutSetting = LayoutSetting("Threshold", default_value=1, parent=self)
        setting_kernel : LayoutSetting = LayoutSetting("Kernel size", parent=self)
        setting_ksize : LayoutSetting = LayoutSetting("Blurry kernel gaussien size", parent=self)
        setting_sigmax : LayoutSetting = LayoutSetting("SigmaX", default_value=1, parent=self)

        leftLayout.addLayout(setting_fwhm)
        leftLayout.addLayout(setting_threshold)
        leftLayout.addLayout(setting_kernel)
        leftLayout.addLayout(setting_ksize)
        leftLayout.addLayout(setting_sigmax)

        ############################
        # CREATION DU LAYOUT DROIT #
        ############################
        rightLayout : Layout = Layout()
        
        # Layout haut droit
        right_top_layout : Layout = Layout(full_size=False)
        self.labelImage : Label = Label()
        self.labelImage.setScaledContents(False)
        self.labelImage.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )
        self.labelImage.setAlignment(Qt.AlignCenter)
        
        rightLayout.addLayout(right_top_layout)
        
        right_top_layout.addWidget(self.labelImage)
        
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


    def resizeEvent(self, event):
        if self.labelImage.pixmap():
            self.labelImage.setPixmap(
                self.labelImage.pixmap().scaled(
                    self.labelImage.size(),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
            )
        super().resizeEvent(event)
