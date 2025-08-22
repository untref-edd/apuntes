"""
Agenda persistente usando shelve y pickle.

Permite agregar, buscar y eliminar contactos con múltiples teléfonos y correos.
"""

import shelve
import pickle


class Contacto:
    """
    Representa un contacto de la agenda.

    Atributos:
        nombre (str)
        apellido (str)
        correos (list[str])
        telefonos (list[str])
    """
    def __init__(self, nombre, apellido, correos=None, telefonos=None):
        self.nombre = nombre
        self.apellido = apellido
        self.correos = correos if correos else []
        self.telefonos = telefonos if telefonos else []

    def __str__(self):
        return (f"{self.nombre} {self.apellido}\n"
                f"  Correos: {', '.join(self.correos)}\n"
                f"  Teléfonos: {', '.join(self.telefonos)}")


def agregar_contacto(agenda, contacto):
    """Agrega un contacto a la agenda usando nombre+apellido como clave."""
    clave = f"{contacto.nombre.lower()}_{contacto.apellido.lower()}"
    agenda[clave] = pickle.dumps(contacto)
    print("Contacto agregado.")


def buscar_contacto(agenda, nombre, apellido):
    """Busca un contacto por nombre y apellido."""
    clave = f"{nombre.lower()}_{apellido.lower()}"
    if clave in agenda:
        contacto = pickle.loads(agenda[clave])
        print(contacto)
    else:
        print("Contacto no encontrado.")


def eliminar_contacto(agenda, nombre, apellido):
    """Elimina un contacto por nombre y apellido."""
    clave = f"{nombre.lower()}_{apellido.lower()}"
    if clave in agenda:
        del agenda[clave]
        print("Contacto eliminado.")
    else:
        print("Contacto no encontrado.")


def listar_agenda(agenda):
    """Muestra todos los contactos de la agenda."""
    if not agenda:
        print("Agenda vacía.")
        return
    for clave in agenda:
        contacto = pickle.loads(agenda[clave])
        print(contacto)
        print("-" * 30)


def menu():
    """
    Muestra el menú principal de la agenda.
    """
    with shelve.open("agenda_db") as agenda:
        while True:
            print("\n--- Agenda ---")
            print("1. Agregar contacto")
            print("2. Buscar contacto")
            print("3. Eliminar contacto")
            print("4. Listar agenda")
            print("0. Salir")
            opcion = input("Opción: ")
            if opcion == "1":
                nombre = input("Nombre: ")
                apellido = input("Apellido: ")
                correos = input("Correos (separados por coma): ").split(",")
                telefonos = input("Teléfonos (separados por coma): ").split(",")
                contacto = Contacto(nombre, apellido,
                                    [c.strip() for c in correos if c.strip()],
                                    [t.strip() for t in telefonos if t.strip()])
                agregar_contacto(agenda, contacto)
            elif opcion == "2":
                nombre = input("Nombre: ")
                apellido = input("Apellido: ")
                buscar_contacto(agenda, nombre, apellido)
            elif opcion == "3":
                nombre = input("Nombre: ")
                apellido = input("Apellido: ")
                eliminar_contacto(agenda, nombre, apellido)
            elif opcion == "4":
                listar_agenda(agenda)
            elif opcion == "0":
                print("Saliendo...")
                break
            else:
                print("Opción inválida.")


if __name__ == "__main__":
    menu()
