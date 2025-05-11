import requests
import pandas as pd
from bs4 import BeautifulSoup
from logger import Logger
import os

class Collector:
    def __init__(self, logger):
        self.url = 'https://finance.yahoo.com/quote/META/history/?period1=1337347800&period2=1746906104'
        self.logger = logger

        # Crear carpetas si no existen
        if not os.path.exists('src/edu_piv/static'):
            os.makedirs('src/edu_piv/static')
        if not os.path.exists('src/edu_piv/static/data'):
            os.makedirs('src/edu_piv/static/data')

    def collector_data(self):
        df = pd.DataFrame()  # Crear df vacío por si ocurre un error

        try:
            headers = {
                'User-Agent': 'Mozilla/5.0'
            }

            response = requests.get(self.url, headers=headers)
            if response.status_code != 200:
                self.logger.error("Collector", "collector_data", f"Error al consultar la URL: {response.status_code}")
                return df

            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.select_one('div[data-testid="history-table"] table')

            if table is None:
                self.logger.error("Collector", "collector_data", "Error al buscar la tabla con data-testid=history-table")
                return df

            headerss = [th.get_text(strip=True) for th in table.thead.find_all('th')]
            rows = []

            for tr in table.tbody.find_all('tr'):
                columns = [td.get_text(strip=True) for td in tr.find_all('td')]
                if len(columns) == len(headerss):
                    rows.append(columns)

            df = pd.DataFrame(rows, columns=headerss).rename(columns={
                'Fecha': 'fecha',
                'Abrir': 'abrir',
                'Máx.': 'max',
                'Mín.': 'min',
                'CerrarPrecio de cierre ajustado para splits.': 'cerrar',
                'Cierre ajustadoPrecio de cierre ajustado para splits y distribuciones de dividendos o plusvalías.': 'cierre_ajustado',
                'Volumen': 'volumen'
            })

            self.logger.info("Collector", "collector_data", f"Datos obtenidos exitosamente {df.shape}")
            return df

        except Exception as error:
            self.logger.error("Collector", "collector_data", f"Error al obtener los datos de la URL: {error}")
            return df


