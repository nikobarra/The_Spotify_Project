# Informe Integrador – Semana 2  
## Análisis de Intensidad Musical en Spotify

### Equipo y Roles

Durante la primera semana se definieron los roles del equipo en base a los perfiles y fortalezas individuales:

- **Project Manager (PM):** Nicolás Barra  
- **Data Engineer:** Nicolás Barra  
- **Data Analyst:** Nazareth Agüero  
- **ML Specialist:** José Mondragón  
- **Communication & Documentation Lead:** Gabriela Vicente  
---

## Propósito del Proyecto

El objetivo fue organizar un grupo de trabajo, abordando un problema realista con impacto social y laboral. Se eligió analizar la evolución de la intensidad musical en Spotify, entendida como la combinación de energía y sonoridad, para identificar tendencias y patrones relevantes para la industria musical.

---

## Justificación Social y Profesional

Este análisis permite comprender cómo han cambiado las preferencias musicales a lo largo de las décadas, aportando información valiosa para:

- **Sellos discográficos:** decisiones sobre estilos y lanzamientos  
- **Artistas:** adaptación a tendencias de consumo  
- **Investigadores:** estudios sobre cultura, emociones y música  
- **Plataformas de streaming:** recomendaciones personalizadas  

---

## Marco Profesional y Ético

Cada rol fue abordado desde su función real en el campo laboral:

- El **Data Engineer** gestionó la calidad de más de 1.2M registros musicales.  
- El **Data Analyst** exploró correlaciones entre géneros, décadas e intensidad.  
- El **ML Specialist** diseñó métricas de intensidad (ponderada, simple, compleja).  
- El **PM** organizó entregas y facilitó la comunicación interna.  
- Como **Communication Lead**, documenté el proceso, redacté informes y aseguré la inclusión de enfoque de género y equidad.

Se reflexionó sobre la responsabilidad ética del análisis de datos musicales, especialmente en relación con la representación de géneros, culturas y emociones.

---

## Preparación y Análisis de Datos

- Se combinaron 7 archivos CSV en un único dataset limpio de 627.9 MB.  
- Se eliminaron duplicados, valores nulos y fuera de rango.  
- Se crearon variables derivadas como género, década e intensidad.  
- Se validó la calidad con métricas de completitud y coherencia.

Visualizaciones clave incluyeron histogramas por década, rankings de géneros y evolución temporal.

---

## Resultados y Hallazgos

- La intensidad musical aumentó de 0.587 (1960s) a 0.732 (2010s).  
- Géneros más intensos: Rock (0.830), Electronic (0.796), Latin (0.792).  
- Géneros más tranquilos: Classical (0.396), Jazz (0.666), Country (0.672).  
- Se observó una leve disminución en los 2020s (0.719), lo que abre nuevas líneas de análisis.


## Cierre Integrador

Este proyecto permitió integrar saberes técnicos con habilidades comunicativas y éticas. Se destacó:

- El valor de documentar con claridad y perspectiva inclusiva  
- La importancia del enfoque de género en el análisis musical  
- El rol social de los datos como herramienta de transformación cultural

---

## Archivos Entregados

- `README.md`: resumen técnico del proyecto  
- `spotify_music_intensity_clean.csv`: dataset final  
- `intensity_by_decade.csv`, `genre_statistics.csv`: resúmenes analíticos  
- `pipeline_completo.py`: script principal  
- `data_dictionary.md`, `metadata.json`: documentación técnica  
- `semana2.md`: trabajo realizado y actualizado de la semana 1 y 2

---

