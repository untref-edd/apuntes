"""
Módulo Círculo - Representación de círculos en el plano.
"""

import math
from elipse import Elipse
from punto import Punto


class Circulo(Elipse):
    """
    Representa un círculo, que es una elipse con ambos radios iguales.

    Hereda de Elipse donde radio_a = radio_b = radio.
    """

    def __init__(self, centro=None, radio=1.0):
        """
        Inicializa un círculo.

        Args:
            centro (Punto): Centro del círculo. Por defecto en el origen.
            radio (float): Radio del círculo. Por defecto 1.0.
        """
        centro = centro if centro is not None else Punto()
        super().__init__(centro, radio, radio)
        self.radio = float(radio)

    def perimetro(self):
        """
        Calcula el perímetro (circunferencia) del círculo.

        Returns:
            float: El perímetro del círculo.
        """
        return 2 * math.pi * self.radio

    def area(self):
        """
        Calcula el área del círculo.

        Returns:
            float: El área del círculo.
        """
        return math.pi * self.radio * self.radio

    def __str__(self):
        """Representación en string del círculo."""
        return f"Circulo(centro={self.centro}, radio={self.radio})"
