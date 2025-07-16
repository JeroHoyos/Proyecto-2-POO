class Pasajero:
    def __init__(self, nombre, documento):
        self.nombre = nombre
        self.documento = documento

    def to_string(self) -> str:
        return f"{self.nombre}:{self.documento}"

    @staticmethod
    def from_string(data_string):
        parts = data_string.split(':')
        if len(parts) != 2:
            raise ValueError(f"Formato de línea de pasajero incorrecto: {data_string}")
        return Pasajero(parts[0], parts[1])