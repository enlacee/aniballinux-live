import sys
import time
import math
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QPainter, QColor, QPen, QGuiApplication
from PyQt6.QtCore import Qt, QTimer, QPoint
from pynput import mouse

# --- Configuración ---
CONFIG = {
    "radius": 60,
    "glow_extra_radius": 2,
    "color_idle": QColor(255, 0, 0, 180),   # Rojo semi-transparente
    "color_active": QColor(0, 255, 0, 200), # Verde al click
    "fps": 60,
    "pulse_speed": 4,
    "glow_pen_width": 5,
    "circle_pen_width": 3
}

class Overlay(QWidget):
    def __init__(self):
        super().__init__()

        # Estado del ratón
        self.mx = 0
        self.my = 0
        self.current_color = CONFIG["color_idle"]
        self.radius = CONFIG["radius"]

        # Configuración de ventana para overlay
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool |
            Qt.WindowType.WindowTransparentForInput
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        # Geometría de pantalla completa
        geo = QGuiApplication.primaryScreen().virtualGeometry()
        self.setGeometry(geo)
        self.move(geo.x(), geo.y())

        # Timer de refresco (~60fps)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(1000 // CONFIG["fps"])

        # Listener de mouse (Global)
        self.listener = mouse.Listener(
            on_move=self.on_move,
            on_click=self.on_click
        )
        self.listener.daemon = True # Asegura que muera con el proceso principal
        self.listener.start()

        self.show()

    def on_move(self, x, y):
        # Mantenemos el print por petición del usuario
        print("Mouse:", x, y)
        self.mx = x
        self.my = y

    def on_click(self, x, y, button, pressed):
        if pressed:
            self.current_color = CONFIG["color_active"]
        else:
            self.current_color = CONFIG["color_idle"]

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Mapeo de coordenadas globales a locales
        point = self.mapFromGlobal(QPoint(int(self.mx), int(self.my)))
        draw_x, draw_y = point.x(), point.y()

        # 1. Dibujar Glow (Animado)
        self._draw_glow(painter, draw_x, draw_y)

        # 2. Dibujar Círculo Principal
        pen = QPen(self.current_color)
        pen.setWidth(CONFIG["circle_pen_width"])
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        
        painter.drawEllipse(
            QPoint(draw_x, draw_y), 
            self.radius, 
            self.radius
        )

    def _draw_glow(self, painter, x, y):
        painter.save()

        # Cálculo de pulso optimizado
        t = time.time()
        pulse = (math.sin(t * CONFIG["pulse_speed"]) + 1) / 2
        alpha = int(20 + pulse * 40)
        
        glow_radius = self.radius + CONFIG["glow_extra_radius"]

        pen = QPen(QColor(255, 255, 255, alpha))
        pen.setWidth(CONFIG["glow_pen_width"])
        painter.setPen(pen)
        
        painter.drawEllipse(
            QPoint(x, y), 
            glow_radius, 
            glow_radius
        )

        painter.restore()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    overlay = Overlay()
    sys.exit(app.exec())

