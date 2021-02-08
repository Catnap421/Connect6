# gameStatus에서 Turn의 변화가 생기면(두 개의 돌을 놓으면) 서버로 데이터 전송하기
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from calculator import *
from gameStatus import *
from coordinateConverter import *
from socket import *
from connect6_protocol import *
import struct
import random
import time


class Payload():
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color


class Adapter(QThread):
    drawImage = pyqtSignal(int, int)

    def __init__(self, color, gameStatus, isCalculate, sock):
        super().__init__()
        self.calculator = Calculator(color, gameStatus)
        self.gameStatus = gameStatus # class
        self.isCalculate = isCalculate # AI의 차례가 되었음을 알리는 변수
        self.sock = sock
        

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

    def startGame(self):
        gameStartData = GameStartData(0, 3, 'jhw')
        err, data = make_game_start_payload(0, gameStartData)
        if 0 != err:
            print(err.name)
            return False
        self.gameStatus.start = True
        self.sock.send(data)

        return True
         
    def checkServer(self):
        if self.gameStatus.isStart() == False:
            if not self.startGame():
                raise Exception("Game Error")
        print("check Server")

        recvdata = self.sock.recv(1024)
        print("recvdata:",repr(recvdata))

        err, header = hdr_parsing(recvdata)
        print(header.version, header._type, header.player_num, header.data_length)
        if header._type == ProtocolType.GAME_START:
            print('GAME_START')

        elif header._type == ProtocolType.PUT:   
            print('PUT')
            err, data = put_turn_data_parsing(recvdata)
            print(data.coord_num, data.xy)
        elif header._type == ProtocolType.TURN:
            print('TURN')
            err, data = put_turn_data_parsing(recvdata)
            print(data.coord_num, data.xy)        
        elif header._type == ProtocolType.GAME_OVER:
            print('GAME_OVER')

        elif header._type == ProtocolType.ERROR:
            print('GAME_ERROR')

        elif header._type == ProtocolType.TIMEOUT:
            print('TIMEOUT')

        elif header._type == ProtocolType.GAME_DISCARD:
            print('GAME_DISCARD')


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
