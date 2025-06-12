from tkinter import *
from PIL import ImageTk, Image
import imutils
import pyodbc  # Conexión a SQL Server
import subprocess
import sys
from lista_empleados import ventana_lista_empleados

from tkinter import messagebox
from LoginAdmin import validar_usuario  # Importamos solo la función
from diseñoLogin import show_uniform_message
from diseño_botones import crear_boton_estilizado  # Importamos nuestro nuevo diseño


print(pyodbc.drivers())


# Función para mostrar el frame de ingreso
def abrir_registro_personal():
    # Por ahora solo muestra un mensaje (puedes conectar después el módulo real)
    subprocess.Popen([sys.executable, "Registro_personal.py"])

def abrir_lista_empleados():
    ventana_lista_empleados(pantalla)

def mostrar_frame_ingreso():
    frame_inicio.pack_forget()
    frame_ingreso.pack(fill="both", expand=1)


# Función para regresar al frame de inicio
def mostrar_frame_inicio():
    frame_ingreso.pack_forget()
    frame_inicio.pack(fill="both", expand=1)


# Función para mostrar el frame principal (imagen 3)
def mostrar_frame_principal():
    frame_ingreso.pack_forget()
    frame_principal.pack(fill="both", expand=1)


# cambio 
def validar_login():
    usuario = entry_usuario.get().strip()
    contrasena = entry_contrasena.get().strip()

    if not usuario or not contrasena:
        show_uniform_message(pantalla, "Error", "Usuario y contraseña son obligatorios", "error")
        return

    if validar_usuario(usuario, contrasena):
        show_uniform_message(pantalla, "Éxito", "Inicio de sesión correcto", "success")
        mostrar_frame_principal()
    else:
        show_uniform_message(pantalla, "Error", "Datos incorrectos", "error")
# fin cambio


# --- Ventana principal ---
pantalla = Tk()
pantalla.title("CFBD S.A.C Sistema de ingreso personal")
pantalla.overrideredirect(True)  # Elimina la barra de título

# Centrar ventana
ancho_pantalla = pantalla.winfo_screenwidth()
alto_pantalla = pantalla.winfo_screenheight()
ancho_ventana = 1280
alto_ventana = 720
x = (ancho_pantalla // 2) - (ancho_ventana // 2)
y = (alto_pantalla // 2) - (alto_ventana // 2)
pantalla.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")

# --- Frame de inicio ---
frame_inicio = Frame(pantalla)
frame_inicio.pack(fill="both", expand=1)

imagen1 = Image.open("SetUp/1.png")
imagen1 = imagen1.resize((1280, 720))
imagen1F = ImageTk.PhotoImage(imagen1)

background1 = Label(frame_inicio, image=imagen1F)
background1.place(x=0, y=0, relwidth=1, relheight=1)

# cambio 
# centrado
ancho_total_botones = 320  # 150 c/botón + 20 de separación
x_centro = ancho_ventana / 2
x_boton1 = x_centro - ancho_total_botones/2
x_boton2 = x_centro + ancho_total_botones/2 - 150  # 150 = ancho estimado del botón

# Botón Ingreso (izquierda)
boton1 = crear_boton_estilizado(frame_inicio, "Ingreso")
boton1.place(x=x_boton1, y=550,  height=40)  # Ajustar width/height

# Botón Administrador (derecha)
boton2 = crear_boton_estilizado(frame_inicio, "Administrador", command=mostrar_frame_ingreso)
boton2.place(x=x_boton2, y=550, width=150, height=40)
# fin cambio


# --- Frame de ingreso ---
frame_ingreso = Frame(pantalla)

imagen2 = Image.open("SetUp/2.png")
imagen2 = imagen2.resize((1280, 720))
imagen2F = ImageTk.PhotoImage(imagen2)

background2 = Label(frame_ingreso, image=imagen2F)
background2.place(x=0, y=0, relwidth=1, relheight=1)


# cambio 
estilo_entry = {
    'font': ("Arial", 12),
    'fg': 'white',            # Color del texto
    'bg': '#0C0A27',          # Fondo negro (se verá transparente sobre la imagen)
    'borderwidth': 0,         # Sin bordes
    'highlightthickness': 0,  # Sin resaltado

    'relief': FLAT            # Sin relieve
}

# Cuadro de texto para usuario (solo línea)
entry_usuario = Entry(frame_ingreso, **estilo_entry)
entry_usuario.place(x=550, y=273, width=300, height=32)

# Línea decorativa bajo el Entry (simulando subrayado)
Frame(frame_ingreso, bg='white', height=1).place(x=550, y=305, width=300)

# Cuadro de texto para contraseña (solo línea)
entry_contrasena = Entry(frame_ingreso, show="*", **estilo_entry)
entry_contrasena.place(x=550, y=393, width=300, height=32)

# Línea decorativa bajo el Entry (simulando subrayado)
Frame(frame_ingreso, bg='white', height=1).place(x=550, y=425, width=300)

# Botones en frame_ingreso
boton_regresar = crear_boton_estilizado(frame_ingreso, "Regresar", command=mostrar_frame_inicio)
boton_regresar.place(x=100, y=100)

boton_entrar = crear_boton_estilizado(frame_ingreso, "Entrar", command=validar_login)
boton_entrar.place(x=550, y=550)

# fin cambio

# --- Frame principal (imagen 3) ---
frame_principal = Frame(pantalla)

imagen3 = Image.open("SetUp/Fondo.jpg")  # Asegúrate que exista SetUp/3.png
imagen3 = imagen3.resize((1280, 720))
imagen3F = ImageTk.PhotoImage(imagen3)

background3 = Label(frame_principal, image=imagen3F)
background3.place(x=0, y=0, relwidth=1, relheight=1)
# Botón: Registro de Personal
btn_registro = crear_boton_estilizado(frame_principal, "Registro de Personal", command=abrir_registro_personal)
btn_registro.place(x=400, y=500)

# Botón: Lista de Empleados
btn_lista = crear_boton_estilizado(frame_principal, "Lista de Empleados", command=abrir_lista_empleados)
btn_lista.place(x=700, y=500)


def abrir_lista_empleados():
    ventana_lista_empleados()



pantalla.mainloop()
