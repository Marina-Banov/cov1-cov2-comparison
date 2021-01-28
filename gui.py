import sys
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtGui import QIcon, QFont
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
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

        dropdown = QComboBox()
        dropdown.setObjectName('dropdownList')
        dropdown.addItems(cov2.groups.keys())
        dropdown.resize(100, 50)
        dropdown.setFont(QFont('Ubuntu', 11, QFont.Medium))
        dropdown.currentTextChanged.connect(self.on_combobox_changed)

        self.canvas = FigureCanvasQTAgg(Figure(figsize=(4, 4)))
        self.canvas.figure.add_subplot(2, 2, 1)
        self.canvas.figure.add_subplot(2, 2, 2)
        self.canvas.figure.add_subplot(2, 2, 3)
        self.canvas.figure.add_subplot(2, 2, 4)

        self.update_all_graphs(list(cov2.groups.keys())[0])
        set_mpl(self.canvas.figure.get_axes())

        grid = QtWidgets.QGridLayout(self._main)
        grid.setSpacing(20)
        grid.addWidget(dropdown, 1, 3, 1, 2)  # row, col, rowspan, colspan
        grid.addWidget(self.canvas, 3, 0, 8, 8)
        grid.setContentsMargins(50, 50, 50, 50)
        self.setLayout(grid)

        self.showMaximized()

    def update_all_graphs(self, country):
        self.canvas.figure.set_canvas(self.canvas)
        all_axes = self.canvas.figure.get_axes()
        totals = ['total_confirmed', 'total_deceased', 'total_recovered']
        new = ['new_confirmed', 'new_deceased', 'new_recovered']

        try:
            g1 = cov1.get_group(country)
            update_graph(g1, totals, all_axes[0], 'SARS', True)
            update_graph(g1, new, all_axes[2], '', True)
        except KeyError as e:
            update_graph(None, None, all_axes[0], 'SARS', False)
            update_graph(None, None, all_axes[2], '', False)

        g2 = cov2.get_group(country)
        update_graph(g2, totals, all_axes[1], 'COVID-19', True)
        update_graph(g2, new, all_axes[3], '', True)

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


def update_graph(group, data, ax, title, available_data):
    ax.clear()
    if available_data:
        group.plot(ax=ax, x='date', y=data,
                   color=['r', 'k', 'g'], xlabel='', rot=0)
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b\n%Y'))
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    else:
        ax.text(0.3, 0.5, 'Nije zabilježen niti jedan slučaj', fontsize=12)
        ax.set_xticklabels([])
        ax.set_yticklabels([])
    if title != '':
        ax.set_title(title, pad=30)


if __name__ == '__main__':
    cov1, cov2 = dt.init_data()

    plt.rc('axes', titlesize=22)
    qapp = QtWidgets.QApplication.instance()
    if not qapp:
        qapp = QtWidgets.QApplication(sys.argv)
    app = App()
    app.show()
    app.activateWindow()
    app.raise_()
    # qapp.exec_()
    qapp.quit()
