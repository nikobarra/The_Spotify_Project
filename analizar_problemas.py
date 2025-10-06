#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para analizar problemas en los datos de Spotify
Nivel: Desarrollador
"""

import pandas as pd
import numpy as np
import os

def analizar_calidad_datos(archivo):
    """Función para analizar la calidad de un archivo CSV"""
    print(f"\n=== ANALISIS DE CALIDAD: {archivo} ===")
    
    try:
        # Cargar el archivo
        df = pd.read_csv(archivo)
        
        # 1. Valores nulos
        print("\n1. VALORES NULOS:")
        nulos = df.isnull().sum()
        porcentaje_nulos = (nulos / len(df)) * 100
        
        hay_nulos = False
        for columna in df.columns:
            if nulos[columna] > 0:
                hay_nulos = True
                print(f"  {columna}: {nulos[columna]} nulos ({porcentaje_nulos[columna]:.1f}%)")
        
        if not hay_nulos:
            print("  ¡Excelente! No hay valores nulos")
        
        # 2. Duplicados
        print(f"\n2. DUPLICADOS:")
        duplicados_totales = df.duplicated().sum()
        print(f"  Filas duplicadas exactas: {duplicados_totales}")
        
        # Verificar duplicados por identificador único si existe
        if 'uri' in df.columns:
            duplicados_uri = df.duplicated(subset=['uri']).sum()
            print(f"  Duplicados por URI: {duplicados_uri}")
        elif 'track_id' in df.columns:
            duplicados_id = df.duplicated(subset=['track_id']).sum()
            print(f"  Duplicados por track_id: {duplicados_id}")
        
        # 3. Información de columnas numéricas importantes
        print(f"\n3. INFORMACION DE COLUMNAS NUMERICAS IMPORTANTES:")
        
        # Verificar energy
        if 'energy' in df.columns:
            energy_stats = df['energy'].describe()
            print(f"  Energy: min={energy_stats['min']:.3f}, max={energy_stats['max']:.3f}, media={energy_stats['mean']:.3f}")
            
            # Verificar si energy está en rango correcto (0-1)
            energy_fuera_rango = ((df['energy'] < 0) | (df['energy'] > 1)).sum()
            if energy_fuera_rango > 0:
                print(f"    ADVERTENCIA: {energy_fuera_rango} valores de energy fuera de rango (0-1)")
        
        # Verificar loudness
        if 'loudness' in df.columns:
            loudness_stats = df['loudness'].describe()
            print(f"  Loudness: min={loudness_stats['min']:.1f}, max={loudness_stats['max']:.1f}, media={loudness_stats['mean']:.1f}")
            
            # Verificar si loudness está en rango razonable (-60 a 0)
            loudness_fuera_rango = ((df['loudness'] < -60) | (df['loudness'] > 0)).sum()
            if loudness_fuera_rango > 0:
                print(f"    ADVERTENCIA: {loudness_fuera_rango} valores de loudness fuera de rango (-60 a 0)")
        
        # Verificar tempo
        if 'tempo' in df.columns:
            tempo_stats = df['tempo'].describe()
            print(f"  Tempo: min={tempo_stats['min']:.1f}, max={tempo_stats['max']:.1f}, media={tempo_stats['mean']:.1f}")
            
            # Verificar si tempo está en rango razonable (40-200 BPM)
            tempo_fuera_rango = ((df['tempo'] < 40) | (df['tempo'] > 200)).sum()
            if tempo_fuera_rango > 0:
                print(f"    ADVERTENCIA: {tempo_fuera_rango} valores de tempo fuera de rango (40-200 BPM)")
        
        # 4. Información de fechas si existe
        print(f"\n4. INFORMACION DE FECHAS:")
        if 'year' in df.columns:
            year_stats = df['year'].describe()
            print(f"  Year: min={year_stats['min']:.0f}, max={year_stats['max']:.0f}")
            
            # Verificar fechas futuras o muy antiguas
            fechas_futuras = (df['year'] > 2024).sum()
            fechas_muy_antiguas = (df['year'] < 1920).sum()
            
            if fechas_futuras > 0:
                print(f"    ADVERTENCIA: {fechas_futuras} canciones con fechas futuras (>2024)")
            if fechas_muy_antiguas > 0:
                print(f"    ADVERTENCIA: {fechas_muy_antiguas} canciones con fechas muy antiguas (<1920)")
        
        # 5. Información de géneros si existe
        print(f"\n5. INFORMACION DE GENEROS:")
        if 'genre' in df.columns:
            generos_unicos = df['genre'].nunique()
            print(f"  Géneros únicos: {generos_unicos}")
            
            # Top 10 géneros más frecuentes
            top_generos = df['genre'].value_counts().head(10)
            print(f"  Top 10 géneros:")
            for genero, cantidad in top_generos.items():
                print(f"    {genero}: {cantidad} canciones")
        
        return df
        
    except Exception as e:
        print(f"ERROR al analizar {archivo}: {str(e)}")
        return None

def analizar_todos_los_archivos():
    """Analizar todos los archivos CSV"""
    
    print("ANALIZANDO PROBLEMAS EN LOS DATOS")
    print("=" * 50)
    
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
    
    # Analizar cada archivo
    resultados = {}
    for archivo in archivos:
        if os.path.exists(archivo):
            df = analizar_calidad_datos(archivo)
            if df is not None:
                resultados[archivo] = df
        else:
            print(f"ERROR: {archivo} no encontrado")
    
    print("\n" + "=" * 50)
    print("RESUMEN GENERAL:")
    print("=" * 50)
    
    total_canciones = 0
    for archivo, df in resultados.items():
        total_canciones += len(df)
        print(f"{archivo}: {len(df):,} canciones")
    
    print(f"\nTOTAL DE CANCIONES: {total_canciones:,}")
    print("\nAnalisis de problemas completado!")

if __name__ == "__main__":
    analizar_todos_los_archivos()
