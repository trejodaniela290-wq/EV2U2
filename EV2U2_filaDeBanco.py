from collections import deque
from datetime import datetime
"""
Simulación de Fila de Banco
Estructuras utilizadas: Cola, Pila y Búsqueda Binaria
Hecho por Roman Medina, Daniela Trejo e Ivan Quezada
"""
# Clase para el cliente que llega
class Cliente:
    def __init__(self, nombre, numero_cuenta):
        self.nombre = nombre
        self.numero_cuenta = numero_cuenta
        self.hora_llegada = datetime.now().strftime("%H:%M")
    #Para registrar la hora actual solo intenté con el mismo metodo strftime de C++ y funcionó
    #Los formatos de hora/minuto los saque de https://www.w3schools.com/python/gloss_python_date_format_codes.asp#gsc.tab=0
    def __str__(self):
        return f"{self.nombre} | Cuenta: {self.numero_cuenta} | Llegó: {self.hora_llegada}"


# Cola del banco para el orden de atención de los clientes
class ColaBanco:
    def __init__(self):
        self._cola = deque()

    def agregar(self, cliente):
        self._cola.append(cliente)

    def atender(self):
        return self._cola.popleft() if self._cola else None # Retorna None si la cola está vacía

    def esta_vacia(self):
        return len(self._cola) == 0

    def lista_clientes(self):
        return list(self._cola)

    def __len__(self):
        return len(self._cola)


# Pila para almacenar movimientos y poder deshacerlos
class PilaBanco:
    def __init__(self):
        self._pila = []

    def registrar(self, tipo_accion, cliente):
        self._pila.append((tipo_accion, cliente))

    def deshacer(self):
        return self._pila.pop() if self._pila else None # Retorna None si no hay movimientos para deshacer

    def esta_vacia(self):
        return len(self._pila) == 0


# Búsqueda binaria sobre una lista de clientes ordenada por nombre
def busqueda_binaria(clientes_ordenados, nombre_cliente):
    """
    Precondición: la lista debe estar ordenada alfabéticamente por nombre.
    Retorna el índice del cliente si se encuentra, -1 si no existe.
    """
    nombre_cliente = nombre_cliente.lower()
    izquierda, derecha = 0, len(clientes_ordenados) - 1

    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2
        nombre_actual = clientes_ordenados[medio].nombre.lower()

        if nombre_actual == nombre_cliente:
            return medio
        elif nombre_actual < nombre_cliente:
            izquierda = medio + 1
        else:
            derecha = medio - 1

    return -1


# Sistema principal que integra las tres cosas (cola, pila y búsqueda)
class SistemaBanco:
    def __init__(self):
        self.cola = ColaBanco()
        self.historial = PilaBanco()

    def agregar_cliente(self, nombre, numero_cuenta):
        cliente = Cliente(nombre, numero_cuenta)
        self.cola.agregar(cliente)
        self.historial.registrar("agregar", cliente)
        print(f"  Cliente agregado: {cliente}")

    def atender_cliente(self):
        cliente = self.cola.atender()
        if cliente:
            self.historial.registrar("atender", cliente)
            print(f"  Atendiendo a: {cliente}")
        else:
            print("  La fila está vacía.")

    def deshacer_accion(self):
        resultado = self.historial.deshacer()
        if resultado is None:
            print("  No hay acciones que deshacer.")
            return

        tipo, cliente = resultado

        if tipo == "agregar":
            # Reconstruir la cola sin ese cliente
            clientes_actuales = self.cola.lista_clientes()
            if cliente in clientes_actuales:
                clientes_actuales.remove(cliente)
                self.cola = ColaBanco()
                for c in clientes_actuales:
                    self.cola.agregar(c)
                print(f"  Deshecho: se eliminó a {cliente.nombre} de la fila.")
            else:
                print(f"  El cliente {cliente.nombre} ya fue atendido; no se puede revertir el ingreso.")

        elif tipo == "atender":
            # Volver a insertar al cliente al frente
            nueva_cola = ColaBanco()
            nueva_cola.agregar(cliente)
            for c in self.cola.lista_clientes():
                nueva_cola.agregar(c)
            self.cola = nueva_cola
            print(f"  Deshecho: {cliente.nombre} regresó al frente de la fila.")

    def buscar_cliente(self, nombre):
        clientes = self.cola.lista_clientes()
        if not clientes:
            print("  La fila está vacía.")
            return

        # Ordenar copia por nombre para aplicar búsqueda binaria
        clientes_ordenados = sorted(clientes, key=lambda c: c.nombre.lower())
        indice = busqueda_binaria(clientes_ordenados, nombre)

        if indice != -1:
            print(f"  Cliente encontrado: {clientes_ordenados[indice]}")
        else:
            print(f"  No se encontró ningún cliente con el nombre '{nombre}'.")

    def mostrar_fila(self):
        clientes = self.cola.lista_clientes()
        if not clientes:
            print("  La fila está vacía.")
        else:
            print(f"  Fila actual ({len(clientes)} cliente(s)):")
            for i, c in enumerate(clientes, 1):
                print(f"    {i}. {c}")


# Menú de texto para interactuar con el sistema
def menu():
    sistema = SistemaBanco()
    opciones = {
        "1": "Agregar cliente",
        "2": "Atender cliente",
        "3": "Deshacer última acción",
        "4": "Buscar cliente por nombre",
        "5": "Ver fila actual",
        "6": "Salir",
    }

    while True:
        print("\nSistema de Fila de Banco")
        for clave, descripcion in opciones.items():
            print(f"  {clave}. {descripcion}")

        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            nombre = input("  Nombre del cliente: ").strip()
            cuenta = input("  Número de cuenta: ").strip()
            if nombre and cuenta:
                sistema.agregar_cliente(nombre, cuenta)
            else:
                print("  Nombre y número de cuenta son obligatorios.")

        elif opcion == "2":
            sistema.atender_cliente()

        elif opcion == "3":
            sistema.deshacer_accion()

        elif opcion == "4":
            nombre = input("  Nombre a buscar: ").strip()
            sistema.buscar_cliente(nombre)

        elif opcion == "5":
            sistema.mostrar_fila()

        elif opcion == "6":
            print("Cerrando el sistema. ¡Hasta luego!")
            break

        else:
            print("  Opción no válida. Intenta de nuevo.")


if __name__ == "__main__":
    menu()