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
        self.turn = 1 # 1 : black 2: white
        self.modified = False
        self.groundX = 0
        self.groundY = 0
        self.gameStatus = GameStatus()
        self.status = False # False: 시작 불가 True: 시작 가능

        # Set Converter
        self.coordinateConverter = CoordinateConverter()

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
        self.statusView = QListWidget(self)

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
        oneByOneButton = QPushButton('1 vs 1(테스트)')
        oneByAiButton = QPushButton('1 vs AI')
        aiByAiButton = QPushButton('AI vs AI')

        grid.addWidget(oneByOneButton, 0, 0)
        grid.addWidget(oneByAiButton, 1, 0)
        grid.addWidget(aiByAiButton, 1, 1)

        oneByOneButton.clicked.connect(self.oneByOneGameStart)
        oneByAiButton.clicked.connect(self.oneByAiGameStart)
        aiByAiButton.clicked.connect(self.aiByAiGameStart)

        resetButton = QPushButton("재시작")
        quitButton = QPushButton("종료")

        resetButton.clicked.connect(self.reset)
        quitButton.clicked.connect(QCoreApplication.instance().quit)

        grid.addWidget(resetButton, 2, 0)
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
        painter.drawImage(self.groundX, self.groundY, self.black if self.turn is 1 else self.white)
        self.background.setPixmap(self.pixmap)
        self.modified = False
        self.turn = 3 - self.turn

    def mouseDoubleClickEvent(self, event):
        if not self.status:
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
        x,y = (self.coordinateConverter.ConvertImageToBoard(x, y))

        # GameStatus 호출하기
        imageX, imageY = self.gameStatus.checkBoard(x, y, self.turn)
        
        if imageX is -1:
            print('이미 놓았습니다')
            return

        text = QListWidgetItem("{0}: ({1}, {2})에 돌을 놓았습니다. ".format("BLACK" if self.turn is 1 else "WHITE", x, y))
        self.playList.addItem(text)
  
        self.updateView(imageX, imageY)

    def updateView(self, posX, posY):
        self.groundX, self.groundY = posX, posY
        self.modified = True
        self.update()

    def reset(self):
        print("resetting..")
        self.__initWidget()

    def oneByOneGameStart(self):
        print('one vs one')
        self.status = True

    def oneByAiGameStart(self):
        print("one vs ai")

    def aiByAiGameStart(self):
        print("ai vs ai")
        
