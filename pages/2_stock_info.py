import streamlit as st 
import numpy as np
import pyodbc
import pandas as pd
import cufflinks as cf
import yfinance as yf 


@st.cache_data
def getsp500_Symbol():
    sp500_csv_= pd.read_csv('https://raw.githubusercontent.com/datasets/s-and-p-500-companies/main/data/constituents.csv')
    return sp500_csv_


@st.cache_data
def nq_Symbol():
    nasdaq_csv_= pd.read_csv('https://raw.githubusercontent.com/datasets/nasdaq-listings/master/data/nasdaq-listed.csv')
    return nasdaq_csv_

@st.cache_data
def get_stock_info(ticker):
    stock = yf.Ticker(ticker)
    
    # Fetch historical market data
   
    
    # Fetch other info
    return stock.info

chosen = st.sidebar.radio('Select', ("S&P 500", "Nasdaq"))

if chosen == 'S&P 500':
    options = st.sidebar.selectbox(
        "Select S&P 500 Symbol",
        getsp500_Symbol()['Symbol'].unique().tolist(),
    )
else:  # chosen == 'Nasdaq'
    options = st.sidebar.selectbox(
        "Select Nasdaq Symbol",
        nq_Symbol()['Symbol'].unique().tolist(),
    )





info = get_stock_info(options)
st.header(info['longName'])
st.write('---')
try:
    st.write(info['website'])
except:
    st.warning("NO Website")
st.info(info['longBusinessSummary'])
info_display = {
"Company Name": info.get("longName", "N/A"),
"Sector": info.get("sector", "N/A"),
"Industry": info.get("industry", "N/A"),
"Current Price": info.get('currentPrice', 'N/A'),
"Market Cap": info.get('marketCap', 'N/A'),
"52 Week High": info.get('fiftyTwoWeekHigh', 'N/A'),
"52 Week Low": info.get('fiftyTwoWeekLow', 'N/A'),
}
#st.write(info['website'])
st.table(info_display)
st.write(info)


