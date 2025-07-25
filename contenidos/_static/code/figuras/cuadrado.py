"""
Módulo Cuadrado - Representación de cuadrados en el plano.
"""

from punto import Punto
from rectangulo import Rectangulo


class Cuadrado(Rectangulo):
    """
    Representa un cuadrado, que es un rectángulo con todos los lados iguales.
    
    Hereda de Rectángulo y asegura que el ancho y alto sean iguales.
    
    Atributos:
        p1 (Punto): Esquina inferior izquierda del cuadrado.
        p2 (Punto): Esquina superior derecha del cuadrado.
    """
    
    def __init__(self, p1=None, lado=1.0):
        """
        Inicializa un cuadrado con un punto base y el tamaño del lado.
        
        Args:
            p1 (Punto): Punto de la esquina inferior izquierda. Por defecto origen.
            lado (float): Longitud del lado del cuadrado. Por defecto 1.0.
        """
        p1 = p1 if p1 is not None else Punto()
        p2 = Punto(p1.x + lado, p1.y + lado)
        super().__init__(p1, p2)
    
    def lado(self):
        """
        Obtiene la longitud del lado del cuadrado.
        
        Returns:
            float: La longitud del lado.
        """
        return self.ancho()  # En un cuadrado, ancho = alto
    
    def __str__(self):
        """Representación en string del cuadrado."""
        return f"Cuadrado({self.p1}, lado={self.lado()})"
    
    def __repr__(self):
        """Representación técnica del cuadrado."""
        return f"Cuadrado(p1={self.p1!r}, lado={self.lado()})"