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
else:  
    options = st.sidebar.selectbox(
        "Select Nasdaq Symbol",
        nq_Symbol()['Symbol'].unique().tolist(),
        
    )




info = get_stock_info(options)

try:
    st.header(info['longName'])
    st.subheader(options)
    st.write('---')
    st.write(info['website'])
except:
    st.warning("Not available")
st.write(info['longBusinessSummary'])
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


with st.expander("Show more info"):
   st.write(info)

if st.button("Click me"):
    pass

# if chosen == 'Nasdaq':

#     try:

#         st.header(get_stock_info(options2)['longName'])
#     except:
#         st.warning("NOT FOUND ")
#     st.write('---')
#     try:
#         st.write(get_stock_info(options2)['irWebsite'])
#     except:
#         st.warning("NO Website")
#     st.info(get_stock_info(options2)['longBusinessSummary'])


