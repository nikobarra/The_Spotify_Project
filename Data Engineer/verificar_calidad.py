#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar la calidad de los datos procesados
Nivel: Desarrollador
"""

import pandas as pd
import numpy as np
import os

def verificar_distribuciones(df):
    """Verificar que las distribuciones de intensidad tienen sentido"""
    
    print("=== VERIFICACION DE DISTRIBUCIONES ===")
    
    if 'intensity_weighted' in df.columns and 'release_decade' in df.columns:
        # Ver estadísticas básicas por década
        for decada in sorted(df['release_decade'].unique()):
            if pd.notna(decada):
                datos_decada = df[df['release_decade'] == decada]['intensity_weighted']
                print(f"\n{decada}:")
                print(f"  Promedio: {datos_decada.mean():.3f}")
                print(f"  Mediana: {datos_decada.median():.3f}")
                print(f"  Minimo: {datos_decada.min():.3f}")
                print(f"  Maximo: {datos_decada.max():.3f}")
                print(f"  Canciones: {len(datos_decada):,}")
        
        return True
    else:
        print("ERROR: Faltan columnas necesarias")
        return False

def verificar_tendencia_temporal(df):
    """Verificar que la tendencia temporal tiene sentido"""
    
    print("\n=== VERIFICACION DE TENDENCIA TEMPORAL ===")
    
    if 'intensity_weighted' in df.columns and 'release_decade' in df.columns:
        # Calcular intensidad promedio por década
        intensidad_por_decada = df.groupby('release_decade')['intensity_weighted'].mean().sort_index()
        
        print("Intensidad promedio por década:")
        for decada, intensidad in intensidad_por_decada.items():
            if pd.notna(decada) and decada != 'Unknown':
                print(f"  {decada}: {intensidad:.3f}")
        
        # Ver si hay tendencia creciente
        decadas_numericas = []
        intensidades = []
        
        for decada, intensidad in intensidad_por_decada.items():
            if pd.notna(decada) and decada != 'Unknown':
                año = int(decada.replace('s', ''))
                decadas_numericas.append(año)
                intensidades.append(intensidad)
        
        # Calcular correlación entre año e intensidad
        if len(decadas_numericas) > 1:
            correlacion = np.corrcoef(decadas_numericas, intensidades)[0, 1]
            print(f"\nCorrelación año-intensidad: {correlacion:.3f}")
            
            if correlacion > 0.3:
                print("RESULTADO: Hay tendencia creciente (la música se volvió más intensa con el tiempo)")
            elif correlacion < -0.3:
                print("RESULTADO: Hay tendencia decreciente (la música se volvió menos intensa con el tiempo)")
            else:
                print("RESULTADO: No hay tendencia clara")
        
        return True
    else:
        print("ERROR: Faltan columnas necesarias")
        return False

def verificar_coherencia_generos(df):
    """Verificar que los géneros tienen valores de intensidad coherentes"""
    
    print("\n=== VERIFICACION DE COHERENCIA DE GENEROS ===")
    
    if 'intensity_weighted' in df.columns and 'main_genre' in df.columns:
        # Intensidad promedio por género
        intensidad_por_genero = df.groupby('main_genre')['intensity_weighted'].mean().sort_values(ascending=False)
        
        print("Intensidad promedio por género:")
        for genero, intensidad in intensidad_por_genero.items():
            print(f"  {genero}: {intensidad:.3f}")
        
        # Verificar que los géneros "intensos" tienen valores altos
        generos_intensos = ['Electronic', 'Hip-Hop', 'Rock']
        generos_tranquilos = ['Jazz', 'Classical', 'Country']
        
        print(f"\nGéneros que deberían ser intensos: {generos_intensos}")
        print(f"Géneros que deberían ser tranquilos: {generos_tranquilos}")
        
        # Verificar coherencia
        for genero in generos_intensos:
            if genero in intensidad_por_genero.index:
                intensidad = intensidad_por_genero[genero]
                if intensidad > 0.6:
                    print(f"  OK: {genero} es intenso ({intensidad:.3f})")
                else:
                    print(f"  ADVERTENCIA: {genero} no es tan intenso como esperado ({intensidad:.3f})")
        
        for genero in generos_tranquilos:
            if genero in intensidad_por_genero.index:
                intensidad = intensidad_por_genero[genero]
                if intensidad < 0.5:
                    print(f"  OK: {genero} es tranquilo ({intensidad:.3f})")
                else:
                    print(f"  ADVERTENCIA: {genero} es más intenso de lo esperado ({intensidad:.3f})")
        
        return True
    else:
        print("ERROR: Faltan columnas necesarias")
        return False

def verificar_reglas_basicas(df):
    """Verificar que los datos cumplen reglas básicas"""
    
    print("\n=== VERIFICACION DE REGLAS BASICAS ===")
    
    errores = []
    
    # 1. No debe haber fechas futuras
    if 'release_year' in df.columns:
        fechas_futuras = (df['release_year'] > 2024).sum()
        if fechas_futuras > 0:
            errores.append(f"ERROR: {fechas_futuras} canciones tienen fechas futuras (> 2024)")
        else:
            print("OK: No hay fechas futuras")
    
    # 2. Energy debe estar entre 0 y 1
    if 'energy' in df.columns:
        energy_fuera_rango = ((df['energy'] < 0) | (df['energy'] > 1)).sum()
        if energy_fuera_rango > 0:
            errores.append(f"ERROR: {energy_fuera_rango} canciones tienen energy fuera de rango (0-1)")
        else:
            print("OK: Todos los valores de energy están entre 0 y 1")
    
    # 3. Loudness_normalized debe estar entre 0 y 1
    if 'loudness_normalized' in df.columns:
        loudness_fuera_rango = ((df['loudness_normalized'] < 0) | (df['loudness_normalized'] > 1)).sum()
        if loudness_fuera_rango > 0:
            errores.append(f"ERROR: {loudness_fuera_rango} canciones tienen loudness_normalized fuera de rango (0-1)")
        else:
            print("OK: Todos los valores de loudness_normalized están entre 0 y 1")
    
    # 4. Energy y loudness deben estar correlacionados positivamente
    if 'energy' in df.columns and 'loudness' in df.columns:
        correlacion = df['energy'].corr(df['loudness'])
        if correlacion < 0.3:
            errores.append(f"ERROR: Correlación energy-loudness muy baja: {correlacion:.3f} (debería ser > 0.3)")
        elif correlacion > 0.7:
            errores.append(f"ADVERTENCIA: Correlación energy-loudness muy alta: {correlacion:.3f} (puede indicar redundancia)")
        else:
            print(f"OK: Correlación energy-loudness normal: {correlacion:.3f}")
    
    # Mostrar errores si los hay
    if errores:
        print("\nERRORES ENCONTRADOS:")
        for error in errores:
            print(f"  {error}")
        return False
    else:
        print("\nRESULTADO: Todas las reglas básicas se cumplen")
        return True

def verificar_completitud_por_decada(df):
    """Verificar que tenemos suficientes datos por década"""
    
    print("\n=== VERIFICACION DE COMPLETITUD POR DECADA ===")
    
    if 'release_decade' in df.columns and 'is_complete' in df.columns:
        completitud_decada = df.groupby('release_decade').agg({
            'is_complete': 'mean',  # % de canciones completas
            'track_id': 'count'     # Número de canciones
        })
        
        print("Completitud por década:")
        for decada, row in completitud_decada.iterrows():
            if pd.notna(decada):
                canciones = row['track_id']
                completitud = row['is_complete'] * 100
                
                print(f"  {decada}: {canciones:,} canciones, {completitud:.1f}% completas")
                
                # Verificar criterios
                if canciones < 500:
                    print(f"    ADVERTENCIA: Pocas canciones (< 500)")
                elif canciones < 1000:
                    print(f"    OK: Cantidad aceptable (500-1000)")
                else:
                    print(f"    EXCELENTE: Buena cantidad (> 1000)")
                
                if completitud < 80:
                    print(f"    ADVERTENCIA: Baja completitud (< 80%)")
                else:
                    print(f"    OK: Buena completitud (> 80%)")
        
        return completitud_decada
    else:
        print("ERROR: Faltan columnas necesarias")
        return None

def verificar_completitud_por_genero(df):
    """Verificar que tenemos suficientes datos por género"""
    
    print("\n=== VERIFICACION DE COMPLETITUD POR GENERO ===")
    
    if 'main_genre' in df.columns and 'is_complete' in df.columns:
        completitud_genero = df.groupby('main_genre').agg({
            'is_complete': 'mean',
            'track_id': 'count'
        }).sort_values('track_id', ascending=False)
        
        print("Completitud por género:")
        for genero, row in completitud_genero.iterrows():
            canciones = row['track_id']
            completitud = row['is_complete'] * 100
            
            print(f"  {genero}: {canciones:,} canciones, {completitud:.1f}% completas")
            
            # Verificar criterios
            if canciones < 1000:
                print(f"    ADVERTENCIA: Pocas canciones (< 1000)")
            else:
                print(f"    OK: Buena cantidad (> 1000)")
            
            if completitud < 80:
                print(f"    ADVERTENCIA: Baja completitud (< 80%)")
            else:
                print(f"    OK: Buena completitud (> 80%)")
        
        return completitud_genero
    else:
        print("ERROR: Faltan columnas necesarias")
        return None

def verificar_balance_temporal(df):
    """Verificar que los datos están balanceados por década"""
    
    print("\n=== VERIFICACION DE BALANCE TEMPORAL ===")
    
    if 'release_decade' in df.columns:
        # Distribución por década
        distribucion_decada = df['release_decade'].value_counts(normalize=True).sort_index()
        
        print("Distribución por década:")
        for decada, porcentaje in distribucion_decada.items():
            if pd.notna(decada):
                print(f"  {decada}: {porcentaje*100:.1f}%")
        
        # Verificar si hay desbalance severo
        max_porcentaje = distribucion_decada.max()
        if max_porcentaje > 0.5:
            print(f"\nADVERTENCIA: Una década representa el {max_porcentaje*100:.1f}% de los datos")
            print("   Esto puede crear sesgo en el análisis")
        else:
            print(f"\nOK: Balance temporal aceptable (máximo: {max_porcentaje*100:.1f}%)")
        
        return distribucion_decada
    else:
        print("ERROR: Faltan columnas necesarias")
        return None

def verificar_balance_generos(df):
    """Verificar que los géneros están balanceados"""
    
    print("\n=== VERIFICACION DE BALANCE DE GENEROS ===")
    
    if 'main_genre' in df.columns:
        # Distribución por género
        distribucion_genero = df['main_genre'].value_counts(normalize=True)
        
        print("Distribución por género:")
        for genero, porcentaje in distribucion_genero.items():
            print(f"  {genero}: {porcentaje*100:.1f}%")
        
        # Verificar concentración en top géneros
        top_5_porcentaje = distribucion_genero.head(5).sum()
        if top_5_porcentaje > 0.7:
            print(f"\nADVERTENCIA: Los top 5 géneros representan el {top_5_porcentaje*100:.1f}% de los datos")
            print("   Esto puede crear sesgo hacia ciertos géneros")
        else:
            print(f"\nOK: Balance de géneros aceptable (top 5: {top_5_porcentaje*100:.1f}%)")
        
        return distribucion_genero
    else:
        print("ERROR: Faltan columnas necesarias")
        return None

def verificar_todo():
    """Función principal para verificar todo"""
    
    print("VERIFICANDO CALIDAD DE LOS DATOS")
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
    
    # Ejecutar todas las verificaciones
    print("\n" + "="*60)
    print("EJECUTANDO VERIFICACIONES")
    print("="*60)
    
    # Verificaciones estadísticas
    verificar_distribuciones(df)
    verificar_tendencia_temporal(df)
    verificar_coherencia_generos(df)
    
    # Verificaciones de reglas básicas
    reglas_ok = verificar_reglas_basicas(df)
    
    # Verificaciones de completitud
    verificar_completitud_por_decada(df)
    verificar_completitud_por_genero(df)
    
    # Verificaciones de balance
    verificar_balance_temporal(df)
    verificar_balance_generos(df)
    
    print(f"\n{'='*60}")
    print("VERIFICACION COMPLETADA")
    print(f"{'='*60}")
    
    if reglas_ok:
        print("RESULTADO FINAL: Los datos están listos para análisis")
        print("OK: Todas las verificaciones pasaron exitosamente")
    else:
        print("RESULTADO FINAL: Hay problemas que deben corregirse")
        print("ERROR: Algunas verificaciones fallaron")
    
    return reglas_ok

if __name__ == "__main__":
    resultado = verificar_todo()
