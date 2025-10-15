#!/usr/bin/env python3
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
        print("❌ Error: TWITTER_BEARER_TOKEN no encontrado en variables de entorno")
        print("\n📝 Para configurar las credenciales:")
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
        
        print(f"🔍 Buscando tweets sobre: '{query}'")
        
        # Buscar tweets recientes
        tweets = client.search_recent_tweets(
            query=f"{query} -is:retweet lang:es",  # Excluir retweets, solo español
            max_results=max_results,
            tweet_fields=["created_at", "public_metrics", "author_id", "lang"],
            expansions=["author_id"],
            user_fields=["username", "name", "public_metrics"]
        )
        
        if not tweets.data:
            print("❌ No se encontraron tweets. Verifica tu Bearer Token y cuota de API.")
            return
        
        print(f"✅ Encontrados {len(tweets.data)} tweets")
        
        # Procesar y mostrar resultados
        archivo_salida = f"/tmp/tweets_{query.replace(' ', '_')}.jsonl"
        
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
                print(f"\n📝 Tweet: {tweet.text[:100]}...")
                if author:
                    print(f"👤 Autor: @{author.username} ({author.name})")
                print(f"❤️ Likes: {tweet.public_metrics['like_count']} | "
                      f"🔄 Retweets: {tweet.public_metrics['retweet_count']}")
                
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
        
        print(f"\n💾 Tweets guardados en: {archivo_salida}")
        
    except tweepy.errors.Forbidden as e:
        print("❌ Error 403 - Acceso denegado:")
        print("   • Verifica que tu Bearer Token sea válido")
        print("   • Asegúrate de que tu aplicación esté asociada a un Proyecto")
        print("   • Revisa que tengas permisos para usar la API v2")
        print(f"   • Detalles del error: {e}")
        
    except tweepy.errors.TooManyRequests as e:
        print("❌ Error 429 - Demasiadas solicitudes:")
        print("   • Has excedido el límite de la API")
        print("   • Espera unos minutos antes de intentar de nuevo")
        print(f"   • Detalles del error: {e}")
        
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
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
        
        print("✅ Autenticación exitosa")
        if hasattr(response, "meta") and "result_count" in response.meta:
            print(f"• Resultados de búsqueda de prueba: {response.meta['result_count']}")
        print("\n📊 Información de la API:")
        print("• API Version: v2")
        print("• Tier: Free (500K tweets/mes)")
        print("• Search Recent: ✅ Disponible")
        print("• Rate Limit: Consulta los límites vigentes en la documentación oficial:")
        print("  https://developer.twitter.com/en/docs/twitter-api/rate-limits")
        
    except Exception as e:
        print(f"❌ Error al verificar API: {e}")

def main():
    """Función principal del programa"""
    
    print("🐦 Twitter/X API - Ejemplo de Análisis de Datos")
    print("=" * 50)
    
    # Verificar configuración
    print("\n1️⃣ Verificando configuración...")
    mostrar_estadisticas_api()
    
    # Buscar tweets sobre Python
    print("\n2️⃣ Buscando tweets sobre Python...")
    buscar_tweets_recientes("python", max_results=5)
    
    # Buscar tweets sobre programación
    print("\n3️⃣ Buscando tweets sobre programación...")
    buscar_tweets_recientes("programacion", max_results=5)
    
    print("\n✅ Análisis completado")
    print("\n📚 Para más información sobre cómo obtener credenciales:")
    print("    Ver: contenidos/Anexos/Twitter.md")

if __name__ == "__main__":
    # Intentar cargar variables de entorno desde .env si existe
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("📄 Variables de entorno cargadas desde .env")
    except ImportError:
        print("💡 Tip: Instala python-dotenv para usar archivos .env")
        print("    pip install python-dotenv")
    
    main()