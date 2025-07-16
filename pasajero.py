class Pasajero:
    """Representa un pasajero con su nombre y documento."""
    def __init__(self, nombre: str, documento: str):
        self.nombre = nombre
        self.documento = documento

    def to_string(self) -> str:
        """Convierte el objeto Pasajero a una cadena para serialización."""
        return f"{self.nombre}:{self.documento}"

    @staticmethod
    def from_string(data_string: str):
        """Crea un objeto Pasajero a partir de una cadena."""
        parts = data_string.split(':')
        if len(parts) != 2:
            raise ValueError(f"Formato de línea de pasajero incorrecto: {data_string}")
        return Pasajero(parts[0], parts[1])