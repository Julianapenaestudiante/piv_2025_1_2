import requests
import pandas as pd
from bs4 import BeautifulSoup
from logger import Logger
import os

class Collector:
    def __init__(self, logger):
        self.url = 'https://finance.yahoo.com/quote/META/history/?period1=1337347800&period2=1746906104'
        self.logger = logger

        # Crear las carpetas necesarias si no existen
        os.makedirs('src/edu_piv/static/data', exist_ok=True)

    def collector_data(self):
        df = pd.DataFrame()  # DataFrame vacío en caso de error

        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(self.url, headers=headers)

            if response.status_code != 200:
                self.logger.error("Collector", "collector_data", f"Error al consultar la URL: {response.status_code}")
                return df

            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.select_one('div[data-testid="history-table"] table')

            if table is None:
                self.logger.error("Collector", "collector_data", "Tabla no encontrada en la página.")
                return df

            # Extraer encabezados y filas
            headerss = [th.get_text(strip=True) for th in table.thead.find_all('th')]
            rows = []
            for tr in table.tbody.find_all('tr'):
                columns = [td.get_text(strip=True) for td in tr.find_all('td')]
                if len(columns) == len(headerss):
                    rows.append(columns)

            # Crear DataFrame
            df = pd.DataFrame(rows, columns=headerss)

            print("🔎 Encabezados originales:")
            print(df.columns.tolist())

            # Renombrado dinámico basado en contenido
            column_map = {}
            for col in df.columns:
                col_lower = col.lower()
                if "date" in col_lower or "fecha" in col_lower:
                    column_map[col] = "fecha"
                elif "open" in col_lower or "abrir" in col_lower:
                    column_map[col] = "abrir"
                elif "high" in col_lower or "máx" in col_lower:
                    column_map[col] = "max"
                elif "low" in col_lower or "mín" in col_lower:
                    column_map[col] = "min"
                elif "close" in col_lower and "adj" not in col_lower:
                    column_map[col] = "cerrar"
                elif "adj" in col_lower:
                    column_map[col] = "cierre_ajustado"
                elif "volume" in col_lower or "volumen" in col_lower:
                    column_map[col] = "volumen"

            df.rename(columns=column_map, inplace=True)

            # Normalizar todos los nombres de columnas
            df.columns = df.columns.str.lower().str.replace(" ", "_").str.replace("*", "").str.replace("**", "")

            self.logger.info("Collector", "collector_data", f"Datos obtenidos exitosamente {df.shape}")
            return df

        except Exception as error:
            self.logger.error("Collector", "collector_data", f"Error al obtener los datos: {error}")
            return df



