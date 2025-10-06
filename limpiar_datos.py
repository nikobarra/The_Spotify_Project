#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para limpiar los datos de Spotify
Nivel: Desarrollador
"""

import pandas as pd
import numpy as np
import os

def eliminar_duplicados(df, nombre_archivo):
    """Función para eliminar duplicados de un DataFrame"""
    
    print(f"\n=== ELIMINANDO DUPLICADOS: {nombre_archivo} ===")
    print(f"Registros antes: {len(df)}")
    
    # Opción 1: Si existe track_id, usarlo como clave única
    if 'track_id' in df.columns:
        duplicados = df.duplicated(subset=['track_id']).sum()
        print(f"Duplicados por track_id: {duplicados}")
        df = df.drop_duplicates(subset=['track_id'], keep='first')
    
    # Opción 2: Si existe uri, usarlo como clave única
    elif 'uri' in df.columns:
        duplicados = df.duplicated(subset=['uri']).sum()
        print(f"Duplicados por URI: {duplicados}")
        df = df.drop_duplicates(subset=['uri'], keep='first')
    
    # Opción 3: Si no hay identificador único, usar nombre + artista
    elif 'track' in df.columns and 'artist' in df.columns:
        duplicados = df.duplicated(subset=['track', 'artist']).sum()
        print(f"Duplicados por nombre+artista: {duplicados}")
        df = df.drop_duplicates(subset=['track', 'artist'], keep='first')
    
    # Opción 4: Eliminar filas exactamente iguales
    else:
        duplicados = df.duplicated().sum()
        print(f"Duplicados exactos: {duplicados}")
        df = df.drop_duplicates(keep='first')
    
    print(f"Registros después: {len(df)}")
    print(f"Eliminados: {duplicados}")
    
    return df

def arreglar_valores_criticos(df):
    """Arreglar valores faltantes en columnas críticas"""
    
    print("\n--- Arreglando valores críticos ---")
    
    # Si energy o loudness faltan, eliminar la canción
    if 'energy' in df.columns and 'loudness' in df.columns:
        antes = len(df)
        df = df.dropna(subset=['energy', 'loudness'])
        despues = len(df)
        print(f"Eliminadas {antes - despues} canciones sin energy o loudness")
    
    # Verificar que energy esté entre 0 y 1
    if 'energy' in df.columns:
        antes = len(df)
        df = df[(df['energy'] >= 0) & (df['energy'] <= 1)]
        despues = len(df)
        if antes != despues:
            print(f"Eliminadas {antes - despues} canciones con energy fuera de rango (0-1)")
    
    # Verificar que loudness esté entre -60 y 0
    if 'loudness' in df.columns:
        antes = len(df)
        df = df[(df['loudness'] >= -60) & (df['loudness'] <= 0)]
        despues = len(df)
        if antes != despues:
            print(f"Eliminadas {antes - despues} canciones con loudness fuera de rango (-60 a 0)")
    
    return df

def arreglar_fechas(df):
    """Arreglar fechas de lanzamiento"""
    
    print("\n--- Arreglando fechas ---")
    
    # Si hay columna year, crear release_date
    if 'year' in df.columns:
        # Eliminar canciones sin año
        antes = len(df)
        df = df.dropna(subset=['year'])
        despues = len(df)
        if antes != despues:
            print(f"Eliminadas {antes - despues} canciones sin año")
        
        # Crear release_date a partir del año
        df['release_date'] = pd.to_datetime(df['year'].astype(str) + '-01-01', errors='coerce')
        
        # Eliminar fechas que no se pudieron convertir
        antes = len(df)
        df = df.dropna(subset=['release_date'])
        despues = len(df)
        if antes != despues:
            print(f"Eliminadas {antes - despues} canciones con fechas inválidas")
        
        # Eliminar fechas muy raras (antes de 1920 o después de 2024)
        antes = len(df)
        df = df[(df['release_date'].dt.year >= 1920) & (df['release_date'].dt.year <= 2024)]
        despues = len(df)
        if antes != despues:
            print(f"Eliminadas {antes - despues} canciones con fechas fuera de rango (1920-2024)")
    
    return df

def arreglar_generos(df):
    """Arreglar géneros faltantes"""
    
    print("\n--- Arreglando géneros ---")
    
    # Si no hay columna genre, crear una
    if 'genre' not in df.columns:
        df['genre'] = 'Unknown'
        print("Creada columna genre con valor 'Unknown'")
    else:
        # Si no hay género, poner "Unknown"
        antes = df['genre'].isnull().sum()
        df['genre'] = df['genre'].fillna('Unknown')
        if antes > 0:
            print(f"Reemplazados {antes} géneros nulos con 'Unknown'")
        
        # Limpiar géneros (quitar espacios, convertir a minúsculas)
        df['genre'] = df['genre'].str.strip().str.lower()
    
    return df

def arreglar_energy(df):
    """Arreglar valores de energy"""
    
    print("\n--- Arreglando energy ---")
    
    if 'energy' in df.columns:
        # Si energy está en escala 0-100, convertir a 0-1
        if df['energy'].max() > 1:
            print("Convirtiendo energy de escala 0-100 a 0-1")
            df['energy'] = df['energy'] / 100
        
        # Asegurar que esté entre 0 y 1
        df['energy'] = df['energy'].clip(0, 1)
    
    return df

def arreglar_loudness(df):
    """Arreglar valores de loudness"""
    
    print("\n--- Arreglando loudness ---")
    
    if 'loudness' in df.columns:
        # Asegurar que esté entre -60 y 0
        df['loudness'] = df['loudness'].clip(-60, 0)
        
        # Crear una versión normalizada entre 0 y 1 (para combinar con energy)
        df['loudness_normalized'] = (df['loudness'] + 60) / 60
        df['loudness_normalized'] = df['loudness_normalized'].clip(0, 1)
        print("Creada columna loudness_normalized (escala 0-1)")
    
    return df

def crear_columnas_fecha(df):
    """Crear columnas útiles a partir de la fecha de lanzamiento"""
    
    print("\n--- Creando columnas de fecha ---")
    
    if 'release_date' in df.columns:
        # Extraer el año
        df['release_year'] = df['release_date'].dt.year
        
        # Crear década (ej: 1985 → "1980s")
        def obtener_decada(año):
            if pd.isna(año):
                return None
            decada = (año // 10) * 10
            return f"{decada}s"
        
        df['release_decade'] = df['release_year'].apply(obtener_decada)
        print("Creadas columnas release_year y release_decade")
    
    return df

def organizar_generos(df):
    """Organizar y limpiar géneros musicales"""
    
    print("\n--- Organizando géneros ---")
    
    if 'genre' in df.columns:
        # 1. Limpiar géneros (minúsculas, sin espacios extra)
        df['genre_clean'] = df['genre'].str.lower().str.strip()
        
        # 2. Unificar variaciones comunes
        df['genre_clean'] = df['genre_clean'].replace({
            'hip hop': 'hip-hop',
            'hiphop': 'hip-hop', 
            'hip_hop': 'hip-hop',
            'edm': 'electronic',
            'electronic dance music': 'electronic',
            'r&b': 'r-n-b',
            'rnb': 'r-n-b',
            'r and b': 'r-n-b'
        })
        
        # 3. Crear categorías principales
        def asignar_categoria_genero(genero):
            if pd.isna(genero):
                return 'Other'
            
            genero = genero.lower()
            
            # Pop
            if any(x in genero for x in ['pop', 'dance-pop', 'electropop', 'synthpop']):
                return 'Pop'
            
            # Rock  
            elif any(x in genero for x in ['rock', 'indie', 'alternative', 'hard-rock', 'metal', 'alt-rock']):
                return 'Rock'
            
            # Hip-Hop
            elif any(x in genero for x in ['hip-hop', 'rap', 'trap']):
                return 'Hip-Hop'
            
            # Electronic
            elif any(x in genero for x in ['electronic', 'house', 'techno', 'dubstep', 'trance']):
                return 'Electronic'
            
            # R&B
            elif any(x in genero for x in ['r-n-b', 'soul', 'neo-soul']):
                return 'R&B'
            
            # Country
            elif any(x in genero for x in ['country', 'folk', 'americana']):
                return 'Country'
            
            # Latin
            elif any(x in genero for x in ['latin', 'reggaeton', 'salsa', 'bachata']):
                return 'Latin'
            
            # Jazz
            elif any(x in genero for x in ['jazz', 'blues']):
                return 'Jazz'
            
            # Classical
            elif any(x in genero for x in ['classical', 'soundtrack', 'instrumental']):
                return 'Classical'
            
            # Si no coincide con nada, poner "Other"
            else:
                return 'Other'
        
        df['main_genre'] = df['genre_clean'].apply(asignar_categoria_genero)
        print("Creada columna main_genre con categorías principales")
    
    return df

def estandarizar_nombres_columnas(df, archivo):
    """Estandarizar nombres de columnas para que todos los archivos tengan la misma estructura"""
    
    print(f"\n--- Estandarizando nombres de columnas para {archivo} ---")
    
    # Mapeo de nombres de columnas
    mapeo_columnas = {
        'track': 'track_name',
        'artist': 'artist_name',
        'uri': 'track_id',
        'Unnamed: 0': 'id'
    }
    
    # Renombrar columnas
    df = df.rename(columns=mapeo_columnas)
    
    # Si no hay track_id pero hay uri, usar uri como track_id
    if 'track_id' not in df.columns and 'uri' in df.columns:
        df['track_id'] = df['uri']
    
    # Si no hay track_name pero hay track, usar track como track_name
    if 'track_name' not in df.columns and 'track' in df.columns:
        df['track_name'] = df['track']
    
    # Si no hay artist_name pero hay artist, usar artist como artist_name
    if 'artist_name' not in df.columns and 'artist' in df.columns:
        df['artist_name'] = df['artist']
    
    print("Nombres de columnas estandarizados")
    
    return df

def limpiar_archivo(archivo):
    """Función principal para limpiar un archivo"""
    
    print(f"\n{'='*60}")
    print(f"LIMPIANDO ARCHIVO: {archivo}")
    print(f"{'='*60}")
    
    try:
        # Cargar el archivo
        df = pd.read_csv(archivo)
        print(f"Archivo cargado: {len(df)} registros")
        
        # Aplicar todas las funciones de limpieza
        df = estandarizar_nombres_columnas(df, archivo)
        df = eliminar_duplicados(df, archivo)
        df = arreglar_valores_criticos(df)
        df = arreglar_fechas(df)
        df = arreglar_generos(df)
        df = arreglar_energy(df)
        df = arreglar_loudness(df)
        df = crear_columnas_fecha(df)
        df = organizar_generos(df)
        
        print(f"\nArchivo limpiado: {len(df)} registros")
        print(f"Columnas finales: {list(df.columns)}")
        
        return df
        
    except Exception as e:
        print(f"ERROR al limpiar {archivo}: {str(e)}")
        return None

def limpiar_todos_los_archivos():
    """Limpiar todos los archivos CSV"""
    
    print("INICIANDO LIMPIEZA DE DATOS")
    print("=" * 60)
    
    # Lista de archivos CSV
    archivos = [
        'data/raw/dataset-of-60s.csv',
        'data/raw/dataset-of-70s.csv', 
        'data/raw/dataset-of-80s.csv',
        'data/raw/dataset-of-90s.csv',
        'data/raw/dataset-of-00s.csv',
        'data/raw/dataset-of-10s.csv',
        'data/raw/spotify_data.csv'
    ]
    
    # Limpiar cada archivo
    datos_limpios = {}
    for archivo in archivos:
        if os.path.exists(archivo):
            df_limpio = limpiar_archivo(archivo)
            if df_limpio is not None:
                datos_limpios[archivo] = df_limpio
        else:
            print(f"ERROR: {archivo} no encontrado")
    
    print(f"\n{'='*60}")
    print("RESUMEN DE LIMPIEZA:")
    print(f"{'='*60}")
    
    total_registros = 0
    for archivo, df in datos_limpios.items():
        total_registros += len(df)
        print(f"{archivo}: {len(df):,} registros")
    
    print(f"\nTOTAL DE REGISTROS LIMPIOS: {total_registros:,}")
    print("\nLimpieza completada!")
    
    return datos_limpios

if __name__ == "__main__":
    datos_limpios = limpiar_todos_los_archivos()
