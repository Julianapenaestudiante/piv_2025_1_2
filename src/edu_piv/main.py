from logger import Logger
from collector import Collector
import pandas as pd
from sqlalchemy import create_engine
import sqlite3
from datetime import date

def main():
    # === Inicializar logger y colector ===
    logger = Logger()
    logger.info("Main", "main", "Inicializar clase Logger")

    collector = Collector(logger)
    df = collector.collector_data()

    # === LIMPIEZA DE DATOS ===
    df = df.loc[:, ~df.columns.duplicated()]  # Eliminar columnas duplicadas

    # Limpiar fechas
    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
    df = df.dropna(subset=['fecha'])

    # Convertir columna 'fecha' a solo date (sin hora)
    df['fecha'] = df['fecha'].dt.date

    # Convertir columnas numéricas
    columnas_numericas = ['abrir', 'max', 'min', 'cerrar', 'cierre_ajustado', 'volumen']
    for col in columnas_numericas:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace(',', '').str.replace('.', '.', regex=False)
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Agregar columna de fecha de descarga
    df['fecha_descarga'] = date.today()

    # === VISTA PREVIA ===
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_colwidth', None)
    pd.set_option('display.width', None)

    print("\n📊 Vista previa de los datos limpios:")
    print(df.head())
    print(f"\n📐 Dimensión final: {df.shape}")
    print(f"🧾 Columnas: {df.columns.tolist()}")

    # === GUARDAR COMO CSV ===
    csv_path = "src/edu_piv/static/data/meta_history.csv"
    df.to_csv(csv_path, index=False)
    print(f"\n✅ CSV guardado en: {csv_path}")

    # === GUARDAR EN SQLITE SIN DUPLICAR FECHAS ===
    db_path = "src/edu_piv/static/data/meta_data.db"
    engine = create_engine(f"sqlite:///{db_path}")
    conn = sqlite3.connect(db_path)

    try:
        df_existente = pd.read_sql("SELECT * FROM meta", conn)
        df_existente['fecha'] = pd.to_datetime(df_existente['fecha'], errors='coerce').dt.date
        fechas_existentes = df_existente['fecha'].unique()

        # Filtrar solo fechas nuevas
        df_nuevo = df[~df['fecha'].isin(fechas_existentes)]
        print(f"\n🔁 Filas nuevas a guardar: {df_nuevo.shape[0]}")

    except Exception:
        print("\nℹ️ La tabla no existe. Se guardarán todos los datos.")
        df_nuevo = df

    if not df_nuevo.empty:
        df_nuevo.to_sql("meta", con=engine, if_exists="append", index=False)
        print("✅ Nuevos datos guardados en base de datos.")
    else:
        print("⚠️ No hay filas nuevas para guardar.")

if __name__ == "__main__":
    main()

