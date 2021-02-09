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

    def __init__(self, color, gameStatus, isCalculate, name, sock):
        super().__init__()
        self.calculator = Calculator(color, gameStatus)
        self.gameStatus = gameStatus # class
        self.isCalculate = isCalculate # AI의 차례가 되었음을 알리는 변수
        self.name = name
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
        gameStartData = GameStartData(0, len(self.name), self.name)
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
        headerdata = recvdata[:4]
        bodydata = recvdata[4:]
        err, header = hdr_parsing(headerdata)
        print(header.version, header.type, header.player_num, header.data_length)


        if header.type == ProtocolType.GAME_START:
            self.calculator.color = header.player_num
            print("Calculator.color:", self.calculator.color)
            print('GAME_START')
            err, data = game_start_data_parsing(bodydata)
            print("data.req_res_flag, data.name, data.name_length:", data.req_res_flag, data.name, data.name_length)

        elif header.type == ProtocolType.PUT:   # 사실 PUT은 딱 한번만 입력받음
            print('PUT')
            err, data = put_turn_data_parsing(bodydata)

            for i in range(data.coord_num):
                boardX, boardY = data.xy[i * 2], data.xy[i * 2 + 1]
                self.drawImage.emit(boardX, boardY) 
                time.sleep(0.5)

        elif header.type == ProtocolType.TURN: # 그림 그리고 calculate -> 이후 put
            print('TURN')
            err, data = put_turn_data_parsing(bodydata)
            for i in range(data.coord_num):
                boardX, boardY = data.xy[i * 2], data.xy[i * 2 + 1]
                self.drawImage.emit(boardX, boardY) 
                time.sleep(0.5)

            xy = self.turnAi()

            coord_num = int(len(xy) / 2)

            putTurnData = PutTurnData(coord_num, xy)
            err, senddata = make_put_payload(self.calculator.color, putTurnData)

            self.sock.send(senddata)     
        elif header.type == ProtocolType.GAME_OVER:
            print('GAME_OVER')

        elif header.type == ProtocolType.ERROR:
            print('GAME_ERROR')

        elif header.type == ProtocolType.TIMEOUT:
            print('TIMEOUT')
            
        elif header.type == ProtocolType.GAME_DISCARD:
            print('GAME_DISCARD')


        return 

    def randomPick(self):
        nextPos = [[8, 8], [9, 8], [10, 8], [8, 9], [10, 9], [8, 10], [9, 10], [10, 10]]
        random1 = random.randrange(0, 8)

        return nextPos[random1]

    def turnAi(self):
        boardX1, boardY1 = self.calculator.run(2)
        self.drawImage.emit(boardX1, boardY1)
        time.sleep(1)
        boardX2, boardY2 = self.calculator.run(1)
        self.drawImage.emit(boardX2, boardY2)
        self.isCalculate = False
        return [boardX1, boardY1, boardX2, boardY2]
    
    def sendLocalOne(self, pos1, pos2):
        print(pos1, pos2)
        self.drawImage.emit(pos1, pos2)

    # def sendServer():
