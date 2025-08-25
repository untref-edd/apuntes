"""
Módulo Punto - Representación de puntos en el plano cartesiano.
"""

import math


class Punto:
    """
    Representa un punto en el plano cartesiano con coordenadas (x, y).

    Atributos:
        x (float): Coordenada x del punto.
        y (float): Coordenada y del punto.
    """

    def __init__(self, x=0.0, y=0.0):
        """
        Inicializa un punto en el plano.

        Args:
            x (float): Coordenada x. Por defecto 0.0.
            y (float): Coordenada y. Por defecto 0.0.
        """
        self.x = float(x)
        self.y = float(y)

    def distancia_a(self, otro_punto):
        """
        Calcula la distancia euclidiana a otro punto.

        Args:
            otro_punto (Punto): El otro punto.

        Returns:
            float: La distancia entre los dos puntos.
        """
        dx = self.x - otro_punto.x
        dy = self.y - otro_punto.y
        return math.sqrt(dx * dx + dy * dy)

    def __str__(self):
        """Representación en string del punto."""
        return f"({self.x}, {self.y})"

    def __repr__(self):
        """Representación técnica del punto."""
        return f"Punto({self.x}, {self.y})"
