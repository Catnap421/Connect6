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
import asyncio

class Adapter(QThread):
    drawImage = pyqtSignal(int, int)
    startTimer = pyqtSignal()

    def __init__(self, color, gameStatus, isTurn, name, sock):
        super().__init__()
        self.calculator = Calculator(color, gameStatus)
        self.gameStatus = gameStatus # class
        self.isTurn = isTurn # AI의 차례가 되었음을 알리는 변수
        self.name = name
        self.sock = sock

    def run(self):
        while True:
            if self.isTurn is True:
                self.turnAi()
            elif self.sock != None:
                self.checkServer()
                time.sleep(0.5)
            else:
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
            
            if self.calculator.color == 1:
                self.gameStatus.player1 = self.name
                self.gameStatus.player2 = data.name
            else:
                self.gameStatus.player1 = data.name
                self.gameStatus.player2 = self.name   
            
            print("player1, player2:", self.gameStatus.player1, self.gameStatus.player2)   
            self.startTimer.emit()   

        elif header.type == ProtocolType.PUT:  
            print('PUT')
            err, data = put_turn_data_parsing(bodydata)

            self.drawGui(data)

        elif header.type == ProtocolType.TURN: 
            print('TURN')
            err, data = put_turn_data_parsing(bodydata)
            self.drawGui(data)

        elif header.type == ProtocolType.GAME_OVER:
            print('GAME_OVER')
            err, data = game_over_data_parsing(bodydata)
            print(f'game_over: {data.result}')
            
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

    def calculateAi(self):
        boardX1, boardY1 = self.calculator.run(2)
        self.drawImage.emit(boardX1, boardY1)
        time.sleep(1)
        boardX2, boardY2 = self.calculator.run(1)
        self.drawImage.emit(boardX2, boardY2)
        self.isTurn = False
        return [boardX1, boardY1, boardX2, boardY2]
    
    def drawGui(self, data):
        for i in range(data.coord_num):
            boardX, boardY = data.xy[i * 2], data.xy[i * 2 + 1]
            self.drawImage.emit(boardX, boardY) 
            time.sleep(0.7)

    def turnAi(self):
        xy = self.calculateAi()

        if self.sock == None:
            return

        coord_num = int(len(xy) / 2)

        putTurnData = PutTurnData(coord_num, xy)
        err, senddata = make_put_payload(self.calculator.color, putTurnData)

        self.sock.send(senddata)

