from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QApplication
import sys
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from matplotlib.axes._subplots import Axes


class PMMatplotlibQt5Widget(QWidget):
    def __init__(self):
        super().__init__()
        self.figure = plt.figure(facecolor='#FFD7C4')  # 可选参数,facecolor为背景颜色
        self.canvas = FigureCanvasQTAgg(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def add_subplot(self, param) -> 'Axes':
        return self.figure.add_subplot(param)


# 运行程序
if __name__ == '__main__':
    app = QApplication(sys.argv)
    pmqt5mplwgt = PMMatplotlibQt5Widget()
    pmqt5mplwgt.show()


    def draw():
        ax = pmqt5mplwgt.add_subplot(121)
        ax2 = pmqt5mplwgt.add_subplot(122)
        ax.plot([1, 2, 3])
        ax.set_xlabel('test_x_label')
        ax2.set_xlabel('test_2')
        ax2.plot([1,3,1,4,15])
        pmqt5mplwgt.canvas.draw()

    draw()
    app.exec()
