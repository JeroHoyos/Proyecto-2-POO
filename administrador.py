from usuario import Usuario

class Administrador(Usuario):
    def __init__(self, nombre, correo, documento, contrasena, millas=0, reservas_ids_str=""):
        super().__init__(nombre, correo, documento, contrasena, millas, reservas_ids_str)

    def ver_menu(self):
        return "Menú del Administrador"