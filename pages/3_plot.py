import streamlit as st 
import pyodbc
from numpy import NaN
import pandas as pd
import cufflinks as cf
import yfinance as yf 
import datetime
import plotly.express as px 
import pandas_ta as ta 

#ta.ma

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

@st.cache_data
def get_price(code):
    stock = yf.Ticker(code)
    data = stock.history(period="5y")
    if data.empty:
            st.warning(f"No data found for {code}. This symbol may be delisted.")
            return pd.DataFrame()  # Return an empty DataFrame
    data.reset_index(inplace=True)
    data['Date'] = data['Date'].dt.strftime('%Y/%m/%d')
    data["Code"] = code
    data = data.drop(columns=['Dividends', 'Stock Splits'])
    data = data.round(2)
    return data
    

start_date = st.sidebar.date_input("Start date", datetime.date(2019, 1, 1))
end_date = st.sidebar.date_input("End date", datetime.date.today())

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

stock_price = get_price(options)

@st.cache_data
def calculate_price_difference(stock_data):
    latest_price = stock_data.iloc[-1]["Close"]
    previous_year_price = stock_data.iloc[-252]["Close"] if len(stock_data) > 252 else stock_data.iloc[0]["Close"]
    price_difference = latest_price - previous_year_price
    percentage_difference = (price_difference / previous_year_price) * 100
    return price_difference, percentage_difference

price_difference, percentage_difference = calculate_price_difference(stock_price)

latest_close_price = stock_price.iloc[-1]["Close"]
max_52_week_high = stock_price["High"].tail(252).max()
min_52_week_low = stock_price["Low"].tail(252).min()
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
    
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Close Price", f"${latest_close_price:.2f}")
with col2:
    st.metric("Price Difference (YoY)", f"${price_difference:.2f}", f"{percentage_difference:+.2f}%")
with col3:
    st.metric("52-Week High", f"${max_52_week_high:.2f}")
with col4:
    st.metric("52-Week Low", f"${min_52_week_low:.2f}")
    

try:
    tickerData = yf.Ticker(options) # Get ticker data
    df = tickerData.history(period='1d', start=start_date, end=end_date) #get the historical prices for this ticker
    df.reset_index(inplace=True)
    df = df.round(2)
    df['Date'] = df['Date'].dt.strftime('%Y/%m/%d')
    st.title(options)
    df.set_index('Date', inplace=True)
    st.line_chart(df['Close'])
except:
    st.warning("Stock not available")
    


