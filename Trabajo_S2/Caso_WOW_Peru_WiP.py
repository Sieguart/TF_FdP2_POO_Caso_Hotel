#Inicio
# -----------------------------------------
# 1. CLASES DE DOMINIO Y DE NEGOCIO
# -----------------------------------------

class Cliente:
    def __init__(self, dni: str, nombre: str, direccion: str, plan_internet: str):
        self._dni = dni
        self._nombre = nombre
        self._direccion = direccion
        self._plan_internet = plan_internet

    @property
    def dni(self) -> str:
        return self._dni

    @property
    def nombre(self) -> str:
        return self._nombre

    def __str__(self) -> str:
        return f"Cliente: {self._nombre} (DNI: {self._dni}) - Plan: {self._plan_internet}"


class Incidencia:
    def __init__(self, codigo: str, cliente: Cliente, descripcion: str):
        self._codigo = codigo
        self._cliente = cliente
        self._descripcion = descripcion
        self._estado = "Pendiente"  # Pendiente / Atendida
        self._tecnico_asignado: Optional['Tecnico'] = None

    @property
    def codigo(self) -> str:
        return self._codigo

    @property
    def estado(self) -> str:
        return self._estado

    def asignar_tecnico(self, tecnico: 'Tecnico'):
        self._tecnico_asignado = tecnico
        self._estado = "Atendida"

    def __str__(self) -> str:
        tec_str = self._tecnico_asignado.nombre if self._tecnico_asignado else "Sin Asignar"
        return f"Ticket: {self._codigo} | Cliente: {self._cliente.nombre} | Estado: {self._estado} | Técnico: {tec_str}"


# ------------------------------------------
# 2. JERARQUÍA DE CLASES: EMPLEADOS
# ------------------------------------------

class Empleado(ABC):
    def __init__(self, dni: str, nombre: str, sueldo_base: float):
        self._dni = dni
        self._nombre = nombre
        self._sueldo_base = sueldo_base

    @property
    def dni(self) -> str:
        return self._dni

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def sueldo_base(self) -> float:
        return self._sueldo_base

    # Reglas de negocio
    def calcular_afp(self) -> float:
        """Descuento del 10% obligatorio de AFP"""
        return self._sueldo_base * 0.10

    def calcular_essalud(self) -> float:
        """Aporte del 8% a EsSalud por parte del empleador"""
        return self._sueldo_base * 0.08

    @abstractmethod
    def calcular_sueldo_neto(self) -> float:
        """Método polimórfico a ser implementado por las subclases"""
        pass


class Tecnico(Empleado):
    def __init__(self, dni: str, nombre: str, sueldo_base: float, especialidad: str):
        super().__init__(dni, nombre, sueldo_base)
        self._especialidad = especialidad
        self._incidencias_resueltas = 0

    @property
    def incidencias_resueltas(self) -> int:
        return self._incidencias_resueltas

    def incrementar_incidencias(self):
        self._incidencias_resueltas += 1

    def calcular_bono(self) -> float:
        # Bono de S/ 50 por cada incidencia resuelta
        return self._incidencias_resueltas * 50.0

    def calcular_sueldo_neto(self) -> float:
        # Sueldo Base + Bono - AFP
        return (self._sueldo_base + self.calcular_bono()) - self.calcular_afp()


class Administrativo(Empleado):
    def __init__(self, dni: str, nombre: str, sueldo_base: float, bono_gestion: float = 200.0):
        super().__init__(dni, nombre, sueldo_base)
        self._bono_gestion = bono_gestion

    def calcular_sueldo_neto(self) -> float:
        # Sueldo Base + Bono de Gestión - AFP
        return (self._sueldo_base + self._bono_gestion) - self.calcular_afp()




























































# Para guardar en git
git add .
git status
git commit -m "Mensaje"
git pudh