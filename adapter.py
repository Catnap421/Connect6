# gameStatus에서 Turn의 변화가 생기면(두 개의 돌을 놓으면) 서버로 데이터 전송하기
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from calculator import *
from gameStatus import *
from coordinateConverter import *
import random
import time


class Payload():
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color


class Adapter(QThread):
    drawImage = pyqtSignal(int, int)

    def __init__(self, color, gameStatus, isCalculate):
        super().__init__()
        self.calculator = Calculator(color, gameStatus)
        self.gameStatus = gameStatus
        self.isCalculate = isCalculate # AI의 차례가 되었음을 알리는 변수

    """
    adpater가 지속적으로 돌아가고 adapter에서 서버로부터 입력을 받게되면, 
    GUI에 노출하고, GUI에서 다시 adapter로 계산을 진행하게 해서, GUI로 노출하고 동시에 서버로 전달
    """
    def run(self):
        while True:
            if self.isCalculate is True:
                self.turnAi()
            else :
                self.checkServer()
                time.sleep(0.5)
    
    def stop(self):
        self.terminate()
         
    def checkServer(self):
        # print("check Server")
        # print("draw GUI")
        return 

    def randomPick(self):
        nextPos = [[8, 8], [9, 8], [10, 8], [8, 9], [10, 9], [8, 10], [9, 10], [10, 10]]
        random1 = random.randrange(0, 8)

        return nextPos[random1]

    def turnAi(self):
        boardX, boardY = self.calculator.run(2)
        self.drawImage.emit(boardX, boardY)
        time.sleep(1)
        boardX, boardY = self.calculator.run(1)
        self.drawImage.emit(boardX, boardY)
        print('turnAi')
        self.isCalculate = False
    
    def sendLocalOne(self, pos1, pos2):
        print(pos1, pos2)
        self.drawImage.emit(pos1, pos2)

    # def sendServer():
