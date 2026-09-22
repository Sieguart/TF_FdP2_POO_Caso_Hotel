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

# Para guardar en git
git add .
git status
git commit -m "Mensaje"
git pudh