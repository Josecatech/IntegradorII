from PyQt5.QtWidgets import (QDialog, QLabel, QPushButton, QVBoxLayout,
                             QHBoxLayout, QFrame, QApplication)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QColor


class UniformMessageBox(QDialog):
    def __init__(self, parent, title, message, message_type="success"):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setFixedSize(400, 220)

        # Eliminar barra de título y bordes, y hacer el fondo transparente
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)  # Fondo transparente

        # Configuración de colores según el tipo
        self.color_config = {
            "success": {
                "bg": "#4CAF50",  # Verde
                "button_bg": "#388E3C",  # Verde oscuro
                "button_hover": "#0D7037",  # Verde más oscuro para hover
                "separator": "#81C784"  # Verde claro
            },
            "error": {
                "bg": "#F44336",  # Rojo
                "button_bg": "#D32F2F",  # Rojo oscuro
                "button_hover": "#A4291C",  # Rojo más oscuro para hover
                "separator": "#EF9A9A"  # Rojo claro
            }
        }
        colors = self.color_config.get(message_type, self.color_config["success"])

        # Layout principal SIN márgenes
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)  # Sin márgenes
        main_layout.setSpacing(0)

        # Frame principal con bordes redondeados (ahora ocupa todo el QDialog)
        main_frame = QFrame()
        main_frame.setStyleSheet(f"""
            background-color: {colors['bg']};
            border-radius: 10px;
        """)
        main_layout.addWidget(main_frame)

        # Layout del frame principal con márgenes internos para el contenido
        frame_layout = QVBoxLayout(main_frame)
        frame_layout.setContentsMargins(30, 50, 30, 50)  # Margen interno para el texto
        frame_layout.setSpacing(0)

        # Mensaje principal
        message_label = QLabel(message)
        message_label.setStyleSheet("""
            color: white;
            font: 12pt "Arial";
        """)
        message_label.setWordWrap(True)
        message_label.setAlignment(Qt.AlignCenter)
        message_label.setMinimumWidth(300)  # Ancho mínimo para mejor legibilidad
        frame_layout.addWidget(message_label, 1, Qt.AlignCenter)

        # Espaciador
        frame_layout.addSpacing(20)

        # Frame para el botón (transparente)
        button_frame = QFrame()
        button_frame.setStyleSheet("background: transparent;")
        frame_layout.addWidget(button_frame, 0, Qt.AlignCenter)

        # Botón Aceptar
        self.ok_button = QPushButton("  Aceptar  ")
        self.ok_button.setStyleSheet(f"""
            QPushButton {{
                font: bold 11pt "Arial";
                color: white;
                background-color: {colors['button_bg']};
                border: none;
                padding: 8px 30px;
                border-radius: 5px;
                min-width: 100px;
            }}
            QPushButton:hover {{
                background-color: {colors['button_hover']};
            }}
        """)
        self.ok_button.setCursor(Qt.PointingHandCursor)
        self.ok_button.clicked.connect(self.accept)

        # Layout del frame del botón
        button_layout = QHBoxLayout(button_frame)
        button_layout.addWidget(self.ok_button)

        # Centrar ventana
        self.center_window()
        self.setModal(True)

    def center_window(self):
        screen_geometry = QApplication.desktop().availableGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)


def show_uniform_message(parent, title, message, message_type="success"):
    msg = UniformMessageBox(parent, title, message, message_type)
    msg.exec_()
