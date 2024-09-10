import streamlit as st 
import pyodbc
import pandas as pd
import cufflinks as cf
import yfinance as yf 
import datetime
import plotly.express as px 
import pandas_ta as ta


def get_stock_info(ticker):
    stock = yf.Ticker(ticker)
    
    # Fetch historical market data
   
    
    # Fetch other info
    return stock.info

st.write(get_stock_info('aapl'))