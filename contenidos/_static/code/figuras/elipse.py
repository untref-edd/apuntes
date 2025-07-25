"""
Módulo Elipse - Representación de elipses en el plano.
"""

import math
from punto import Punto


class Elipse:
    """
    Representa una elipse definida por su centro y dos radios.
    
    Atributos:
        centro (Punto): Centro de la elipse.
        radio_a (float): Radio semi-mayor (eje horizontal).
        radio_b (float): Radio semi-menor (eje vertical).
    """
    
    def __init__(self, centro=None, radio_a=1.0, radio_b=1.0):
        """
        Inicializa una elipse.
        
        Args:
            centro (Punto): Centro de la elipse. Por defecto en el origen.
            radio_a (float): Radio semi-mayor. Por defecto 1.0.
            radio_b (float): Radio semi-menor. Por defecto 1.0.
        """
        self.centro = centro if centro is not None else Punto()
        self.radio_a = float(radio_a)
        self.radio_b = float(radio_b)
    
    def perimetro(self):
        """
        Calcula el perímetro aproximado de la elipse usando la fórmula de Ramanujan.
        
        Returns:
            float: El perímetro aproximado de la elipse.
        """
        a, b = self.radio_a, self.radio_b
        h = ((a - b) ** 2) / ((a + b) ** 2)
        return math.pi * (a + b) * (1 + (3 * h) / (10 + math.sqrt(4 - 3 * h)))
    
    def area(self):
        """
        Calcula el área de la elipse.
        
        Returns:
            float: El área de la elipse.
        """
        return math.pi * self.radio_a * self.radio_b
    
    def __str__(self):
        """Representación en string de la elipse."""
        return f"Elipse(centro={self.centro}, radio_a={self.radio_a}, radio_b={self.radio_b})"