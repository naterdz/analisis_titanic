# Calidad del dataset sintético — Titanic

> **Importante:** este archivo es sintético y fue creado para practicar limpieza y reproducibilidad.
> No debe presentarse como el `train.csv` original de Kaggle.

## Problemas introducidos intencionalmente

- Más de 1,000 pasajeros.
- Duplicados exactos.
- `Age` con faltantes, texto, valores negativos y edades imposibles.
- `Cabin` con alta proporción de faltantes.
- `Embarked` con faltantes y variantes (`S`, `Southampton`, `southampton`, etc.).
- `Sex` con mayúsculas, espacios y abreviaturas.
- `Pclass` con valores como `1st`, `2nd`, `First`.
- `Survived` con algunos `Yes/No`.
- `Fare` con valores faltantes, texto y outliers.
- `SibSp` y `Parch` con algunos errores de captura.
- Nombres con espacios inconsistentes.
- Duplicados para comprobar su detección.

## Objetivo de limpieza

El análisis debe:
1. normalizar variables categóricas;
2. convertir columnas numéricas con coerción;
3. tratar edades y tarifas inválidas;
4. imputar valores faltantes con criterios explicados;
5. conservar la ausencia de cabina como información;
6. crear `FamilySize`, `IsAlone`, `HasCabin` y `AgeGroup`;
7. documentar las correcciones realizadas.
