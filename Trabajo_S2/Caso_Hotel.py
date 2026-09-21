#Inicio

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