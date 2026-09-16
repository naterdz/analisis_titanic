from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = BASE_DIR / "data" / "train.csv"
OUTPUT_DIR = BASE_DIR / "outputs" / "resultados"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def section(title):
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)

def norm_text(series):
    return series.astype("string").str.strip().str.lower()

def main():
    df = pd.read_csv(DATA_FILE)

    section("1. EXPLORACIÓN INICIAL")
    print("Pasajeros:", len(df))
    print("Columnas:", df.shape[1])
    print("\nTipos:\n", df.dtypes)
    print("\nFaltantes:\n", df.isna().sum())
    print("\nDuplicados:", df.duplicated().sum())

    section("2. LIMPIEZA Y PREPROCESAMIENTO")
    original_rows = len(df)
    duplicate_count = int(df.duplicated().sum())
    df = df.drop_duplicates().copy()

    # Normalización de texto
    df["Name"] = df["Name"].astype("string").str.strip()
    df["Sex"] = norm_text(df["Sex"]).replace({"m":"male","f":"female"})
    df["Embarked"] = norm_text(df["Embarked"]).replace({
        "southampton":"s", "cherbourg":"c", "queenstown":"q"
    }).str.upper()

    # Survived
    df["Survived"] = norm_text(df["Survived"]).replace({
        "yes":"1", "no":"0"
    })
    df["Survived"] = pd.to_numeric(df["Survived"], errors="coerce")
    df.loc[~df["Survived"].isin([0,1]), "Survived"] = pd.NA

    # Pclass
    df["Pclass"] = norm_text(df["Pclass"]).replace({
        "1st":"1", "first":"1", "2nd":"2", "second":"2",
        "3rd":"3", "third":"3"
    })
    df["Pclass"] = pd.to_numeric(df["Pclass"], errors="coerce")
    df.loc[~df["Pclass"].isin([1,2,3]), "Pclass"] = pd.NA
    df["Pclass"] = df["Pclass"].fillna(df["Pclass"].mode().iloc[0]).astype(int)

    # Numéricas con coerción
    for col in ["Age","SibSp","Parch","Fare"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Rango lógico
    df.loc[~df["Age"].between(0, 100), "Age"] = pd.NA
    df.loc[df["SibSp"] < 0, "SibSp"] = pd.NA
    df.loc[df["Parch"] < 0, "Parch"] = pd.NA
    df.loc[df["Fare"] < 0, "Fare"] = pd.NA

    age_missing = int(df["Age"].isna().sum())
    fare_missing = int(df["Fare"].isna().sum())
    sib_missing = int(df["SibSp"].isna().sum())
    parch_missing = int(df["Parch"].isna().sum())

    # Imputación documentada
    df["Age"] = df["Age"].fillna(df["Age"].median())
    df["Fare"] = df["Fare"].fillna(df["Fare"].median())
    df["SibSp"] = df["SibSp"].fillna(0).astype(int)
    df["Parch"] = df["Parch"].fillna(0).astype(int)

    embarked_mode = df["Embarked"].dropna().mode()
    df["Embarked"] = df["Embarked"].fillna(embarked_mode.iloc[0] if not embarked_mode.empty else "S")
    df["Cabin"] = df["Cabin"].astype("string").str.strip()
    df["Cabin"] = df["Cabin"].fillna("Unknown").replace({"":"Unknown", "<NA>":"Unknown"})
    df["Sex"] = df["Sex"].fillna("unknown")
    df["Survived"] = df["Survived"].fillna(0).astype(int)

    # Nuevas variables
    df["FamilySize"] = df["SibSp"] + df["Parch"] + 1
    df["IsAlone"] = (df["FamilySize"] == 1).astype(int)
    df["HasCabin"] = (df["Cabin"] != "Unknown").astype(int)
    df["AgeGroup"] = pd.cut(
        df["Age"],
        bins=[0,13,20,60,float("inf")],
        labels=["Niño","Joven","Adulto","Adulto mayor"],
        right=False,
        include_lowest=True
    )

    print(f"Filas iniciales: {original_rows}")
    print(f"Duplicados eliminados: {duplicate_count}")
    print(f"Filas finales: {len(df)}")
    print(f"Age corregidos/imputados: {age_missing}")
    print(f"Fare corregidos/imputados: {fare_missing}")
    print(f"SibSp corregidos/imputados: {sib_missing}")
    print(f"Parch corregidos/imputados: {parch_missing}")

    section("3. ANÁLISIS")
    survival = df["Survived"].mean() * 100
    by_sex = df.groupby("Sex")["Survived"].mean().mul(100).sort_values(ascending=False)
    by_class = df.groupby("Pclass")["Survived"].mean().mul(100).sort_index()
    by_age = df.groupby("AgeGroup", observed=False)["Survived"].mean().mul(100)
    by_alone = df.groupby("IsAlone")["Survived"].mean().mul(100)

    print(f"Supervivencia total: {survival:.2f}%")
    print("\nPor sexo:\n", by_sex)
    print("\nPor clase:\n", by_class)
    print("\nPor edad:\n", by_age)
    print("\nSolo/acompañado:\n", by_alone)

    section("4. VISUALIZACIONES")
    plt.figure(figsize=(7,4))
    by_sex.plot(kind="bar")
    plt.title("Supervivencia por sexo")
    plt.ylabel("Supervivencia (%)")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "01_supervivencia_por_sexo.png", dpi=150)
    plt.close()

    plt.figure(figsize=(7,4))
    by_class.plot(kind="bar")
    plt.title("Supervivencia por clase")
    plt.ylabel("Supervivencia (%)")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "02_supervivencia_por_clase.png", dpi=150)
    plt.close()

    plt.figure(figsize=(7,4))
    by_age.plot(kind="bar")
    plt.title("Supervivencia por grupo de edad")
    plt.ylabel("Supervivencia (%)")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "03_supervivencia_por_edad.png", dpi=150)
    plt.close()

    df.to_csv(OUTPUT_DIR / "titanic_limpio.csv", index=False)
    by_sex.to_csv(OUTPUT_DIR / "supervivencia_por_sexo.csv", header=["supervivencia_pct"])
    by_class.to_csv(OUTPUT_DIR / "supervivencia_por_clase.csv", header=["supervivencia_pct"])
    by_age.to_csv(OUTPUT_DIR / "supervivencia_por_edad.csv", header=["supervivencia_pct"])

    with (OUTPUT_DIR / "reporte_limpieza.txt").open("w", encoding="utf-8") as f:
        f.write(f"Filas iniciales: {original_rows}\n")
        f.write(f"Duplicados eliminados: {duplicate_count}\n")
        f.write(f"Filas finales: {len(df)}\n")
        f.write(f"Age corregidos/imputados: {age_missing}\n")
        f.write(f"Fare corregidos/imputados: {fare_missing}\n")
        f.write(f"SibSp corregidos/imputados: {sib_missing}\n")
        f.write(f"Parch corregidos/imputados: {parch_missing}\n")

    with (OUTPUT_DIR / "conclusiones.txt").open("w", encoding="utf-8") as f:
        f.write(f"- Supervivencia total: {survival:.2f}%.\n")
        f.write(f"- Mayor supervivencia por sexo: {by_sex.idxmax()} ({by_sex.max():.2f}%).\n")
        f.write(f"- Clase con mayor supervivencia: {by_class.idxmax()} ({by_class.max():.2f}%).\n")
        f.write(f"- Grupo de edad con mayor supervivencia: {by_age.idxmax()} ({by_age.max():.2f}%).\n")

if __name__ == "__main__":
    main()
