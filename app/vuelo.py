import re #Esto es para manejar expresiones regulares
from silla import Silla
from enums import TipoSilla

class Vuelo:
    def __init__(self, codigo: str, ciudad_origen: str, ciudad_destino: str, dia: str, horario: str, cant_preferencial: int = 0, cant_economica: int = 0, sillas_str_data: str = ""):
        self.codigo = codigo
        self.ciudad_origen = ciudad_origen
        self.ciudad_destino = ciudad_destino
        self.dia = dia
        self.horario = horario
        self.sillas: list[Silla] = []
        self.silla_id_counter = 0

        if sillas_str_data:
            sillas_parts = sillas_str_data.split(';')
            for s_str in sillas_parts:
                if s_str: 
                    silla = Silla.from_string(s_str)
                    self.sillas.append(silla)
                    if silla.id_silla >= self.silla_id_counter:
                        self.silla_id_counter = silla.id_silla + 1
        else:
            for _ in range(cant_preferencial):
                self.sillas.append(Silla(TipoSilla.PREFERENCIAL, self.silla_id_counter))
                self.silla_id_counter += 1
            for _ in range(cant_economica):
                self.sillas.append(Silla(TipoSilla.ECONOMICA, self.silla_id_counter))
                self.silla_id_counter += 1

    def obtener_disponibilidad(self):
        disponibilidad = {
            TipoSilla.PREFERENCIAL.value: 0,
            TipoSilla.ECONOMICA.value: 0
        }
        for silla in self.sillas:
            if not silla.esta_reservada:
                disponibilidad[silla.tipo.value] += 1
        return disponibilidad

    def asignar_silla(self, tipo_silla: TipoSilla):
        for silla in self.sillas:
            if not silla.esta_reservada and silla.tipo == tipo_silla:
                silla.esta_reservada = True
                return silla
        return None

    def reservar_silla(self, tipo_silla):
        return self.asignar_silla(tipo_silla)

    def liberar_silla(self, id_silla: int) -> bool:
        for silla in self.sillas:
            if silla.id_silla == id_silla:
                silla.esta_reservada = False
                return True
        return False

    def to_string(self):
        sillas_str = ";".join([s.to_string() for s in self.sillas])
        return f"{self.codigo}:{self.ciudad_origen}:{self.ciudad_destino}:{self.dia}:{self.horario}:{sillas_str}"

    @staticmethod
    def from_string(data_string):
        match = re.match(r'^([^:]+):([^:]+):([^:]+):([^:]+):(\d{1,2}:\d{2}):(.*)$', data_string)
        if not match:
            raise ValueError(f"Formato de línea de vuelo persistente incorrecto: {data_string}. No coincide con el patrón esperado.")
        
        codigo, origen, destino, dia, horario, sillas_str_data = match.groups()

        return Vuelo(codigo, origen, destino, dia, horario, sillas_str_data=sillas_str_data)

    @staticmethod
    def from_txt_line(data_string):
        match = re.match(r'(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\d{1,2}:\d{2})\s+(\S+)\s+(\S+)', data_string.strip())
        if not match:
            raise ValueError(f"Formato de línea de vuelos.txt incorrecto: {data_string}. No coincide con el patrón esperado.")
        
        codigo, origen, destino, dia, horario, cant_preferencial_str, cant_economica_str = match.groups()

        try:
            cant_preferencial = int(cant_preferencial_str)
            cant_economica = int(cant_economica_str)
        except ValueError:
            raise ValueError(f"Cantidades de sillas no son números en línea: {data_string}")

        return Vuelo(codigo, origen, destino, dia, horario, cant_preferencial, cant_economica)

    def __str__(self) -> str:
        disp = self.obtener_disponibilidad()
        return (f"Vuelo {self.codigo} de {self.ciudad_origen} a {self.ciudad_destino} "
                f"el {self.dia} a las {self.horario}. Sillas Preferenciales: {disp[TipoSilla.PREFERENCIAL.value]}, Económicas: {disp[TipoSilla.ECONOMICA.value]}")
