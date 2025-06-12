# crud_db.py
import pyodbc
from datetime import datetime

def conectar_bd():
    return pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=LAPTOP-6SOD4TD3\SQLEXPRESS;'
        'DATABASE=UTP_SECURITYFACIAL;'  # <-- cambia esto por el nombre de tu base
        'Trusted_Connection=yes;'
    )

def obtener_personal():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, apellido, dni, cargo, fecha_registro FROM personal")
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def insertar_personal(nombre, apellido, dni, cargo):
    conn = conectar_bd()
    cursor = conn.cursor()
    fecha_actual = datetime.now()
    cursor.execute(
        "INSERT INTO personal (nombre, apellido, dni, cargo, fecha_registro) VALUES (?, ?, ?, ?, ?)",
        (nombre, apellido, dni, cargo, fecha_actual)
    )
    conn.commit()
    conn.close()

def actualizar_personal(id_personal, nombre, apellido, dni, cargo):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE personal SET nombre=?, apellido=?, dni=?, cargo=? WHERE id=?",
        (nombre, apellido, dni, cargo, id_personal)
    )
    conn.commit()
    conn.close()

def eliminar_personal(id_personal):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM personal WHERE id=?", (id_personal,))
    conn.commit()
    conn.close()

def dni_existe(dni):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM personal WHERE dni = ?", (dni,))
    existe = cursor.fetchone()[0] > 0
    conn.close()
    return existe
