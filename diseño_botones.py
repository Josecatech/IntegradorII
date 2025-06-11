from tkinter import Button, FLAT
from tkinter import Button, Frame

def crear_boton_estilizado(master, texto, command=None):
    """
    Crea un botón con estilo profesional usando la paleta de colores proporcionada

    Args:
        master: Widget padre
        texto: Texto del botón
        command: Función a ejecutar al hacer click

    Returns:
        Button: Botón estilizado con efectos hover
    """
    paleta = {
        "azul_oscuro": "#0C0A27",  # Color principal
        "turquesa": "#0C0A27",  # Color hover
        "celeste_metalico": "#0F7E8D",  # Color activo
        "borde": "#FFFFFF",  # Azul intermedio para borde
        "borde_hover": "#0F7E8D"  # Turquesa claro para borde hover
    }

    # Creamos un contenedor para el botón (permite mostrar el borde correctamente)
    contenedor = Frame(master,
                       bg=paleta["borde"],
                       bd=0,
                       highlightthickness=0)

    # Botón principal
    btn = Button(contenedor,
                 text=f"  {texto}  ",
                 font=("Arial", 11, "bold"),
                 bg=paleta["azul_oscuro"],
                 fg="white",
                 activebackground=paleta["celeste_metalico"],
                 activeforeground="white",
                 relief="flat",
                 borderwidth=0,
                 padx=25,
                 pady=6,
                 command=command)

    # Ajustes de padding para el borde
    btn.pack(padx=1.3, pady=1.3)  # Grosor del borde

    # Efectos hover dinámicos
    def on_enter(e):
        contenedor.config(bg=paleta["borde_hover"])
        btn.config(bg=paleta["turquesa"], cursor="hand2")

    def on_leave(e):
        contenedor.config(bg=paleta["borde"])
        btn.config(bg=paleta["azul_oscuro"], cursor="")

    contenedor.bind("<Enter>", on_enter)
    contenedor.bind("<Leave>", on_leave)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

    return contenedor
