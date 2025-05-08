def validar_admin(usuario, contrasena):
    ADMIN_USER = "admin"
    ADMIN_PASS = "admin123"
    return usuario == ADMIN_USER and contrasena == ADMIN_PASS


# este codigo es para puebras independientes (es opcional equisde)
if __name__ == "__main__":
    user = input("Usuario: ")
    pwd = input("Contraseña: ")
    if validar_admin(user, pwd):
        print("Acceso concedido.")
    else:
        print("Contraseña incorrecta.")
