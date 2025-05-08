def validar_admin(usuario, contrasena):
    ADMIN_USER = "admin"
    ADMIN_PASS = "admin123"
    return usuario == ADMIN_USER and contrasena == ADMIN_PASS


# este codigo es para puebras independientes (es opcional equisde) 
# psdt: este codigo es para pobrar en la terminal, by: john
# para las pruebas poner esto en terminal "$ python LoginAdmin.py"
if __name__ == "__main__":
    user = input("Usuario: ")
    pwd = input("Contraseña: ")
    if validar_admin(user, pwd):
        print("Acceso concedido.")
    else:
        print("Contraseña incorrecta.")
