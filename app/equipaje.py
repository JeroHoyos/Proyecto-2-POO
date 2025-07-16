from enums import TipoEquipaje

class Equipaje:
    def __init__(self, tipo, peso):
        self.tipo = tipo
        self.peso = peso
        self.costo = 0.0

    def to_string(self):
        return f"{self.tipo.value}:{self.peso}:{self.costo}"

    @staticmethod
    def from_string(data_string):
        parts = data_string.split(':')

        if len(parts) != 3:
            raise ValueError(f"Formato de línea de equipaje incorrecto: {data_string}")
        
        tipo_equipaje = TipoEquipaje(parts[0])
        peso = float(parts[1])
        costo = float(parts[2])
        equipaje = Equipaje(tipo_equipaje, peso)
        equipaje.costo = costo
        return equipaje
