import pyodbc

def conectar_db():
    """
    Establece conexión con la base de datos SQL Server

    """
    try:
        connection_string = """
            DRIVER={ODBC Driver 17 for SQL Server};
            SERVER=DESKTOP-PVMS4J8;
            DATABASE=UTP_SECURITYFACIAL;
            Trusted_Connection=yes;
        """
        return pyodbc.connect(connection_string)
    except Exception as e:
        print(f"Error de conexión: {str(e)}")
        return None


def validar_usuario(usuario, contrasena):
    """
    Valida las credenciales  en la base de datos

    """
    conn = conectar_db()
    if not conn:
        return False

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios_sistema WHERE usuario = ? AND contrasena = ?",
                       (usuario, contrasena))
        return cursor.fetchone() is not None
    except Exception as e:
        print(f"Error al validar usuario: {str(e)}")
        return False
    finally:
        conn.close()
