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

# Recuperación de la Información de las Redes Sociales

```{code-cell} python
---
tags: [hide-output, remove-cell]
---
"""Borra todos los archivos y carpetas en /tmp"""
import os
import shutil

tmp_dir = "/tmp"
os.chdir(tmp_dir)
for filename in os.listdir(tmp_dir):
    file_path = os.path.join(tmp_dir, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print(f"No se pudo borrar {file_path}: {e}")
```

Las redes sociales se han convertido en una de las fuentes más importantes de información en la actualidad. Plataformas como Facebook, Twitter e Instagram generan enormes volúmenes de datos cada segundo, que pueden ser analizados para obtener insights valiosos sobre comportamientos, tendencias y patrones sociales.

En este capítulo exploraremos diferentes técnicas y herramientas para recuperar y analizar información de redes sociales, centrándonos en tres casos de estudio principales:

1. **Facebook**: Modelado de redes sociales como grafos y recorrido mediante algoritmos de búsqueda en profundidad (DFS).
2. **Twitter**: Procesamiento de streams de tweets en tiempo real y análisis de datos históricos en formato JSON.
3. **Instagram**: Web scraping con Scrapy para extraer información de perfiles y publicaciones.

En todos los casos, exploraremos cómo persistir la información recolectada en diferentes formatos de archivo para su posterior análisis.

```{note}
Es importante mencionar que al trabajar con datos de redes sociales, debemos respetar los términos de servicio de cada plataforma, las leyes de protección de datos personales, y considerar las implicaciones éticas del uso de información pública.
```

## Caso de estudio: Facebook y Grafos de Redes Sociales

Las redes sociales pueden modelarse naturalmente como grafos, donde los nodos representan usuarios y las aristas representan relaciones de amistad o conexión. Este modelo nos permite aplicar algoritmos de teoría de grafos para analizar la estructura y propiedades de la red.

### Registro como Desarrollador de Facebook

Para acceder a datos de Facebook mediante su API oficial, primero debemos registrarnos como desarrolladores:

**Paso 1: Crear una cuenta de desarrollador**

1. Visitar [Facebook for Developers](https://developers.facebook.com/)
2. Hacer clic en "Get Started" o "Comenzar"
3. Iniciar sesión con tu cuenta de Facebook personal
4. Completar el registro como desarrollador aceptando los términos de servicio

**Paso 2: Crear una aplicación**

1. En el panel de desarrollador, hacer clic en "My Apps" > "Create App"
2. Seleccionar el tipo de aplicación (por ejemplo, "Consumer" o "Business")
3. Completar los detalles de la aplicación:
   - Nombre de la aplicación
   - Email de contacto
   - Categoría de la aplicación
4. Una vez creada, obtendrás:
   - **App ID**: Identificador único de tu aplicación
   - **App Secret**: Clave secreta (mantener confidencial)

**Paso 3: Configurar permisos**

1. En el dashboard de la aplicación, ir a "Settings" > "Basic"
2. Agregar productos necesarios (por ejemplo, "Facebook Login")
3. Configurar los permisos que necesitarás:
   - `public_profile`: Información pública de perfil
   - `user_friends`: Lista de amigos
   - `user_posts`: Publicaciones del usuario

**Documentación oficial:**

- [Meta for Developers - Getting Started](https://developers.facebook.com/docs/development/create-an-app/)
- [Graph API Reference](https://developers.facebook.com/docs/graph-api/)
- [Facebook Python SDK](https://facebook-sdk.readthedocs.io/)

```{important}
**Nota sobre privacidad**: La API de Facebook Graph ha limitado significativamente el acceso a datos de usuarios desde 2018 por razones de privacidad. Actualmente, solo se puede acceder a datos del propio usuario autenticado y amigos que hayan autorizado la aplicación. Para fines educativos, trabajaremos con grafos simulados pero usando la estructura de datos real que proporciona la API.
```

### Instalación de la Librería Facebook SDK

Para trabajar con la API de Facebook en Python, usamos la librería `facebook-sdk`:

```{code-cell} python
---
tags: [hide-output]
---
# Instalación (ejecutar en terminal)
# pip install facebook-sdk

# Importar la librería
try:
    import facebook
    print("✓ facebook-sdk instalado correctamente")
    print(f"Versión: {facebook.__version__}")
except ImportError:
    print("⚠ facebook-sdk no está instalado")
    print("Instalar con: pip install facebook-sdk")
```

### Ejemplo de Uso de Facebook Graph API

Aquí un ejemplo de cómo usar la API real de Facebook (requiere credenciales):

```{code-cell} python
---
tags: [hide-output]
mystnb:
  number_source_lines: true
---
# IMPORTANTE: Este código es un ejemplo de estructura
# Para ejecutarlo, necesitas reemplazar 'YOUR_ACCESS_TOKEN' con tu token real

ejemplo_uso_api = '''
import facebook

# Configurar el token de acceso
# Obtener desde: https://developers.facebook.com/tools/explorer/
access_token = "YOUR_ACCESS_TOKEN"

# Crear conexión a la API
graph = facebook.GraphAPI(access_token=access_token, version="3.1")

# Obtener información del usuario autenticado
perfil = graph.get_object(id="me", fields="id,name,friends")

print(f"Usuario: {perfil['name']}")
print(f"ID: {perfil['id']}")

# Obtener lista de amigos (requiere permiso user_friends)
# Nota: Solo devuelve amigos que usan la misma aplicación
if 'friends' in perfil:
    amigos = perfil['friends']['data']
    print(f"Amigos que usan la app: {len(amigos)}")
    
    # Construir grafo de conexiones
    for amigo in amigos:
        print(f"  - {amigo['name']} (ID: {amigo['id']})")
'''

print("=== Ejemplo de uso de Facebook Graph API ===")
print(ejemplo_uso_api)
print("\n⚠ Nota: Este ejemplo requiere credenciales reales de Facebook Developer")
```

### Modelado de una Red Social como Grafo

Dado que el acceso a datos reales de Facebook está limitado, trabajaremos con un grafo simulado que representa la estructura que obtendríamos de la API. En una red social como Facebook, cada usuario puede ser representado como un vértice en un grafo, y las relaciones de amistad como aristas no dirigidas (ya que la amistad es bidireccional).

```{mermaid}
---
name: red_social_grafo
title: Grafo de Red Social
---
graph LR
    A[Ana] --- B[Bruno]
    A --- C[Clara]
    A --- D[Diego]
    B --- C
    B --- E[Elena]
    C --- F[Fernando]
    D --- F
    E --- F
    F --- G[Gabriela]
    
    style A fill:#ffcccc,stroke:#cc0000,stroke-width:2px
    style B fill:#ccffcc,stroke:#00cc00,stroke-width:2px
    style C fill:#ccccff,stroke:#0000cc,stroke-width:2px
    style D fill:#ffffcc,stroke:#cccc00,stroke-width:2px
    style E fill:#ffccff,stroke:#cc00cc,stroke-width:2px
    style F fill:#ccffff,stroke:#00cccc,stroke-width:2px
    style G fill:#ffddcc,stroke:#cc6600,stroke-width:2px
```

### Recorrido en Profundidad (DFS) en una Red Social

El algoritmo de búsqueda en profundidad (DFS) es útil para explorar redes sociales. Podemos usarlo para:

- Encontrar todos los usuarios alcanzables desde un usuario dado
- Identificar componentes conexas (grupos de usuarios conectados entre sí)
- Calcular el grado de separación entre usuarios
- Detectar posibles ciclos en la red

Implementemos un ejemplo práctico:

```{code-cell} python
---
tags: [hide-output]
mystnb:
  number_source_lines: true
---
class RedSocial:
    """Representa una red social como un grafo no dirigido."""
    
    def __init__(self):
        self.usuarios = {}
        
    def agregar_usuario(self, nombre):
        """Agrega un nuevo usuario a la red."""
        if nombre not in self.usuarios:
            self.usuarios[nombre] = []
            
    def agregar_amistad(self, usuario1, usuario2):
        """Establece una relación de amistad bidireccional entre dos usuarios."""
        if usuario1 not in self.usuarios:
            self.agregar_usuario(usuario1)
        if usuario2 not in self.usuarios:
            self.agregar_usuario(usuario2)
            
        # Agregar la conexión en ambas direcciones
        if usuario2 not in self.usuarios[usuario1]:
            self.usuarios[usuario1].append(usuario2)
        if usuario1 not in self.usuarios[usuario2]:
            self.usuarios[usuario2].append(usuario1)
    
    def dfs(self, usuario_inicial, visitados=None):
        """
        Realiza un recorrido en profundidad (DFS) desde un usuario inicial.
        Retorna la lista de usuarios visitados en orden de visita.
        """
        if visitados is None:
            visitados = set()
        
        # Lista para mantener el orden de visita
        orden_visita = []
        
        def _dfs_recursivo(usuario):
            # Marcar como visitado
            visitados.add(usuario)
            orden_visita.append(usuario)
            
            # Visitar todos los amigos no visitados
            for amigo in self.usuarios.get(usuario, []):
                if amigo not in visitados:
                    _dfs_recursivo(amigo)
        
        _dfs_recursivo(usuario_inicial)
        return orden_visita
    
    def obtener_componentes_conexas(self):
        """
        Encuentra todas las componentes conexas en la red.
        Cada componente es un grupo de usuarios conectados entre sí.
        """
        visitados = set()
        componentes = []
        
        for usuario in self.usuarios:
            if usuario not in visitados:
                # Realizar DFS desde este usuario
                componente = self.dfs(usuario, visitados)
                componentes.append(componente)
        
        return componentes
    
    def distancia_entre_usuarios(self, origen, destino):
        """
        Calcula la distancia (grados de separación) entre dos usuarios.
        Usa BFS para encontrar el camino más corto.
        """
        if origen not in self.usuarios or destino not in self.usuarios:
            return -1
        
        if origen == destino:
            return 0
        
        from collections import deque
        
        visitados = {origen}
        cola = deque([(origen, 0)])
        
        while cola:
            usuario_actual, distancia = cola.popleft()
            
            for amigo in self.usuarios[usuario_actual]:
                if amigo == destino:
                    return distancia + 1
                
                if amigo not in visitados:
                    visitados.add(amigo)
                    cola.append((amigo, distancia + 1))
        
        return -1  # No hay camino
```

Ahora creemos una red social de ejemplo y realicemos algunos análisis:

```{code-cell} python
---
tags: [hide-output]
---
# Crear la red social
red = RedSocial()

# Agregar relaciones de amistad
amistades = [
    ("Ana", "Bruno"),
    ("Ana", "Clara"),
    ("Ana", "Diego"),
    ("Bruno", "Clara"),
    ("Bruno", "Elena"),
    ("Clara", "Fernando"),
    ("Diego", "Fernando"),
    ("Elena", "Fernando"),
    ("Fernando", "Gabriela"),
]

for usuario1, usuario2 in amistades:
    red.agregar_amistad(usuario1, usuario2)

print("=== Red Social creada ===")
print(f"Total de usuarios: {len(red.usuarios)}")
print(f"Usuarios: {', '.join(sorted(red.usuarios.keys()))}\n")

# Mostrar las conexiones de cada usuario
print("=== Conexiones de cada usuario ===")
for usuario in sorted(red.usuarios.keys()):
    amigos = ', '.join(sorted(red.usuarios[usuario]))
    print(f"{usuario}: {amigos}")
```

```{code-cell} python
---
tags: [hide-output]
---
# Realizar un recorrido DFS desde Ana
print("\n=== Recorrido DFS desde Ana ===")
orden_visita = red.dfs("Ana")
print(f"Orden de visita: {' -> '.join(orden_visita)}")

# Encontrar componentes conexas
print("\n=== Componentes conexas ===")
componentes = red.obtener_componentes_conexas()
for i, componente in enumerate(componentes, 1):
    print(f"Componente {i}: {', '.join(componente)}")

# Calcular distancias entre usuarios
print("\n=== Grados de separación ===")
pares = [("Ana", "Gabriela"), ("Bruno", "Diego"), ("Elena", "Clara")]
for origen, destino in pares:
    distancia = red.distancia_entre_usuarios(origen, destino)
    print(f"De {origen} a {destino}: {distancia} grados de separación")
```

### Persistencia de Datos de la Red Social

Es importante poder guardar y cargar la información de la red social. Implementemos funciones para persistir los datos en formato JSON:

```{code-cell} python
---
tags: [hide-output]
mystnb:
  number_source_lines: true
---
import json

def guardar_red_social(red, archivo):
    """Guarda la red social en un archivo JSON."""
    with open(archivo, 'w', encoding='utf-8') as f:
        json.dump(red.usuarios, f, ensure_ascii=False, indent=2)
    print(f"Red social guardada en {archivo}")

def cargar_red_social(archivo):
    """Carga una red social desde un archivo JSON."""
    red = RedSocial()
    with open(archivo, 'r', encoding='utf-8') as f:
        red.usuarios = json.load(f)
    print(f"Red social cargada desde {archivo}")
    return red

# Guardar la red en un archivo
archivo_red = "/tmp/red_social.json"
guardar_red_social(red, archivo_red)

# Leer el archivo para verificar
with open(archivo_red, 'r') as f:
    contenido = f.read()
    print(f"\nContenido del archivo:\n{contenido[:300]}...")
```

```{code-cell} python
---
tags: [hide-output]
---
# Cargar la red desde el archivo
red_cargada = cargar_red_social(archivo_red)

# Verificar que se cargó correctamente
print(f"\nUsuarios cargados: {len(red_cargada.usuarios)}")
print(f"Recorrido DFS desde Ana: {' -> '.join(red_cargada.dfs('Ana'))}")
```

### Análisis de Centralidad

Podemos también calcular métricas importantes como el grado de centralidad de cada usuario:

```{code-cell} python
---
tags: [hide-output]
---
def calcular_grado_centralidad(red):
    """Calcula el grado de centralidad de cada usuario (número de amigos)."""
    centralidad = {}
    for usuario, amigos in red.usuarios.items():
        centralidad[usuario] = len(amigos)
    return centralidad

# Calcular y mostrar centralidad
centralidad = calcular_grado_centralidad(red)
print("=== Grado de Centralidad ===")
for usuario, grado in sorted(centralidad.items(), key=lambda x: x[1], reverse=True):
    print(f"{usuario}: {grado} conexiones")

# Guardar métricas en un archivo
archivo_metricas = "/tmp/metricas_red_social.json"
metricas = {
    "total_usuarios": len(red.usuarios),
    "total_conexiones": sum(centralidad.values()) // 2,  # Dividir por 2 porque son bidireccionales
    "centralidad": centralidad,
    "componentes_conexas": len(red.obtener_componentes_conexas())
}

with open(archivo_metricas, 'w', encoding='utf-8') as f:
    json.dump(metricas, f, ensure_ascii=False, indent=2)
    
print(f"\nMétricas guardadas en {archivo_metricas}")
```

## Caso de estudio: Twitter/X y Procesamiento de JSON

Twitter (ahora X) es una plataforma de microblogging donde los usuarios publican mensajes cortos llamados "tweets". La información de tweets se obtiene en formato JSON mediante la API oficial, tanto de streams en tiempo real como de datos históricos.

### Registro como Desarrollador de Twitter/X

Para acceder a la API de Twitter/X, debemos registrarnos en el portal de desarrolladores:

**Paso 1: Crear una cuenta de desarrollador**

1. Visitar [Twitter Developer Portal](https://developer.twitter.com/)
2. Hacer clic en "Sign up" o iniciar sesión con tu cuenta de Twitter/X
3. Solicitar acceso como desarrollador:
   - Seleccionar el propósito de uso (educativo, investigación, comercial)
   - Describir cómo planeas usar la API
   - Aceptar los términos de servicio

**Paso 2: Crear un proyecto y aplicación**

1. En el Developer Portal, ir a "Projects & Apps"
2. Crear un nuevo proyecto:
   - Nombre del proyecto
   - Descripción y caso de uso
3. Crear una aplicación dentro del proyecto
4. Obtener las credenciales:
   - **API Key** (Consumer Key)
   - **API Secret Key** (Consumer Secret)
   - **Bearer Token** (para API v2)
   - **Access Token** y **Access Token Secret** (para autenticación de usuario)

**Paso 3: Configurar permisos**

1. En la configuración de la aplicación, establecer permisos:
   - Read: Solo lectura de tweets
   - Read and Write: Leer y publicar
   - Read, Write and Direct Messages: Acceso completo
2. Para acceso básico (Free tier):
   - 500,000 tweets por mes
   - Acceso a API v2
   - Limitado a 1 aplicación

**Niveles de acceso:**

- **Free**: Acceso básico para aprender y construir
- **Basic** ($100/mes): Más tweets y mejor acceso
- **Pro** ($5,000/mes): Acceso completo para empresas
- **Enterprise**: Acceso personalizado

**Documentación oficial:**

- [Twitter API Documentation](https://developer.twitter.com/en/docs)
- [API v2 Quick Start](https://developer.twitter.com/en/docs/twitter-api/getting-started/getting-access-to-the-twitter-api)
- [Tweepy Documentation](https://docs.tweepy.org/) (Librería Python oficial)
- [API Reference](https://developer.twitter.com/en/docs/api-reference-index)

### Instalación de Tweepy

Tweepy es la librería oficial de Python para trabajar con la API de Twitter:

```{code-cell} python
---
tags: [hide-output]
---
# Instalación (ejecutar en terminal)
# pip install tweepy

# Importar la librería
try:
    import tweepy
    print("✓ tweepy instalado correctamente")
    print(f"Versión: {tweepy.__version__}")
except ImportError:
    print("⚠ tweepy no está instalado")
    print("Instalar con: pip install tweepy")
```

### Ejemplo de Autenticación con Twitter API v2

```{code-cell} python
---
tags: [hide-output]
mystnb:
  number_source_lines: true
---
# IMPORTANTE: Este código es un ejemplo de estructura
# Para ejecutarlo, necesitas reemplazar las credenciales con tus valores reales

ejemplo_autenticacion = '''
import tweepy

# Método 1: Autenticación con Bearer Token (API v2)
bearer_token = "YOUR_BEARER_TOKEN"
client = tweepy.Client(bearer_token=bearer_token)

# Método 2: Autenticación OAuth 1.0a (API v1.1)
consumer_key = "YOUR_API_KEY"
consumer_secret = "YOUR_API_SECRET"
access_token = "YOUR_ACCESS_TOKEN"
access_token_secret = "YOUR_ACCESS_TOKEN_SECRET"

client = tweepy.Client(
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_token_secret
)

# Verificar autenticación
try:
    user = client.get_me()
    print(f"✓ Autenticado como: @{user.data.username}")
except Exception as e:
    print(f"✗ Error de autenticación: {e}")
'''

print("=== Ejemplo de autenticación con Twitter API ===")
print(ejemplo_autenticacion)
print("\n⚠ Nota: Este ejemplo requiere credenciales reales de Twitter Developer Portal")
```

### Ejemplo de Búsqueda de Tweets con API v2

```{code-cell} python
---
tags: [hide-output]
mystnb:
  number_source_lines: true
---
# Ejemplo de búsqueda de tweets usando la API real

ejemplo_busqueda_tweets = '''
import tweepy
import json

# Configurar cliente con Bearer Token
bearer_token = "YOUR_BEARER_TOKEN"
client = tweepy.Client(bearer_token=bearer_token)

# Buscar tweets recientes sobre un tema
query = "python programación -is:retweet"  # Tweets sobre Python, sin retweets

# API v2: search_recent_tweets (últimos 7 días)
tweets = client.search_recent_tweets(
    query=query,
    max_results=10,
    tweet_fields=["created_at", "public_metrics", "author_id", "lang"],
    expansions=["author_id"],
    user_fields=["username", "name", "public_metrics"]
)

# Procesar resultados
print(f"Encontrados {len(tweets.data)} tweets:")

for tweet in tweets.data:
    # Obtener información del autor
    author = next(
        (user for user in tweets.includes["users"] 
         if user.id == tweet.author_id), 
        None
    )
    
    print(f"\\n@{author.username}: {tweet.text[:100]}...")
    print(f"  ❤️ {tweet.public_metrics['like_count']} | "
          f"🔄 {tweet.public_metrics['retweet_count']}")
    
    # Guardar en formato JSON
    tweet_dict = {
        "id": tweet.id,
        "created_at": str(tweet.created_at),
        "text": tweet.text,
        "author": {
            "username": author.username,
            "name": author.name,
            "followers": author.public_metrics["followers_count"]
        },
        "metrics": tweet.public_metrics,
        "lang": tweet.lang
    }
    
    # Guardar en archivo JSONL
    with open("/tmp/tweets_reales.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(tweet_dict, ensure_ascii=False) + "\\n")

print("\\n✓ Tweets guardados en /tmp/tweets_reales.jsonl")
'''

print("=== Ejemplo de búsqueda de tweets con API v2 ===")
print(ejemplo_busqueda_tweets)
print("\n⚠ Nota: Este ejemplo requiere credenciales reales de Twitter Developer")
```

### Ejemplo de Streaming de Tweets en Tiempo Real

```{code-cell} python
---
tags: [hide-output]
mystnb:
  number_source_lines: true
---
# Ejemplo de streaming en tiempo real usando la API

ejemplo_streaming = '''
import tweepy
import json

class TweetStreamListener(tweepy.StreamingClient):
    """Clase para procesar tweets en streaming."""
    
    def __init__(self, bearer_token, max_tweets=50):
        super().__init__(bearer_token)
        self.tweet_count = 0
        self.max_tweets = max_tweets
        
    def on_tweet(self, tweet):
        """Callback cuando llega un nuevo tweet."""
        self.tweet_count += 1
        
        print(f"[{self.tweet_count}] Nuevo tweet: {tweet.text[:80]}...")
        
        # Guardar en archivo
        tweet_data = {
            "id": tweet.id,
            "text": tweet.text,
            "created_at": str(tweet.created_at)
        }
        
        with open("/tmp/stream_tweets.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(tweet_data, ensure_ascii=False) + "\\n")
        
        # Detener después de max_tweets
        if self.tweet_count >= self.max_tweets:
            self.disconnect()
            print(f"\\n✓ Stream detenido después de {self.max_tweets} tweets")
    
    def on_errors(self, errors):
        """Callback para manejar errores."""
        print(f"Error en streaming: {errors}")

# Configurar y ejecutar streaming
bearer_token = "YOUR_BEARER_TOKEN"
stream = TweetStreamListener(bearer_token, max_tweets=50)

# Agregar reglas de filtrado
# stream.add_rules(tweepy.StreamRule("python OR javascript"))

# Iniciar streaming
# stream.filter(tweet_fields=["created_at", "public_metrics"])
print("Stream configurado. Descomenta las últimas líneas para ejecutar.")
'''

print("=== Ejemplo de streaming de tweets en tiempo real ===")
print(ejemplo_streaming)
print("\n⚠ Nota: El streaming requiere credenciales y puede consumir tu cuota de API")
```

### Estructura de un Tweet en JSON (API v2)

La API v2 de Twitter devuelve tweets en formato JSON con esta estructura:

```{code-cell} python
---
tags: [hide-output]
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
print("\n📚 Documentación: https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/tweet")
```

### Procesamiento de Tweets Históricos

Cuando trabajamos con datos históricos de Twitter, comúnmente recibimos archivos en formato JSONL (JSON Lines), donde cada línea es un objeto JSON independiente. Esto facilita el procesamiento de grandes volúmenes de datos.

```{note}
**Datos de práctica**: Los siguientes ejemplos usan datos simulados con la estructura real de la API de Twitter v2. Para trabajar con datos reales, sigue los pasos de registro y autenticación descritos anteriormente y usa los ejemplos de código con Tweepy.
```

```{code-cell} python
---
tags: [hide-output]
mystnb:
  number_source_lines: true
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
tags: [hide-output]
---
# Guardar tweets en formato JSONL
archivo_tweets = "/tmp/tweets_historicos.jsonl"

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
    print(f"{i}. @{tweet['user']['screen_name']}: {tweet['text'][:50]}...")
```

### Procesamiento y Análisis de Tweets

Ahora procesemos los tweets para extraer información útil:

```{code-cell} python
---
tags: [hide-output]
mystnb:
  number_source_lines: true
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

### Simulación de Stream en Tiempo Real

Ahora simulemos el procesamiento de un stream en tiempo real, donde los tweets van llegando uno por uno:

```{code-cell} python
---
tags: [hide-output]
mystnb:
  number_source_lines: true
---
import time

class TwitterStreamProcessor:
    """
    Procesa tweets de un stream en tiempo real.
    Compatible con la estructura de Twitter API v2.
    """
    
    def __init__(self):
        self.tweets_procesados = 0
        self.hashtags_trending = {}
        self.archivo_log = "/tmp/twitter_stream.log"
        
        # Inicializar archivo de log
        with open(self.archivo_log, 'w', encoding='utf-8') as f:
            f.write(f"=== Stream iniciado a las {datetime.now()} ===\n")
    
    def procesar_tweet(self, tweet):
        """Procesa un tweet individual del stream (formato API v2)."""
        self.tweets_procesados += 1
        
        # Actualizar hashtags trending (de entities)
        if "entities" in tweet and "hashtags" in tweet["entities"]:
            for hashtag_obj in tweet["entities"]["hashtags"]:
                hashtag = hashtag_obj.get("tag", "")
                if hashtag:
                    self.hashtags_trending[hashtag] = \
                        self.hashtags_trending.get(hashtag, 0) + 1
        
        # Registrar en log
        self._log_tweet(tweet)
        
        # Detectar tweets populares (usando public_metrics)
        if "public_metrics" in tweet:
            metrics = tweet["public_metrics"]
            retweets = metrics.get("retweet_count", 0)
            likes = metrics.get("like_count", 0)
            
            if retweets > 30 or likes > 50:
                self._alertar_tweet_popular(tweet)
    
    def _log_tweet(self, tweet):
        """Registra el tweet en un archivo de log."""
        username = tweet.get("_user", {}).get("username", "unknown")
        with open(self.archivo_log, 'a', encoding='utf-8') as f:
            f.write(f"[{tweet['created_at']}] @{username}: {tweet['text']}\n")
    
    def _alertar_tweet_popular(self, tweet):
        """Alerta sobre tweets que están ganando popularidad."""
        username = tweet.get("_user", {}).get("username", "unknown")
        metrics = tweet.get("public_metrics", {})
        
        print(f"⚡ Tweet popular detectado!")
        print(f"   @{username}: {tweet['text'][:60]}...")
        print(f"   ❤️ {metrics.get('like_count', 0)} | 🔄 {metrics.get('retweet_count', 0)}")
    
    def obtener_trending_topics(self, top_n=5):
        """Obtiene los hashtags trending del momento."""
        return sorted(self.hashtags_trending.items(), 
                     key=lambda x: x[1], reverse=True)[:top_n]
    
    def guardar_estadisticas(self):
        """Guarda estadísticas del stream procesado."""
        stats = {
            "tweets_procesados": self.tweets_procesados,
            "trending_topics": dict(self.obtener_trending_topics(10)),
            "timestamp": datetime.now().isoformat()
        }
        
        archivo_stats = "/tmp/twitter_stream_stats.json"
        with open(archivo_stats, 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)
        
        return archivo_stats

# Simular procesamiento de stream
print("=== Simulación de Stream de Twitter ===\n")
processor = TwitterStreamProcessor()

for tweet in tweets[:10]:  # Procesar primeros 10 tweets
    processor.procesar_tweet(tweet)
    # Simular pequeño delay entre tweets
    time.sleep(0.1)

print(f"\n=== Resumen del Stream ===")
print(f"Tweets procesados: {processor.tweets_procesados}")

print("\nTrending Topics:")
for hashtag, count in processor.obtener_trending_topics():
    print(f"  #{hashtag}: {count} menciones")

# Guardar estadísticas
archivo_stats = processor.guardar_estadisticas()
print(f"\nEstadísticas guardadas en: {archivo_stats}")
```

### Filtrado y Búsqueda de Tweets

Implementemos funciones para filtrar y buscar tweets por diferentes criterios:

```{code-cell} python
---
tags: [hide-output]
---
def buscar_tweets_por_hashtag(archivo, hashtag):
    """Busca tweets que contengan un hashtag específico (formato API v2)."""
    tweets_encontrados = []
    
    with open(archivo, 'r', encoding='utf-8') as f:
        for linea in f:
            tweet = json.loads(linea)
            # Buscar en entities.hashtags
            if "entities" in tweet and "hashtags" in tweet["entities"]:
                tags = [h.get("tag", "") for h in tweet["entities"]["hashtags"]]
                if hashtag in tags:
                    tweets_encontrados.append(tweet)
    
    return tweets_encontrados

def buscar_tweets_por_usuario(archivo, username):
    """Busca todos los tweets de un usuario específico (formato API v2)."""
    tweets_usuario = []
    
    with open(archivo, 'r', encoding='utf-8') as f:
        for linea in f:
            tweet = json.loads(linea)
            # Buscar en _user.username (metadato auxiliar)
            if "_user" in tweet and tweet["_user"].get("username") == username:
                tweets_usuario.append(tweet)
    
    return tweets_usuario

def filtrar_tweets_populares(archivo, min_retweets=20):
    """Filtra tweets con un mínimo de retweets (formato API v2)."""
    tweets_populares = []
    
    with open(archivo, 'r', encoding='utf-8') as f:
        for linea in f:
            tweet = json.loads(linea)
            # Usar public_metrics.retweet_count
            if "public_metrics" in tweet:
                retweets = tweet["public_metrics"].get("retweet_count", 0)
                if retweets >= min_retweets:
                    tweets_populares.append(tweet)
    
    return tweets_populares

# Ejemplos de uso
print("=== Búsqueda de tweets sobre #Python ===")
tweets_python = buscar_tweets_por_hashtag(archivo_tweets, "Python")
print(f"Encontrados {len(tweets_python)} tweets")
for tweet in tweets_python[:3]:
    username = tweet.get("_user", {}).get("username", "unknown")
    print(f"  - @{username}: {tweet['text']}")

print("\n=== Tweets del usuario @ana_tech ===")
tweets_ana = buscar_tweets_por_usuario(archivo_tweets, "ana_tech")
print(f"Encontrados {len(tweets_ana)} tweets de @ana_tech")

print("\n=== Tweets populares (>20 retweets) ===")
tweets_pop = filtrar_tweets_populares(archivo_tweets, min_retweets=20)
print(f"Encontrados {len(tweets_pop)} tweets populares")
for tweet in tweets_pop[:3]:
    retweets = tweet.get("public_metrics", {}).get("retweet_count", 0)
    print(f"  - {tweet['text'][:50]}... (🔄 {retweets})")
```

## Caso de estudio: Instagram y Web Scraping con Scrapy

Instagram es una plataforma visual donde los usuarios comparten fotos y videos. Aunque Instagram tiene una API oficial, en muchos casos es útil utilizar web scraping para obtener información pública de perfiles y publicaciones.

```{note}
**Importante**: El web scraping debe realizarse respetando los términos de servicio de Instagram y las leyes aplicables. Este ejemplo es educativo y utiliza un sitio de prueba. En producción, se debe considerar usar la API oficial de Instagram.
```

### Configuración del Proyecto Scrapy

Para este ejemplo, crearemos un spider de Scrapy que simula la extracción de información de perfiles de una red social:

```{code-cell} python
---
tags: [hide-output]
mystnb:
  number_source_lines: true
---
# Estructura básica de un Spider de Scrapy para Instagram
# Este código muestra la estructura, pero no se ejecuta directamente en el notebook

codigo_spider = '''
import scrapy
import json
from datetime import datetime

class InstagramSpider(scrapy.Spider):
    """
    Spider para extraer información de perfiles de Instagram.
    Nota: Este es un ejemplo educativo.
    """
    name = 'instagram_spider'
    
    # Configuración personalizada
    custom_settings = {
        'DOWNLOAD_DELAY': 2,  # Espera 2 segundos entre peticiones
        'ROBOTSTXT_OBEY': True,
        'USER_AGENT': 'Mozilla/5.0 (compatible; InstagramSpider/1.0)',
        'FEEDS': {
            'instagram_data.jsonl': {
                'format': 'jsonlines',
                'encoding': 'utf-8',
                'overwrite': False,
            },
        },
    }
    
    def start_requests(self):
        """Define las URLs iniciales para comenzar el scraping."""
        # En un caso real, estas serían URLs de perfiles de Instagram
        perfiles = [
            'https://example.com/perfil1',
            'https://example.com/perfil2',
        ]
        
        for url in perfiles:
            yield scrapy.Request(url=url, callback=self.parse_perfil)
    
    def parse_perfil(self, response):
        """
        Extrae información del perfil de usuario.
        """
        # Extraer información del perfil
        perfil = {
            'username': response.css('h1.username::text').get(),
            'nombre_completo': response.css('div.nombre::text').get(),
            'biografia': response.css('div.bio::text').get(),
            'num_publicaciones': response.css('span.posts::text').get(),
            'num_seguidores': response.css('span.followers::text').get(),
            'num_seguidos': response.css('span.following::text').get(),
            'url': response.url,
            'fecha_scraping': datetime.now().isoformat(),
        }
        
        yield perfil
        
        # Seguir enlaces a las publicaciones
        enlaces_posts = response.css('a.post-link::attr(href)').getall()
        for enlace in enlaces_posts[:12]:  # Limitar a 12 posts
            yield response.follow(enlace, callback=self.parse_publicacion)
    
    def parse_publicacion(self, response):
        """
        Extrae información de una publicación individual.
        """
        publicacion = {
            'tipo': 'publicacion',
            'url': response.url,
            'descripcion': response.css('div.caption::text').get(),
            'likes': response.css('span.likes::text').get(),
            'comentarios': response.css('span.comments::text').get(),
            'fecha_publicacion': response.css('time::attr(datetime)').get(),
            'hashtags': response.css('a.hashtag::text').getall(),
            'fecha_scraping': datetime.now().isoformat(),
        }
        
        yield publicacion
'''

print("=== Estructura de un Spider para Instagram ===")
print(codigo_spider)
```

### Simulación de Datos Extraídos

Ya que no podemos ejecutar Scrapy directamente en este notebook, simulemos los datos que obtendríamos:

```{code-cell} python
---
tags: [hide-output]
---
def generar_datos_instagram_ejemplo():
    """Genera datos de ejemplo simulando extracción de Instagram."""
    
    # Datos de perfiles
    perfiles = [
        {
            "tipo": "perfil",
            "username": "fotografia_urbana",
            "nombre_completo": "María Fotógrafa",
            "biografia": "Capturando momentos en la ciudad 📸 | Buenos Aires",
            "num_publicaciones": 324,
            "num_seguidores": 12500,
            "num_seguidos": 892,
            "url": "https://example.com/fotografia_urbana",
            "fecha_scraping": datetime.now().isoformat()
        },
        {
            "tipo": "perfil",
            "username": "chef_casero",
            "nombre_completo": "Carlos Cocina",
            "biografia": "Recetas fáciles para todos 🍳 | Chef amateur",
            "num_publicaciones": 187,
            "num_seguidores": 8300,
            "num_seguidos": 456,
            "url": "https://example.com/chef_casero",
            "fecha_scraping": datetime.now().isoformat()
        },
        {
            "tipo": "perfil",
            "username": "viajes_aventura",
            "nombre_completo": "Ana Exploradora",
            "biografia": "Recorriendo el mundo 🌍 | Travel blogger",
            "num_publicaciones": 456,
            "num_seguidores": 23400,
            "num_seguidos": 1234,
            "url": "https://example.com/viajes_aventura",
            "fecha_scraping": datetime.now().isoformat()
        }
    ]
    
    # Datos de publicaciones
    publicaciones = [
        {
            "tipo": "publicacion",
            "username": "fotografia_urbana",
            "url": "https://example.com/p/ABC123",
            "descripcion": "Atardecer en el centro #fotografia #atardecer #buenosaires",
            "likes": 1234,
            "comentarios": 45,
            "fecha_publicacion": "2024-01-15T18:30:00Z",
            "hashtags": ["fotografia", "atardecer", "buenosaires"],
            "fecha_scraping": datetime.now().isoformat()
        },
        {
            "tipo": "publicacion",
            "username": "chef_casero",
            "url": "https://example.com/p/DEF456",
            "descripcion": "Pasta casera 🍝 #recetas #cocina #pasta",
            "likes": 876,
            "comentarios": 32,
            "fecha_publicacion": "2024-01-16T12:15:00Z",
            "hashtags": ["recetas", "cocina", "pasta"],
            "fecha_scraping": datetime.now().isoformat()
        },
        {
            "tipo": "publicacion",
            "username": "viajes_aventura",
            "url": "https://example.com/p/GHI789",
            "descripcion": "Montañas de Patagonia ⛰️ #viajes #patagonia #naturaleza",
            "likes": 2341,
            "comentarios": 89,
            "fecha_publicacion": "2024-01-17T09:45:00Z",
            "hashtags": ["viajes", "patagonia", "naturaleza"],
            "fecha_scraping": datetime.now().isoformat()
        }
    ]
    
    return perfiles + publicaciones

# Generar datos de ejemplo
datos_instagram = generar_datos_instagram_ejemplo()

print("=== Datos extraídos de Instagram (simulados) ===")
print(f"Total de registros: {len(datos_instagram)}")
print(f"\nEjemplo de perfil:")
print(json.dumps(datos_instagram[0], indent=2, ensure_ascii=False))
```

### Persistencia de Datos en JSONL

Guardemos los datos extraídos en formato JSONL, que es ideal para procesar grandes volúmenes de datos:

```{code-cell} python
---
tags: [hide-output]
---
# Guardar en formato JSONL
archivo_instagram = "/tmp/instagram_data.jsonl"

with open(archivo_instagram, 'w', encoding='utf-8') as f:
    for item in datos_instagram:
        f.write(json.dumps(item, ensure_ascii=False) + '\n')

print(f"Datos guardados en {archivo_instagram}")

# Verificar
with open(archivo_instagram, 'r', encoding='utf-8') as f:
    lineas = f.readlines()
    print(f"\nTotal de líneas en el archivo: {len(lineas)}")
    print("\nPrimera línea (perfil):")
    print(json.dumps(json.loads(lineas[0]), indent=2, ensure_ascii=False)[:200] + "...")
```

### Análisis de Datos de Instagram

Ahora analicemos los datos extraídos:

```{code-cell} python
---
tags: [hide-output]
mystnb:
  number_source_lines: true
---
def analizar_datos_instagram(archivo):
    """Analiza los datos extraídos de Instagram."""
    
    perfiles = []
    publicaciones = []
    hashtags_counter = {}
    
    with open(archivo, 'r', encoding='utf-8') as f:
        for linea in f:
            item = json.loads(linea)
            
            if item.get("tipo") == "perfil":
                perfiles.append(item)
            elif item.get("tipo") == "publicacion":
                publicaciones.append(item)
                
                # Contar hashtags
                for hashtag in item.get("hashtags", []):
                    hashtags_counter[hashtag] = hashtags_counter.get(hashtag, 0) + 1
    
    # Calcular estadísticas
    estadisticas = {
        "total_perfiles": len(perfiles),
        "total_publicaciones": len(publicaciones),
        "promedio_seguidores": sum(p.get("num_seguidores", 0) for p in perfiles) / len(perfiles) if perfiles else 0,
        "promedio_publicaciones": sum(p.get("num_publicaciones", 0) for p in perfiles) / len(perfiles) if perfiles else 0,
        "total_likes": sum(p.get("likes", 0) for p in publicaciones),
        "total_comentarios": sum(p.get("comentarios", 0) for p in publicaciones),
        "hashtags_populares": sorted(hashtags_counter.items(), key=lambda x: x[1], reverse=True)[:10],
    }
    
    return estadisticas, perfiles, publicaciones

# Analizar los datos
stats, perfiles, publicaciones = analizar_datos_instagram(archivo_instagram)

print("=== Análisis de Datos de Instagram ===\n")
print(f"Perfiles analizados: {stats['total_perfiles']}")
print(f"Publicaciones analizadas: {stats['total_publicaciones']}")
print(f"Promedio de seguidores: {stats['promedio_seguidores']:.0f}")
print(f"Promedio de publicaciones por perfil: {stats['promedio_publicaciones']:.0f}")
print(f"Total de likes: {stats['total_likes']}")
print(f"Total de comentarios: {stats['total_comentarios']}")

print("\n=== Hashtags más populares ===")
for hashtag, count in stats['hashtags_populares']:
    print(f"#{hashtag}: {count} veces")
```

### Exportar a CSV para Análisis

Finalmente, exportemos los datos a formato CSV para facilitar el análisis en otras herramientas:

```{code-cell} python
---
tags: [hide-output]
---
import csv

def exportar_perfiles_a_csv(perfiles, archivo):
    """Exporta los perfiles a un archivo CSV."""
    if not perfiles:
        return
    
    campos = ["username", "nombre_completo", "biografia", 
              "num_publicaciones", "num_seguidores", "num_seguidos"]
    
    with open(archivo, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=campos, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(perfiles)

def exportar_publicaciones_a_csv(publicaciones, archivo):
    """Exporta las publicaciones a un archivo CSV."""
    if not publicaciones:
        return
    
    # Preparar datos (convertir lista de hashtags a string)
    pubs_procesadas = []
    for pub in publicaciones:
        pub_copia = pub.copy()
        pub_copia['hashtags'] = ', '.join(pub.get('hashtags', []))
        pubs_procesadas.append(pub_copia)
    
    campos = ["username", "descripcion", "likes", "comentarios", 
              "fecha_publicacion", "hashtags"]
    
    with open(archivo, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=campos, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(pubs_procesadas)

# Exportar a CSV
archivo_perfiles_csv = "/tmp/instagram_perfiles.csv"
archivo_publicaciones_csv = "/tmp/instagram_publicaciones.csv"

exportar_perfiles_a_csv(perfiles, archivo_perfiles_csv)
exportar_publicaciones_a_csv(publicaciones, archivo_publicaciones_csv)

print(f"Perfiles exportados a: {archivo_perfiles_csv}")
print(f"Publicaciones exportadas a: {archivo_publicaciones_csv}")

# Mostrar contenido de los CSV
print("\n=== Contenido de perfiles.csv ===")
with open(archivo_perfiles_csv, 'r', encoding='utf-8') as f:
    print(f.read())

print("\n=== Contenido de publicaciones.csv ===")
with open(archivo_publicaciones_csv, 'r', encoding='utf-8') as f:
    print(f.read())
```

### Visualización con Mermaid

Podemos visualizar el proceso de scraping con un diagrama:

```{mermaid}
---
name: instagram_scraping_flow
title: Flujo de Scraping de Instagram
---
flowchart TB
    A[Inicio del Spider] --> B[Lista de perfiles a extraer]
    B --> C{Procesar perfil}
    C --> D[Extraer datos del perfil]
    D --> E[Guardar perfil en JSONL]
    E --> F[Obtener enlaces de publicaciones]
    F --> G{¿Hay más publicaciones?}
    G -->|Sí| H[Extraer datos de publicación]
    H --> I[Guardar publicación en JSONL]
    I --> G
    G -->|No| J{¿Hay más perfiles?}
    J -->|Sí| C
    J -->|No| K[Analizar datos]
    K --> L[Generar estadísticas]
    L --> M[Exportar a CSV]
    M --> N[Fin]
    
    style A fill:#90EE90,stroke:#006400,stroke-width:2px
    style N fill:#90EE90,stroke:#006400,stroke-width:2px
    style E fill:#87CEEB,stroke:#4682B4,stroke-width:2px
    style I fill:#87CEEB,stroke:#4682B4,stroke-width:2px
    style L fill:#FFD700,stroke:#FF8C00,stroke-width:2px
    style M fill:#FFD700,stroke:#FF8C00,stroke-width:2px
```

## Consideraciones Éticas y Legales

Al trabajar con datos de redes sociales, es fundamental considerar:

### Aspectos Legales

- **Términos de Servicio**: Cada plataforma tiene términos que debemos respetar.
- **APIs Oficiales**: Siempre que sea posible, usar las APIs oficiales en lugar de web scraping.
- **Protección de Datos**: Cumplir con regulaciones como GDPR, CCPA y leyes locales.
- **Robots.txt**: Respetar las directivas de los archivos robots.txt.

### Aspectos Éticos

- **Privacidad**: No recopilar información sensible o personal sin consentimiento.
- **Uso Responsable**: Usar los datos solo para fines legítimos y éticos.
- **Rate Limiting**: No sobrecargar los servidores con demasiadas peticiones.
- **Transparencia**: Ser claro sobre cómo y por qué se recopilan los datos.

```{important}
Los ejemplos de este capítulo son educativos. En producción, siempre se debe:
1. Consultar con un experto legal
2. Usar APIs oficiales cuando estén disponibles
3. Obtener consentimiento cuando sea necesario
4. Implementar medidas de seguridad para proteger los datos recopilados
```

## Resumen

En este capítulo hemos explorado tres casos de estudio para la recuperación de información de redes sociales:

1. **Facebook y Grafos**: Modelamos redes sociales como grafos y aplicamos algoritmos de recorrido como DFS para analizar las relaciones entre usuarios.

2. **Twitter y JSON**: Procesamos tweets en formato JSON, tanto de streams en tiempo real como de datos históricos, extrayendo estadísticas y tendencias.

3. **Instagram y Scrapy**: Simulamos el uso de Scrapy para extraer información de perfiles y publicaciones, persistiendo los datos en diferentes formatos.

En todos los casos, implementamos mecanismos de persistencia de datos utilizando JSON, JSONL y CSV, que son formatos estándar en la industria para el almacenamiento y análisis de datos.

### Puntos Clave

- Las redes sociales generan grandes volúmenes de datos que pueden ser analizados usando estructuras de datos y algoritmos apropiados.
- Los grafos son una representación natural de las redes sociales y permiten aplicar algoritmos de teoría de grafos.
- JSON y JSONL son formatos ideales para trabajar con datos de APIs y streams.
- Scrapy es una herramienta poderosa para web scraping, pero debe usarse de manera responsable y ética.
- La persistencia de datos es crucial para poder analizar y procesar la información posteriormente.
