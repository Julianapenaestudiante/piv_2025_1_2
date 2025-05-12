import requests
import pandas as pd
import requests
import pandas as pd
from bs4 import BeautifulSoup
from logger import Logger
import os
import re

class Collector:
    def __init__(self, logger):
        self.url = 'https://es.finance.yahoo.com/quote/META/history/'
        self.logger = logger

        os.makedirs('src/edu_piv/static/data', exist_ok=True)

    def collector_data(self):
        df = pd.DataFrame()

        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(self.url, headers=headers)

            if response.status_code != 200:
                self.logger.error("Collector", "collector_data", f"Error al consultar la URL: {response.status_code}")
                return df

            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.select_one('div[data-testid="history-table"] table')

            if table is None:
                self.logger.error("Collector", "collector_data", "No se encontró la tabla con data-testid='history-table'")
                return df

            headerss = [th.get_text(strip=True) for th in table.thead.find_all('th')]
            rows = []
            for tr in table.tbody.find_all('tr'):
                columnas = [td.get_text(strip=True) for td in tr.find_all('td')]
                if len(columnas) == len(headerss):
                    rows.append(columnas)

            df = pd.DataFrame(rows, columns=headerss)

            # Renombrar columnas si se reconocen
            mapeo_columnas = {}
            for col in df.columns:
                c = col.lower()
                if 'date' in c or 'fecha' in c:
                    mapeo_columnas[col] = 'fecha'
                elif 'open' in c or 'abrir' in c:
                    mapeo_columnas[col] = 'abrir'
                elif 'high' in c or 'máx' in c:
                    mapeo_columnas[col] = 'max'
                elif 'low' in c or 'mín' in c:
                    mapeo_columnas[col] = 'min'
                elif 'close' in c and 'adj' not in c:
                    mapeo_columnas[col] = 'cerrar'
                elif 'adj' in c:
                    mapeo_columnas[col] = 'cierre_ajustado'
                elif 'volume' in c or 'volumen' in c:
                    mapeo_columnas[col] = 'volumen'

            df.rename(columns=mapeo_columnas, inplace=True)

            # LIMPIEZA DE VALORES CON EXPRESIONES REGULARES
            columnas_flotantes = ['abrir', 'max', 'min', 'cerrar', 'cierre_ajustado']
            for col in columnas_flotantes:
                if col in df.columns:
                    df[col] = df[col].astype(str).apply(lambda x: re.sub(r'[^\d.,-]', '', x))
                    df[col] = df[col].str.replace(',', '')
                    df[col] = pd.to_numeric(df[col], errors='coerce')

            if 'volumen' in df.columns:
                df['volumen'] = df['volumen'].astype(str).apply(lambda x: re.sub(r'[^\d]', '', x))
                df['volumen'] = pd.to_numeric(df['volumen'], errors='coerce', downcast='integer')

            self.logger.info("Collector", "collector_data", f"Datos obtenidos exitosamente {df.shape}")
            return df

        except Exception as error:
            self.logger.error("Collector", "collector_data", f"Error al obtener los datos: {error}")
            return df
