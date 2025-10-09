#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para crear la variable de intensidad musical
Nivel: Desarrollador
"""

import pandas as pd
import numpy as np
import os

def crear_intensidad_ponderada(df):
    """Crear intensidad dando más peso a energy"""
    
    print("\n--- Creando intensidad ponderada ---")
    
    if 'energy' in df.columns and 'loudness_normalized' in df.columns:
        # Energy es más importante para la percepción de intensidad (60%)
        # Loudness es importante pero menos (40%)
        df['intensity_weighted'] = (df['energy'] * 0.6) + (df['loudness_normalized'] * 0.4)
        print("Creada columna intensity_weighted (energy 60% + loudness 40%)")
        
        # Estadísticas básicas
        print(f"  Intensidad promedio: {df['intensity_weighted'].mean():.3f}")
        print(f"  Intensidad mínima: {df['intensity_weighted'].min():.3f}")
        print(f"  Intensidad máxima: {df['intensity_weighted'].max():.3f}")
        
        return df
    else:
        print("ERROR: Faltan columnas energy o loudness_normalized")
        return df

def crear_intensidad_simple(df):
    """Crear intensidad como promedio simple de energy y loudness"""
    
    print("\n--- Creando intensidad simple ---")
    
    if 'energy' in df.columns and 'loudness_normalized' in df.columns:
        # Promedio simple: (energy + loudness_normalized) / 2
        df['intensity_simple'] = (df['energy'] + df['loudness_normalized']) / 2
        print("Creada columna intensity_simple (promedio simple)")
        
        # Estadísticas básicas
        print(f"  Intensidad promedio: {df['intensity_simple'].mean():.3f}")
        print(f"  Intensidad mínima: {df['intensity_simple'].min():.3f}")
        print(f"  Intensidad máxima: {df['intensity_simple'].max():.3f}")
        
        return df
    else:
        print("ERROR: Faltan columnas energy o loudness_normalized")
        return df

def crear_intensidad_compleja(df):
    """Crear intensidad incluyendo más factores"""
    
    print("\n--- Creando intensidad compleja ---")
    
    if 'energy' in df.columns and 'loudness_normalized' in df.columns:
        # Si tenemos tempo, incluirlo también
        if 'tempo' in df.columns:
            # Normalizar tempo (asumir que va de 0 a 200 BPM)
            tempo_normalizado = df['tempo'] / 200
            tempo_normalizado = tempo_normalizado.clip(0, 1)
            
            # Combinar energy (50%), loudness (30%), tempo (20%)
            df['intensity_complex'] = (
                df['energy'] * 0.5 +
                df['loudness_normalized'] * 0.3 +
                tempo_normalizado * 0.2
            )
            print("Creada columna intensity_complex (energy 50% + loudness 30% + tempo 20%)")
        else:
            # Si no hay tempo, usar solo energy y loudness
            df['intensity_complex'] = (df['energy'] * 0.6) + (df['loudness_normalized'] * 0.4)
            print("Creada columna intensity_complex (energy 60% + loudness 40%)")
        
        # Estadísticas básicas
        print(f"  Intensidad promedio: {df['intensity_complex'].mean():.3f}")
        print(f"  Intensidad mínima: {df['intensity_complex'].min():.3f}")
        print(f"  Intensidad máxima: {df['intensity_complex'].max():.3f}")
        
        return df
    else:
        print("ERROR: Faltan columnas energy o loudness_normalized")
        return df

def crear_marcador_completo(df):
    """Marcar canciones que tienen toda la información necesaria"""
    
    print("\n--- Creando marcador de completitud ---")
    
    df['is_complete'] = (
        df['energy'].notna() &           # Tiene energy
        df['loudness'].notna() &         # Tiene loudness  
        df['release_date'].notna() &     # Tiene fecha
        df['main_genre'].notna()         # Tiene género
    )
    
    completas = df['is_complete'].sum()
    total = len(df)
    porcentaje = (completas / total) * 100
    
    print(f"  Canciones completas: {completas:,} de {total:,} ({porcentaje:.1f}%)")
    
    return df

def crear_marcador_fecha_valida(df):
    """Marcar canciones con fechas que tienen sentido"""
    
    print("\n--- Creando marcador de fecha válida ---")
    
    df['is_valid_date'] = (
        (df['release_year'] >= 1920) &   # No muy antigua
        (df['release_year'] <= 2024)     # No futura
    )
    
    validas = df['is_valid_date'].sum()
    total = len(df)
    porcentaje = (validas / total) * 100
    
    print(f"  Fechas válidas: {validas:,} de {total:,} ({porcentaje:.1f}%)")
    
    return df

def crear_marcador_outliers(df):
    """Marcar canciones con valores muy raros de intensidad"""
    
    print("\n--- Creando marcador de outliers ---")
    
    if 'intensity_weighted' in df.columns:
        # Calcular qué valores son "normales" usando el método IQR
        Q1 = df['intensity_weighted'].quantile(0.25)  # 25% más bajo
        Q3 = df['intensity_weighted'].quantile(0.75)  # 75% más alto
        IQR = Q3 - Q1  # Rango intercuartil
        
        # Un valor es "raro" si está muy lejos de lo normal
        df['is_outlier'] = (
            (df['intensity_weighted'] < Q1 - 1.5 * IQR) |  # Muy bajo
            (df['intensity_weighted'] > Q3 + 1.5 * IQR)    # Muy alto
        )
        
        outliers = df['is_outlier'].sum()
        total = len(df)
        porcentaje = (outliers / total) * 100
        
        print(f"  Outliers detectados: {outliers:,} de {total:,} ({porcentaje:.1f}%)")
        print(f"  Rango normal: {Q1 - 1.5 * IQR:.3f} a {Q3 + 1.5 * IQR:.3f}")
        
        return df
    else:
        print("ERROR: No se puede crear marcador de outliers sin intensity_weighted")
        return df

def crear_puntuacion_calidad(df):
    """Crear una puntuación de calidad de 0 a 100"""
    
    print("\n--- Creando puntuación de calidad ---")
    
    # Cada marcador vale puntos
    df['data_quality_score'] = (
        (df['is_complete'].astype(int) * 40) +      # 40 puntos si está completa
        (df['is_valid_date'].astype(int) * 20) +    # 20 puntos si fecha es válida
        ((~df['is_outlier']).astype(int) * 20) +    # 20 puntos si no es outlier
        (20)  # 20 puntos base (asumiendo que no hay conflictos)
    )
    
    score_promedio = df['data_quality_score'].mean()
    print(f"  Puntuación promedio: {score_promedio:.1f}/100")
    
    return df

def crear_resumen_por_decada(df):
    """Crear resumen de intensidad por década"""
    
    print("\n--- Creando resumen por década ---")
    
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
        
        print("  Resumen por década creado:")
        for _, row in resumen_decada.iterrows():
            decada = row['release_decade']
            intensidad = row['intensity_weighted_mean']
            canciones = row['track_id_count']
            print(f"    {decada}: {intensidad:.3f} intensidad promedio ({canciones:,} canciones)")
        
        return resumen_decada
    else:
        print("ERROR: Faltan columnas intensity_weighted o release_decade")
        return None

def crear_resumen_por_decada_genero(df):
    """Crear resumen de intensidad por década y género"""
    
    print("\n--- Creando resumen por década y género ---")
    
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
        
        print(f"  Resumen por década y género creado: {len(resumen_decada_genero)} combinaciones")
        
        return resumen_decada_genero
    else:
        print("ERROR: Faltan columnas necesarias")
        return None

def crear_estadisticas_genero(df):
    """Crear estadísticas por género"""
    
    print("\n--- Creando estadísticas por género ---")
    
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
        
        print(f"  Estadísticas por género creadas: {len(stats_genero)} géneros")
        
        return stats_genero
    else:
        print("ERROR: Faltan columnas necesarias")
        return None

def crear_variables_intensidad():
    """Función principal para crear todas las variables de intensidad"""
    
    print("CREANDO VARIABLES DE INTENSIDAD")
    print("=" * 60)
    
    # Cargar el dataset combinado
    # Por simplicidad, vamos a recrear el proceso completo
    from combinar_archivos import combinar_todos_los_archivos
    
    print("Cargando dataset combinado...")
    df = combinar_todos_los_archivos()
    
    if df is None:
        print("ERROR: No se pudo cargar el dataset combinado")
        return None
    
    print(f"Dataset cargado: {len(df):,} canciones")
    
    # Crear variables de intensidad
    df = crear_intensidad_ponderada(df)
    df = crear_intensidad_simple(df)
    df = crear_intensidad_compleja(df)
    
    # Crear marcadores de calidad
    df = crear_marcador_completo(df)
    df = crear_marcador_fecha_valida(df)
    df = crear_marcador_outliers(df)
    df = crear_puntuacion_calidad(df)
    
    # Crear resúmenes
    resumen_decada = crear_resumen_por_decada(df)
    resumen_decada_genero = crear_resumen_por_decada_genero(df)
    stats_genero = crear_estadisticas_genero(df)
    
    print(f"\n{'='*60}")
    print("CREACION DE VARIABLES COMPLETADA")
    print(f"{'='*60}")
    print(f"Dataset final: {len(df):,} canciones")
    print(f"Columnas: {len(df.columns)}")
    
    if 'intensity_weighted' in df.columns:
        print(f"Intensidad promedio: {df['intensity_weighted'].mean():.3f}")
        print(f"Puntuación de calidad promedio: {df['data_quality_score'].mean():.1f}/100")
    
    return df, resumen_decada, resumen_decada_genero, stats_genero

if __name__ == "__main__":
    resultado = crear_variables_intensidad()
