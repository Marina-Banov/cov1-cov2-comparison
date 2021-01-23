import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot, Qt
import data_init as data


class App(QWidget):

    def __init__(self):
        Form, Window = uic.loadUiType('app.ui')

        window = Window()
        window.show()

        super().__init__()
        self.title = 'test'
        self.left = 50
        self.top = 50
        self.width = 640
        self.height = 480
        self.label = QLabel(self)
        self.initUI()

    def initUI(self):
        qssFile = 'style.qss'
        with open(qssFile, 'r') as f:
            self.setStyleSheet(f.read())

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowIcon(QIcon('4jsm10.jpg'))

        # Create widget
        button = QPushButton('test', self)
        button.setObjectName('butt')
        button.setToolTip('This is load picture button')
        button.move(100, 20)
        button.clicked.connect(self.on_click)

        self.label.move(100, 50)

        self.show()

    # show image on button click
    @pyqtSlot()
    def on_click(self):
        imagePath = '4jsm10.jpg'
        pixmap = QPixmap(imagePath)
        self.label.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio))
        self.label.adjustSize()
        self.label.setSizePolicy(100, 50)


if __name__ == '__main__':
    app = QApplication([])
    data1, data2 = data.init_data()
    data.plot_group(data1.get_group('China'))
    ex = App()
    sys.exit(app.exec_())
