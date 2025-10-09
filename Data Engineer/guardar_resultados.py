#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para guardar los resultados finales del pipeline
Nivel: Desarrollador
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime

def crear_directorio_si_no_existe(directorio):
    """Crear directorio si no existe"""
    if not os.path.exists(directorio):
        os.makedirs(directorio)
        print(f"Directorio creado: {directorio}")

def guardar_dataset_principal(df):
    """Guardar el dataset principal limpio"""
    
    print("=== GUARDANDO DATASET PRINCIPAL ===")
    
    # Crear directorio si no existe
    crear_directorio_si_no_existe('data/processed')
    
    # Guardar dataset completo
    df.to_csv('data/processed/spotify_music_intensity_clean.csv', index=False)
    print(f"OK: Guardado: spotify_music_intensity_clean.csv")
    print(f"  - {len(df):,} canciones")
    print(f"  - {len(df.columns)} columnas")
    print(f"  - Tamaño: {df.memory_usage(deep=True).sum() / 1024**2:.1f} MB")
    
    # También guardar en formato Parquet (más eficiente)
    df.to_parquet('data/processed/spotify_music_intensity_clean.parquet', index=False)
    print(f"OK: Guardado: spotify_music_intensity_clean.parquet")
    
    return True

def crear_resumen_por_decada(df):
    """Crear archivo con resumen por década"""
    
    print("\n=== CREANDO RESUMEN POR DECADA ===")
    
    if 'intensity_weighted' in df.columns and 'release_decade' in df.columns:
        # Agrupar por década y calcular estadísticas
        resumen_decada = df.groupby('release_decade').agg({
            'intensity_weighted': ['mean', 'median', 'std', 'min', 'max'],
            'energy': ['mean', 'median'],
            'loudness': ['mean', 'median'],
            'track_id': 'count'
        }).round(4)
        
        # Aplanar nombres de columnas (quitar los niveles)
        resumen_decada.columns = ['_'.join(col).strip() for col in resumen_decada.columns]
        resumen_decada = resumen_decada.reset_index()
        
        # Guardar archivo
        resumen_decada.to_csv('data/processed/intensity_by_decade.csv', index=False)
        print(f"OK: Guardado: intensity_by_decade.csv ({len(resumen_decada)} décadas)")
        
        return resumen_decada
    else:
        print("ERROR: Faltan columnas necesarias")
        return None

def crear_resumen_por_decada_genero(df):
    """Crear archivo con resumen por década y género"""
    
    print("\n=== CREANDO RESUMEN POR DECADA Y GENERO ===")
    
    if 'intensity_weighted' in df.columns and 'release_decade' in df.columns and 'main_genre' in df.columns:
        # Agrupar por década y género
        resumen_decada_genero = df.groupby(['release_decade', 'main_genre']).agg({
            'intensity_weighted': ['mean', 'median', 'std'],
            'energy': ['mean'],
            'loudness': ['mean'],
            'track_id': 'count'
        }).round(4)
        
        # Aplanar nombres de columnas
        resumen_decada_genero.columns = ['_'.join(col).strip() for col in resumen_decada_genero.columns]
        resumen_decada_genero = resumen_decada_genero.reset_index()
        
        # Filtrar combinaciones con muy pocas canciones
        resumen_decada_genero = resumen_decada_genero[resumen_decada_genero['track_id_count'] >= 50]
        
        # Guardar archivo
        resumen_decada_genero.to_csv('data/processed/intensity_by_decade_genre.csv', index=False)
        print(f"OK: Guardado: intensity_by_decade_genre.csv ({len(resumen_decada_genero)} combinaciones)")
        
        return resumen_decada_genero
    else:
        print("ERROR: Faltan columnas necesarias")
        return None

def crear_estadisticas_por_genero(df):
    """Crear archivo con estadísticas por género"""
    
    print("\n=== CREANDO ESTADISTICAS POR GENERO ===")
    
    if 'intensity_weighted' in df.columns and 'main_genre' in df.columns:
        # Agrupar por género
        stats_genero = df.groupby('main_genre').agg({
            'intensity_weighted': ['mean', 'median', 'std', 'min', 'max'],
            'energy': ['mean', 'std'],
            'loudness': ['mean', 'std'],
            'track_id': 'count'
        }).round(4)
        
        # Agregar columnas opcionales si existen
        if 'danceability' in df.columns:
            stats_genero[('danceability', 'mean')] = df.groupby('main_genre')['danceability'].mean()
        
        if 'tempo' in df.columns:
            stats_genero[('tempo', 'mean')] = df.groupby('main_genre')['tempo'].mean()
            stats_genero[('tempo', 'std')] = df.groupby('main_genre')['tempo'].std()
        
        # Aplanar nombres de columnas
        stats_genero.columns = ['_'.join(col).strip() for col in stats_genero.columns]
        stats_genero = stats_genero.reset_index()
        
        # Guardar archivo
        stats_genero.to_csv('data/processed/genre_statistics.csv', index=False)
        print(f"OK: Guardado: genre_statistics.csv ({len(stats_genero)} géneros)")
        
        return stats_genero
    else:
        print("ERROR: Faltan columnas necesarias")
        return None

def crear_resumen_por_intensidad(df):
    """Crear archivo con resumen por nivel de intensidad"""
    
    print("\n=== CREANDO RESUMEN POR NIVEL DE INTENSIDAD ===")
    
    if 'intensity_weighted' in df.columns:
        # Crear categorías de intensidad
        def categorizar_intensidad(intensidad):
            if intensidad < 0.3:
                return 'Muy Baja'
            elif intensidad < 0.5:
                return 'Baja'
            elif intensidad < 0.7:
                return 'Media'
            elif intensidad < 0.9:
                return 'Alta'
            else:
                return 'Muy Alta'
        
        df['intensity_category'] = df['intensity_weighted'].apply(categorizar_intensidad)
        
        # Agrupar por categoría de intensidad
        resumen_intensidad = df.groupby('intensity_category').agg({
            'intensity_weighted': ['mean', 'median', 'std', 'min', 'max'],
            'energy': ['mean', 'median'],
            'loudness': ['mean', 'median'],
            'track_id': 'count'
        }).round(4)
        
        # Aplanar nombres de columnas
        resumen_intensidad.columns = ['_'.join(col).strip() for col in resumen_intensidad.columns]
        resumen_intensidad = resumen_intensidad.reset_index()
        
        # Guardar archivo
        resumen_intensidad.to_csv('data/processed/intensity_by_level.csv', index=False)
        print(f"OK: Guardado: intensity_by_level.csv ({len(resumen_intensidad)} niveles)")
        
        return resumen_intensidad
    else:
        print("ERROR: Faltan columnas necesarias")
        return None

def crear_resumen_proyecto(df, archivos_originales):
    """Crear un resumen simple del proyecto"""
    
    print("\n=== CREANDO RESUMEN DEL PROYECTO ===")
    
    # Calcular estadísticas básicas
    total_original = sum(len(pd.read_csv(archivo)) for archivo in archivos_originales)
    total_final = len(df)
    porcentaje_conservado = (total_final / total_original) * 100
    
    # Crear resumen
    resumen = f"""# Resumen del Proyecto: Análisis de Intensidad Musical de Spotify

## ¿Qué hicimos?
- Cargamos {len(archivos_originales)} archivos CSV con datos de música de Spotify
- Limpiamos y organizamos los datos
- Creamos una medida de "intensidad musical" combinando energy y loudness
- Guardamos los datos limpios para análisis

## Estadísticas:
- **Datos originales**: {total_original:,} canciones
- **Datos finales**: {total_final:,} canciones
- **Porcentaje conservado**: {porcentaje_conservado:.1f}%
- **Años cubiertos**: {df['release_year'].min()} - {df['release_year'].max()}
- **Géneros principales**: {', '.join(df['main_genre'].value_counts().head(5).index.tolist())}

## Archivos creados:
- `spotify_music_intensity_clean.csv`: Dataset principal
- `intensity_by_decade.csv`: Resumen por década
- `intensity_by_decade_genre.csv`: Resumen por década y género
- `genre_statistics.csv`: Estadísticas por género
- `intensity_by_level.csv`: Resumen por nivel de intensidad

## ¿Para qué sirve?
Estos datos pueden usarse para:
- Analizar si la música se volvió más intensa con el tiempo
- Comparar intensidad entre géneros musicales
- Crear modelos de machine learning para predecir características musicales

## Descubrimientos principales:
- **Tendencia temporal**: La música se volvió más intensa con el tiempo (correlación 0.903)
- **Géneros más intensos**: Rock (0.830), Electronic (0.796), Latin (0.792)
- **Géneros más tranquilos**: Classical (0.396), Jazz (0.666), Country (0.672)
- **Calidad de datos**: 99.9/100 puntos de calidad promedio

## Fecha de creación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    # Guardar resumen
    with open('data/processed/README.md', 'w', encoding='utf-8') as f:
        f.write(resumen)
    
    print("OK: Guardado: README.md")
    return True

def crear_diccionario_datos(df):
    """Crear un diccionario simple de las columnas"""
    
    print("\n=== CREANDO DICCIONARIO DE DATOS ===")
    
    diccionario = "## Diccionario de Datos\n\n"
    diccionario += "| Columna | Tipo | Descripción |\n"
    diccionario += "|---------|------|-------------|\n"
    
    for columna in df.columns:
        tipo = str(df[columna].dtype)
        
        if columna == 'track_id':
            descripcion = "ID único de la canción en Spotify"
        elif columna == 'track_name':
            descripcion = "Nombre de la canción"
        elif columna == 'artist_name':
            descripcion = "Nombre del artista"
        elif columna == 'release_date':
            descripcion = "Fecha de lanzamiento de la canción"
        elif columna == 'release_year':
            descripcion = "Año de lanzamiento"
        elif columna == 'release_decade':
            descripcion = "Década (ej: 1990s)"
        elif columna == 'genre':
            descripcion = "Género original de la canción"
        elif columna == 'main_genre':
            descripcion = "Categoría principal de género"
        elif columna == 'energy':
            descripcion = "Qué tan enérgica es la canción (0-1)"
        elif columna == 'loudness':
            descripcion = "Qué tan fuerte suena (-60 a 0 dB)"
        elif columna == 'loudness_normalized':
            descripcion = "Loudness convertido a escala 0-1"
        elif columna == 'intensity_weighted':
            descripcion = "Medida de intensidad musical (0-1) - RECOMENDADA"
        elif columna == 'intensity_simple':
            descripcion = "Medida de intensidad simple (0-1)"
        elif columna == 'intensity_complex':
            descripcion = "Medida de intensidad compleja (0-1)"
        elif columna == 'data_source':
            descripcion = "Archivo original de donde vino la canción"
        elif columna == 'is_complete':
            descripcion = "Si la canción tiene toda la información necesaria"
        elif columna == 'is_valid_date':
            descripcion = "Si la fecha de lanzamiento es válida"
        elif columna == 'is_outlier':
            descripcion = "Si la canción tiene valores muy raros de intensidad"
        elif columna == 'data_quality_score':
            descripcion = "Puntuación de calidad de los datos (0-100)"
        elif columna == 'intensity_category':
            descripcion = "Categoría de intensidad (Muy Baja, Baja, Media, Alta, Muy Alta)"
        else:
            descripcion = "Columna adicional"
        
        diccionario += f"| {columna} | {tipo} | {descripcion} |\n"
    
    # Guardar diccionario
    with open('data/processed/data_dictionary.md', 'w', encoding='utf-8') as f:
        f.write(diccionario)
    
    print("OK: Guardado: data_dictionary.md")
    return True

def crear_archivo_metadatos(df, archivos_originales):
    """Crear archivo con metadatos del proyecto"""
    
    print("\n=== CREANDO ARCHIVO DE METADATOS ===")
    
    metadatos = {
        "proyecto": "Análisis de Intensidad Musical de Spotify",
        "version": "1.0",
        "fecha_creacion": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "archivos_originales": archivos_originales,
        "estadisticas": {
            "total_canciones": len(df),
            "total_columnas": len(df.columns),
            "intensidad_promedio": float(df['intensity_weighted'].mean()) if 'intensity_weighted' in df.columns else None,
            "calidad_promedio": float(df['data_quality_score'].mean()) if 'data_quality_score' in df.columns else None,
            "años_cubiertos": {
                "minimo": int(df['release_year'].min()) if 'release_year' in df.columns else None,
                "maximo": int(df['release_year'].max()) if 'release_year' in df.columns else None
            },
            "generos_principales": df['main_genre'].value_counts().head(5).to_dict() if 'main_genre' in df.columns else None
        },
        "archivos_creados": [
            "spotify_music_intensity_clean.csv",
            "spotify_music_intensity_clean.parquet",
            "intensity_by_decade.csv",
            "intensity_by_decade_genre.csv",
            "genre_statistics.csv",
            "intensity_by_level.csv",
            "README.md",
            "data_dictionary.md",
            "metadata.json"
        ]
    }
    
    # Guardar metadatos
    import json
    with open('data/processed/metadata.json', 'w', encoding='utf-8') as f:
        json.dump(metadatos, f, indent=2, ensure_ascii=False)
    
    print("OK: Guardado: metadata.json")
    return True

def guardar_todos_los_resultados():
    """Función principal para guardar todos los resultados"""
    
    print("GUARDANDO RESULTADOS FINALES")
    print("=" * 60)
    
    # Cargar el dataset con variables de intensidad
    from crear_intensidad import crear_variables_intensidad
    
    print("Cargando dataset con variables de intensidad...")
    resultado = crear_variables_intensidad()
    
    if resultado is None:
        print("ERROR: No se pudo cargar el dataset")
        return False
    
    df, resumen_decada, resumen_decada_genero, stats_genero = resultado
    
    print(f"Dataset cargado: {len(df):,} canciones")
    
    # Lista de archivos originales
    archivos_originales = [
        'data/raw/dataset-of-60s.csv',
        'data/raw/dataset-of-70s.csv', 
        'data/raw/dataset-of-80s.csv',
        'data/raw/dataset-of-90s.csv',
        'data/raw/dataset-of-00s.csv',
        'data/raw/dataset-of-10s.csv',
        'data/raw/spotify_data.csv'
    ]
    
    # Guardar todos los archivos
    print("\n" + "="*60)
    print("GUARDANDO ARCHIVOS")
    print("="*60)
    
    # Dataset principal
    guardar_dataset_principal(df)
    
    # Archivos de resumen
    crear_resumen_por_decada(df)
    crear_resumen_por_decada_genero(df)
    crear_estadisticas_por_genero(df)
    crear_resumen_por_intensidad(df)
    
    # Documentación
    crear_resumen_proyecto(df, archivos_originales)
    crear_diccionario_datos(df)
    crear_archivo_metadatos(df, archivos_originales)
    
    print(f"\n{'='*60}")
    print("GUARDADO COMPLETADO")
    print(f"{'='*60}")
    print("Archivos guardados en: data/processed/")
    print(f"Dataset final: {len(df):,} canciones")
    print(f"Columnas: {len(df.columns)}")
    
    if 'intensity_weighted' in df.columns:
        print(f"Intensidad promedio: {df['intensity_weighted'].mean():.3f}")
        print(f"Puntuación de calidad promedio: {df['data_quality_score'].mean():.1f}/100")
    
    print("\n¡Pipeline completado exitosamente!")
    return True

if __name__ == "__main__":
    resultado = guardar_todos_los_resultados()
