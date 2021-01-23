from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

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

        # Set Background
        pixmap = QPixmap('./images/baduk_19.png')
        pixmap = pixmap.scaledToHeight(550)

        lbl_img = QLabel()
        lbl_img.setPixmap(pixmap)
        hbox.addWidget(lbl_img)
      
        # Declare Mouse Tracking
        self.setMouseTracking(True)

        x = 0
        y = 0

        self.text = "x: {0} ,y: {1} ".format(x, y)
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

    def reset(self):
        print("reset view")
     
    def mousePressEvent(self, event):
        if not(event.buttons() & Qt.LeftButton):
            return

        x = event.x()
        y = event.y()
        text = "x: {0}, y: {1} ".format(x, y)
        self.label.setText(text)

        # Converter 호출하기
    
    def loadImageFromFile(self) :
        #QPixmap 객체 생성 후 이미지 파일을 이용하여 QPixmap에 사진 데이터 Load하고, Label을 이용하여 화면에 표시
        print('ho')

