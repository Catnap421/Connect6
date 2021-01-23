import guiWindow
import qtmodern.styles
import qtmodern.windows
from PyQt5.QtWidgets import QApplication
import sys

__author__ = "Deokyu Lim <hong18s@gmail.com>"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = guiWindow.App()

    qtmodern.styles.light(app)
    mw = qtmodern.windows.ModernWindow(win)    
    mw.show()

    exit(app.exec_())