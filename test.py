class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.mModified = True
        self.initUI()
        self.currentRegion = QRect(50, 50, 50, 80)
        self.x0 = 5
        self.x1 = 25
        self.y0 = 5
        self.y1 = 25
        self.mPixmap = QPixmap()
        self.func = (None, None)

    def initUI(self):
        self.setGeometry(300, 300, 280, 270)
        self.setWindowTitle('Painter training')
        self.show()

    def paintEvent(self, event):
        if self.mModified:
            pixmap = QPixmap(self.size())
            pixmap.fill(Qt.white)
            painter = QPainter(pixmap)
            painter.drawPixmap(0, 0, self.mPixmap)
            self.drawBackground(painter)
            self.mPixmap = pixmap
            self.mModified = False

        qp = QPainter(self)
        qp.drawPixmap(0, 0, self.mPixmap)

    def drawBackground(self, qp):
        func, kwargs = self.func
        if func is not None:
            kwargs["qp"] = qp
            func(**kwargs)

    def drawFundBlock(self, qp):
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        pen.setStyle(Qt.DashLine)

        qp.setPen(pen)
        for i in range(1, 10):
            qp.drawLine(self.x0, i * self.y0, self.x1, self.y0 * i)

    def drawNumber(self, qp, notePoint):
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        qp.setPen(pen)
        qp.setFont(QFont('Arial', 10))
        qp.drawText(notePoint, "5")

    def nextRegion(self):
        self.x0 += 30
        self.x1 += 30
        self.y0 += 30
        self.y1 += 30

    def keyPressEvent(self, event):
        gey = event.key()
        self.func = (None, None)
        if gey == Qt.Key_M:
            print("Key 'm' pressed!")
        elif gey == Qt.Key_Right:
            print("Right key pressed!, call drawFundBlock()")
            self.func = (self.drawFundBlock, {})
            self.mModified = True
            self.update()
            self.nextRegion()
        elif gey == Qt.Key_5:
            print("#5 pressed, call drawNumber()")
            self.func = (self.drawNumber, {"notePoint": QPoint(100, 100)})
            self.mModified = True
            self.update()