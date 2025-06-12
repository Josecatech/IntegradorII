from PyQt5.QtWidgets import QPushButton, QFrame, QHBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QCursor


def crear_boton_estilizado_qt(master, texto, command=None):
    """
    Crea un botón con estilo profesional usando la paleta de colores proporcionada (versión PyQt5)

    Args:
        master: Widget padre (QWidget)
        texto: Texto del botón
        command: Función a ejecutar al hacer click

    Returns:
        QFrame: Contenedor con el botón estilizado y efectos hover
    """
    paleta = {
        "azul_oscuro": "#0C0A27",  # Color principal
        "turquesa": "#0C0A27",  # Color hover
        "celeste_metalico": "#0F7E8D",  # Color activo
        "borde": "#FFFFFF",  # Azul intermedio para borde
        "borde_hover": "#0F7E8D"  # Turquesa claro para borde hover
    }

    # Creamos un contenedor para el botón (permite mostrar el borde correctamente)
    contenedor = QFrame(master)
    contenedor.setStyleSheet(f"""
        background-color: {paleta['borde']}; 
        border-radius: 4px;
        border: none;
    """)
    contenedor.setFixedHeight(35)  # Ajustamos altura para contener el botón

    # Layout para centrar el botón
    layout = QHBoxLayout(contenedor)
    layout.setContentsMargins(1, 1, 1, 1)  # Grosor del borde
    layout.setSpacing(0)

    # Botón principal
    btn = QPushButton(f"  {texto}  ", contenedor)
    btn.setStyleSheet(f"""
        QPushButton {{
            font: bold 11pt "Arial";
            color: white;
            background-color: {paleta['azul_oscuro']};
            border: none;
            padding: 6px 25px;
            border-radius: 4px;
        }}
        QPushButton:pressed {{
            background-color: {paleta['celeste_metalico']};
            border-radius: 9px;
        }}
    """)

    # Conectar la señal clicked si se proporciona un comando
    if command is not None:
        btn.clicked.connect(command)

    # Añadir el botón al layout
    layout.addWidget(btn)

    # Efectos hover dinámicos
    def on_enter():
        contenedor.setStyleSheet(f"""
            background-color: {paleta['borde_hover']}; 
            border-radius: 5px;
            border: none;
        """)
        btn.setStyleSheet(f"""
            QPushButton {{
                font: bold 11pt "Arial";
                color: white;
                background-color: {paleta['turquesa']};
                border: none;
                padding: 6px 25px;
                border-radius: 4px;
            }}
            QPushButton:pressed {{
                background-color: {paleta['celeste_metalico']};
                border-radius: 4px;
            }}
        """)
        btn.setCursor(QCursor(Qt.PointingHandCursor))

    def on_leave():
        contenedor.setStyleSheet(f"""
            background-color: {paleta['borde']}; 
            border-radius: 5px;
            border: none;
        """)
        btn.setStyleSheet(f"""
            QPushButton {{
                font: bold 11pt "Arial";
                color: white;
                background-color: {paleta['azul_oscuro']};
                border: none;
                padding: 6px 25px;
                border-radius: 4px;
            }}
            QPushButton:pressed {{
                background-color: {paleta['celeste_metalico']};
                border-radius: 4px;
            }}
        """)
        btn.setCursor(QCursor(Qt.ArrowCursor))

    # Conectar eventos hover
    btn.enterEvent = lambda event: on_enter()
    btn.leaveEvent = lambda event: on_leave()
    contenedor.enterEvent = lambda event: on_enter()
    contenedor.leaveEvent = lambda event: on_leave()

    return contenedor
