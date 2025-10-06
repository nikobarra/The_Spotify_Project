# Resumen del Proyecto: Análisis de Intensidad Musical de Spotify

## ¿Qué hicimos?
- Cargamos 7 archivos CSV con datos de música de Spotify
- Limpiamos y organizamos los datos
- Creamos una medida de "intensidad musical" combinando energy y loudness
- Guardamos los datos limpios para análisis

## Estadísticas:
- **Datos originales**: 1,200,870 canciones
- **Datos finales**: 1,199,120 canciones
- **Porcentaje conservado**: 99.9%
- **Años cubiertos**: 1965 - 2023
- **Géneros principales**: Other, Rock, Electronic, Pop, Jazz

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

## Fecha de creación: 2025-10-06 14:08:04
