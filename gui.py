import sys
from PyQt5.QtWidgets import QComboBox, QLabel
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
import data_init as dt
import time
import numpy as np
from matplotlib.backends.qt_compat import QtCore, QtWidgets
import mplcursors
from matplotlib.ticker import MaxNLocator

if QtCore.qVersion() >= "5.":
    from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
else:
    from matplotlib.backends.backend_qt4agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
    from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self):
        fig = Figure(figsize=(4, 4), dpi=100)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class App(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.title = 'Usporedba COVID-19 i SARS epidemije'
        self.left = 50
        self.top = 50
        self.width = 1080
        self.height = 720

        with open('style.qss', 'r') as f:
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
        self.dropdown.addItems(cov1.groups.keys())
        self.dropdown.resize(100, 50)
        self.dropdown.currentTextChanged.connect(self.on_combobox_changed)

        self.cov1Txt = QLabel('SARS')
        self.cov1Txt.setFont(QFont('Ubuntu', 18, QFont.Medium))
        self.cov2Txt = QLabel('COVID-19')
        self.cov2Txt.setFont(QFont('Ubuntu', 18, QFont.Medium))
        self.cov1FirstCase = QLabel('Prvi slučaj: ')
        self.cov1FirstCase.setFont(QFont('Ubuntu', 14, QFont.Medium))
        self.cov2FirstCase = QLabel('Prvi slučaj: ')
        self.cov2FirstCase.setFont(QFont('Ubuntu', 14, QFont.Medium))

        self.grid = QtWidgets.QGridLayout(self._main)
        self.grid.setSpacing(20)
        self.grid.addWidget(self.dropdown, 0, 2, 1, 4)  # row, col, rowspan, colspan
        self.grid.addWidget(self.cov1Txt, 2, 0, 1, 2)
        self.grid.addWidget(self.cov2Txt, 2, 4, 1, 2)
        self.grid.addWidget(self.cov1FirstCase, 3, 0, 1, 2)
        self.grid.addWidget(self.cov2FirstCase, 3, 4, 1, 2)
        # grid.addWidget(self.covGraph, 4, 0, 4, 4)

        self.sc = MplCanvas()
        self.grid.addWidget(self.sc, 4, 0, 4, 4)
        self.update_graph('Australia')
        self.mpl = self.set_mpl()

        # dynamic_canvas = FigureCanvas(Figure(figsize=(4,4)))
        # grid.addWidget(dynamic_canvas, 4, 4, 4, 4)
        # self._dynamic_ax = dynamic_canvas.figure.subplots()
        # # Set up a Line2D.
        # self._line, = self._dynamic_ax.plot(cov1.get_group('China')['date'], cov1.get_group('China')['new_confirmed'])
        # self._timer = dynamic_canvas.new_timer(50)
        # self._timer.add_callback(self._update_canvas)
        # self._timer.start()

        self.grid.setAlignment(Qt.AlignCenter)
        self.setLayout(self.grid)

    def update_graph(self, country):
        self.sc.figure.set_canvas(self.sc)
        self.sc.axes.clear()
        cov1.get_group(country).plot(ax=self.sc.axes,
                                     x='date',
                                     y=['total_confirmed', 'total_deceased', 'total_recovered'],
                                     color=['r', 'k', 'g'],
                                     xlabel='')
        self.sc.axes.yaxis.set_major_locator(MaxNLocator(integer=True))
        self.sc.figure.canvas.draw()

    def set_mpl(self):
        mpl = mplcursors.cursor(self.sc.axes,
                                hover=2,
                                highlight=True,
                                highlight_kwargs={'color': 'b', 'lw': 3})
        mpl.connect('add', lambda sel: sel.annotation.get_bbox_patch().set(fc='white', alpha=1))
        mpl.connect('add', lambda sel: sel.annotation.set_text(
            'x = {}\ny = {}'.format(sel.target[0], int(sel.target[1]))))
        return mpl

    def on_combobox_changed(self, value):
        print("combobox changed", value)
        self.update_graph(value)
        self.mpl = self.set_mpl()

    def _update_canvas(self):
        t = np.linspace(0, 10, 101)
        # Shift the sinusoid as a function of time.
        self._line.set_data(t, np.sin(t + time.time()))
        self._line.figure.canvas.draw()


if __name__ == '__main__':
    cov1, cov2 = dt.init_data()

    qapp = QtWidgets.QApplication.instance()
    if not qapp:
        qapp = QtWidgets.QApplication(sys.argv)
    app = App()
    app.show()
    app.activateWindow()
    app.raise_()
    qapp.exec_()
