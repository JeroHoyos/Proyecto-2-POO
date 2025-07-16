from abc import ABC, abstractmethod

class Usuario(ABC):
    def __init__(self, nombre: str, correo: str, documento: str, contrasena: str, millas: int = 0, reservas_ids_str: str = ""):
        self.nombre = nombre
        self.correo = correo
        self.documento = documento
        self.contrasena = contrasena
        self.millas = millas
        self.reservas_ids = [int(x) for x in reservas_ids_str.split(',') if x] if reservas_ids_str else []
        self.reservas = []

    def cambiar_contrasena(self, nueva):
        self.contrasena = nueva

    @abstractmethod
    def ver_menu(self):
        pass

    def to_string(self):
        reservas_ids_str = ",".join(map(str, self.reservas_ids))
        return f"{self.__class__.__name__}|{self.nombre}|{self.correo}|{self.documento}|{self.contrasena}|{self.millas}|{reservas_ids_str}"

    @staticmethod
    def from_string(data_string):
        from cliente import Cliente
        from administrador import Administrador

        parts = data_string.split('|')
        if len(parts) < 7:
            raise ValueError(f"Formato de línea de usuario incorrecto: {data_string}.")
        
        tipo, nombre, correo, documento, contrasena, millas_str, reservas_ids_str = parts[0], parts[1], parts[2], parts[3], parts[4], parts[5], parts[6]
        
        try:
            millas = int(millas_str)
        except ValueError:
            raise ValueError(f"El valor de millas no es un número entero en la línea: {data_string}")

        if tipo == 'Cliente':
            return Cliente(nombre, correo, documento, contrasena, millas, reservas_ids_str)
        elif tipo == 'Administrador':
            return Administrador(nombre, correo, documento, contrasena, millas, reservas_ids_str)
        else:
            raise ValueError(f"Tipo de usuario desconocido: {tipo}")
            
    def consultar_vuelos_vendidos(self, sistema):
        """Consulta los vuelos que tienen reservas asociadas a este usuario."""
        return [r for r in self.reservas if r.vuelo is not None]

    def consultar_datos_pasajeros(self, sistema):
        """Consulta los datos de los pasajeros asociados a las reservas de este usuario."""
        pasajeros_por_reserva = []
        for reserva in self.reservas:
            pasajeros_nombres = [p.nombre for p in reserva.pasajeros]
            if pasajeros_nombres:
                pasajeros_por_reserva.append((reserva.id_reserva, pasajeros_nombres))
        return pasajeros_por_reserva