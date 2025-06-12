from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from subprocess import Popen
import sys

# Función para mostrar el frame de ingreso
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

# Función para abrir el CRUD de empleados
def abrir_crud():
    Popen([sys.executable, "crud_interface.py"])

# Función para abrir el registro de personal (por ahora muestra un mensaje)
def abrir_registro_personal():
    messagebox.showinfo("Información", "Funcionalidad en desarrollo: Registro de personal")

# --- Ventana principal ---
pantalla = Tk()
pantalla.title("CFBD S.A.C - Sistema de ingreso personal")

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

# Botones en Frame de inicio
boton1 = Button(frame_inicio, text="Ingreso", width=15, height=2)
boton1.place(x=500, y=550)

boton2 = Button(frame_inicio, text="Administrador", width=15, height=2, command=mostrar_frame_ingreso)
boton2.place(x=700, y=550)

# --- Frame de ingreso ---
frame_ingreso = Frame(pantalla)

imagen2 = Image.open("SetUp/2.png")
imagen2 = imagen2.resize((1280, 720))
imagen2F = ImageTk.PhotoImage(imagen2)

background2 = Label(frame_ingreso, image=imagen2F)
background2.place(x=0, y=0, relwidth=1, relheight=1)

# Cuadros de texto
entry_usuario = Entry(frame_ingreso, width=30, font=("Arial", 14))
entry_usuario.place(x=550, y=280)

entry_contrasena = Entry(frame_ingreso, show="*", width=30, font=("Arial", 14))
entry_contrasena.place(x=550, y=400)

# Botones en frame_ingreso
boton_regresar = Button(frame_ingreso, text="Regresar", width=15, height=2, command=mostrar_frame_inicio)
boton_regresar.place(x=100, y=100)

boton_entrar = Button(frame_ingreso, text="Entrar", width=15, height=2, command=mostrar_frame_principal)
boton_entrar.place(x=550, y=550)

# --- Frame principal (imagen 3) ---
frame_principal = Frame(pantalla)

imagen3 = Image.open("SetUp/Blue Futuristic Technology Presentation.jpg")  # Asegúrate que la imagen exista
imagen3 = imagen3.resize((1280, 720))
imagen3F = ImageTk.PhotoImage(imagen3)

background3 = Label(frame_principal, image=imagen3F)
background3.place(x=0, y=0, relwidth=1, relheight=1)

# Botón 1 - Registro de Personal (por ahora muestra alerta)
boton_registro = Button(frame_principal, text="Registro de Personal", width=20, height=2, command=abrir_registro_personal)
boton_registro.place(x=400, y=550)

# Botón 2 - Lista de Empleados (CRUD)
boton_crud = Button(frame_principal, text="Lista de Empleados", width=20, height=2, command=abrir_crud)
boton_crud.place(x=700, y=550)

pantalla.mainloop()
