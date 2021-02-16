from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from coordinateConverter import *
from gameStatus import *
from color import *
from adapter import *
from timer import *
import time
import threading
import logging
import socket

black_path = "./images/black.png"
white_path = "./images/white.png"
background_path = './images/baduk_19.png'

class QUserEvent(QEvent):
    def __init__(self, x, y):
        super().__init__(QEvent.User)
        self.x = x
        self.y = y

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Connect6")
        self.setGeometry(500, 200, 900, 650)
        self.setFixedSize(900, 650)
        self.__initWidget()

    def __initWidget(self):
        # Declare Layout Variables
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()
        grid = QGridLayout()
        
        # Declare Image
        self.black = QImage(black_path).scaledToHeight(25)
        self.white = QImage(white_path).scaledToHeight(25)

        # Declare Mouse Tracking
        self.setMouseTracking(True)

        # Set Ground Status
        self.modified = False
        self.groundX = 0
        self.groundY = 0
        self.gameStatus = GameStatus()
        self.status = None # None: 시작 불가 True: 시작 가능

        # Set Background
        self.pixmap = QPixmap(background_path)
        self.pixmap = self.pixmap.scaledToHeight(578)
        self.background = QLabel()
        self.background.setPixmap(self.pixmap)  

        # Set StatusView
        self.statusView = QLabel('READY')
        self.statusView.setStyleSheet("color: black;"
                      "background-color: #d5f4e6;"
                      "font-weight: 700;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: black;"
                      "border-radius: 5px")

        # Set Timer Display
        self.lcd = QLCDNumber()
        self.lcd.display("0")
        self.lcd.setDigitCount(8)

        # Set PlayList View
        self.playList = QListWidget(self)

        # Set Buttons
        self.oneByOneButton = QPushButton('1 vs 1(테스트)')
        self.oneByAiButton = QPushButton('1 vs AI')
        self.aiByAiButton = QPushButton('AI vs AI')
        self.resetButton = QPushButton("재시작")
        quitButton = QPushButton("종료")

        self.oneByOneButton.clicked.connect(self.__oneByOneGameStart)
        self.oneByAiButton.clicked.connect(self.__oneByAiGameStart)
        self.aiByAiButton.clicked.connect(self.__aiByAiGameStart)
        self.resetButton.clicked.connect(self.__reset)
        quitButton.clicked.connect(QCoreApplication.instance().quit)

        grid.addWidget(self.oneByOneButton, 0, 0)
        grid.addWidget(self.oneByAiButton, 1, 0)
        grid.addWidget(self.aiByAiButton, 1, 1)
        grid.addWidget(self.resetButton, 2, 0)
        grid.addWidget(quitButton, 2, 1)

        self.resetButton.setEnabled(False)

        # Set Layout
        hbox.addWidget(self.background)
        hbox.addStretch(1)

        vbox.addStretch(2)
        vbox.addWidget(self.statusView, 1)
        vbox.addWidget(self.lcd, 2)

        vbox.addWidget(self.playList)
        vbox.addStretch(1)

        vbox.addLayout(grid)
        vbox.addStretch(3)
        hbox.addLayout(vbox)
        hbox.addStretch(1)

        self.setLayout(hbox)

    def updateTime(self, time):
        print('update Time')
        self.lcd.display(str(time))

    def mouseDoubleClickEvent(self, event):
        if self.status == None:
            QMessageBox.warning(self, "게임 입장 오류", "게임 모드를 선택해주세요")
            return

        if not(event.buttons() & Qt.LeftButton):
            return

        # Get Mouse Coordinate
        x = event.x()
        y = event.y() 

        if self.status == "oneByOne":
            self.__playOneByOne(x, y)
        elif self.status == "oneByAi":
            self.__playOneByAi(x, y)

    def __playOneByOne(self, x, y):
        # 기준 28 <= x <= 570, 53 <= y <= 595
        if 27 > x or x > 571 or y < 52 or y > 596:
            return

        boardX, boardY = CoordinateConverter.ConvertImageToBoard(x, y)
        self.updateStatus(boardX, boardY)

    def __playOneByAi(self, oneX, oneY):
        # 내 차례면 돌을 둘 수 있게 하고,
        # 돌을 두게 되면, (adapter) -> calculator로 전달
        # 어디에서 메시지를 보내는 게 맞을까? adapter

        if self.gameStatus.getTurn() != 1: #흑
            QMessageBox.warning(self, "차례Error", "아직 당신의 차례가 아닙니다.")
            return
        
        boardX, boardY = CoordinateConverter.ConvertImageToBoard(oneX, oneY)
  
        self.updateStatus(boardX, boardY) # 여기서 차례를 바꿔줌
        
    def customEvent(self, event):
        if not self.gameStatus.start:
            return

        if self.gameStatus.getTurn() == self.adapter.calculator.color:
            self.adapter.isTurn = True

    def paintEvent(self, event):
        if not self.modified:
            return

        painter = QPainter(self.pixmap)
        painter.drawImage(self.groundX, self.groundY, self.black if self.gameStatus.getTurn() == 1 else self.white)        
        self.background.setPixmap(self.pixmap)
        self.modified = False

        currentTurn = self.gameStatus.getTurn()

        self.gameStatus.setTurn()
        self.statusView.setText("TURN : {}".format(f"BLACK - {self.gameStatus.player1}" \
            if self.gameStatus.getTurn() == 1 else f"WHITE - {self.gameStatus.player2}"))

        nextTurn = self.gameStatus.getTurn()

        # if self.status == "oneByOne":
        #     return 

        if currentTurn != nextTurn:
            self.thTimer.setTime(31)

    def updateStatus(self, boardX, boardY):
        # GameStatus 호출하기
        imageX, imageY = self.gameStatus.checkBoard(boardX, boardY, self.gameStatus.getTurn())
        color, result = self.gameStatus.isConnect6(self.gameStatus.getTurn())

        if imageX == None:
            print('이미 놓았습니다')
            return

        text = QListWidgetItem("{0}: ({1}, {2})".format(f"BLACK - {self.gameStatus.player1}" \
            if self.gameStatus.getTurn() == 1 else f"WHITE - {self.gameStatus.player2}", boardX, boardY))
        self.playList.addItem(text)
        self.groundX, self.groundY = imageX, imageY
        self.modified = True
        self.update()
    
        if not result:
            if self.status != 'oneByOne':
                QApplication.postEvent(self, QUserEvent(boardX, boardY), Qt.LowEventPriority - 1)
            return

        QMessageBox.about(self, "게임 종료", "{0}가 승리하였습니다. ".format(f"BLACK - {self.gameStatus.player1}" \
            if color == 1 else f"WHITE - {self.gameStatus.player2}", boardX, boardY))
        text = QListWidgetItem("{0}가 승리하였습니다. ".format(f"BLACK - {self.gameStatus.player1}" \
            if color == 1 else f"WHITE - {self.gameStatus.player2}", boardX, boardY))
        self.statusView.setText("WINNER : {0}".format(f"BLACK - {self.gameStatus.player1}" \
            if color == 1 else f"WHITE - {self.gameStatus.player2}"))
        self.playList.addItem(text)
        self.status = False
        self.gameStatus.start = False
        self.resetButton.setEnabled(True)
        try:
            self.th.stop()
        except AttributeError:
            return

    def __reset(self):
        print("resetting..")
        self.pixmap = QPixmap(background_path)
        self.pixmap = self.pixmap.scaledToHeight(578)
        self.background.setPixmap(self.pixmap)

        self.modified = False
        self.groundX = 0
        self.groundY = 0
        self.gameStatus = GameStatus()
        self.status = None # None: 시작불가

        self.playList.clear()

        self.oneByOneButton.setEnabled(True)
        self.oneByAiButton.setEnabled(True)
        self.aiByAiButton.setEnabled(True)
        self.resetButton.setEnabled(False)

        self.statusView.setText("READY")

        try:
            if self.adapter.sock != None :
                self.adapter.sock.close()
        except AttributeError:
            return

    def __oneByOneGameStart(self):
        print('one vs one')
        self.oneByOneButton.setEnabled(False)
        self.oneByAiButton.setEnabled(False)
        self.aiByAiButton.setEnabled(False)
        self.resetButton.setEnabled(False)
        self.status = 'oneByOne'

        self.statusView.setText("TURN : {}".format(f"BLACK - {self.gameStatus.player1}" \
            if self.gameStatus.getTurn() == 1 else f"WHITE - {self.gameStatus.player2}"))

        self.timer = Timer(self.gameStatus)
        self.thTimer = self.timer
        self.thTimer.drawTime.connect(self.updateTime)
        self.thTimer.start()

    def __oneByAiGameStart(self):
        print("one vs ai")
        self.oneByOneButton.setEnabled(False)
        self.oneByAiButton.setEnabled(False)
        self.aiByAiButton.setEnabled(False)
        self.resetButton.setEnabled(False)
        self.status = 'oneByAi'
        # one vs ai일 땐 게임 스타트를 여기서 관리
        self.gameStatus.start = True

        self.statusView.setText("TURN : {}".format(f"BLACK - {self.gameStatus.player1}" \
            if self.gameStatus.getTurn() == 1 else f"WHITE - {self.gameStatus.player2}"))
        aiColor = 2

        self.adapter = Adapter(aiColor, self.gameStatus, False, 'player', None)
        self.th = self.adapter
        self.th.drawImage.connect(self.updateStatus)
        self.th.start()

        self.timer = Timer(self.gameStatus)
        self.thTimer = self.timer
        self.thTimer.drawTime.connect(self.updateTime)
        self.thTimer.start()


    def __aiByAiGameStart(self):
        print("ai vs ai")
        self.oneByOneButton.setEnabled(False)
        self.oneByAiButton.setEnabled(False)
        self.aiByAiButton.setEnabled(False)
        self.resetButton.setEnabled(False)
        self.status = 'aiByAi'   
         
        dlg = ConnectDialog()
        dlg.exec_()
        ip = dlg.ip
        port = dlg.port
        name = dlg.name
        print("ip: %s port: %s name: %s" % (ip, port, name))
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((ip, int(port)))
        except TimeoutError:
            QMessageBox.warning(self, "Timeout Error", "서버 연결에 실패하였습니다.")
            self.__reset()
            return

        self.adapter = Adapter(0, self.gameStatus, False, name, sock)
        self.th = self.adapter
        self.th.drawImage.connect(self.updateStatus)
        self.th.start()

        self.timer = Timer(self.gameStatus)
        self.thTimer = self.timer
        self.thTimer.drawTime.connect(self.updateTime)
        self.th.startTimer.connect(self.startTimer)
        
    def startTimer(self):
        self.thTimer.start()

class ConnectDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setupUI()

        self.ip = None
        self.port = None
        self.name = None

    def setupUI(self):
        self.setGeometry(800, 500, 300, 100)
        self.setWindowTitle("Connect Server")

        label1 = QLabel("IP: ")
        label2 = QLabel("Port: ")
        label3 = QLabel("Name: ")

        self.lineEdit1 = QLineEdit()
        self.lineEdit2 = QLineEdit()
        self.lineEdit3 = QLineEdit()

        self.lineEdit1.setText('IP')
        self.lineEdit2.setText('Port')
        self.lineEdit3.setText('Name')

        self.pushButton1= QPushButton("Connect")
        self.pushButton1.clicked.connect(self.pushButtonClicked)

        layout = QGridLayout()
        layout.addWidget(label1, 0, 0)
        layout.addWidget(self.lineEdit1, 0, 1)
        layout.addWidget(label2, 1, 0)
        layout.addWidget(self.lineEdit2, 1, 1)
        layout.addWidget(label3, 2, 0)
        layout.addWidget(self.lineEdit3, 2, 1)
        layout.addWidget(self.pushButton1, 2, 2)

        self.setLayout(layout)

    def pushButtonClicked(self):
        self.ip = self.lineEdit1.text()
        self.port = self.lineEdit2.text()
        self.name = self.lineEdit3.text()
        self.close()        
