import streamlit as st 
import pyodbc
import pandas as pd
import cufflinks as cf
import yfinance as yf 
import datetime
import plotly.express as px 

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Close Price", 1)
with col2:
    st.metric("Price Difference (YoY)", 2)
with col3:
    st.metric("52-Week High",2)
with col4:
    st.metric("52-Week Low", 2)


def get_stock_info(ticker):
    stock = yf.Ticker(ticker)
    
    # Fetch historical market data
   
    
    # Fetch other info
    return stock.info

st.write(get_stock_info('aapl'))

