from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from coordinateConverter import *
from gameStatus import *
from color import *

black_path = "./images/black.png"
white_path = "./images/white.png"
background_path = './images/baduk_19.png'

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Connect6")
        self.setGeometry(500, 200, 900, 650)
        self.setFixedSize(900, 650)
        self.__initWidget()


    def __initWidget(self):
        # Set Ground
        self.modified = False
        self.groundX = 0
        self.groundY = 0
        self.gameStatus = GameStatus()
        self.status = False # False: 시작 불가 True: 시작 가능

        # Declare Layout Variables
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()
        grid = QGridLayout()
        
        self.black = QImage(black_path).scaledToHeight(25)
        self.white = QImage(white_path).scaledToHeight(25)

        # Set Background
        self.pixmap = QPixmap(background_path)

        self.pixmap = self.pixmap.scaledToHeight(578)
        self.background = QLabel()
        self.background.setPixmap(self.pixmap)

        hbox.addWidget(self.background)
        hbox.addStretch(1)
       
        # Declare Mouse Tracking
        self.setMouseTracking(True)

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
        self.lcd.display('15')
        self.lcd.setDigitCount(8)

        # Set PlayList
        self.playList = QListWidget(self)

        vbox.addStretch(2)
        vbox.addWidget(self.statusView, 1)
        vbox.addWidget(self.lcd, 2)

        vbox.addWidget(self.playList)
        vbox.addStretch(1)

        # Set Buttons
        self.oneByOneButton = QPushButton('1 vs 1(테스트)')
        self.oneByAiButton = QPushButton('1 vs AI')
        self.aiByAiButton = QPushButton('AI vs AI')

        grid.addWidget(self.oneByOneButton, 0, 0)
        grid.addWidget(self.oneByAiButton, 1, 0)
        grid.addWidget(self.aiByAiButton, 1, 1)

        self.oneByOneButton.clicked.connect(self.__oneByOneGameStart)
        self.oneByAiButton.clicked.connect(self.__oneByAiGameStart)
        self.aiByAiButton.clicked.connect(self.__aiByAiGameStart)

        self.resetButton = QPushButton("재시작")
        quitButton = QPushButton("종료")

        self.resetButton.clicked.connect(self.__reset)
        quitButton.clicked.connect(QCoreApplication.instance().quit)

        grid.addWidget(self.resetButton, 2, 0)
        self.resetButton.setEnabled(False)
        grid.addWidget(quitButton, 2, 1)

        # Set Layout
        vbox.addLayout(grid)
        vbox.addStretch(3)
        hbox.addLayout(vbox)
        hbox.addStretch(1)

        self.setLayout(hbox)

    def paintEvent(self, event):
        if not self.modified:
            return

        painter = QPainter(self.pixmap)
        painter.drawImage(self.groundX, self.groundY, self.black if self.gameStatus.getTurn() is 1 else self.white)
        self.background.setPixmap(self.pixmap)
        self.modified = False

        self.gameStatus.setTurn()
        self.statusView.setText("BLACK" if self.gameStatus.getTurn() is 1 else "WHITE")


    def mouseDoubleClickEvent(self, event):
        if not self.status:
            QMessageBox.warning(self, "게임 입장 오류", "게임 모드를 선택해주세요")
            return

        if not(event.buttons() & Qt.LeftButton):
            return

        # +- 15 68
        x = event.x()
        y = event.y() 

        # 기준 28 <= x <= 570, 53 <= y <= 595
        if 27 > x or x > 571 or y < 52 or y > 596:
            return
        
        # Converter 호출하기
        x,y = CoordinateConverter.ConvertImageToBoard(x, y)

        # GameStatus 호출하기
        imageX, imageY = self.gameStatus.checkBoard(x, y, self.gameStatus.getTurn())
        color, result = self.gameStatus.isConnect6(self.gameStatus.getTurn())

        if imageX is -1:
            print('이미 놓았습니다')
            return

        text = QListWidgetItem("{0}: ({1}, {2})에 돌을 놓았습니다. ".format("BLACK" if self.gameStatus.getTurn() is 1 else "WHITE", x, y))
        self.playList.addItem(text)
  
        self.updateView(imageX, imageY)

        ## Check Result(승리 확인)
        if result:
            QMessageBox.about(self, "게임 종료", "{0}가 승리하였습니다. ".format("BLACK" if color is 1 else "WHITE", x, y))
            text = QListWidgetItem("{0}가 승리하였습니다. ".format("BLACK" if color is 1 else "WHITE", x, y))
            self.statusView.setText("{0} 승리".format("BLACK" if color is 1 else "WHITE"))
            self.playList.addItem(text)
            self.status = False
            self.resetButton.setEnabled(True)
            return

    def updateView(self, posX, posY):
        self.groundX, self.groundY = posX, posY
        self.modified = True
        self.update()

    def __reset(self):
        print("resetting..")
        self.pixmap = QPixmap(background_path)
        self.pixmap = self.pixmap.scaledToHeight(578)
        self.background.setPixmap(self.pixmap)

        self.modified = False
        self.groundX = 0
        self.groundY = 0
        self.gameStatus = GameStatus()
        self.status = False # False: 시작 불가 True: 시작 가능

        self.playList.clear()

        self.oneByOneButton.setEnabled(True)
        self.oneByAiButton.setEnabled(True)
        self.aiByAiButton.setEnabled(True)
        self.resetButton.setEnabled(False)

        self.statusView.setText("READY")


    def __oneByOneGameStart(self):
        print('one vs one')
        self.oneByOneButton.setEnabled(False)
        self.oneByAiButton.setEnabled(False)
        self.aiByAiButton.setEnabled(False)
        self.resetButton.setEnabled(False)
        self.status = True

        self.statusView.setText("BLACK")

    def __oneByAiGameStart(self):
        print("one vs ai")

    def __aiByAiGameStart(self):
        print("ai vs ai")

        
