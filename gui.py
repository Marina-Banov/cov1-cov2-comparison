from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QComboBox, QLabel
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
import data_init as dt
import time
import numpy as np
from matplotlib.backends.qt_compat import QtCore, QtWidgets
import mplcursors

if QtCore.qVersion() >= "5.":
    from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
else:
    from matplotlib.backends.backend_qt4agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure

class App(QtWidgets.QMainWindow):

    def __init__(self):
        Form, Window = uic.loadUiType('app.ui')
        
        window = Window()
        window.show()
        
        super().__init__()
        self.title = 'Usporedba COVID-19 i SARS epidemije'
        self.left = 50
        self.top = 50
        self.width = 1080
        self.height = 720
        self.initUI()
        

    def initUI(self):
        qssFile = 'style.qss'
        with open(qssFile,'r') as f:
            self.setStyleSheet(f.read())
            
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowIcon(QIcon('img/covid'))
        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        
        # self.covGraph  = QLabel(self)
        # imagePath = '4jsm10.jpg'
        # pixmap = QPixmap(imagePath)
        # self.covGraph.setPixmap(pixmap.scaled(640 , 640, Qt.KeepAspectRatio))
        
        self.dropdown = QComboBox()
        self.dropdown.setObjectName('dropdownList')
        self.dropdown.addItems([j for sub in cov1['country'].unique().values.tolist() for j in sub])
        self.dropdown.resize(100, 50)
        self.dropdown.currentTextChanged.connect(self.on_combobox_changed)
        
        cov1Txt = QLabel('SARS')
        cov1Txt.setFont(QFont('Ubuntu', 18, QFont.Medium))
        cov2Txt = QLabel('COVID-19')
        cov2Txt.setFont(QFont('Ubuntu', 18, QFont.Medium))
        cov1FirstCase = QLabel('Prvi slučaj: ')
        cov1FirstCase.setFont(QFont('Ubuntu', 14, QFont.Medium))
        cov2FirstCase = QLabel('Prvi slučaj: ')
        cov2FirstCase.setFont(QFont('Ubuntu', 14, QFont.Medium))
        
        grid = QtWidgets.QGridLayout(self._main)
        grid.setSpacing(20)
        grid.addWidget(self.dropdown, 0, 2, 1, 4) #row, col, rowspan, colspan
        grid.addWidget(cov1Txt, 2, 0, 1, 2)
        grid.addWidget(cov2Txt, 2, 4, 1, 2)
        grid.addWidget(cov1FirstCase, 3, 0, 1, 2)
        grid.addWidget(cov2FirstCase, 3, 4, 1, 2)
        #grid.addWidget(self.covGraph, 4, 0, 4, 4)
        
        static_canvas = FigureCanvas(Figure(figsize=(4,4)))
        grid.addWidget(static_canvas, 4, 0, 4, 4)
        self.addToolBar(NavigationToolbar(static_canvas, self))
        self.cov1Total = static_canvas.figure.subplots()
        App.update_graph(self, 'Australia')
    
        # dynamic_canvas = FigureCanvas(Figure(figsize=(4,4)))
        # grid.addWidget(dynamic_canvas, 4, 4, 4, 4)
        # self._dynamic_ax = dynamic_canvas.figure.subplots()
        # # Set up a Line2D.
        # self._line, = self._dynamic_ax.plot(cov1.get_group('China')['date'], cov1.get_group('China')['new_confirmed'])
        # self._timer = dynamic_canvas.new_timer(50)
        # self._timer.add_callback(self._update_canvas)
        # self._timer.start()
        
        grid.setAlignment(Qt.AlignCenter)
        self.setLayout(grid)
     
    def update_graph(self, country):
        self.cov1Total.x = []
        self.cov1Total.y = []
        self.cov1Total.clear()
        self.cov1Total.plot(cov1.get_group(country)['date'], cov1.get_group(country)['total_confirmed'])
        self.cov1Total.plot(cov1.get_group(country)['date'], cov1.get_group(country)['total_deceased'])
        self.cov1Total.plot(cov1.get_group(country)['date'], cov1.get_group(country)['total_recovered'])
        
        mpl = mplcursors.cursor(self.cov1Total,
                                hover=2,
                                highlight=True,
                                highlight_kwargs={'color': 'b', 'lw': 3})
        mpl.connect('add', lambda sel: sel.annotation.get_bbox_patch().set(fc='white', alpha=1))
        mpl.connect('add', lambda sel: sel.annotation.set_text(
            'x = {}\ny = {}'.format(sel.target[0], round(sel.target[1], 0))))  

    def on_combobox_changed(self, value):
        print("combobox changed", value)
        App.update_graph(self, value)

    def _update_canvas(self):
        t = np.linspace(0, 10, 101)
        # Shift the sinusoid as a function of time.
        self._line.set_data(t, np.sin(t + time.time()))
        self._line.figure.canvas.draw() 

        
 
        


if __name__ == '__main__':
    cov1, cov2 = dt.init_data()
    
    # qapp = QtWidgets.QApplication.instance()
    # if not qapp:
    #     qapp = QtWidgets.QApplication(sys.argv)
        
    app = QApplication([])
    ex = App()
    ex.show()
    app.quit()

