"""
Demostración de polimorfismo con figuras geométricas.

Este módulo muestra cómo diferentes tipos de figuras pueden ser
tratadas de manera uniforme gracias al polimorfismo de Python.
"""

from punto import Punto
from rectangulo import Rectangulo
from cuadrado import Cuadrado
from circulo import Circulo
from elipse import Elipse
from triangulo import Triangulo


def imprimir_propiedades_figura(figura):
    """
    Imprime las propiedades de una figura usando polimorfismo.

    Args:
        figura: Cualquier objeto que tenga métodos perimetro() y area().
    """
    print(f"Figura: {figura}")
    print(f"  Perímetro: {figura.perimetro():.2f}")
    print(f"  Área: {figura.area():.2f}")
    print()


def demo_polimorfismo():
    """
    Demostración de polimorfismo con una lista de diferentes figuras.
    """
    print("=== Demostración de Polimorfismo con Figuras ===\n")

    # Crear diferentes tipos de figuras
    figuras = [
        # Rectángulo de 3x4
        Rectangulo(Punto(0, 0), Punto(3, 4)),
        # Cuadrado de lado 5
        Cuadrado(Punto(1, 1), 5),
        # Círculo de radio 3
        Circulo(Punto(2, 2), 3),
        # Elipse con radios 4 y 2
        Elipse(Punto(0, 0), 4, 2),
        # Triángulo rectángulo
        Triangulo(Punto(0, 0), Punto(3, 0), Punto(0, 4)),
        # Triángulo equilátero aproximado
        Triangulo(Punto(0, 0), Punto(2, 0), Punto(1, 1.732)),  # altura ≈ √3
    ]

    # Demostrar polimorfismo: mismo código funciona para todas las figuras
    total_perimetro = 0
    total_area = 0

    for i, figura in enumerate(figuras, 1):
        print(f"--- Figura {i} ---")
        imprimir_propiedades_figura(figura)

        # Acumular totales
        total_perimetro += figura.perimetro()
        total_area += figura.area()

    # Mostrar totales
    print("=" * 50)
    print(f"Total de figuras: {len(figuras)}")
    print(f"Perímetro total: {total_perimetro:.2f}")
    print(f"Área total: {total_area:.2f}")


def demo_herencia():
    """
    Demostración de relaciones de herencia.
    """
    print("\n=== Demostración de Herencia ===\n")

    # Crear instancias
    rectangulo = Rectangulo(Punto(0, 0), Punto(4, 3))
    cuadrado = Cuadrado(Punto(0, 0), 4)
    elipse = Elipse(Punto(0, 0), 3, 2)
    circulo = Circulo(Punto(0, 0), 3)

    print("Relaciones de herencia:")
    print(f"¿Cuadrado es instancia de Rectángulo? "
          f"{isinstance(cuadrado, Rectangulo)}")
    print(f"¿Círculo es instancia de Elipse? "
          f"{isinstance(circulo, Elipse)}")
    print(f"¿Rectángulo es instancia de Cuadrado? "
          f"{isinstance(rectangulo, Cuadrado)}")
    print()

    # Mostrar jerarquías de clases
    print("Jerarquías de clases:")
    print(f"Cuadrado MRO: "
          f"{[cls.__name__ for cls in Cuadrado.__mro__]}")
    print(f"Círculo MRO: "
          f"{[cls.__name__ for cls in Circulo.__mro__]}")


def demo_casos_especiales():
    """
    Demostración de casos especiales y validaciones.
    """
    print("\n=== Casos Especiales ===\n")

    # Figuras con valores por defecto
    print("Figuras con valores por defecto:")
    figuras_default = [
        Rectangulo(), Cuadrado(), Circulo(), Elipse(), Triangulo()
    ]

    for figura in figuras_default:
        print(f"{figura} -> Área: {figura.area():.2f}")

    print()

    # Casos límite
    print("Casos límite:")

    # Triángulo degenerado (área = 0)
    triangulo_degenerado = Triangulo(Punto(0, 0), Punto(1, 0), Punto(2, 0))
    print(f"Triángulo degenerado: {triangulo_degenerado}")
    print(f"Área: {triangulo_degenerado.area():.2f}")

    # Círculo muy pequeño
    circulo_pequeno = Circulo(Punto(0, 0), 0.001)
    print(f"Círculo pequeño: {circulo_pequeno}")
    print(f"Área: {circulo_pequeno.area():.6f}")


if __name__ == "__main__":
    demo_polimorfismo()
    demo_herencia()
    demo_casos_especiales()
