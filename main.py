import streamlit as st


import pyodbc
import os 
from dotenv import load_dotenv
import pandas as pd




load_dotenv()



# server = os.getenv('DATABASE_SER')
# database = 'mySampleDatabase'
# username = os.getenv('DATABASE_USERNAME')
# password = os.getenv('DATABASE_PASSWORD')
# driver = '{ODBC Driver 18 for SQL Server}'

server = st.secrets['DATABASE_SER']
database = 'donavan02_1'
username = st.secrets['DATABASE_USERNAME']
password = st.secrets['DATABASE_PASSWORD']
driver = '{ODBC Driver 17 for SQL Server}'


#with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
#    with conn.cursor() as cursor:
#        # Execute the query
#        cursor.execute('''
#      SELECT TOP (1000) [id]
#      ,[date]
#      ,[open]
#      ,[high]
#      ,[low]
#      ,[close]
#      ,[volume]
#      ,[code]
#      ,[diff]
#  FROM [dbo].[sp500_stock_data]
          
#        ''')
#        # Fetch all rows
#        rows = cursor.fetchall()
#        # Convert to DataFrame
#        df = pd.DataFrame.from_records(rows, columns=[desc[0] for desc in cursor.description])




st.write("""
         # Stock Analysis App 

## Overview
This project is a Streamlit application that allows users to analyze stock data for companies listed in the S&P 500 and Nasdaq. Users can filter companies by GICS sector and sub-industry, view historical stock performance, and visualize key metrics such as moving averages and the Relative Strength Index (RSI).

## Features
- **Data Visualization**: Display stock prices using candlestick charts and moving averages.
- **Stock Filtering**: Filter companies by sector and sub-industry.
- **Historical Data**: Fetch and display historical stock data for selected companies.
- **Metrics Display**: Show important financial metrics such as current price, market cap, 52-week high/low, and more.
- **Downloadable Data**: Export historical stock data as a CSV file.

## Requirements
To run this application, ensure you have the following Python packages installed:

- `streamlit`
- `pandas==2.2.2`
- `pyodbc==5.1.0`
- `python-dotenv`
- `yfinance==0.2.43`
- `cufflinks==0.17.3`
- `prophet==1.1.5`
- `numpy==1.26.4`
- `plotly==5.24.0`
- `pandas_ta==0.3.14b0`
- `matplotlib==3.9.0`

You can install these packages using pip:
```bash
pip install requirements.txt
```
To install Microsoft ODBC driver 17 for SQL Server on macOS, run the following commands:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
brew update
HOMEBREW_ACCEPT_EULA=Y brew install msodbcsql17 mssql-tools
```
To install Microsoft ODBC driver 17 for SQL Server on Windows

https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver16 

please install `Version 17`

## Getting Started
1. **Clone the Repository**: 
   ```bash
   git clone https://github.com/DonDonDon02/stock_streamlit.git
   
   ```

2. **Run the Application**:
   ```bash
   streamlit run main.py
   ```

3. **Interact with the App**:
   - Use the sidebar to select between S&P 500 and Nasdaq.
   - Choose a specific stock symbol to view its data.
   - Use the filters to narrow down your search based on sector and sub-industry.
   - Visualize stock performance and metrics.
""")


