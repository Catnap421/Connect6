from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import time
from gameStatus import * 

class Timer(QThread):
    drawTime = pyqtSignal(int)

    def __init__(self, gameStatus):
        super().__init__()
        self.time = 31
        self.gameStatus = gameStatus

    def run(self):
        print(self.time, self.gameStatus.isStart())
        while True:
            if self.time > 0 and self.gameStatus.isStart():
                self.time -= 1
                self.drawTime.emit(self.time)
                time.sleep(1)

    def setTime(self, time):
        self.time = time
    
