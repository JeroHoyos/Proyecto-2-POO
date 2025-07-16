import re #Más expresiones regulares
from enums import TipoSilla

class Silla:
    def __init__(self, tipo: TipoSilla, id_silla: int, esta_reservada: bool = False):
        self.tipo = tipo
        self.id_silla = id_silla
        self.esta_reservada = esta_reservada

    def to_string(self) -> str:
        return f"{self.id_silla}:{self.tipo.value}:{self.esta_reservada}"

    @staticmethod
    def from_string(data_string):
        parts = data_string.split(':')
        if len(parts) != 3:
            parts = re.split(r'\s+', data_string.strip())
            if len(parts) != 3:
                raise ValueError(f"Formato de línea de silla incorrecto: {data_string}")
        
        id_silla = int(parts[0])
        tipo_silla = TipoSilla(parts[1])
        esta_reservada = parts[2].lower() == 'true'
        return Silla(tipo_silla, id_silla, esta_reservada)