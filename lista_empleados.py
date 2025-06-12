import customtkinter as ctk
from tkinter import messagebox, ttk
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
        messagebox.showerror("Error", f"No se pudo conectar:\n{str(e)}")
        return None

def ventana_lista_empleados(parent=None):
    app = ctk.CTkToplevel(parent)
    app.title("Lista de Empleados")
    app.geometry("1000x600")
    app.resizable(False, False)

    frame = ctk.CTkFrame(app)
    frame.pack(fill="both", expand=True, padx=20, pady=20)

    tree = ttk.Treeview(frame, columns=("ID", "Nombre", "Apellido", "DNI", "Cargo", "Fecha"), show="headings")
    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, width=150)
    tree.pack(fill="both", expand=True, pady=10)

    def cargar_datos():
        tree.delete(*tree.get_children())
        conn = conectar_db()
        if not conn:
            return
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, apellido, dni, cargo, fecha_registro FROM personal")
        for row in cursor.fetchall():
            tree.insert("", "end", values=[str(item).strip() for item in row])
        conn.close()

    def eliminar_empleado():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un registro para eliminar.")
            app.lift(); app.focus_force()
            return
        item = tree.item(selected[0])
        id_personal = int(str(item["values"][0]).replace("'", "").strip())
        confirm = messagebox.askyesno("Confirmar", f"¿Eliminar empleado ID {id_personal}?")
        if not confirm:
            return
        try:
            conn = conectar_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM personal WHERE id = ?", (id_personal,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Éxito", "Empleado eliminado.")
            app.lift(); app.focus_force()
            cargar_datos()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar:\n{str(e)}")
            app.lift(); app.focus_force()

    def editar_empleado():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un registro para editar.")
            app.lift(); app.focus_force()
            return
        item = tree.item(selected[0])
        id_personal = int(str(item["values"][0]).replace("'", "").strip())
        nombre = str(item["values"][1]).replace("'", "").strip()
        apellido = str(item["values"][2]).replace("'", "").strip()
        dni = str(item["values"][3]).replace("'", "").strip()
        cargo = str(item["values"][4]).replace("'", "").strip()

        def guardar_edicion():
            nuevo_nombre = entry_nombre.get()
            nuevo_apellido = entry_apellido.get()
            nuevo_dni = entry_dni.get()
            nuevo_cargo = entry_cargo.get()

            if not nuevo_nombre or not nuevo_apellido or not nuevo_dni or not nuevo_cargo:
                messagebox.showwarning("Campos vacíos", "Todos los campos son obligatorios.")
                app.lift(); app.focus_force()
                return
            try:
                conn = conectar_db()
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE personal SET nombre=?, apellido=?, dni=?, cargo=? WHERE id=?",
                    (nuevo_nombre, nuevo_apellido, nuevo_dni, nuevo_cargo, id_personal)
                )
                conn.commit()
                conn.close()
                top.destroy()
                cargar_datos()
                messagebox.showinfo("Éxito", "Empleado actualizado.")
                app.lift(); app.focus_force()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo actualizar:\n{str(e)}")
                app.lift(); app.focus_force()

        top = ctk.CTkToplevel(app)
        top.title("Editar Empleado")
        top.geometry("400x350")

        entry_nombre = ctk.CTkEntry(top, placeholder_text="Nombre")
        entry_nombre.insert(0, nombre)
        entry_nombre.pack(pady=10)

        entry_apellido = ctk.CTkEntry(top, placeholder_text="Apellido")
        entry_apellido.insert(0, apellido)
        entry_apellido.pack(pady=10)

        entry_dni = ctk.CTkEntry(top, placeholder_text="DNI")
        entry_dni.insert(0, dni)
        entry_dni.pack(pady=10)

        entry_cargo = ctk.CTkEntry(top, placeholder_text="Cargo")
        entry_cargo.insert(0, cargo)
        entry_cargo.pack(pady=10)

        ctk.CTkButton(top, text="Guardar Cambios", command=guardar_edicion).pack(pady=20)

    btn_frame = ctk.CTkFrame(app, fg_color="transparent")
    btn_frame.pack(pady=10)

    ctk.CTkButton(btn_frame, text="Actualizar Lista", command=cargar_datos).pack(side="left", padx=10)
    ctk.CTkButton(btn_frame, text="Editar", command=editar_empleado).pack(side="left", padx=10)
    ctk.CTkButton(btn_frame, text="Eliminar", command=eliminar_empleado, fg_color="red").pack(side="left", padx=10)

    cargar_datos()
