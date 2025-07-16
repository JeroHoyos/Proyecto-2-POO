from usuario import Usuario

class Administrador(Usuario):
    """Representa a un administrador del sistema con funcionalidades extendidas."""
    def __init__(self, nombre, correo, documento, contrasena, millas=0, reservas_ids_str=""):
        super().__init__(nombre, correo, documento, contrasena, millas, reservas_ids_str)

    def ver_menu(self):
        """Retorna el título del menú específico para el administrador."""
        return "Menú del Administrador"