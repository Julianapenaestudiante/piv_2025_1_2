from logger import Logger
from collector import Collector
import pandas as pd

def main():
    logger = Logger()  # Usa tu clase completa
    logger.info("Main", "main", "Inicializar clase Logger")

    collector = Collector(logger)
    df = collector.collector_data()

    df.to_csv("src/edu_piv/static/data/Meta_data.csv", index=False)

if __name__ == "__main__":
    main()