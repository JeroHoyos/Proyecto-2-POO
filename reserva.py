import uuid #Esto para generar ID o identificadores de forma comoda xd 
from silla import Silla
from pasajero import Pasajero
from enums import TipoSilla
from vuelo import Vuelo
from usuario import Usuario

class Reserva:
    def __init__(self, id_reserva: int, vuelo: Vuelo, usuario: Usuario, pasajeros: list[Pasajero], sillas: list[Silla], checkin_realizado: bool = False, precio_total: float = 0.0):
        self.id_reserva = id_reserva
        self.vuelo = vuelo
        self.usuario = usuario
        self.pasajeros = pasajeros
        self.sillas = sillas
        self.checkin_realizado = checkin_realizado
        self.precio_total = precio_total

    def to_string(self) -> str:
        pasajeros_str = ",".join([p.to_string() for p in self.pasajeros])
        sillas_str = ";".join([s.to_string() for s in self.sillas])
        return f"{self.id_reserva}|{self.vuelo.codigo}|{self.usuario.documento}|{pasajeros_str}|{sillas_str}|{self.checkin_realizado}|{self.precio_total}"

    @staticmethod
    def from_string(data_string, all_vuelos, all_usuarios):
        parts = data_string.strip().split('|')
        if len(parts) != 7:
            raise ValueError(f"Formato de línea de reserva incorrecto: {data_string}. Se esperaban 7 partes separadas por '|'.")

        id_reserva = int(parts[0])
        vuelo_codigo = parts[1]
        usuario_documento = parts[2]
        pasajeros_data_str = parts[3]
        sillas_data_str = parts[4]
        checkin_realizado = parts[5].lower() == 'true'
        precio_total = float(parts[6])

        vuelo = next((v for v in all_vuelos if v.codigo == vuelo_codigo), None)
        if not vuelo:
            raise ValueError(f"Vuelo con código {vuelo_codigo} no encontrado para la reserva {id_reserva}")

        usuario = next((u for u in all_usuarios if u.documento == usuario_documento), None)
        if not usuario:
            raise ValueError(f"Usuario con documento {usuario_documento} no encontrado para la reserva {id_reserva}")

        pasajeros = [Pasajero.from_string(p_str) for p_str in pasajeros_data_str.split(',')] if pasajeros_data_str else []
        sillas = [Silla.from_string(s_str) for s_str in sillas_data_str.split(';')] if sillas_data_str else []

        return Reserva(id_reserva, vuelo, usuario, pasajeros, sillas, checkin_realizado, precio_total)
