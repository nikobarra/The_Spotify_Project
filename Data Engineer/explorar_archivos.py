#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para explorar los archivos CSV de Spotify
Nivel: Desarrollador
"""

import pandas as pd
import numpy as np
import os

def explorar_archivos_csv():
    """Función principal para explorar todos los archivos CSV"""
    
    print("EXPLORANDO ARCHIVOS DE SPOTIFY")
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
    
    # Verificar que los archivos existen
    print("Verificando archivos...")
    archivos_existentes = []
    for archivo in archivos:
        if os.path.exists(archivo):
            archivos_existentes.append(archivo)
            print(f"  OK: {archivo}")
        else:
            print(f"  ERROR: {archivo} - NO ENCONTRADO")
    
    if not archivos_existentes:
        print("ERROR: No se encontraron archivos CSV. Verifica las rutas.")
        return
    
    print(f"\nEncontrados {len(archivos_existentes)} archivos para analizar")
    print("=" * 50)
    
    # Analizar cada archivo
    for archivo in archivos_existentes:
        print(f"\n=== ARCHIVO: {archivo} ===")
        try:
            # Cargar el archivo
            df = pd.read_csv(archivo)
            
            # Información básica
            print(f"Filas: {len(df):,}")
            print(f"Columnas: {len(df.columns)}")
            print(f"Tamaño en memoria: {df.memory_usage(deep=True).sum() / 1024**2:.1f} MB")
            
            # Lista de columnas
            print(f"\nColumnas disponibles:")
            for i, col in enumerate(df.columns, 1):
                print(f"  {i:2d}. {col}")
            
            # Tipos de datos
            print(f"\nTipos de datos:")
            tipos = df.dtypes.value_counts()
            for tipo, cantidad in tipos.items():
                print(f"  {tipo}: {cantidad} columnas")
            
            # Primeras 3 filas
            print(f"\nPrimeras 3 filas:")
            print(df.head(3).to_string())
            
            print("-" * 50)
            
        except Exception as e:
            print(f"ERROR al leer {archivo}: {str(e)}")
    
    print("\nExploración completada!")

if __name__ == "__main__":
    explorar_archivos_csv()
