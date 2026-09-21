#Inicio
#1
Class Empleado:
    def __init__(self, dni: str, nombre: str, sueldo_base: float):
        self._dni = dni
        self._nombre = nombre
        self._sueldo_base = sueldo_base

    @property
    def dni(self):
        return self._dni

    @property
    def sueldo_base(self):
        return self._sueldo_base

#Reglas
def calcular_afp(self) -> float:
        return self._sueldo_base * 0.10  # 10% AFP

def calcular_essalud(self) -> float:
        return self._sueldo_base * 0.08  # 8% EsSalud

#2
class EmpleadoPlanilla(Empleado):
    def __init__(self, dni: str, nombre: str, sueldo_base: float, asignacion_familiar: float = 102.50):
        super().__init__(dni, nombre, sueldo_base)
        self._asignacion_familiar = asignacion_familiar

    def calcular_sueldo_neto(self) -> float:
        descuentos = self.calcular_afp()
        return self._sueldo_base + self._asignacion_familiar - descuentos


class EmpleadoPorHoras(Empleado):
    def __init__(self, dni: str, nombre: str, horas_trabajadas: int, tarifa_hora: float):
        super().__init__(dni, nombre, horas_trabajadas * tarifa_hora)
        self.horas_trabajadas = horas_trabajadas
        self.tarifa_hora = tarifa_hora

    def calcular_sueldo_neto(self) -> float:
        return self.horas_trabajadas * self.tarifa_hora