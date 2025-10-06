#!/usr/bin/env python3
"""
Script de ejecución para el spider de Books to Scrape.

Este script proporciona una interfaz simplificada para ejecutar el spider
con diferentes opciones y configuraciones.
"""

import argparse
import subprocess
import sys
import os
from pathlib import Path


def run_spider(
    spider_name='books',
    output_format='csv',
    output_file=None,
    log_level='INFO',
    delay=1,
    concurrent_requests=8
):
    """
    Ejecuta el spider con las opciones especificadas.
    
    Args:
        spider_name: Nombre del spider a ejecutar
        output_format: Formato de salida (csv, json, xml)
        output_file: Archivo de salida personalizado
        log_level: Nivel de logging
        delay: Delay entre requests
        concurrent_requests: Número de requests concurrentes
    """
    
    # Construir comando base
    cmd = ['scrapy', 'crawl', spider_name]
    
    # Agregar opciones de configuración
    cmd.extend(['-s', f'DOWNLOAD_DELAY={delay}'])
    cmd.extend(['-s', f'CONCURRENT_REQUESTS_PER_DOMAIN={concurrent_requests}'])
    cmd.extend(['-L', log_level])
    
    # Agregar archivo de salida si se especifica
    if output_file:
        cmd.extend(['-o', output_file])
    elif output_format:
        default_files = {
            'csv': 'books_output.csv',
            'json': 'books_output.json',
            'xml': 'books_output.xml'
        }
        if output_format in default_files:
            cmd.extend(['-o', default_files[output_format]])
    
    print(f"Ejecutando comando: {' '.join(cmd)}")
    print(f"Directorio de trabajo: {os.getcwd()}")
    
    try:
        # Ejecutar el comando
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("Spider ejecutado exitosamente!")
        print(f"Output:\n{result.stdout}")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"Error ejecutando spider: {e}")
        print(f"Error output:\n{e.stderr}")
        return False
    except FileNotFoundError:
        print("Error: Scrapy no está instalado o no está en el PATH")
        print("Instala Scrapy con: pip install scrapy")
        return False


def check_project_structure():
    """Verifica que la estructura del proyecto sea correcta."""
    required_files = [
        'scrapy.cfg',
        'books_scraper/__init__.py',
        'books_scraper/items.py',
        'books_scraper/pipelines.py',
        'books_scraper/settings.py',
        'books_scraper/spiders/__init__.py',
        'books_scraper/spiders/books.py'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("Error: Faltan archivos del proyecto:")
        for file_path in missing_files:
            print(f"  - {file_path}")
        return False
    
    print("✓ Estructura del proyecto verificada")
    return True


def main():
    """Función principal del script."""
    parser = argparse.ArgumentParser(
        description='Ejecutar spider de Books to Scrape',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python run_spider.py                          # Ejecución básica
  python run_spider.py --format json            # Salida en JSON
  python run_spider.py --output books.csv       # Archivo personalizado
  python run_spider.py --delay 2 --debug        # Con delay y debug
  python run_spider.py --concurrent 4           # 4 requests concurrentes
        """
    )
    
    parser.add_argument(
        '--spider', '-s',
        default='books',
        help='Nombre del spider a ejecutar (default: books)'
    )
    
    parser.add_argument(
        '--format', '-f',
        choices=['csv', 'json', 'xml'],
        default='csv',
        help='Formato de salida (default: csv)'
    )
    
    parser.add_argument(
        '--output', '-o',
        help='Archivo de salida personalizado'
    )
    
    parser.add_argument(
        '--delay', '-d',
        type=float,
        default=1.0,
        help='Delay entre requests en segundos (default: 1.0)'
    )
    
    parser.add_argument(
        '--concurrent', '-c',
        type=int,
        default=8,
        help='Número de requests concurrentes (default: 8)'
    )
    
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Activar modo debug (logging detallado)'
    )
    
    parser.add_argument(
        '--check',
        action='store_true',
        help='Solo verificar estructura del proyecto'
    )
    
    args = parser.parse_args()
    
    # Verificar estructura del proyecto
    if not check_project_structure():
        sys.exit(1)
    
    if args.check:
        print("Estructura del proyecto es correcta")
        sys.exit(0)
    
    # Determinar nivel de logging
    log_level = 'DEBUG' if args.debug else 'INFO'
    
    # Ejecutar spider
    success = run_spider(
        spider_name=args.spider,
        output_format=args.format,
        output_file=args.output,
        log_level=log_level,
        delay=args.delay,
        concurrent_requests=args.concurrent
    )
    
    if not success:
        sys.exit(1)
    
    print("\n✓ Ejecución completada!")
    
    # Mostrar archivos generados
    output_files = ['horror_books.csv', 'books_export.json', 'scrapy.log']
    if args.output:
        output_files.append(args.output)
    
    print("\nArchivos generados:")
    for file_path in output_files:
        if Path(file_path).exists():
            size = Path(file_path).stat().st_size
            print(f"  ✓ {file_path} ({size} bytes)")


if __name__ == '__main__':
    main()