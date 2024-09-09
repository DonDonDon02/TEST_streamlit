import streamlit as st 
import pyodbc
import pandas as pd
import cufflinks as cf
import yfinance as yf 
import datetime
import plotly.express as px 

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

start_date = st.sidebar.date_input("Start date", datetime.date(2019, 1, 1))
end_date = st.sidebar.date_input("End date", datetime.date(2021, 1, 31))

chosen = st.sidebar.radio('Select', ("S&P 500", "Nasdaq"))

options = st.sidebar.selectbox(
        "S&P 500",
        getsp500_Symbol()['Symbol'].unique().tolist(),
    )

options2 = st.sidebar.selectbox(
        "nasdaq",
        nq_Symbol()['Symbol'].unique().tolist(),
    )


# if chosen == 'S&P 500':

#     tickerData = yf.Ticker(options) # Get ticker data
#     tickerDf = tickerData.history(period='1d', start=start_date, end=end_date)

#     st.header('**Bollinger Bands**')
#     qf=cf.QuantFig(tickerDf,title='First Quant Figure',legend='top',name='GS')
#     qf.add_bollinger_bands()
#     fig = qf.iplot(asFigure=True)
#     st.plotly_chart(fig)  




# if chosen == 'Nasdaq':

#     tickerData = yf.Ticker(options2) # Get ticker data
#     tickerDf = tickerData.history(period='1d', start=start_date, end=end_date)

#     st.header('**Bollinger Bands**')
#     qf=cf.QuantFig(tickerDf,title='First Quant Figure',legend='top',name='GS')
#     qf.add_bollinger_bands()
#     fig = qf.iplot(asFigure=True)
#     st.plotly_chart(fig)  
    
    
tickerData = yf.Ticker("AAPL") # Get ticker data
df = tickerData.history(period='1d', start='2020-01-01', end='2024-01-01') #get the historical prices for this ticker
df.reset_index(inplace=True)
df = df.round(2)
df['Date'] = df['Date'].dt.strftime('%Y/%m/%d')
df.set_index('Date', inplace=True)
st.line_chart(df['Close'])