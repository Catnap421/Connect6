from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from coordinateConverter import *

black_path = "./images/black.png"
white_path = "./images/white.png"

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Connect6")
        self.setGeometry(500, 200, 900, 650)
        self.setFixedSize(900, 650)
        self.__initWidget()


    def __initWidget(self):
        # Set Ground
        self.turn = 0 # 1 : black 0: white
        self.modified = False
        self.groundX = 0
        self.groundY = 0

        # Set Converter
        self.coordinateConverter = CoordinateConverter()

        # Declare Layout Variables
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()
        
        self.black = QImage(black_path).scaledToHeight(25)
        self.white = QImage(white_path).scaledToHeight(25)

        # Set Background
        self.pixmap = QPixmap('./images/baduk_19.png')

        self.pixmap = self.pixmap.scaledToHeight(578)
        self.background = QLabel()
        self.background.setPixmap(self.pixmap)

        hbox.addWidget(self.background)
       
        # Declare Mouse Tracking
        self.setMouseTracking(True)

        ## 지울 예정
        x = 0
        y = 0
        arrX = "-"
        arrY = "-"

        self.text = "x: {0}, y: {1}, arrX: {2}, arrY: {3} ".format(x, y, arrX, arrY)
        
        self.label = QLabel(self.text, self)
        self.label.setMaximumWidth(250)
        self.label.setMaximumHeight(250)
        vbox.addWidget(self.label)

        # Set Buttons
        okButton = QPushButton('OK')
        cancelButton = QPushButton('Cancel')

        vbox.addWidget(okButton)
        vbox.addWidget(cancelButton)

        # Set Layout
        hbox.addLayout(vbox)

        self.setLayout(hbox)

    def paintEvent(self, event):
        if not self.modified:
            return

        painter = QPainter(self.pixmap)
        painter.drawImage(self.groundX, self.groundY, self.black if self.turn is 1 else self.white)
        self.background.setPixmap(self.pixmap)
        self.modified = False

    def reset(self):
        print("reset view")
     
    def mouseDoubleClickEvent(self, event):
        if not(event.buttons() & Qt.LeftButton):
            return

        # +- 15 68
        x = event.x()
        y = event.y() 

        # 기준 28 <= x <= 570, 53 <= y <= 595
        if 27 > x or x > 571 or y < 52 or y > 596:
            return
        
        # Converter 호출하기
        self.groundX, self.groundY = (self.coordinateConverter.ConvertImageToArray(x, y))

        if self.groundX is False:
            print('이미 놓았습니다')
            return
        text = "x: {0}, y: {1}, groundX: {2}, groundY: {3} ".format(x, y, self.groundX, self.groundY)
        self.label.setText(text)

        self.turn = 1 - self.turn
        self.modified = True
        self.update()

    def showBadukDol(self, posX, posY):
        print(posX, posY)
    

