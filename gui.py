import sys
from PyQt5.QtWidgets import QComboBox, QLabel, QLayout, QVBoxLayout
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
import data_init as dt
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


class App(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.title = 'Usporedba COVID-19 i SARS epidemije'
        self.left = 0
        self.top = 0
        self.width = 1080
        self.height = 720

        with open('style.qss', 'r') as f:
            self.setStyleSheet(f.read())

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowIcon(QIcon('windowIcon'))
        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)

        self.dropdown = QComboBox()
        self.dropdown.setObjectName('dropdownList')
        self.dropdown.addItems(cov2.groups.keys())
        self.dropdown.resize(100, 50)
        self.dropdown.setFont(QFont('Ubuntu', 11, QFont.Medium))
        self.dropdown.currentTextChanged.connect(self.on_combobox_changed)

        self.cov1Txt = QLabel('SARS')
        self.cov1Txt.setFont(QFont('Ubuntu', 18, QFont.Medium))
        self.cov2Txt = QLabel('COVID-19')
        self.cov2Txt.setFont(QFont('Ubuntu', 18, QFont.Medium))
        # self.cov1FirstCase = QLabel('Prvi slučaj: ')
        # self.cov1FirstCase.setFont(QFont('Ubuntu', 14, QFont.Medium))
        # self.cov2FirstCase = QLabel('Prvi slučaj: ')
        # self.cov2FirstCase.setFont(QFont('Ubuntu', 14, QFont.Medium))
        
        #mainLayout = QVBoxLayout(self)

        self.grid = QtWidgets.QGridLayout(self._main)
        self.grid.setSpacing(20)
        self.grid.addWidget(self.dropdown, 1, 3, 1, 2)  # row, col, rowspan, colspan
        self.grid.addWidget(self.cov1Txt, 3, 2, 1, 1)
        self.grid.addWidget(self.cov2Txt, 3, 5, 1, 1)
        # self.grid.addWidget(self.cov1FirstCase, 3, 0, 1, 2)
        # self.grid.addWidget(self.cov2FirstCase, 3, 4, 1, 2)

        self.sc = FigureCanvasQTAgg(Figure(figsize=(4, 4)))
        self.sc.figure.add_subplot(2, 2, 1)
        self.sc.figure.add_subplot(2, 2, 2)
        self.sc.figure.add_subplot(2, 2, 3)
        self.sc.figure.add_subplot(2, 2, 4)
        self.grid.addWidget(self.sc, 4, 0, 8, 8)
        self.update_all_graphs(list(cov2.groups.keys())[0])
        self.set_mpl()

        #self.grid.setAlignment(Qt.AlignVCenter)
        self.grid.setContentsMargins(50, 50, 50, 50)
        self.setLayout(self.grid)
        self.showMaximized()

    def update_all_graphs(self, country):
        self.sc.figure.set_canvas(self.sc)
        all_axes = self.sc.figure.get_axes()
        totals = ['total_confirmed', 'total_deceased', 'total_recovered']
        new = ['new_confirmed', 'new_deceased', 'new_recovered']
        try:
            g1 = cov1.get_group(country)
            update_graph(g1, totals, all_axes[0], 1)
            update_graph(g1, new, all_axes[2], 1)
        except KeyError as e:
            #print ('I got a KeyError - reason "%s"' % str(e))
            update_graph(None, None, all_axes[0], 0)
            update_graph(None, None, all_axes[2], 0)
        
        
        g2 = cov2.get_group(country)
        update_graph(g2, totals, all_axes[1], 1)
        update_graph(g2, new, all_axes[3], 1)
        self.sc.figure.subplots_adjust(hspace=0.5, wspace=0.2)
        self.sc.figure.canvas.draw()

    def set_mpl(self):
        all_axes = self.sc.figure.get_axes()
        for i in range(4):
            mpl = mplcursors.cursor(all_axes[i], hover=2,
                                    highlight=True, highlight_kwargs={'color': 'b', 'lw': 3})
            mpl.connect('add', lambda sel: sel.annotation.get_bbox_patch().set(fc='white', alpha=1))
            mpl.connect('add', lambda sel: sel.annotation.set_text(
                '{} ({})'.format(int(sel.target[0]), int(sel.target[1]))))

    def on_combobox_changed(self, value):
        print("combobox changed", value)
        self.update_all_graphs(value)
        self.set_mpl()


def update_graph(group, data, ax, availableData):
    ax.clear()
    if availableData:
        group.plot(ax=ax, x='date', y=data,
                   color=['r', 'k', 'g'])#, xlabel='')
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    else:
        ax.text(0.3, 0.6, 'Nije zabilježen niti jedan slučaj', fontsize=12)
        

if __name__ == '__main__':
    cov1, cov2 = dt.init_data()

    qapp = QtWidgets.QApplication.instance()
    if not qapp:
        qapp = QtWidgets.QApplication(sys.argv)
    app = App()
    app.show()
    app.activateWindow()
    app.raise_()
    #qapp.exec_()
    qapp.quit()
