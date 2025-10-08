#!/usr/bin/env python3
"""
Script de análisis de datos para los libros extraídos.

Este script analiza los datos CSV generados por el spider y produce
estadísticas e insights sobre los libros de horror.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import sys


def load_data(csv_file='./books_scraper/horror_books.csv'):
    """
    Carga los datos desde el archivo CSV.
    
    Args:
        csv_file: Ruta al archivo CSV
        
    Returns:
        DataFrame con los datos o None si hay error
    """
    try:
        df = pd.read_csv(csv_file)
        print(f"✓ Datos cargados: {len(df)} registros")
        return df
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {csv_file}")
        print("Ejecuta primero el spider para generar los datos")
        return None
    except Exception as e:
        print(f"Error cargando datos: {e}")
        return None


def clean_data(df):
    """
    Limpia y prepara los datos para análisis.
    
    Args:
        df: DataFrame con datos originales
        
    Returns:
        DataFrame limpio
    """
    # Crear copia para no modificar original
    df_clean = df.copy()
    
    # Limpiar precios: convertir a float
    df_clean['price'] = pd.to_numeric(df_clean['price'], errors='coerce')
    
    # Mapear ratings a números
    rating_map = {
        'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5
    }
    df_clean['rating_numeric'] = df_clean['rating'].map(rating_map)
    
    # Limpiar disponibilidad
    df_clean['in_stock'] = df_clean['availability'].str.contains(
        'In stock', case=False, na=False
    )
    
    # Extraer número de libros disponibles si está en el texto
    df_clean['stock_number'] = df_clean['availability'].str.extract(
        r'(\d+)', expand=False
    ).astype('Int64')
    
    return df_clean


def basic_statistics(df):
    """
    Calcula y muestra estadísticas básicas.
    
    Args:
        df: DataFrame con los datos
    """
    print("\n" + "="*50)
    print("ESTADÍSTICAS BÁSICAS")
    print("="*50)
    
    print(f"Total de libros: {len(df)}")
    print(f"Libros con precio válido: {df['price'].notna().sum()}")
    
    if df['price'].notna().any():
        print(f"\nPRECIOS:")
        print(f"  Precio promedio: £{df['price'].mean():.2f}")
        print(f"  Precio mediano: £{df['price'].median():.2f}")
        print(f"  Precio mínimo: £{df['price'].min():.2f}")
        print(f"  Precio máximo: £{df['price'].max():.2f}")
        print(f"  Desviación estándar: £{df['price'].std():.2f}")
    
    print(f"\nDISPONIBILIDAD:")
    availability_counts = df['availability'].value_counts()
    for availability, count in availability_counts.head().items():
        print(f"  {availability}: {count}")
    
    print(f"\nCALIFICACIONES:")
    rating_counts = df['rating'].value_counts()
    for rating, count in rating_counts.items():
        print(f"  {rating}: {count}")


def create_visualizations(df, output_dir='plots'):
    """
    Crea visualizaciones de los datos.
    
    Args:
        df: DataFrame con los datos
        output_dir: Directorio para guardar gráficos
    """
    # Crear directorio si no existe
    Path(output_dir).mkdir(exist_ok=True)
    
    # Configurar estilo
    plt.style.use('seaborn-v0_8')
    sns.set_palette("husl")
    
    # 1. Distribución de precios
    if df['price'].notna().any():
        plt.figure(figsize=(10, 6))
        plt.subplot(2, 2, 1)
        plt.hist(df['price'].dropna(), bins=20, alpha=0.7, edgecolor='black')
        plt.title('Distribución de Precios')
        plt.xlabel('Precio (£)')
        plt.ylabel('Frecuencia')
        
        # 2. Box plot de precios
        plt.subplot(2, 2, 2)
        plt.boxplot(df['price'].dropna(), vert=True)
        plt.title('Box Plot de Precios')
        plt.ylabel('Precio (£)')
    
    # 3. Distribución de calificaciones
    plt.subplot(2, 2, 3)
    rating_counts = df['rating'].value_counts()
    plt.bar(rating_counts.index, rating_counts.values)
    plt.title('Distribución de Calificaciones')
    plt.xlabel('Calificación')
    plt.ylabel('Número de Libros')
    plt.xticks(rotation=45)
    
    # 4. Disponibilidad
    plt.subplot(2, 2, 4)
    availability_counts = df['availability'].value_counts().head(5)
    plt.pie(availability_counts.values, labels=availability_counts.index, 
            autopct='%1.1f%%')
    plt.title('Distribución de Disponibilidad')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/books_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print(f"✓ Gráficos guardados en {output_dir}/books_analysis.png")


def price_analysis(df):
    """
    Análisis detallado de precios.
    
    Args:
        df: DataFrame con los datos
    """
    print("\n" + "="*50)
    print("ANÁLISIS DE PRECIOS")
    print("="*50)
    
    if not df['price'].notna().any():
        print("No hay datos de precios válidos")
        return
    
    # Quartiles
    q1 = df['price'].quantile(0.25)
    q3 = df['price'].quantile(0.75)
    iqr = q3 - q1
    
    print(f"Quartil 1 (25%): £{q1:.2f}")
    print(f"Quartil 3 (75%): £{q3:.2f}")
    print(f"Rango intercuartílico: £{iqr:.2f}")
    
    # Libros caros y baratos
    expensive_threshold = df['price'].quantile(0.9)
    cheap_threshold = df['price'].quantile(0.1)
    
    expensive_books = df[df['price'] >= expensive_threshold]
    cheap_books = df[df['price'] <= cheap_threshold]
    
    print(f"\nLIBROS MÁS CAROS (top 10%):")
    print(f"Umbral: £{expensive_threshold:.2f}")
    for _, book in expensive_books.nlargest(5, 'price').iterrows():
        print(f"  {book['title']}: £{book['price']:.2f}")
    
    print(f"\nLIBROS MÁS BARATOS (bottom 10%):")
    print(f"Umbral: £{cheap_threshold:.2f}")
    for _, book in cheap_books.nsmallest(5, 'price').iterrows():
        print(f"  {book['title']}: £{book['price']:.2f}")


def rating_analysis(df):
    """
    Análisis detallado de calificaciones.
    
    Args:
        df: DataFrame con los datos
    """
    print("\n" + "="*50)
    print("ANÁLISIS DE CALIFICACIONES")
    print("="*50)
    
    if 'rating_numeric' not in df.columns:
        print("No hay datos de calificaciones válidos")
        return
    
    # Estadísticas de rating
    valid_ratings = df['rating_numeric'].notna()
    if valid_ratings.any():
        avg_rating = df.loc[valid_ratings, 'rating_numeric'].mean()
        print(f"Calificación promedio: {avg_rating:.2f}/5")
        
        rating_dist = df['rating_numeric'].value_counts().sort_index()
        print(f"\nDistribución detallada:")
        for rating, count in rating_dist.items():
            percentage = (count / len(df)) * 100
            stars = "★" * int(rating) + "☆" * (5 - int(rating))
            print(f"  {stars} ({rating}): {count} libros ({percentage:.1f}%)")
    
    # Relación precio-calificación
    if df['price'].notna().any() and valid_ratings.any():
        price_by_rating = df.groupby('rating_numeric')['price'].agg([
            'count', 'mean', 'median', 'std'
        ]).round(2)
        
        print(f"\nPrecio promedio por calificación:")
        for rating, stats in price_by_rating.iterrows():
            if pd.notna(rating):
                print(f"  {int(rating)} estrella(s): £{stats['mean']:.2f} "
                      f"(n={stats['count']})")


def export_summary(df, output_file='books_summary.txt'):
    """
    Exporta un resumen completo a archivo de texto.
    
    Args:
        df: DataFrame con los datos
        output_file: Archivo de salida
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("RESUMEN DE ANÁLISIS - LIBROS DE HORROR\n")
        f.write("="*50 + "\n\n")
        
        f.write(f"Fecha de análisis: {pd.Timestamp.now()}\n")
        f.write(f"Total de libros analizados: {len(df)}\n\n")
        
        if df['price'].notna().any():
            f.write("ESTADÍSTICAS DE PRECIOS:\n")
            f.write(f"  Precio promedio: £{df['price'].mean():.2f}\n")
            f.write(f"  Precio mediano: £{df['price'].median():.2f}\n")
            f.write(f"  Rango de precios: £{df['price'].min():.2f} - "
                   f"£{df['price'].max():.2f}\n\n")
        
        f.write("TOP 10 LIBROS:\n")
        for i, (_, book) in enumerate(df.head(10).iterrows(), 1):
            f.write(f"  {i:2d}. {book['title']}\n")
            f.write(f"      Precio: £{book['price']:.2f} | "
                   f"Rating: {book['rating']}\n")
    
    print(f"✓ Resumen exportado a {output_file}")


def main():
    """Función principal del script de análisis."""
    print("ANÁLISIS DE LIBROS DE HORROR")
    print("="*50)
    
    # Verificar si matplotlib está disponible
    try:
        import matplotlib.pyplot as plt
        import seaborn as sns
        plots_available = True
    except ImportError:
        print("Nota: matplotlib/seaborn no disponibles. "
              "No se generarán gráficos.")
        plots_available = False
    
    # Cargar datos
    df = load_data()
    if df is None:
        sys.exit(1)
    
    # Limpiar datos
    df_clean = clean_data(df)
    
    # Realizar análisis
    basic_statistics(df_clean)
    price_analysis(df_clean)
    rating_analysis(df_clean)
    
    # Crear visualizaciones si es posible
    if plots_available:
        try:
            create_visualizations(df_clean)
        except Exception as e:
            print(f"Error creando visualizaciones: {e}")
    
    # Exportar resumen
    export_summary(df_clean)
    
    print(f"\n✓ Análisis completado!")
    print(f"  - Datos analizados: {len(df_clean)} libros")
    print(f"  - Archivos generados: books_summary.txt")
    if plots_available:
        print(f"  - Gráficos: plots/books_analysis.png")


if __name__ == '__main__':
    main()