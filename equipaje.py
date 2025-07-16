from enums import TipoEquipaje

class Equipaje:
    """Representa un equipaje con su tipo, peso, volumen y costo."""
    def __init__(self, tipo: TipoEquipaje, peso: float, volumen: float):
        self.tipo = tipo
        self.peso = peso
        self.volumen = volumen
        self.costo = 0.0

    def to_string(self) -> str:
        """Convierte el objeto Equipaje a una cadena."""
        return f"{self.tipo.value}:{self.peso}:{self.volumen}:{self.costo}"

    @staticmethod
    def from_string(data_string: str):
        """Crea un objeto Equipaje a partir de una cadena."""
        parts = data_string.split(':')
        if len(parts) != 4:
            raise ValueError(f"Formato de línea de equipaje incorrecto: {data_string}")
        
        tipo_equipaje = TipoEquipaje(parts[0])
        peso = float(parts[1])
        volumen = float(parts[2])
        costo = float(parts[3])
        equipaje = Equipaje(tipo_equipaje, peso, volumen)
        equipaje.costo = costo
        return equipaje