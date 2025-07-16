from equipaje import Equipaje
from enums import TipoEquipaje, TipoSilla

class CheckIn:
    def __init__(self, reserva):
        self.reserva = reserva
        self.equipajes = []
        self.costo_total_equipaje = 0

    def agregar_equipaje(self, equipaje_data):
        self.equipajes.append(equipaje_data)

    def realizar_check_in(self):
        if not self.reserva.checkin_realizado:
            self.reserva.usuario.millas += 500
            
            self.reserva.checkin_realizado = True
            
            self.calcular_costo_total_equipaje()
            self.reserva.precio_total += self.costo_total_equipaje
            
            info = (f"Check-in realizado para reserva {self.reserva.id_reserva} (Vuelo {self.reserva.vuelo.codigo}).\n"
                    f"Millas acumuladas: 500. Total actual de millas: {self.reserva.usuario.millas}.")
            
            if self.costo_total_equipaje > 0:
                info += f"\nCosto total de equipaje adicional: ${self.costo_total_equipaje:,.0f}."
            
            return True, info
        return False, f"Error: El check-in para la reserva {self.reserva.id_reserva} ya ha sido realizado."

    def calcular_costo_total_equipaje(self):
        self.costo_total_equipaje = 0
        maletas_bodega_gratuitas_usadas_por_silla_preferencial_count = {silla.id_silla: 0 for silla in self.reserva.sillas if silla.tipo == TipoSilla.PREFERENCIAL}

        for silla_asociada, equipaje_actual in self.equipajes:
            tipo_silla = silla_asociada.tipo
            
            costo_individual = 0

            if equipaje_actual.tipo == TipoEquipaje.MANO:
                costo_individual = 0 
            
            elif equipaje_actual.tipo == TipoEquipaje.CABINA:
                if tipo_silla == TipoSilla.PREFERENCIAL:
                    costo_individual = 0
                elif tipo_silla == TipoSilla.ECONOMICA:
                    costo_individual = 40000 
            
            elif equipaje_actual.tipo == TipoEquipaje.BODEGA:
                if tipo_silla == TipoSilla.PREFERENCIAL:
                    if maletas_bodega_gratuitas_usadas_por_silla_preferencial_count.get(silla_asociada.id_silla, 0) == 0:
                        costo_individual = 0
                        maletas_bodega_gratuitas_usadas_por_silla_preferencial_count[silla_asociada.id_silla] = 1 
                    else:
                        costo_individual = 50000 + (equipaje_actual.peso * 1000)
                elif tipo_silla == TipoSilla.ECONOMICA:
                    costo_individual = 50000 + (equipaje_actual.peso * 1000)
            
            equipaje_actual.costo = costo_individual
            self.costo_total_equipaje += costo_individual