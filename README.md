# Análisis exploratorio de pasajeros del Titanic

Proyecto de limpieza, preprocesamiento, análisis exploratorio y visualización del dataset Titanic. **No utiliza modelos de Machine Learning.**

## Dataset

- **Nombre:** Titanic
- **Fuente:** Kaggle — https://www.kaggle.com/c/titanic/data
- **Archivo utilizado:** `train.csv`
- **Descripción:** contiene información demográfica, clase de viaje, tarifa, relaciones familiares y supervivencia de pasajeros.

Coloca el archivo en:

```text
data/train.csv
```

## Objetivo

Analizar características asociadas con la supervivencia de los pasajeros mediante limpieza, transformación, análisis descriptivo y visualizaciones.

## Tratamiento de valores faltantes

- **Age:** se completa con la mediana para conservar registros y limitar la influencia de valores extremos.
- **Embarked:** se completa con la moda por ser una variable categórica.
- **Cabin:** se reemplaza el faltante con `Unknown`, evitando inventar una cabina específica.

## Nuevas variables

- `FamilySize = SibSp + Parch + 1`
- `IsAlone`: indica si el pasajero viaja solo.
- `HasCabin`: indica si existe información de cabina.
- `AgeGroup`:
  - Niño: menor de 13.
  - Joven: 13 a 19.
  - Adulto: 20 a 59.
  - Adulto mayor: 60 o más.

## Estructura

```text
proyecto_2_titanic/
├── data/
│   ├── README.md
│   └── train.csv
├── src/
│   └── analysis.py
├── outputs/
│   └── resultados/
├── README.md
├── requirements.txt
└── .gitignore
```

## Requisitos

- Python 3.10 o superior.
- Dependencias indicadas en `requirements.txt`.

## Instalación

```bash
git clone URL_DE_TU_REPOSITORIO
cd proyecto_2_titanic
python -m venv .venv
```

### Linux/macOS

```bash
source .venv/bin/activate
```

### Windows

```powershell
.venv\Scripts\activate
```

Instala dependencias:

```bash
pip install -r requirements.txt
```

## Ejecución

```bash
python src/analysis.py
```

## Análisis realizados

1. Porcentaje total de pasajeros que sobrevivió.
2. Supervivencia por sexo.
3. Supervivencia por clase.
4. Supervivencia por grupo de edad.
5. Supervivencia según viajar solo o acompañado.

## Visualizaciones

El script genera automáticamente:

- `01_supervivencia_por_sexo.png`
- `02_supervivencia_por_clase.png`
- `03_supervivencia_por_edad.png`

También guarda el dataset limpio y tablas resumen en CSV.

## Resultados y conclusiones

Las conclusiones se calculan con el dataset real al ejecutar el script y se guardan en:

```text
outputs/resultados/conclusiones.txt
```

## Reproducibilidad

Una segunda persona debe poder clonar el repositorio, crear un entorno virtual limpio, instalar `requirements.txt` y ejecutar el análisis siguiendo este README.

> Antes de la entrega final, si instalas dependencias adicionales, actualiza `requirements.txt` con `pip freeze > requirements.txt`.

Proyecto preparado para ejecución reproducible en entorno local.
