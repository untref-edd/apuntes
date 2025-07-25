"""
Módulo Triángulo - Representación de triángulos en el plano.
"""

import math
from punto import Punto


class Triangulo:
    """
    Representa un triángulo definido por tres puntos en el plano.
    
    Atributos:
        p1 (Punto): Primer vértice del triángulo.
        p2 (Punto): Segundo vértice del triángulo.
        p3 (Punto): Tercer vértice del triángulo.
    """
    
    def __init__(self, p1=None, p2=None, p3=None):
        """
        Inicializa un triángulo con tres puntos.
        
        Args:
            p1 (Punto): Primer vértice. Por defecto en el origen.
            p2 (Punto): Segundo vértice. Por defecto en (1, 0).
            p3 (Punto): Tercer vértice. Por defecto en (0, 1).
        """
        self.p1 = p1 if p1 is not None else Punto()
        self.p2 = p2 if p2 is not None else Punto(1, 0)
        self.p3 = p3 if p3 is not None else Punto(0, 1)
    
    def lado_a(self):
        """Distancia entre p2 y p3."""
        return self.p2.distancia_a(self.p3)
    
    def lado_b(self):
        """Distancia entre p1 y p3."""
        return self.p1.distancia_a(self.p3)
    
    def lado_c(self):
        """Distancia entre p1 y p2."""
        return self.p1.distancia_a(self.p2)
    
    def perimetro(self):
        """
        Calcula el perímetro del triángulo.
        
        Returns:
            float: El perímetro del triángulo.
        """
        return self.lado_a() + self.lado_b() + self.lado_c()
    
    def area(self):
        """
        Calcula el área del triángulo usando la fórmula de Herón.
        
        Returns:
            float: El área del triángulo.
        """
        # Usar la fórmula de Herón
        a, b, c = self.lado_a(), self.lado_b(), self.lado_c()
        s = (a + b + c) / 2  # Semi-perímetro
        
        # Evitar errores por precisión de punto flotante
        discriminante = s * (s - a) * (s - b) * (s - c)
        if discriminante < 0:
            return 0.0
        
        return math.sqrt(discriminante)
    
    def __str__(self):
        """Representación en string del triángulo."""
        return f"Triangulo({self.p1}, {self.p2}, {self.p3})"