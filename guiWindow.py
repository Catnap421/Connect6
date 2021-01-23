from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

class App(QWidget):
    
    """
    만들고자 하는 프로그램의 기본이 되는 창 또는 폼 위젯.
    본 위젯 위에 다른 위젯을 올려서 모양을 만든다.
    QWidget을 상속받아서 필요한 메소드를 작성.
    """

    def __init__(self):
        """
        보통 __init__ (생성자)에서 필요한 것들을 다를 위젯들을 선언해줘도 되지만 init_widget을 따로 만들어서 호출한다.
        """
        super().__init__()
        self.init_widget()

    def init_widget(self):
        pixmap = QPixmap('baduk_19.png')
        pixmap = pixmap.scaledToHeight(550)


        lbl_img = QLabel()
        lbl_img.setPixmap(pixmap)
        lbl_size = QLabel('Width: '+str(pixmap.width())+', Height: '+str(pixmap.height()))
        lbl_size.setAlignment(Qt.AlignCenter)

        vbox = QVBoxLayout()
        vbox.addWidget(lbl_img)
        vbox.addWidget(lbl_size)
    

        okButton = QPushButton('OK')
        cancelButton = QPushButton('Cancel')

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(okButton)
        hbox.addWidget(cancelButton)
        hbox.addStretch(1)


        vbox.addStretch(3)
        vbox.addLayout(hbox)
        vbox.addStretch(1)

        self.setLayout(vbox)


        self.setWindowTitle("meat-thursday")
        self.setGeometry(400, 100, 200, 200)
        self.resize(1000, 800)


    
    def loadImageFromFile(self) :
        #QPixmap 객체 생성 후 이미지 파일을 이용하여 QPixmap에 사진 데이터 Load하고, Label을 이용하여 화면에 표시
        print('ho')

