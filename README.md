# BAI Analysis: Anxiety Patterns in Engineering Students

Este proyecto analiza niveles y patrones de ansiedad en estudiantes de ingeniería usando el Inventario de Ansiedad de Beck (BAI). El flujo completo va desde la limpieza del archivo original hasta el análisis exploratorio, clustering, modelado predictivo y reporte final de insights.

El objetivo no es hacer diagnóstico clínico, sino convertir las respuestas del BAI en evidencia descriptiva e interpretable para entender cómo se distribuye la ansiedad, qué síntomas pesan más y qué perfiles aparecen dentro de la muestra.

## Resumen Ejecutivo

- Dataset procesado: 113 registros y 21 ítems BAI.
- Variable principal: `totalScore`, calculada como suma de `BAI_1` a `BAI_21`.
- Categorías analizadas: `LOW`, `MODERATE` y `SEVERE`.
- Distribución observada: 71 casos `LOW`, 34 `MODERATE` y 8 `SEVERE`.
- Proporción moderada o severa: 37.2% de la muestra.
- Clustering: KMeans con 3 perfiles ordenados por severidad promedio.
- Clasificación: Random Forest para estimar la categoría de ansiedad a partir de síntomas, sin usar `totalScore` como predictor.

## Preguntas del Análisis

1. ¿Cómo se distribuyen los niveles de ansiedad en la muestra?
2. ¿Qué síntomas del BAI aparecen con mayor intensidad o mayor asociación con severidad?
3. ¿Existen perfiles de estudiantes con patrones diferenciados de síntomas?
4. ¿Qué tan bien se puede predecir el nivel de ansiedad usando solamente los 21 síntomas?
5. ¿Qué limitaciones deben considerarse antes de interpretar los resultados?

## Metodología

El proyecto está organizado como un pipeline reproducible en notebooks:

1. **Limpieza de datos**: carga del archivo raw, parsing de respuestas, expansión de los 21 ítems BAI, estandarización de categorías y eliminación de columnas sensibles.
2. **EDA**: revisión de distribuciones, síntomas principales, relación con variables demográficas y correlaciones.
3. **Modeling**: escalamiento de síntomas, diagnóstico de valores de `k`, clustering con KMeans, PCA para visualización, Random Forest y análisis de importancia de variables.
4. **Insights and reporting**: síntesis ejecutiva de hallazgos, interpretación, limitaciones e implicaciones prácticas.

## Hallazgos Principales

El 37.2% de la muestra se ubica en niveles `MODERATE` o `SEVERE`, por lo que la ansiedad relevante no aparece como un caso aislado dentro del dataset.

Los síntomas más informativos para el modelo incluyen inestabilidad, temblor general, miedo a perder el control, dificultad para respirar, temblor en las manos, incapacidad para relajarse, terror o miedo y latidos fuertes o rápidos. Esto sugiere que, en esta muestra, la severidad se expresa con fuerza a través de síntomas fisiológicos y de activación corporal.

El clustering identifica tres perfiles:

| Perfil | n | % | Score promedio | Lectura |
|---|---:|---:|---:|---|
| Cluster 1 | 62 | 54.9% | 10.63 | Perfil de baja ansiedad |
| Cluster 2 | 31 | 27.4% | 23.71 | Perfil intermedio, mayormente moderado |
| Cluster 3 | 20 | 17.7% | 35.70 | Perfil de mayor severidad |

El modelo Random Forest alcanza aproximadamente 79% de accuracy en test. El resultado debe leerse con cautela porque la clase `SEVERE` tiene pocos casos, pero muestra que los patrones de síntomas contienen información suficiente para aproximar la categoría de ansiedad.

## Estructura del Proyecto

```text
bai-analysis/
|-- data/
|   |-- raw/
|   |   `-- bai_raw.xlsx
|   `-- processed/
|       `-- BAI_PROCESSED.xlsx
|-- notebooks/
|   |-- 01_data_cleaning.ipynb
|   |-- 02_eda.ipynb
|   |-- 03_modeling.ipynb
|   `-- 04_insights_and_reporting.ipynb
|-- outputs/
|   `-- figures/
|       |-- anxiety_distribution.png
|       |-- bai_correlation_heatmap.png
|       |-- cluster_pca_scatter.png
|       |-- cluster_profiles.png
|       |-- cluster_sizes.png
|       |-- final_cluster_symptom_heatmap.png
|       |-- final_confusion_matrix.png
|       |-- final_feature_importance.png
|       |-- final_pca_profiles.png
|       `-- top_symptoms.png
|-- src/
|   |-- config.py
|   |-- data_loader.py
|   |-- preprocessing.py
|   `-- utils.py
|-- .env
|-- .gitignore
|-- requirements.txt
`-- README.md
```

## Datos

El archivo raw esperado es:

```text
data/raw/bai_raw.xlsx
```

El dataset limpio se guarda como:

```text
data/processed/BAI_PROCESSED.xlsx
```

Durante la preparación se eliminan columnas auxiliares o sensibles como `answers`, `email`, `name` y `date` del dataset final. El análisis usa principalmente `category`, `gender`, `totalScore` y las columnas `BAI_1` a `BAI_21`.

## Configuración

Crea un archivo `.env` en la raíz del proyecto con:

```env
BAI_DATA_PATH=data/raw/bai_raw.xlsx
DATA_PROCESSED_DIR=data/processed
```

Luego instala las dependencias:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Cómo Ejecutar

Ejecuta los notebooks en este orden:

1. `notebooks/01_data_cleaning.ipynb`
2. `notebooks/02_eda.ipynb`
3. `notebooks/03_modeling.ipynb`
4. `notebooks/04_insights_and_reporting.ipynb`

También puedes ejecutarlos con Jupyter:

```bash
jupyter notebook
```

## Outputs

Las figuras se guardan en `outputs/figures/`. Las visualizaciones principales cubren distribución de ansiedad, síntomas principales, correlaciones, perfiles de cluster, PCA, matriz de confusión e importancia de variables del modelo final.

## Limitaciones

- La muestra es pequeña, especialmente para la clase `SEVERE`.
- Las respuestas son auto-reportadas y pueden contener sesgos de respuesta.
- El análisis es transversal, así que no permite inferir causalidad.
- El modelo predictivo no debe interpretarse como herramienta diagnóstica.
- KMeans se usa con `k = 3` por alineación interpretativa con los tres niveles BAI; si el objetivo fuera separación geométrica pura, el diagnóstico de silhouette sugiere revisar alternativas.

## Estado

Pipeline completo: limpieza, EDA, modelado e insights finales. El proyecto queda listo para revisión, presentación o extensión con una muestra más grande.
