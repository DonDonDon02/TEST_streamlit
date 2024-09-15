# Stock Analysis App 

## Overview
This project is a Streamlit application that allows users to analyze stock data for companies listed in the S&P 500 and Nasdaq. Users can filter companies by GICS sector and sub-industry, view historical stock performance, and visualize key metrics such as moving averages and the Relative Strength Index (RSI).

## Features

- **Stock Information and Overview**: Users can view company details, stock prices, and market data for S&P 500 and Nasdaq companies.
- **Data Filtering and Visualization**: Filter companies based on sectors and sub-industries, and visualize stock performance with candlestick charts and moving averages.
- **Stock Metrics and Indicators**: View key metrics such as 52-week high/low, relative strength index (RSI), and moving averages (MA, EMA).
- **Portfolio Management**: Users can simulate buying and selling stocks, track their portfolio, and view a summary of holdings.


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
 -  Use the sidebar to select companies from S&P 500 or Nasdaq.
 - Visualize stock performance with interactive charts.
 - Filter companies by sector or sub-industry.
 - Simulate buying and selling stocks.
 - Track your portfolio and view holdings in real time.
