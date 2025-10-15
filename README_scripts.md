# Scripts de Análisis de Redes Sociales

Este directorio contiene scripts de ejemplo para analizar datos de redes sociales usando APIs oficiales.

## Archivos

- `twitter.py` - Script para analizar tweets usando la API de X (Twitter)
- `.env.example` - Plantilla de configuración para credenciales
- `contenidos/Anexos/Twitter.md` - Instructivo completo para obtener credenciales de X
- `contenidos/Anexos/Facebook.md` - Instructivo completo para obtener credenciales de Facebook

## Configuración

### 1. Instalar dependencias

```bash
pip install tweepy python-dotenv facebook-sdk
```

### 2. Configurar credenciales

Opción A - Variables de entorno:
```bash
export TWITTER_BEARER_TOKEN='tu_bearer_token_aqui'
```

Opción B - Archivo .env:
```bash
cp .env.example .env
# Editar .env con tus credenciales reales
```

### 3. Obtener credenciales

- **Twitter/X**: Seguir el instructivo en `contenidos/Anexos/Twitter.md`
- **Facebook**: Seguir el instructivo en `contenidos/Anexos/Facebook.md`

## Uso

### Análisis de Twitter

```bash
python twitter.py
```

El script buscará tweets sobre "python" y "programación", guardando los resultados en archivos JSONL en `/tmp/`.

### Características del script de Twitter

- ✅ **Manejo de errores robusto**: Detecta problemas de autenticación y cuotas
- ✅ **Configuración segura**: Usa variables de entorno para credenciales
- ✅ **Formato estándar**: Guarda datos en JSONL para análisis posterior
- ✅ **Filtros inteligentes**: Excluye retweets y filtra por idioma
- ✅ **Información detallada**: Incluye métricas de engagement y autor

### Salida de ejemplo

```json
{
  "id": "1234567890",
  "created_at": "2024-01-15T10:30:00+00:00",
  "text": "Las estructuras de datos son fundamentales en #Python",
  "author": {
    "username": "developer123",
    "name": "Juan Programador", 
    "followers": 1523
  },
  "metrics": {
    "like_count": 47,
    "retweet_count": 15,
    "reply_count": 3
  },
  "lang": "es"
}
```

## Consideraciones Importantes

### Límites de API

- **Twitter Free**: 500,000 tweets/mes, 300 requests/15min
- **Facebook Graph**: Datos limitados al usuario autenticado

### Privacidad y Ética

- Solo acceder a datos públicos o autorizados
- Respetar términos de servicio de cada plataforma
- Implementar rate limiting apropiado
- No almacenar datos sensibles

### Resolución de Problemas

#### Error 403 - Forbidden
- Verificar que las credenciales sean válidas
- Asegurar que la aplicación esté asociada a un Proyecto
- Confirmar permisos de API v2

#### Error 429 - Too Many Requests  
- Esperar antes de hacer más solicitudes
- Implementar delays entre llamadas
- Considerar upgrade a tier pagado

#### Error de importación
```bash
# Instalar dependencias faltantes
pip install tweepy python-dotenv facebook-sdk
```

## Próximos Pasos

1. **Análisis avanzado**: Implementar análisis de sentimientos
2. **Visualización**: Crear gráficos de tendencias y redes
3. **Automatización**: Configurar tareas programadas
4. **Base de datos**: Persistir datos en PostgreSQL o MongoDB
5. **Dashboard**: Crear interfaz web con Streamlit o Dash

## Recursos Útiles

- [Documentación Tweepy](https://docs.tweepy.org/)
- [Twitter API v2 Docs](https://developer.twitter.com/en/docs/twitter-api)
- [Facebook Graph API](https://developers.facebook.com/docs/graph-api/)
- [Jupyter Book - Capítulo 3.8](contenidos/3-recuperacion-de-la-informacion/3-8-redes-sociales.md)