## Diccionario de Datos

| Columna | Tipo | Descripción |
|---------|------|-------------|
| track_id | object | ID único de la canción en Spotify |
| track_name | object | Nombre de la canción |
| artist_name | object | Nombre del artista |
| energy | float64 | Qué tan enérgica es la canción (0-1) |
| loudness | float64 | Qué tan fuerte suena (-60 a 0 dB) |
| loudness_normalized | float64 | Loudness convertido a escala 0-1 |
| release_date | datetime64[ns] | Fecha de lanzamiento de la canción |
| release_year | int64 | Año de lanzamiento |
| release_decade | object | Década (ej: 1990s) |
| genre | object | Género original de la canción |
| main_genre | object | Categoría principal de género |
| data_source | object | Archivo original de donde vino la canción |
| danceability | float64 | Columna adicional |
| valence | float64 | Columna adicional |
| tempo | float64 | Columna adicional |
| duration_ms | float64 | Columna adicional |
| intensity_weighted | float64 | Medida de intensidad musical (0-1) - RECOMENDADA |
| intensity_simple | float64 | Medida de intensidad simple (0-1) |
| intensity_complex | float64 | Medida de intensidad compleja (0-1) |
| is_complete | bool | Si la canción tiene toda la información necesaria |
| is_valid_date | bool | Si la fecha de lanzamiento es válida |
| is_outlier | bool | Si la canción tiene valores muy raros de intensidad |
| data_quality_score | int64 | Puntuación de calidad de los datos (0-100) |
| intensity_category | object | Categoría de intensidad (Muy Baja, Baja, Media, Alta, Muy Alta) |
