from usuario import Usuario

class Cliente(Usuario):
    """Representa a un cliente del sistema de reservas de vuelos."""
    def __init__(self, nombre, correo, documento, contrasena, millas=0, reservas_ids_str=""):
        super().__init__(nombre, correo, documento, contrasena, millas, reservas_ids_str)

    def ver_menu(self):
        """Retorna el título del menú específico para el cliente."""
        return "Menú del Cliente"