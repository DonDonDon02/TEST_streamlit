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

options = st.sidebar.selectbox(
        "S&P 500",
        getsp500_Symbol()['Symbol'].unique().tolist(),
    )

options2 = st.sidebar.selectbox(
        "nasdaq",
        nq_Symbol()['Symbol'].unique().tolist(),
    )


if chosen == 'S&P 500':

    info = get_stock_info(options)

    st.header(info['longName'])
    st.write('---')
    try:
        st.write(info['irWebsite'])
    except:
        st.warning("NO Website")
    st.info(info['longBusinessSummary'])

    info_display = {
    "Company Name": info.get("longName", "N/A"),
    "Sector": info.get("sector", "N/A"),
    "Industry": info.get("industry", "N/A"),
    "Current Price": info.get('currentPrice', 'N/A'),
    "Market Cap": info.get('marketCap', 'N/A'),
    "52 Week High": round(info.get('fiftyTwoWeekHigh', 'N/A'),2),
    "52 Week Low": round(info.get('fiftyTwoWeekLow', 'N/A'),2),
    }

    st.table(info_display)



if chosen == 'Nasdaq':

    try:

        st.header(get_stock_info(options2)['longName'])
    except:
        st.warning("NOT FOUND ")
    st.write('---')
    try:
        st.write(get_stock_info(options2)['irWebsite'])
    except:
        st.warning("NO Website")
    st.info(get_stock_info(options2)['longBusinessSummary'])


