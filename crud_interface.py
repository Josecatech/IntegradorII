# crud_interface.py
import tkinter as tk
from tkinter import messagebox
from crud_db import obtener_personal, insertar_personal, actualizar_personal, eliminar_personal, dni_existe

def crud_main():
    ventana = tk.Tk()
    ventana.title("Lista de Empleados")
    ventana.geometry("900x500")

    # Variables
    nombre_var = tk.StringVar()
    apellido_var = tk.StringVar()
    dni_var = tk.StringVar()
    cargo_var = tk.StringVar()
    id_actual = [None]

    # Entradas
    tk.Label(ventana, text="Nombre").place(x=20, y=20)
    tk.Entry(ventana, textvariable=nombre_var, width=30).place(x=100, y=20)

    tk.Label(ventana, text="Apellido").place(x=20, y=60)
    tk.Entry(ventana, textvariable=apellido_var, width=30).place(x=100, y=60)

    tk.Label(ventana, text="DNI").place(x=20, y=100)
    tk.Entry(ventana, textvariable=dni_var, width=30).place(x=100, y=100)

    tk.Label(ventana, text="Cargo").place(x=20, y=140)
    tk.Entry(ventana, textvariable=cargo_var, width=30).place(x=100, y=140)

    lista = tk.Listbox(ventana, width=110, height=15)
    lista.place(x=20, y=200)

    def refrescar_lista():
        lista.delete(0, tk.END)
        for row in obtener_personal():
            id, nombre, apellido, dni, cargo, fecha = row
            texto = f"ID: {id} | {nombre} {apellido} | DNI: {dni} | Cargo: {cargo}"
            lista.insert(tk.END, texto)

    def seleccionar_item(event):
        seleccion = lista.curselection()
        if seleccion:
            index = seleccion[0]
            fila = obtener_personal()[index]
            id_actual[0] = fila[0]
            nombre_var.set(fila[1])
            apellido_var.set(fila[2])
            dni_var.set(fila[3])
            cargo_var.set(fila[4])
    lista.bind("<<ListboxSelect>>", seleccionar_item)

    def agregar():
        nombre = nombre_var.get()
        apellido = apellido_var.get()
        dni = dni_var.get()
        cargo = cargo_var.get()

        if not (nombre and apellido and dni and cargo):
            messagebox.showwarning("Campos vacíos", "Por favor, completa todos los campos.")
            return

        if dni_existe(dni):
            messagebox.showerror("DNI duplicado", f"Ya existe un empleado registrado con el DNI: {dni}")
            return

        insertar_personal(nombre, apellido, dni, cargo)
        refrescar_lista()
        nombre_var.set("")
        apellido_var.set("")
        dni_var.set("")
        cargo_var.set("")
        messagebox.showinfo("Éxito", "Empleado registrado correctamente.")

    def actualizar():
        if id_actual[0]:
            actualizar_personal(id_actual[0], nombre_var.get(), apellido_var.get(), dni_var.get(), cargo_var.get())
            refrescar_lista()
        else:
            messagebox.showwarning("Selección requerida", "Debes seleccionar un registro primero.")

    def eliminar():
        if id_actual[0] is not None:
            confirmar = messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar este registro?")
            if confirmar:
                eliminar_personal(id_actual[0])
                refrescar_lista()
                nombre_var.set("")
                apellido_var.set("")
                dni_var.set("")
                cargo_var.set("")
                id_actual[0] = None
        else:
            messagebox.showwarning("Atención", "Debes seleccionar un empleado primero.")
    # Botones
    tk.Button(ventana, text="Agregar", width=12, command=agregar).place(x=450, y=20)
    tk.Button(ventana, text="Actualizar", width=12, command=actualizar).place(x=450, y=60)
    tk.Button(ventana, text="Eliminar", width=12, command=eliminar).place(x=450, y=100)
    tk.Button(ventana, text="Refrescar", width=12, command=refrescar_lista).place(x=450, y=140)

    refrescar_lista()
    ventana.mainloop()

if __name__ == "__main__":
    crud_main()
