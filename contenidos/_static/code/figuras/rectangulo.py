"""
Módulo Rectángulo - Representación de rectángulos en el plano.
"""

from punto import Punto


class Rectangulo:
    """
    Representa un rectángulo definido por dos puntos diagonalmente opuestos.

    Atributos:
        p1 (Punto): Primer punto (esquina inferior izquierda).
        p2 (Punto): Segundo punto (esquina superior derecha).
    """

    def __init__(self, p1=None, p2=None):
        """
        Inicializa un rectángulo con dos puntos.

        Args:
            p1 (Punto): Primer punto. Por defecto en el origen.
            p2 (Punto): Segundo punto. Por defecto en (1, 1).
        """
        self.p1 = p1 if p1 is not None else Punto()
        self.p2 = p2 if p2 is not None else Punto(1, 1)

    def ancho(self):
        """
        Calcula el ancho del rectángulo.

        Returns:
            float: El ancho del rectángulo.
        """
        return abs(self.p2.x - self.p1.x)

    def alto(self):
        """
        Calcula la altura del rectángulo.

        Returns:
            float: La altura del rectángulo.
        """
        return abs(self.p2.y - self.p1.y)

    def perimetro(self):
        """
        Calcula el perímetro del rectángulo.

        Returns:
            float: El perímetro del rectángulo.
        """
        return 2 * (self.ancho() + self.alto())

    def area(self):
        """
        Calcula el área del rectángulo.

        Returns:
            float: El área del rectángulo.
        """
        return self.ancho() * self.alto()

    def __str__(self):
        """Representación en string del rectángulo."""
        return f"Rectangulo({self.p1}, {self.p2})"

    def __repr__(self):
        """Representación técnica del rectángulo."""
        return f"Rectangulo(p1={self.p1!r}, p2={self.p2!r})"
