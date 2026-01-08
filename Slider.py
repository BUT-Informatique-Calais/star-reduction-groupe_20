from PyQt5.QtWidgets import QSlider
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QFont


class Slider(QSlider):
    def __init__(self, orientation=Qt.Horizontal, parent=None):
        super().__init__(orientation, parent)

        self.setRange(1, 10)
        self.setValue(3)

        self.setTickPosition(QSlider.TicksBelow)
        self.setTickInterval(1)

        self.setStyleSheet("""
            QSlider::groove:horizontal {
                background: #22283A;
                height: 8px;
                border-radius: 4px;
            }

            QSlider::handle:horizontal {
                background: white;
                width: 18px;
                height: 18px;
                margin: -5px 0;
                border-radius: 9px;
            }

            QSlider::handle:horizontal:hover {
                background: #E0E0E0;
            }

            QSlider::sub-page:horizontal {
                background: #22283A;
            }

            QSlider::add-page:horizontal {
                background: #22283A;
            }
        """)

    def paintEvent(self, event):
        super().paintEvent(event)
        
        painter = QPainter(self)
        painter.setPen(Qt.white)
        font = QFont("Arial", 9)
        painter.setFont(font)
        
        # Calculer la position pour chaque chiffre
        min_val = self.minimum()
        max_val = self.maximum()
        
       
        groove_width = self.width() - 20 
        
        for i in range(min_val, max_val + 1):
            # Position proportionnelle
            x = 10 + (i - min_val) * groove_width / (max_val - min_val)
            y = self.height() - 5
            
            # Dessiner le chiffre centré
            text = str(i)
            text_width = painter.fontMetrics().horizontalAdvance(text)
            painter.drawText(int(x - text_width / 2), y, text)