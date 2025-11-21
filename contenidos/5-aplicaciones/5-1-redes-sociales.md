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
description: Facebook y Twitter (X)
---

# Recuperación de la Información de las Redes Sociales

```{code-cell} python
---
tags: hide-output, remove-cell
---
"""Borra todos los archivos y carpetas en /tmp/edd_redes_sociales"""
import os
import shutil

tmp_dir = "/tmp/edd_redes_sociales"
if os.path.exists(tmp_dir):
    shutil.rmtree(tmp_dir)
os.makedirs(tmp_dir, exist_ok=True)
os.chdir(tmp_dir)
```

Las redes sociales se han convertido en una de las fuentes más importantes de información en la actualidad. Plataformas como Facebook, Twitter e Instagram generan enormes volúmenes de datos cada segundo, que pueden ser analizados para obtener insights valiosos sobre comportamientos, tendencias y patrones sociales.

En este capítulo exploraremos diferentes técnicas y herramientas para recuperar y analizar información de redes sociales, centrándonos en dos casos de estudio principales:

1. **Facebook**: Modelado de redes sociales como grafos y recorrido mediante algoritmos de búsqueda en profundidad (DFS).
2. **Twitter**: Procesamiento de streams de tweets en tiempo real y análisis de datos históricos en formato JSON.

```{note} Nota
Es importante mencionar que al trabajar con datos de redes sociales, debemos respetar los términos de servicio de cada plataforma, las leyes de protección de datos personales, y considerar las implicaciones éticas del uso de información pública.
```

## Caso de estudio: Facebook y Grafos de Redes Sociales

Las redes sociales pueden modelarse naturalmente como grafos, donde los nodos representan usuarios y las aristas representan relaciones de amistad o conexión. Este modelo nos permite aplicar algoritmos de teoría de grafos para analizar la estructura y propiedades de la red.

El primer paso es registrarse como desarrollador en la plataforma de Meta (Facebook) y obtener un token de acceso para usar la API Graph de Facebook. Este token es necesario para autenticar las solicitudes y acceder a los datos permitidos. Ver [Anexo: Facebook](../Anexos/Facebook.md) para una guía detallada.

### Instalación de la Librería Facebook SDK

Para trabajar con la API de Facebook en Python, vamos a usar la librería `facebook-sdk`:

```bash
pip install facebook-sdk
```

### Ejemplo de Uso de Facebook Graph API

Copiar el siguiente fragmento de código en un archivo Python y reemplazar `USER_ACCESS_TOKEN` con el token de acceso obtenido

```{code-block} python
---
linenos:
---
import facebook # Importamos la nueva librería


def get_all_likes_sdk(token):
    """
    Obtiene todas las páginas que le han gustado a un usuario usando el facebook-sdk.
    La paginación es manejada automáticamente por la librería.

    Args:
        token (str): El token de acceso de usuario con el permiso 'user_likes'.

    Returns:
        list: Una lista de diccionarios que representan las páginas.
    """
    try:
        # 1. Creamos una instancia del objeto GraphAPI
        graph = facebook.GraphAPI(access_token=token)

        print("Obteniendo tus 'Me gusta' con el SDK de Facebook...")

        # 2. Usamos get_all_connections para manejar la paginación automáticamente.
        #    La librería se encargará de hacer todas las llamadas necesarias.
        pages_generator = graph.get_all_connections(
            id='me',
            connection_name='likes',
            fields='name,category'
        )

        # Convertimos el generador a una lista para tener todos los resultados
        all_likes = list(pages_generator)

        print("\nProceso completado.")
        return all_likes

    except facebook.GraphAPIError as e:
        print(f"Error de la API de Facebook: {e}")
        return []

# --- BLOQUE DE PRUEBA ---
if __name__ == "__main__":

    # --- CONFIGURACIÓN ---
    # Pegar aquí el Access Token de Usuario.
    USER_ACCESS_TOKEN = "USER_ACCESS_TOKEN"

    if "USER_ACCESS_TOKEN" in USER_ACCESS_TOKEN:
        print("Por favor, completar el TOKEN DE ACCESO DE USUARIO.")
    else:
        # Llamamos a la nueva función
        likes = get_all_likes_sdk(USER_ACCESS_TOKEN)

        if likes:
            print(f"\n¡Se encontraron un total de {len(likes)} páginas que te gustan!")
            print("\n--- Ejemplo de los primeros 100 resultados: ---")
            for i, page in enumerate(likes[:100]):
                category = page.get('category', 'Sin categoría')
                print(f"{i+1}. Nombre: {page['name']} | Categoría: {category}")
        else:
            print("\nNo se encontraron 'Me gusta' o ocurrió un error durante el proceso.")

```

### Modelado de una Red Social como Grafo

En Facebook las relaciones de amistad son simétricas o bidireccionales, por lo tanto se pueden representar con un grafo no dirigido. A continuación, mostramos un ejemplo simple de una red social con varios usuarios y sus conexiones:

```{mermaid}
---
name: grafo-facebook
---
graph LR
    A[Ana]
    B[Bruno]
    C[Clara]
    D[Diego]
    E[Elena]
    F[Fernando]
    G[Gabriela]

    A <--> B
    A <--> C
    A <--> D
    B <--> C
    B <--> E
    C <--> F
    D <--> F
    E <--> F
    F <--> G

    style A fill:#ffcccc,stroke:#cc0000,stroke-width:2px
    style B fill:#ccffcc,stroke:#00cc00,stroke-width:2px
    style C fill:#ccccff,stroke:#0000cc,stroke-width:2px
    style D fill:#ffffcc,stroke:#cccc00,stroke-width:2px
    style E fill:#ffccff,stroke:#cc00cc,stroke-width:2px
    style F fill:#ccffff,stroke:#00cccc,stroke-width:2px
    style G fill:#ffddcc,stroke:#cc6600,stroke-width:2px
```

En Facebook se puede acceder online a Graph API Explorer para probar consultas y explorar la estructura de datos: [Graph API Explorer](https://developers.facebook.com/tools/explorer/).

La siguiente consulta devuelve todos los likes e incluye las categorías:

```{code-block}
GET /me/likes?fields=name,category
```

Para listar los amigos de un usuario:

```{code-block}
GET /me/friends
```

Por motivos de seguridad, la API de Facebook no permite profundizar en las conexiones de amigos (amigos de amigos) sin permisos adicionales. En una aplicación no comercial sólo podemos obtener grafos egocéntricos (1 nivel de profundidad).

En una aplicación comercial se deben solicitar los permisos correspondientes y cumplir con las políticas de la plataforma para poder explorar el grafo en más profundidad.

## Caso de estudio: Twitter/X y Procesamiento de JSON

Twitter (ahora X) es una plataforma de microblogging donde los usuarios publican mensajes cortos llamados "tweets". La información de tweets se obtiene en formato JSON mediante la API oficial, tanto de streams en tiempo real como de datos históricos.

A diferencia de Facebook en X las relaciones no son simétricas, por lo tanto se modelan con un grafo dirigido, ya que una persona puede seguir a otra sin que la relación sea recíproca.

Una persona que sigue a otra recibe sus tweets en su timeline, pero la persona seguida no recibe automáticamente los tweets del seguidor a menos que también lo siga.

Antes de poder usar la API de Twitter, es necesario registrarse como desarrollador y crear una aplicación para obtener las credenciales necesarias (Bearer Token y Access Token). Ver [Anexo: Twitter](../Anexos/Twitter.md) para una guía detallada.

Para consultar la API de Twitter en Python, usaremos la librería `tweepy`.

```bash
pip install tweepy
```

### Ejemplo de Streaming de Tweets en Tiempo Real

Copiar el siguiente script en un archivo Python y ejecutar. Requiere un Bearer Token válido.

```{code-block} python
---
linenos:
---
"""
Ejemplo de uso de la API de Twitter/X para análisis de datos
Requiere credenciales válidas de desarrollador de X
"""

import tweepy
import json
import os
from datetime import datetime

def verificar_credenciales():
    """Verifica que las credenciales estén configuradas"""
    bearer_token = os.getenv('TWITTER_BEARER_TOKEN')

    if not bearer_token:
        print("Error: TWITTER_BEARER_TOKEN no encontrado en variables de entorno")
        print("\nPara configurar las credenciales:")
        print("1. Obtén un Bearer Token siguiendo el instructivo en contenidos/Anexos/Twitter.md")
        print("2. Ejecuta: export TWITTER_BEARER_TOKEN='tu_bearer_token_aqui'")
        print("3. O crea un archivo .env con: TWITTER_BEARER_TOKEN=tu_bearer_token_aqui")
        return None

    return bearer_token

def buscar_tweets_recientes(query="python", max_results=10):
    """Busca tweets recientes sobre un tema"""

    bearer_token = verificar_credenciales()
    if not bearer_token:
        return

    try:
        # Crear cliente de Twitter API v2
        client = tweepy.Client(bearer_token=bearer_token)

        print(f"Buscando tweets sobre: '{query}'")

        # Buscar tweets recientes
        tweets = client.search_recent_tweets(
            query=f"{query} -is:retweet lang:es",  # Excluir retweets, solo español
            max_results=max_results,
            tweet_fields=["created_at", "public_metrics", "author_id", "lang"],
            expansions=["author_id"],
            user_fields=["username", "name", "public_metrics"]
        )

        if not tweets.data:
            print("No se encontraron tweets. Verifica tu Bearer Token y cuota de API.")
            return

        print(f"Encontrados {len(tweets.data)} tweets")

        # Procesar y mostrar resultados
        archivo_salida = os.path.join(tmp_dir, f"tweets_{query.replace(' ', '_')}.jsonl")

        with open(archivo_salida, "w", encoding="utf-8") as f:
            for tweet in tweets.data:
                # Obtener información del autor
                author = None
                if tweets.includes and 'users' in tweets.includes:
                    author = next(
                        (user for user in tweets.includes["users"]
                         if user.id == tweet.author_id),
                        None
                    )

                # Mostrar información del tweet
                print(f"\nTweet: {tweet.text[:100]}...")
                if author:
                    print(f"Autor: @{author.username} ({author.name})")
                print(f"Likes: {tweet.public_metrics['like_count']} | "
                      f"Retweets: {tweet.public_metrics['retweet_count']}")

                # Guardar en formato JSON
                tweet_dict = {
                    "id": tweet.id,
                    "created_at": str(tweet.created_at),
                    "text": tweet.text,
                    "author": {
                        "username": author.username if author else "unknown",
                        "name": author.name if author else "unknown",
                        "followers": author.public_metrics["followers_count"] if author else 0
                    } if author else None,
                    "metrics": tweet.public_metrics,
                    "lang": tweet.lang,
                    "fecha_extraccion": datetime.now().isoformat()
                }

                f.write(json.dumps(tweet_dict, ensure_ascii=False) + "\n")

        print(f"\n Tweets guardados en: {archivo_salida}")

    except tweepy.errors.Forbidden as e:
        print("Error 403 - Acceso denegado:")
        print("   • Verifica que tu Bearer Token sea válido")
        print("   • Asegúrate de que tu aplicación esté asociada a un Proyecto")
        print("   • Revisa que tengas permisos para usar la API v2")
        print(f"   • Detalles del error: {e}")

    except tweepy.errors.TooManyRequests as e:
        print("Error 429 - Demasiadas solicitudes:")
        print("   • Has excedido el límite de la API")
        print("   • Espera unos minutos antes de intentar de nuevo")
        print(f"   • Detalles del error: {e}")

    except Exception as e:
        print(f"Error inesperado: {e}")
        print("   • Verifica tu conexión a internet")
        print("   • Asegúrate de que tweepy esté instalado: pip install tweepy")

def mostrar_estadisticas_api():
    """Muestra información sobre los límites de la API"""

    bearer_token = verificar_credenciales()
    if not bearer_token:
        return

    try:
        client = tweepy.Client(bearer_token=bearer_token)

        # Verificar autenticación haciendo una búsqueda mínima
        response = client.search_recent_tweets(
            query="test",
            max_results=10,
            tweet_fields=["created_at"]
        )

        print("Autenticación exitosa")
        print(f"• Resultados de búsqueda de prueba: {response.meta.get('result_count', 0)} tweets encontrados")
        print("\nInformación de la API:")
        print("• API Version: v2")
        print("• Search Recent: Disponible")
        print("• Para información actualizada sobre límites y tiers de la API, consulta la documentación oficial:")
        print("  https://developer.twitter.com/en/docs/twitter-api/rate-limits")

    except Exception as e:
        print(f"Error al verificar API: {e}")

def main():
    """Función principal del programa"""

    print("Twitter/X API - Ejemplo de Análisis de Datos")
    print("=" * 50)

    # Verificar configuración
    print("\n1 Verificando configuración...")
    mostrar_estadisticas_api()

    # Buscar tweets sobre Python
    print("\n2 Buscando tweets sobre Python...")
    buscar_tweets_recientes("python", max_results=5)

    # Buscar tweets sobre programación
    print("\n3 Buscando tweets sobre programación...")
    buscar_tweets_recientes("programacion", max_results=5)

if __name__ == "__main__":
    # Intentar cargar variables de entorno desde .env si existe
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("Variables de entorno cargadas desde .env")
    except ImportError:
        print("Tip: Instala python-dotenv para usar archivos .env")
        print("   pip install python-dotenv")

    main()
```

### Estructura de un Tweet en JSON (API v2)

La API v2 de Twitter devuelve tweets en formato JSON con esta estructura:

```{code-cell} python
---
tags: hide-output
---
import json
from datetime import datetime

# Ejemplo de tweet en formato JSON (estructura real de API v2)
# Basado en la documentación oficial: https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/tweet
tweet_ejemplo_api_v2 = {
    "data": {
        "id": "1234567890123456789",
        "text": "Las estructuras de datos son fundamentales en programación! #EDD #Python",
        "created_at": "2024-01-15T10:30:00.000Z",
        "author_id": "987654321",
        "lang": "es",
        "public_metrics": {
            "retweet_count": 15,
            "reply_count": 3,
            "like_count": 47,
            "quote_count": 2,
            "impression_count": 1523
        },
        "entities": {
            "hashtags": [
                {"start": 55, "end": 59, "tag": "EDD"},
                {"start": 60, "end": 67, "tag": "Python"}
            ]
        }
    },
    "includes": {
        "users": [
            {
                "id": "987654321",
                "name": "Maria Lopez",
                "username": "maria_dev",
                "created_at": "2020-05-10T12:00:00.000Z",
                "public_metrics": {
                    "followers_count": 1523,
                    "following_count": 342,
                    "tweet_count": 2341,
                    "listed_count": 12
                }
            }
        ]
    }
}

print("=== Estructura de un Tweet (Twitter API v2) ===")
print(json.dumps(tweet_ejemplo_api_v2, indent=2, ensure_ascii=False))
print("\nDocumentación: https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/tweet")
```

### Procesamiento de Tweets Históricos

Cuando trabajamos con datos históricos de Twitter, comúnmente recibimos archivos en formato JSONL (JSON Lines), donde cada línea es un objeto JSON independiente. Esto facilita el procesamiento de grandes volúmenes de datos.

```{note} Nota
**Datos de práctica**: Los siguientes ejemplos usan datos simulados con la estructura real de la API de Twitter v2. Para trabajar con datos reales, sigue los pasos de registro y autenticación descritos anteriormente y usa los ejemplos de código con Tweepy.
```

```{code-cell} python
---
tags: hide-output
---
import random

def generar_tweets_ejemplo(n=20):
    """
    Genera tweets de ejemplo usando la estructura real de Twitter API v2.
    Simula datos que se obtendrían usando tweepy.Client.search_recent_tweets()
    """
    usuarios = [
        {"id": "1001", "name": "Ana García", "username": "ana_tech", "followers": 2341},
        {"id": "1002", "name": "Bruno Silva", "username": "bruno_code", "followers": 1523},
        {"id": "1003", "name": "Clara Ruiz", "username": "clara_dev", "followers": 3421},
        {"id": "1004", "name": "Diego Mendoza", "username": "diego_data", "followers": 987},
        {"id": "1005", "name": "Elena Torres", "username": "elena_ai", "followers": 5432},
    ]

    temas = [
        ("Las estructuras de datos son fundamentales", ["EDD", "Programación"]),
        ("Python es un lenguaje muy versátil", ["Python", "Desarrollo"]),
        ("Los grafos tienen muchas aplicaciones prácticas", ["Grafos", "Algoritmos"]),
        ("El análisis de redes sociales es fascinante", ["RedesSociales", "DataScience"]),
        ("Machine learning está revolucionando el mundo", ["ML", "IA"]),
    ]

    tweets = []
    for i in range(n):
        usuario = random.choice(usuarios)
        tema, hashtags = random.choice(temas)

        # Formato real de Twitter API v2
        tweet = {
            "id": str(1000000000000000000 + i),
            "author_id": usuario["id"],
            "created_at": f"2024-01-{random.randint(10,20):02d}T{random.randint(0,23):02d}:{random.randint(0,59):02d}:00.000Z",
            "text": f"{tema} #{' #'.join(hashtags)}",
            "lang": "es",
            "public_metrics": {
                "retweet_count": random.randint(0, 50),
                "reply_count": random.randint(0, 20),
                "like_count": random.randint(0, 100),
                "quote_count": random.randint(0, 10),
                "impression_count": random.randint(100, 5000)
            },
            "entities": {
                "hashtags": [{"tag": tag} for tag in hashtags]
            },
            # Metadatos adicionales para procesamiento
            "_user": usuario  # No viene en API real, lo agregamos para simplificar ejemplos
        }
        tweets.append(tweet)

    return tweets

# Generar tweets de ejemplo
tweets = generar_tweets_ejemplo(20)
print(f"Generados {len(tweets)} tweets de ejemplo (estructura Twitter API v2)")
print(f"\nPrimer tweet:\n{json.dumps(tweets[0], indent=2, ensure_ascii=False)}")
```

```{code-cell} python
---
tags: hide-output
---
# Guardar tweets en formato JSONL
archivo_tweets = os.path.join(tmp_dir, "tweets_historicos.jsonl")

with open(archivo_tweets, 'w', encoding='utf-8') as f:
    for tweet in tweets:
        f.write(json.dumps(tweet, ensure_ascii=False) + '\n')

print(f"Tweets guardados en {archivo_tweets}")

# Verificar el contenido del archivo
with open(archivo_tweets, 'r', encoding='utf-8') as f:
    primeras_lineas = [f.readline() for _ in range(3)]

print(f"\nPrimeras 3 líneas del archivo:")
for i, linea in enumerate(primeras_lineas, 1):
    tweet = json.loads(linea)
    print(f"{i}. @{tweet['_user']['username']}: {tweet['text'][:50]}...")
```

### Procesamiento y Análisis de Tweets

Ahora procesemos los tweets para extraer información útil:

```{code-cell} python
---
tags: hide-output
---
def procesar_tweets_jsonl(archivo):
    """
    Procesa un archivo JSONL de tweets (formato Twitter API v2) y extrae estadísticas.
    Compatible con la estructura real que devuelve tweepy.
    """
    estadisticas = {
        "total_tweets": 0,
        "usuarios_unicos": set(),
        "hashtags": {},
        "total_retweets": 0,
        "total_likes": 0,
        "total_replies": 0,
        "tweets_por_usuario": {},
    }

    with open(archivo, 'r', encoding='utf-8') as f:
        for linea in f:
            tweet = json.loads(linea)
            estadisticas["total_tweets"] += 1

            # Usuario (de metadatos auxiliares _user)
            if "_user" in tweet:
                username = tweet["_user"]["username"]
                estadisticas["usuarios_unicos"].add(username)
                estadisticas["tweets_por_usuario"][username] = \
                    estadisticas["tweets_por_usuario"].get(username, 0) + 1

            # Hashtags (de entities)
            if "entities" in tweet and "hashtags" in tweet["entities"]:
                for hashtag_obj in tweet["entities"]["hashtags"]:
                    hashtag = hashtag_obj.get("tag", "")
                    if hashtag:
                        estadisticas["hashtags"][hashtag] = \
                            estadisticas["hashtags"].get(hashtag, 0) + 1

            # Métricas públicas (estructura real de API v2)
            if "public_metrics" in tweet:
                metrics = tweet["public_metrics"]
                estadisticas["total_retweets"] += metrics.get("retweet_count", 0)
                estadisticas["total_likes"] += metrics.get("like_count", 0)
                estadisticas["total_replies"] += metrics.get("reply_count", 0)

    # Convertir set a lista para serialización
    estadisticas["usuarios_unicos"] = list(estadisticas["usuarios_unicos"])

    return estadisticas

# Procesar los tweets
stats = procesar_tweets_jsonl(archivo_tweets)

print("=== Estadísticas de Tweets ===")
print(f"Total de tweets: {stats['total_tweets']}")
print(f"Usuarios únicos: {len(stats['usuarios_unicos'])}")
print(f"Total de retweets: {stats['total_retweets']}")
print(f"Total de likes: {stats['total_likes']}")
print(f"Total de replies: {stats['total_replies']}")

print("\n=== Hashtags más populares ===")
hashtags_ordenados = sorted(stats["hashtags"].items(), key=lambda x: x[1], reverse=True)
for hashtag, count in hashtags_ordenados[:5]:
    print(f"#{hashtag}: {count} veces")

print("\n=== Usuarios más activos ===")
usuarios_ordenados = sorted(stats["tweets_por_usuario"].items(), key=lambda x: x[1], reverse=True)
for usuario, count in usuarios_ordenados[:5]:
    print(f"@{usuario}: {count} tweets")
```

## Aspectos Importantes de la Recuperación de Información en Redes Sociales

- Las redes sociales generan grandes volúmenes de datos que pueden ser analizados usando estructuras de datos y algoritmos apropiados.
- Los grafos son una representación natural de las redes sociales y permiten aplicar algoritmos de teoría de grafos.
- JSON y JSONL son formatos ideales para trabajar con datos de APIs y streams.
- La persistencia de datos es crucial para poder analizar y procesar la información posteriormente.
