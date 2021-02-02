# gameStatus에서 Turn의 변화가 생기면(두 개의 돌을 놓으면) 서버로 데이터 전송하기
from calculator import *
from gameStatus import *

class Adapter():
    def __init__(self, color, gameStatus):
        self.calculator = Calculator(color)
        self.gameStatus = gameStatus

    def sendLocalAi(self, x, y):
        self.calculator.initWeightBoard([x, y], self.gameStatus.board)

        if self.gameStatus.getTurn() == 2:
            print('ai turn')
            nextPos = self.calculator.calculateNextPos()
            self.calculator.calculateWeight(nextPos, 1, 2, 2, self.gameStatus.board)
            nextPos = self.calculator.calculateNextPos()
            print(nextPos)    
        print("send Local")
    # def sendLocalOne():

    # def sendServer():