from PyQt5.QtWidgets import QMenuBar, QAction

class MenuBar(QMenuBar):

    def __init__(self, mainWindow):
        super().__init__(mainWindow)

        file_menu = self.addMenu('File')

        newAction = QAction('&New', self)
        newAction.setShortcut('Ctrl+N')
        newAction.triggered.connect(mainWindow.newWindow)

        openAction = QAction('&Open', self)
        openAction.setShortcut('Ctrl+O')
        openAction.triggered.connect(mainWindow.openImage)

        exitAction = QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(mainWindow.close)

        
        file_menu.addAction(newAction)
        file_menu.addAction(openAction)
        file_menu.addAction(exitAction)
        
        
