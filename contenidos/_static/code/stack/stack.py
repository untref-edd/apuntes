"""
Módulo Stack - Implementación de Pila (LIFO)

Este módulo proporciona una implementación de la estructura de datos pila
(stack)
utilizando el principio LIFO (Last In, First Out - Último en entrar, primero
en salir).

La pila es una estructura de datos lineal que permite insertar y eliminar
elementos
únicamente desde un extremo llamado "cima" o "tope".

Ejemplo de uso:
    >>> from stack import Stack
    >>> pila = Stack()
    >>> pila.push(10)
    >>> pila.push(20)
    >>> print(pila.peek())  # 20
    >>> print(pila.pop())   # 20
    >>> print(pila.size())  # 1

Clases:
    Stack: Implementación de pila usando lista interna de Python.
"""

from stack_exception import StackException


class Stack:
    """
    Clase Stack - Implementación de una pila (stack) usando lista interna.

    Una pila es una estructura de datos que sigue el principio LIFO
    (Last In, First Out). Los elementos se agregan y eliminan desde
    la misma posición llamada "cima" o "tope".

    Atributos:
        _items (list): Lista interna que almacena los elementos de la pila.
                      Se usa convención de nombre privado con underscore.

    Operaciones principales:
        - push: Agregar elemento a la cima
        - pop: Eliminar y retornar elemento de la cima
        - peek/top: Ver elemento de la cima sin eliminarlo
        - is_empty: Verificar si está vacía
        - size: Obtener número de elementos

    Complejidad temporal:
        - Todas las operaciones son O(1) - tiempo constante

    Ejemplo:
        >>> stack = Stack()
        >>> stack.push(1)
        >>> stack.push(2)
        >>> stack.push(3)
        >>> print(stack.pop())  # 3
        >>> print(stack.peek()) # 2
    """

    def __init__(self):
        """
        Inicializa una pila vacía.

        Crea una nueva instancia de Stack con una lista interna vacía
        para almacenar los elementos.

        Complejidad temporal: O(1)
        Complejidad espacial: O(1)

        Ejemplo:
            >>> stack = Stack()
            >>> print(stack.is_empty())  # True
            >>> print(stack.size())      # 0
        """
        self._items = []

    def push(self, item):
        """
        Agrega un elemento a la cima de la pila.

        Inserta el elemento dado en la posición superior de la pila.
        Esta operación siempre es exitosa y no tiene restricciones
        de capacidad (limitada solo por la memoria disponible).

        Args:
            item: El elemento a agregar a la pila. Puede ser de cualquier tipo.

        Returns:
            None

        Complejidad temporal: O(1)
        Complejidad espacial: O(1)

        Ejemplo:
            >>> stack = Stack()
            >>> stack.push(10)
            >>> stack.push("texto")
            >>> stack.push([1, 2, 3])
            >>> print(stack.size())  # 3
        """
        self._items.append(item)

    def pop(self):
        """
        Elimina y retorna el elemento de la cima de la pila.

        Remueve el elemento que está en la posición superior de la pila
        y lo retorna. La pila se reduce en un elemento.

        Returns:
            El elemento que estaba en la cima de la pila.

        Raises:
            StackException: Si se intenta hacer pop en una pila vacía.

        Complejidad temporal: O(1)
        Complejidad espacial: O(1)

        Ejemplo:
            >>> stack = Stack()
            >>> stack.push(10)
            >>> stack.push(20)
            >>> elemento = stack.pop()
            >>> print(elemento)      # 20
            >>> print(stack.size())  # 1

            # Caso de error:
            >>> stack_vacia = Stack()
            >>> stack_vacia.pop()    # Lanza StackException
        """
        if self.is_empty():
            raise StackException("pop from empty stack")
        return self._items.pop()

    def peek(self):
        """
        Retorna el elemento de la cima sin eliminarlo.

        Permite ver el elemento que está en la posición superior
        de la pila sin modificar la estructura. También conocido
        como operación 'top'.

        Returns:
            El elemento que está en la cima de la pila.

        Raises:
            StackException: Si se intenta hacer peek en una pila vacía.

        Complejidad temporal: O(1)
        Complejidad espacial: O(1)

        Ejemplo:
            >>> stack = Stack()
            >>> stack.push(10)
            >>> stack.push(20)
            >>> elemento = stack.peek()
            >>> print(elemento)      # 20
            >>> print(stack.size())  # 2 (no se eliminó)

            # Caso de error:
            >>> stack_vacia = Stack()
            >>> stack_vacia.peek()   # Lanza StackException
        """
        if self.is_empty():
            raise StackException("peek from empty stack")
        return self._items[-1]

    def is_empty(self):
        """
        Verifica si la pila está vacía.

        Determina si la pila no contiene ningún elemento.
        Es útil para validar antes de realizar operaciones
        que requieren elementos (como pop o peek).

        Returns:
            bool: True si la pila está vacía, False en caso contrario.

        Complejidad temporal: O(1)
        Complejidad espacial: O(1)

        Ejemplo:
            >>> stack = Stack()
            >>> print(stack.is_empty())  # True
            >>> stack.push(10)
            >>> print(stack.is_empty())  # False
            >>> stack.pop()
            >>> print(stack.is_empty())  # True
        """
        return len(self._items) == 0

    def size(self):
        """
        Retorna el número de elementos en la pila.

        Obtiene la cantidad actual de elementos almacenados
        en la pila. Es útil para conocer el estado de la
        estructura de datos.

        Returns:
            int: Número de elementos en la pila (>= 0).

        Complejidad temporal: O(1)
        Complejidad espacial: O(1)

        Ejemplo:
            >>> stack = Stack()
            >>> print(stack.size())  # 0
            >>> stack.push(10)
            >>> stack.push(20)
            >>> print(stack.size())  # 2
            >>> stack.pop()
            >>> print(stack.size())  # 1
        """
        return len(self._items)

    def __str__(self):
        """
        Representación en string de la pila.

        Proporciona una representación legible de la pila
        mostrando los elementos desde la base hasta la cima.

        Returns:
            str: Representación en cadena de la pila.

        Ejemplo:
            >>> stack = Stack()
            >>> stack.push(1)
            >>> stack.push(2)
            >>> stack.push(3)
            >>> print(stack)  # Stack: [1, 2, 3] (cima: 3)
        """
        if self.is_empty():
            return "Stack: [] (vacía)"
        return f"Stack: {self._items} (cima: {self._items[-1]})"

    def __repr__(self):
        """
        Representación técnica de la pila.

        Proporciona una representación que puede usarse
        para recrear el objeto.

        Returns:
            str: Representación técnica del objeto.
        """
        return f"Stack({self._items})"


def demo_stack():
    """
    Función de demostración del uso de la clase Stack.

    Muestra ejemplos de todas las operaciones disponibles
    y casos de uso típicos de una pila.
    """
    print("=== Demostración de la clase Stack ===\n")

    # Crear pila vacía
    stack = Stack()
    print(f"Pila creada: {stack}")
    print(f"¿Está vacía?: {stack.is_empty()}")
    print(f"Tamaño: {stack.size()}\n")

    # Agregar elementos
    print("Agregando elementos (push):")
    elementos = [10, 20, 30, "Python", [1, 2, 3]]
    for elemento in elementos:
        stack.push(elemento)
        print(f"  Push {elemento} -> {stack}")

    print(f"\nTamaño final: {stack.size()}")
    print(f"Elemento en la cima (peek): {stack.peek()}\n")

    # Eliminar elementos
    print("Eliminando elementos (pop):")
    while not stack.is_empty():
        elemento = stack.pop()
        print(f"  Pop -> {elemento}, pila restante: {stack}")

    print(f"\n¿Está vacía?: {stack.is_empty()}")

    # Demostrar manejo de errores
    print("\n=== Manejo de errores ===")
    try:
        stack.pop()
    except StackException as e:
        print(f"Error al hacer pop en pila vacía: {e}")

    try:
        stack.peek()
    except StackException as e:
        print(f"Error al hacer peek en pila vacía: {e}")


if __name__ == "__main__":
    demo_stack()
