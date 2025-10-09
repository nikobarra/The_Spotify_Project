#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para combinar todos los archivos de Spotify
Nivel: Desarrollador
"""

import pandas as pd
import numpy as np
import os

def combinar_archivos_simple(datos_limpios):
    """Combinar todos los archivos en uno solo (método simple)"""
    
    print("COMBINANDO ARCHIVOS")
    print("=" * 50)
    
    # Lista para guardar todos los DataFrames
    todos_los_datos = []
    
    for archivo, df in datos_limpios.items():
        print(f"Procesando: {archivo}")
        print(f"  Registros: {len(df)}")
        
        # Agregar una columna que diga de qué archivo viene
        df['data_source'] = archivo
        
        # Agregar década implícita para archivos de décadas específicas
        if 'dataset-of-60s' in archivo:
            df['release_decade'] = '1960s'
            df['release_year'] = 1965  # Año promedio de la década
        elif 'dataset-of-70s' in archivo:
            df['release_decade'] = '1970s'
            df['release_year'] = 1975
        elif 'dataset-of-80s' in archivo:
            df['release_decade'] = '1980s'
            df['release_year'] = 1985
        elif 'dataset-of-90s' in archivo:
            df['release_decade'] = '1990s'
            df['release_year'] = 1995
        elif 'dataset-of-00s' in archivo:
            df['release_decade'] = '2000s'
            df['release_year'] = 2005
        elif 'dataset-of-10s' in archivo:
            df['release_decade'] = '2010s'
            df['release_year'] = 2015
        
        # Crear release_date si no existe
        if 'release_date' not in df.columns and 'release_year' in df.columns:
            df['release_date'] = pd.to_datetime(df['release_year'].astype(str) + '-01-01', errors='coerce')
        
        todos_los_datos.append(df)
    
    # Combinar todos los DataFrames
    print(f"\nCombinando {len(todos_los_datos)} archivos...")
    df_combinado = pd.concat(todos_los_datos, ignore_index=True)
    
    print(f"Total de canciones combinadas: {len(df_combinado):,}")
    print(f"Columnas: {list(df_combinado.columns)}")
    
    return df_combinado

def resolver_conflictos(df):
    """Resolver conflictos cuando la misma canción aparece varias veces"""
    
    print("\nRESOLVIENDO CONFLICTOS")
    print("=" * 50)
    
    print(f"Registros antes de resolver conflictos: {len(df)}")
    
    # Si hay track_id, usar eso para identificar duplicados
    if 'track_id' in df.columns:
        print("Usando track_id para identificar duplicados...")
        
        # Contar duplicados
        duplicados = df.duplicated(subset=['track_id']).sum()
        print(f"Duplicados encontrados: {duplicados}")
        
        if duplicados > 0:
            # Agrupar por track_id y resolver conflictos
            df_resuelto = df.groupby('track_id').agg({
                'track_name': 'first',  # Usar el primer nombre
                'artist_name': 'first',  # Usar el primer artista
                'energy': 'mean',       # Promediar energy
                'loudness': 'mean',     # Promediar loudness
                'loudness_normalized': 'mean',  # Promediar loudness_normalized
                'release_date': 'min',  # Usar la fecha más temprana
                'release_year': 'min',  # Usar el año más temprano
                'release_decade': 'first',  # Usar la primera década
                'genre': lambda x: x.mode()[0] if len(x.mode()) > 0 else 'Unknown',  # Usar el género más común
                'main_genre': lambda x: x.mode()[0] if len(x.mode()) > 0 else 'Other',  # Usar el género principal más común
                'data_source': lambda x: ', '.join(x.unique()),  # Combinar fuentes
                'danceability': 'mean',  # Promediar otras características
                'valence': 'mean',
                'tempo': 'mean',
                'duration_ms': 'mean'
            }).reset_index()
            
            print(f"Registros después de resolver conflictos: {len(df_resuelto)}")
            print(f"Registros eliminados: {len(df) - len(df_resuelto)}")
            
            return df_resuelto
        else:
            print("No hay conflictos que resolver")
            return df
    
    # Si no hay track_id, usar nombre + artista
    elif 'track_name' in df.columns and 'artist_name' in df.columns:
        print("Usando track_name + artist_name para identificar duplicados...")
        
        # Contar duplicados
        duplicados = df.duplicated(subset=['track_name', 'artist_name']).sum()
        print(f"Duplicados encontrados: {duplicados}")
        
        if duplicados > 0:
            df_resuelto = df.groupby(['track_name', 'artist_name']).agg({
                'energy': 'mean',
                'loudness': 'mean', 
                'loudness_normalized': 'mean',
                'release_date': 'min',
                'release_year': 'min',
                'release_decade': 'first',
                'genre': lambda x: x.mode()[0] if len(x.mode()) > 0 else 'Unknown',
                'main_genre': lambda x: x.mode()[0] if len(x.mode()) > 0 else 'Other',
                'data_source': lambda x: ', '.join(x.unique()),
                'danceability': 'mean',
                'valence': 'mean',
                'tempo': 'mean',
                'duration_ms': 'mean'
            }).reset_index()
            
            print(f"Registros después de resolver conflictos: {len(df_resuelto)}")
            print(f"Registros eliminados: {len(df) - len(df_resuelto)}")
            
            return df_resuelto
        else:
            print("No hay conflictos que resolver")
            return df
    
    else:
        print("No se puede identificar duplicados - no hay identificadores únicos")
        return df

def verificar_dataset_combinado(df):
    """Verificar que el dataset combinado tiene sentido"""
    
    print("\nVERIFICANDO DATASET COMBINADO")
    print("=" * 50)
    
    # Información básica
    print(f"Total de canciones: {len(df):,}")
    print(f"Total de columnas: {len(df.columns)}")
    
    # Verificar columnas críticas
    columnas_criticas = ['track_id', 'track_name', 'artist_name', 'energy', 'loudness', 'release_date', 'main_genre']
    print(f"\nColumnas críticas presentes:")
    for col in columnas_criticas:
        if col in df.columns:
            print(f"  OK: {col}")
        else:
            print(f"  ERROR: {col} - FALTANTE")
    
    # Verificar valores nulos en columnas críticas
    print(f"\nValores nulos en columnas críticas:")
    for col in columnas_criticas:
        if col in df.columns:
            nulos = df[col].isnull().sum()
            porcentaje = (nulos / len(df)) * 100
            print(f"  {col}: {nulos} nulos ({porcentaje:.1f}%)")
    
    # Verificar distribución por década
    print(f"\nDistribución por década:")
    if 'release_decade' in df.columns:
        distribucion = df['release_decade'].value_counts().sort_index()
        for decada, cantidad in distribucion.items():
            porcentaje = (cantidad / len(df)) * 100
            print(f"  {decada}: {cantidad:,} canciones ({porcentaje:.1f}%)")
    
    # Verificar distribución por género principal
    print(f"\nDistribución por género principal:")
    if 'main_genre' in df.columns:
        distribucion = df['main_genre'].value_counts().head(10)
        for genero, cantidad in distribucion.items():
            porcentaje = (cantidad / len(df)) * 100
            print(f"  {genero}: {cantidad:,} canciones ({porcentaje:.1f}%)")
    
    # Verificar distribución por fuente
    print(f"\nDistribución por fuente de datos:")
    if 'data_source' in df.columns:
        distribucion = df['data_source'].value_counts()
        for fuente, cantidad in distribucion.items():
            porcentaje = (cantidad / len(df)) * 100
            print(f"  {fuente}: {cantidad:,} canciones ({porcentaje:.1f}%)")
    
    return True

def combinar_todos_los_archivos():
    """Función principal para combinar todos los archivos"""
    
    print("INICIANDO COMBINACION DE ARCHIVOS")
    print("=" * 60)
    
    # Primero necesitamos cargar los datos limpios
    # Por simplicidad, vamos a recrear el proceso de limpieza
    from limpiar_datos import limpiar_todos_los_archivos
    
    print("Cargando y limpiando archivos...")
    datos_limpios = limpiar_todos_los_archivos()
    
    if not datos_limpios:
        print("ERROR: No se pudieron cargar los datos limpios")
        return None
    
    # Combinar archivos
    print("\nCombinando archivos...")
    df_combinado = combinar_archivos_simple(datos_limpios)
    
    # Resolver conflictos
    df_final = resolver_conflictos(df_combinado)
    
    # Verificar resultado
    verificar_dataset_combinado(df_final)
    
    print(f"\n{'='*60}")
    print("COMBINACION COMPLETADA")
    print(f"{'='*60}")
    print(f"Dataset final: {len(df_final):,} canciones")
    print(f"Columnas: {len(df_final.columns)}")
    
    return df_final

if __name__ == "__main__":
    df_final = combinar_todos_los_archivos()
