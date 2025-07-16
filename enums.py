from enum import Enum

class TipoSilla(Enum):
    """Define los tipos de silla disponibles."""
    PREFERENCIAL = "Preferencial"
    ECONOMICA = "Económica"

class TipoEquipaje(Enum):
    """Define los tipos de equipaje."""
    MANO = "Mano"
    CABINA = "Cabina"
    BODEGA = "Bodega"