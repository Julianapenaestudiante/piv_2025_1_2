# piv_2025_1_2

## Descripción

Este proyecto corresponde a una actividad académica del curso de Programación en Ingeniería de Valores (PIV) del primer semestre de 2025. 
El objetivo principal es analizar el comportamiento histórico de un indicador financiero, en este caso, las acciones de Meta Platforms Inc. (META), 
utilizando herramientas de análisis de datos en Python.

Los datos históricos de las acciones de META se obtuvieron de Yahoo Finance:  
[Historial de precios de META](https://finance.yahoo.com/quote/META/history/?period1=1337347800&period2=1746906104)

## Estructura del Proyecto

El repositorio está organizado de la siguiente manera:
├── .github/
│ └── workflows/
│ └── update_data.yml
├── src/
│ └── edu_piv/
│ ├── static/
│ │ └── data/
│ │ ├── historical.db
│ │ └── historical.csv
│ ├── collector.py
│ └── logger.py
│ └── main.py
├── docs/
│ └── report_entrega1.pdf
├── prueba.py
├── setup.py
├── .gitignore
└── README.md


## Instalación

Para instalar las dependencias y configurar el entorno de desarrollo, sigue los siguientes pasos:

1. Clona el repositorio:

   ```bash
   git clone https://github.com/Julianapenaestudiante/piv_2025_1_2.git
   cd piv_2025_1_2
   
python -m venv env
source env/bin/activate  # En Windows: env\Scripts\activate

python setup.py install
Este comando instalará todas las dependencias necesarias para ejecutar el proyecto.

Uso
Después de completar la instalación, puedes ejecutar el análisis principal con:

bash
Copiar
Editar
python prueba.py
Este script descargará y procesará los datos históricos de las acciones de META.

Indicador Financiero Analizado
El indicador financiero seleccionado son las acciones de Meta Platforms Inc. (símbolo bursátil: META).
Se analizaron los datos históricos de precios obtenidos de Yahoo Finance para evaluar tendencias y comportamientos relevantes.





