import customtkinter as ctk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import os
import pyodbc

def conectar_db():
    try:
        connection_string = """
            DRIVER={ODBC Driver 17 for SQL Server};
            SERVER=LAPTOP-6SOD4TD3\\SQLEXPRESS;
            DATABASE=UTP_SECURITYFACIAL;
            Trusted_Connection=yes;
        """
        return pyodbc.connect(connection_string)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo conectar a la base de datos:\n{str(e)}")
        return None

def ventana_registro():
    pantalla = ctk.CTk()
    pantalla.title("Registro de Personal")
    pantalla.geometry("1280x720")  # ✅ Tamaño fijo desde el inicio

    frame_principal = ctk.CTkFrame(pantalla)
    frame_principal.pack(fill="both", expand=True)  # ESTA LÍNEA ES CLAVE

    imagen3 = Image.open("SetUp/0.jpg")
    background3 = ctk.CTkLabel(frame_principal, text="")
    background3.place(x=0, y=0, relwidth=1, relheight=1)
    frame_principal.bind("<Configure>",
                         lambda e: redimensionar_fondo(e, imagen3, background3))  # type: ignore[attr-defined]

    # Tarjeta flotante para Registro Personal
    fondo_aux_registro = ctk.CTkFrame(
        frame_principal, width=810, height=510, fg_color="#1a1a1a", corner_radius=20
    )
    fondo_aux_registro.place(relx=0.5, rely=0.5, anchor="center")

    tarjeta_registro = ctk.CTkFrame(
        frame_principal, width=800, height=500,
        fg_color="#222222", corner_radius=18
    )
    tarjeta_registro.place(relx=0.5, rely=0.5, anchor="center")

    # Título
    titulo_registro = ctk.CTkLabel(
        tarjeta_registro, text="REGISTRO PERSONAL",
        font=("Orbitron", 28, "bold"), text_color="white"
    )
    titulo_registro.place(relx=0.5, rely=0.1, anchor="center")

    # Íconos para los campos (coloca los archivos correctos)
    icono_nombre = ctk.CTkImage(Image.open("SetUp/user_icon.png"), size=(25, 25))
    icono_apellido = ctk.CTkImage(Image.open("SetUp/user_icon.png"), size=(25, 25))  # Puedes usar otro ícono si quieres
    icono_dni = ctk.CTkImage(Image.open("SetUp/id_icon.png"), size=(25, 25))  # Pon un ícono para DNI
    icono_cargo = ctk.CTkImage(Image.open("SetUp/user_icon.png"), size=(25, 25))

    # En vez de los labels + entries, creamos íconos + entries con placeholder_text
    pos_y = [100, 170, 240]  # Espacios verticales para los 3 campos
    iconos = [icono_nombre, icono_apellido, icono_dni, icono_cargo]
    placeholders = ["Nombre", "Apellido", "DNI", "Cargo"]
    entries = []

    def solo_numeros(texto):
        return texto.isdigit() or texto == ""

    validacion_dni = pantalla.register(solo_numeros)

    contenedor_campos = ctk.CTkFrame(tarjeta_registro, fg_color="transparent")
    contenedor_campos.place(relx=0.5, rely=0.40, anchor="center")  # Ajusta 'rely' según lo necesites

    for i in range(4):
        icono_label = ctk.CTkLabel(contenedor_campos, image=iconos[i], text="")
        icono_label.grid(row=i, column=0, padx=(0, 10), pady=10)

        if i == 2:  # DNI
            entry = ctk.CTkEntry(
                contenedor_campos, width=400, height=40,
                font=("Arial", 16),
                placeholder_text=placeholders[i],
                validate="key",
                validatecommand=(validacion_dni, '%P')
            )
        else:
            entry = ctk.CTkEntry(
                contenedor_campos, width=400, height=40,
                font=("Arial", 16),
                placeholder_text=placeholders[i]
            )

        entry.grid(row=i, column=1, pady=10)
        entries.append(entry)

    #

    def mostrar_ventana_archivo(ruta_archivo):
        import os

        ventana = ctk.CTkToplevel()
        ventana.title("Archivo Cargado")
        ventana.geometry("500x450")
        ventana.resizable(False, False)
        ventana.transient(pantalla)
        ventana.grab_set()

        # Mostrar nombre del archivo
        nombre = os.path.basename(ruta_archivo)
        label_nombre = ctk.CTkLabel(ventana, text=f"Archivo: {nombre}", font=("Arial", 16))
        label_nombre.pack(pady=10)

        # Mostrar ruta completa
        label_ruta = ctk.CTkLabel(ventana, text=ruta_archivo, font=("Arial", 12), text_color="gray")
        label_ruta.pack(pady=5)

        # Intentar mostrar imagen
        imagen_mostrada = False
        try:
            imagen = Image.open(ruta_archivo)
            imagen.thumbnail((400, 300))
            imagen_tk = ImageTk.PhotoImage(imagen)

            label_imagen = ctk.CTkLabel(ventana, text="", image=imagen_tk)  # type: ignore[attr-defined]
            label_imagen.image = imagen_tk
            label_imagen.pack(pady=10)
            imagen_mostrada = True
        except:
            label_error = ctk.CTkLabel(ventana, text="Vista previa no disponible", text_color="red")
            label_error.pack(pady=10)

        # Botón para eliminar el archivo
        def eliminar_archivo():
            try:
                os.remove(ruta_archivo)
                messagebox.showinfo("Eliminado", "Archivo eliminado correctamente.")
                ventana.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar el archivo:\n{str(e)}")

        boton_eliminar = ctk.CTkButton(
            ventana, text="Eliminar archivo", text_color="#FF5050",
            fg_color="transparent", border_color="#FF5050", border_width=2,
            corner_radius=8, hover_color="#400000", font=("Arial", 14, "bold"),
            command=eliminar_archivo
        )
        boton_eliminar.pack(pady=20)

    # Botón con ícono (cara) para registro biométrico

    def seleccionar_archivo_biometrico():
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo biométrico",
            filetypes=[("Imágenes", "*.jpg *.png *.bmp *.tiff"), ("Todos los archivos", "*.*")]
        )
        if archivo:
            mostrar_ventana_archivo(archivo)

    icono_cara = ctk.CTkImage(Image.open("SetUp/face.png"), size=(25, 25))  # ← Asegúrate de tener esta imagen
    boton_biometrico = ctk.CTkButton(
        tarjeta_registro, text=" Registro Biométrico", image=icono_cara,
        compound="left", text_color="#00FF90", fg_color="transparent",
        border_color="#00FF90", border_width=2, corner_radius=8,
        hover_color="#003f2e", font=("Arial", 16, "bold"),
        width=250, height=50,
        command=seleccionar_archivo_biometrico)
    boton_biometrico.place(x=250, y=320)

    # Botón de guardar personal
    boton_guardar_personal = ctk.CTkButton(
        tarjeta_registro, text="Guardar Personal", text_color="#00FF90", fg_color="transparent",
        border_color="#00FF90", border_width=2, corner_radius=8,
        hover_color="#003f2e", font=("Arial", 16, "bold"),
        width=200, height=50,
        command=lambda: guardar_datos_personal()
    )
    boton_guardar_personal.place(x=50, y=420)
    # Botón de cerrar sesión
    boton_cerrar_sesion = ctk.CTkButton(
        tarjeta_registro, text="Cerrar Sesión", text_color="#FF5050", fg_color="transparent",
        border_color="#FF5050", border_width=2, corner_radius=8,
        hover_color="#400000", font=("Arial", 16, "bold"),
        width=200, height=50, command=pantalla.destroy
    )
    boton_cerrar_sesion.place(x=550, y=420)

    def guardar_datos_personal():
        nombre = entries[0].get()
        apellido = entries[1].get()
        dni = entries[2].get()
        cargo = entries[3].get()

        if not nombre or not apellido or not dni or not cargo:
            messagebox.showwarning("Campos incompletos", "Todos los campos son obligatorios.")
            return

        try:
            conn = conectar_db()
            if conn is None:
                return

            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO personal (nombre, apellido, dni, cargo, fecha_registro) VALUES (?, ?, ?, ?, GETDATE())",
                (nombre, apellido, dni, cargo)
            )
            conn.commit()
            conn.close()

            messagebox.showinfo("Éxito", "Datos personales guardados correctamente.")
            for entry in entries:
                entry.delete(0, "end")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar:\n{str(e)}")

    pantalla.mainloop()


if __name__ == "__main__":
    ventana_registro()
