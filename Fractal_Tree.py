import sys
import math
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QSlider, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen, QFont


class FractalWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.angle_deg = 30
        self.depth = 10
        self.length_ratio = 0.7
        self.setStyleSheet("background-color: #202225;")

    def set_angle(self, deg: int):
        self.angle_deg = int(deg)
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setPen(QPen(Qt.white, 2))

        w, h = self.width(), self.height()
        x0, y0 = w // 2, h - 12
        trunk_len = int(h * 0.32)
        x1, y1 = x0, y0 - trunk_len
        p.drawLine(x0, y0, x1, y1)

        self._draw_branches(p, x1, y1, trunk_len * self.length_ratio, -90, self.depth - 1)

    def _draw_branches(self, p: QPainter, x: int, y: int,
                       length: float, base_angle_deg: float, depth: int):
        if depth <= 0 or length < 1:
            return

        left_angle = base_angle_deg - self.angle_deg
        right_angle = base_angle_deg + self.angle_deg

        lx = x + int(length * math.cos(math.radians(left_angle)))
        ly = y + int(length * math.sin(math.radians(left_angle)))
        rx = x + int(length * math.cos(math.radians(right_angle)))
        ry = y + int(length * math.sin(math.radians(right_angle)))

        p.drawLine(x, y, lx, ly)
        p.drawLine(x, y, rx, ry)

        new_len = length * self.length_ratio
        self._draw_branches(p, lx, ly, new_len, left_angle, depth - 1)
        self._draw_branches(p, rx, ry, new_len, right_angle, depth - 1)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Фрактальное дерево")
        self.resize(1000, 650)

        layout = QVBoxLayout(self)

        self.canvas = FractalWidget()
        layout.addWidget(self.canvas, stretch=1)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 90)
        self.slider.setValue(self.canvas.angle_deg)
        self.slider.setTickInterval(5)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.valueChanged.connect(self.canvas.set_angle)
        layout.addWidget(self.slider)

        self.label = QLabel("Угол ветвления (°)")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("color: #cfcfcf;")
        layout.addWidget(self.label)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
