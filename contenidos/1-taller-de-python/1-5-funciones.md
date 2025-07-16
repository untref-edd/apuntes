---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
kernelspec:
  display_name: Python 3
  language: python
  name: python3
---
# Funciones en Python y Paradigma Funcional

## Paradigma funcional

En el paradigma funcional, las funciones son ciudadanos de primera clase y se pueden pasar como argumentos a otras funciones, retornar desde otras funciones y asignarse a variables. Esto permite un estilo de programación más declarativo y menos imperativo.

### Características del paradigma funcional

1. **Inmutabilidad**: Los datos son inmutables, lo que significa que no se pueden cambiar una vez creados. En su lugar, se crean nuevas versiones de los datos con los cambios deseados.
2. **Funciones puras**: Las funciones puras son aquellas que no tienen efectos secundarios y siempre producen el mismo resultado para los mismos argumentos.
3. **Composición de funciones**: Las funciones se pueden combinar para crear nuevas funciones más complejas.

### Ejemplo de funciones en Python

```python
def suma(x, y):
    return x + y

def aplicar_funcion(func, a, b):
    return func(a, b)

resultado = aplicar_funcion(suma, 5, 10)
print(resultado)  # Salida: 15
```

En este ejemplo, la función `suma` se pasa como argumento a la función `aplicar_funcion`, lo que demuestra cómo las funciones pueden ser tratadas como objetos de primera clase en Python.
