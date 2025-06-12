import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, QFrame,
                             QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from PIL import Image
import pyodbc  # Conexión a SQL Server
from LoginAdmin import validar_usuario  # Importamos solo la función
from diseñoLogin1 import show_uniform_message
from IngresoFacial import abrir_reconocimiento_para_ingreso
from diseño_botones1 import crear_boton_estilizado_qt  # Necesitarás adaptar esta función

print(pyodbc.drivers())


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CFBD S.A.C Sistema de ingreso personal")

        # Configuración de tamaño y posición centrada
        self.setFixedSize(1280, 720)
        self.center_window()

        # Crear el widget central y el layout principal
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # Crear los frames (ahora QWidgets)
        self.frame_inicio = QWidget()
        self.frame_ingreso = QWidget()
        self.frame_principal = QWidget()

        # Configurar los frames
        self.setup_frame_inicio()
        self.setup_frame_ingreso()
        self.setup_frame_principal()

        # Mostrar el frame inicial
        self.show_frame(self.frame_inicio)

    def center_window(self):
        frame_geometry = self.frameGeometry()
        center_point = QApplication.desktop().availableGeometry().center()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())

    def show_frame(self, frame):
        # Ocultar todos los frames
        self.frame_inicio.hide()
        self.frame_ingreso.hide()
        self.frame_principal.hide()

        # Mostrar el frame solicitado
        frame.show()
        self.main_layout.addWidget(frame)

    def setup_frame_inicio(self):
        # Configurar el fondo
        self.background1 = QLabel(self.frame_inicio)
        pixmap = QPixmap("SetUp/1.png")
        self.background1.setPixmap(pixmap.scaled(1280, 720, Qt.KeepAspectRatioByExpanding))
        self.background1.setGeometry(0, 0, 1280, 720)

        # Configurar botones
        ancho_total_botones = 320
        x_centro = 1280 / 2
        x_boton1 = x_centro - ancho_total_botones / 2
        x_boton2 = x_centro + ancho_total_botones / 2 - 150

        # Botón Ingreso
        self.boton_ingreso = crear_boton_estilizado_qt(
            self.frame_inicio,
            "Ingreso",
            lambda: abrir_reconocimiento_para_ingreso(self)
        )
        self.boton_ingreso.move(x_boton1, 550)
        self.boton_ingreso.resize(150, 40)

        # Botón Administrador
        self.boton_admin = crear_boton_estilizado_qt(
            self.frame_inicio,
            "Administrador",
            lambda: self.show_frame(self.frame_ingreso)
        )
        self.boton_admin.move(x_boton2, 550)
        self.boton_admin.resize(150, 40)

    def setup_frame_ingreso(self):
        # Configurar el fondo con 5.png
        self.background2 = QLabel(self.frame_ingreso)
        pixmap = QPixmap("SetUp/5.png")
        self.background2.setPixmap(pixmap.scaled(1280, 720, Qt.KeepAspectRatioByExpanding))
        self.background2.setGeometry(0, 0, 1280, 720)

        # Contenedor transparente (solo para campos y botón Entrar)
        self.contenedor_ingreso = QFrame(self.frame_ingreso)
        self.contenedor_ingreso.setGeometry(300, 180, 680, 430)  # Tamaño más compacto
        self.contenedor_ingreso.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.15);
                border-radius: 15px;
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
        """)

        # Campos de texto dentro del contenedor
        self.entry_usuario = QLineEdit(self.contenedor_ingreso)
        self.entry_usuario.setPlaceholderText("Usuario")
        self.entry_usuario.setGeometry(173, 120, 330, 40)
        self.entry_usuario.setStyleSheet("""
            QLineEdit {
                font: 12pt 'Arial';
                color: white;
                background-color: rgba(255,255,255,0.1);
                border: none;
                border-bottom: 1px solid white;
                padding: 8px;
            }
        """)

        self.entry_contrasena = QLineEdit(self.contenedor_ingreso)
        self.entry_contrasena.setPlaceholderText("Contraseña")
        self.entry_contrasena.setEchoMode(QLineEdit.Password)
        self.entry_contrasena.setGeometry(173, 200, 330, 40)
        self.entry_contrasena.setStyleSheet(self.entry_usuario.styleSheet())

        # Botón Entrar dentro del contenedor
        self.boton_entrar = crear_boton_estilizado_qt(
            self.contenedor_ingreso,
            "Entrar",
            self.validar_login
        )
        self.boton_entrar.move(280, 300)

        # Botón Regresar FUERA del contenedor (esquina inferior izquierda)
        self.boton_regresar = crear_boton_estilizado_qt(
            self.frame_ingreso,  # Parent es el frame principal
            "Regresar",
            lambda: self.show_frame(self.frame_inicio)
        )
        self.boton_regresar.move(50, 650)  # Posición absoluta
        self.boton_regresar.resize(120, 40)  # Tamaño más pequeño

    def setup_frame_principal(self):
        # Configurar el fondo
        self.background3 = QLabel(self.frame_principal)
        pixmap = QPixmap("SetUp/3.png")
        self.background3.setPixmap(pixmap.scaled(1280, 720, Qt.KeepAspectRatioByExpanding))
        self.background3.setGeometry(0, 0, 1280, 720)

    def validar_login(self):
        usuario = self.entry_usuario.text().strip()
        contrasena = self.entry_contrasena.text().strip()

        if not usuario or not contrasena:
            show_uniform_message(self, "Error", "Usuario y contraseña son obligatorios", "error")
            return

        if validar_usuario(usuario, contrasena):
            show_uniform_message(self, "Éxito", "Inicio de sesión correcto", "success")
            self.show_frame(self.frame_principal)
        else:
            show_uniform_message(self, "Error", "Datos incorrectos", "error")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
