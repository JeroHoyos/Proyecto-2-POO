import re
from enums import TipoSilla

class Silla:
    """Representa una silla individual en un vuelo."""
    def __init__(self, tipo: TipoSilla, id_silla: int, esta_reservada: bool = False):
        self.tipo = tipo
        self.id_silla = id_silla
        self.esta_reservada = esta_reservada

    def to_string(self) -> str:
        """Convierte el objeto Silla a una cadena para serialización TXT."""
        return f"{self.id_silla}:{self.tipo.value}:{self.esta_reservada}"

    @staticmethod
    def from_string(data_string: str):
        """
        Crea un objeto Silla a partir de una cadena TXT.
        Maneja formatos con ':' o espacios para compatibilidad con datos existentes.
        """
        parts = data_string.split(':')
        if len(parts) != 3:
            # Si no está separado por dos puntos, intenta separar por espacios
            parts = re.split(r'\s+', data_string.strip())
            if len(parts) != 3:
                raise ValueError(f"Formato de línea de silla incorrecto: {data_string}")
        
        id_silla = int(parts[0])
        tipo_silla = TipoSilla(parts[1])
        esta_reservada = parts[2].lower() == 'true'
        return Silla(tipo_silla, id_silla, esta_reservada)