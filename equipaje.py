from enums import TipoEquipaje

class Equipaje:
    def __init__(self, tipo, peso, volumen):
        self.tipo = tipo
        self.peso = peso
        self.volumen = volumen
        self.costo = 0.0

    def to_string(self) -> str:
        return f"{self.tipo.value}:{self.peso}:{self.volumen}:{self.costo}"

    @staticmethod
    def from_string(data_string):
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