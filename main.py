import sys
from MainWindow import MainWindow
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':

    application : QApplication = QApplication(sys.argv)
    main : MainWindow = MainWindow()
    main.show()
    sys.exit(application.exec_())