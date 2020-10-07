  
from PyQt5.QtWidgets import QApplication
from mainWindow import MainWindow

if __name__== "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = MainWindow()
    ui.showFullScreen()
    sys.exit(app.exec_())
