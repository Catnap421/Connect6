from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Timer(QThread):
    drawTime = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.time = 0

    def getTime(self):
        while self.time > 0:
            self.time -= 1
            self.drawTime.emit(self.time)

    def setTime(self, time):
        self.time = time