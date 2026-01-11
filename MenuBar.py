from PyQt5.QtWidgets import QMenuBar, QAction

class MenuBar(QMenuBar):

    def __init__(self, mainWindow):
        super().__init__(mainWindow)

        file_menu = self.addMenu('File')

        newAction : QAction = QAction('&New', self)
        newAction.setShortcut('Ctrl+N')
        newAction.triggered.connect(mainWindow.newWindow)

        openAction : QAction = QAction('&Open', self)
        openAction.setShortcut('Ctrl+O')
        openAction.triggered.connect(mainWindow.openImage)

        saveAction : QAction = QAction('&Save', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.triggered.connect(mainWindow.saveImage)

        exitAction : QAction = QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(mainWindow.close)

        
        file_menu.addAction(newAction)
        file_menu.addAction(openAction)
        file_menu.addAction(saveAction)
        file_menu.addAction(exitAction)
        
        
