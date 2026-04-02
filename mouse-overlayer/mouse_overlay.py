import sys
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QPainter, QColor, QPen
from PyQt6.QtCore import Qt, QTimer
from pynput import mouse
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtCore import QPoint

class Overlay(QWidget):
    def __init__(self):
        super().__init__()

        self.mx = 0
        self.my = 0
        self.radius = 60
        self.color = QColor(255, 0, 0, 255)  # rojo semi-transparente

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        self.glow_radius = self.radius + 20
        self.glow_alpha = 80
        self.glow_direction = 1  # para animación

        # geometry = QApplication.instance().primaryScreen().virtualGeometry()
        geo = QGuiApplication.primaryScreen().virtualGeometry()
        # print("Screen geometry:", geometry)

        self.setGeometry(geo)
        self.move(geo.x(), geo.y())  # 👈 ESTO ES CLAVE
        self.setWindowFlag(Qt.WindowType.WindowTransparentForInput, True)
        self.show()

        # refresco ligero (~60fps)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(16)

        # listener mouse
        self.listener = mouse.Listener(
            on_move=self.on_move,
            on_click=self.on_click
        )
        self.listener.start()

    def on_move(self, x, y):
        print("Mouse:", x, y)
        self.mx = x
        self.my = y

    def on_click(self, x, y, button, pressed):
        if pressed:
            self.color = QColor(0, 255, 0, 200)  # verde al click
        else:
            self.color = QColor(255, 0, 0, 180)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        pen = QPen(self.color)
        pen.setWidth(3)
        painter.setPen(pen)

        painter.setBrush(Qt.BrushStyle.NoBrush)

        # 👇 MAPEO CORRECTO
        local_x = self.mapFromGlobal(self.mapToGlobal(self.rect().topLeft())).x()
        local_y = self.mapFromGlobal(self.mapToGlobal(self.rect().topLeft())).y()

        point = self.mapFromGlobal(QPoint(self.mx, self.my))
        draw_x = point.x()
        draw_y = point.y()

        # 👇 primero el glow (importante)
        self.draw_glow(painter, draw_x, draw_y)

        # 👇 luego tu círculo rojo normal
        painter.drawEllipse(
            int(draw_x - self.radius),
            int(draw_y - self.radius),
            self.radius * 2,
            self.radius * 2
        )

    def draw_glow(self, painter, draw_x, draw_y):
        import time, math

        painter.save()  # 👈 guarda estado actual

        t = time.time()
        pulse = (math.sin(t * 4) + 1) / 2
        alpha = int(20 + pulse * 40)

        glow_radius = self.radius + 2

        pen = QPen(QColor(255, 255, 255, alpha))
        pen.setWidth(5)

        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)

        painter.drawEllipse(
            int(draw_x - glow_radius),
            int(draw_y - glow_radius),
            glow_radius * 2,
            glow_radius * 2
        )

        painter.restore()  # 👈 vuelve al estado anterior

if __name__ == "__main__":
    app = QApplication(sys.argv)
    overlay = Overlay()
    sys.exit(app.exec())

