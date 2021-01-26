import sys
from PyQt5.QtWidgets import QComboBox, QLabel
from PyQt5.QtGui import QIcon, QFont
from matplotlib.backends.qt_compat import QtCore, QtWidgets
if QtCore.qVersion() >= "5.":
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
else:
    from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator
import mplcursors
import data_init as dt


class App(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        with open('style.qss', 'r') as f:
            self.setStyleSheet(f.read())

        self.setWindowTitle('Usporedba COVID-19 i SARS epidemije')
        self.setGeometry(0, 0, 1080, 720)
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

        self.canvas = FigureCanvasQTAgg(Figure(figsize=(4, 4)))
        self.canvas.figure.add_subplot(2, 2, 1)
        self.canvas.figure.add_subplot(2, 2, 2)
        self.canvas.figure.add_subplot(2, 2, 3)
        self.canvas.figure.add_subplot(2, 2, 4)

        self.update_all_graphs(list(cov2.groups.keys())[0])
        set_mpl(self.canvas.figure.get_axes())

        self.grid = QtWidgets.QGridLayout(self._main)
        self.grid.setSpacing(20)
        self.grid.addWidget(self.dropdown, 1, 3, 1, 2)  # row, col, rowspan, colspan
        self.grid.addWidget(self.cov1Txt, 3, 2, 1, 1)
        self.grid.addWidget(self.cov2Txt, 3, 5, 1, 1)
        self.grid.addWidget(self.canvas, 4, 0, 8, 8)
        self.grid.setContentsMargins(50, 50, 50, 50)
        self.setLayout(self.grid)

        self.showMaximized()

    def update_all_graphs(self, country):
        self.canvas.figure.set_canvas(self.canvas)
        all_axes = self.canvas.figure.get_axes()
        totals = ['total_confirmed', 'total_deceased', 'total_recovered']
        new = ['new_confirmed', 'new_deceased', 'new_recovered']

        try:
            g1 = cov1.get_group(country)
            update_graph(g1, totals, all_axes[0], True)
            update_graph(g1, new, all_axes[2], True)
        except KeyError as e:
            update_graph(None, None, all_axes[0], False)
            update_graph(None, None, all_axes[2], False)

        g2 = cov2.get_group(country)
        update_graph(g2, totals, all_axes[1], True)
        update_graph(g2, new, all_axes[3], True)

        self.canvas.figure.subplots_adjust(hspace=0.5, wspace=0.2)
        self.canvas.figure.canvas.draw()

    def on_combobox_changed(self, value):
        self.update_all_graphs(value)
        set_mpl(self.canvas.figure.get_axes())


def set_mpl(all_axes):
    for i in range(len(all_axes)):
        mpl = mplcursors.cursor(all_axes[i], hover=2,
                                highlight=True, highlight_kwargs={'color': 'b', 'lw': 3})
        mpl.connect('add', lambda sel: sel.annotation.get_bbox_patch().set(fc='white', alpha=1))
        mpl.connect('add', lambda sel: sel.annotation.set_text(int(sel.target[1])))


def update_graph(group, data, ax, available_data):
    ax.clear()
    if available_data:
        group.plot(ax=ax, x='date', y=data,
                   color=['r', 'k', 'g'])  # , xlabel='')
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
    # qapp.exec_()
    qapp.quit()
