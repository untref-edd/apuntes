#!/usr/bin/env python3
"""
Script de prueba para verificar que los paquetes grafos e ii funcionen correctamente.
"""

print("=" * 60)
print("Prueba de Paquetes - EDD Code")
print("=" * 60)

# Probar paquete grafos
print("\n✅ Probando paquete 'grafos'...")
try:
    from grafos import caminos_minimos
    print("   ✓ Módulo caminos_minimos importado correctamente")
except ImportError as e:
    print(f"   ✗ Error al importar grafos: {e}")

# Probar paquete ii (Inverted Index)
print("\n✅ Probando paquete 'ii' (Inverted Index)...")
try:
    from ii import BSBI
    print("   ✓ Clase BSBI importada correctamente")
    
    # Crear instancia de BSBI
    bsbi = BSBI(tamaño_bloque=100)
    print(f"   ✓ Instancia BSBI creada con tamaño_bloque={bsbi.tamaño_bloque}")
    
    # Probar tokenización
    texto = "Este es un texto de prueba para el índice invertido"
    tokens = bsbi.tokenizar(texto)
    print(f"   ✓ Tokenización funciona: {len(tokens)} tokens extraídos")
    print(f"     Ejemplo de tokens: {tokens[:5]}")
    
    # Probar parseo de documento
    pares = bsbi.parse_documento(1, texto)
    print(f"   ✓ Parseo de documento funciona: {len(pares)} pares (término, doc_id)")
    
except ImportError as e:
    print(f"   ✗ Error al importar ii: {e}")
except Exception as e:
    print(f"   ✗ Error durante la prueba: {e}")

print("\n" + "=" * 60)
print("Pruebas completadas ✓")
print("=" * 60)
