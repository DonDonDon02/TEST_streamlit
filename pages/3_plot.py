import streamlit as st 
import pyodbc
from numpy import NaN
import pandas as pd
import cufflinks as cf
import yfinance as yf 
import datetime
import plotly.express as px 
import pandas_ta as ta 
import plotly.graph_objs as go
from plotly.subplots import make_subplots

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
    
@st.cache_data
def get_price2(code):
    stock = yf.Ticker(code)
    data = stock.history(period='1d', start=start_date, end=end_date)
    if data.empty:
            st.warning(f"No data found for {code}. This symbol may be delisted.")
            return pd.DataFrame()  # Return an empty DataFrame
    data.reset_index(inplace=True)
    data['Date'] = data['Date'].dt.strftime('%Y/%m/%d')
    data["Code"] = code
    data = data.drop(columns=['Dividends', 'Stock Splits'])
    data2 = data.round(2)
    return data2

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



start_date = st.sidebar.date_input("Start date", datetime.date(2019, 1, 1))
end_date = st.sidebar.date_input("End date", datetime.date.today())

tickerData = yf.Ticker(options) # Get ticker data
cando = tickerData.history(period='1d', start=start_date, end=end_date)

if st.sidebar.button("Export CSV"):
    csv = cando.to_csv(index=False)
    st.sidebar.download_button(
        label="Download CSV",
        data=csv,
        file_name=f'{options}{start_date}--{end_date}data.csv',
        mime='text/csv'
    )
    st.sidebar.write("CSV file is ready to download!")


stock_price = get_price(options)

data2 = get_price2(options)

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


with st.sidebar.expander("moving avg"):
    ma1_checkbox= st.checkbox("MA1")
    ma14_checkbox= st.checkbox("MA14")
    ma50_checkbox = st.checkbox("MA50")
    ma100_checkbox = st.checkbox("MA100")


    

with st.sidebar.expander("Exponential Moving avg"):
    ema14_checkbox = st.checkbox("EMA14")
    ema50_checkbox = st.checkbox("EMA50")
    ema100_checkbox = st.checkbox("EMA100")

try:

    st.title(f'{options} - {get_stock_info(options)["longName"]}')
 
    





 
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # include candlestick with rangeselector
    fig.add_trace(go.Candlestick(x=cando.index,
                    open=cando['Open'], high=cando['High'],
                    low=cando['Low'], close=cando['Close'],name = 'K'),
                secondary_y=True)

    fig.add_trace(go.Bar(x=cando.index, y=cando['Volume'],
                        name='vol',opacity=0.5),  # Name for the trace
                secondary_y=False)

    if ma1_checkbox:
        cando['MA1'] = cando['Close']
        fig.add_trace(go.Scatter(x=cando.index, y=cando['MA1'], mode='lines', line=dict(color='red', width=1.5), name='MA 1'),secondary_y=True)

    if ma14_checkbox:
        cando['MA14'] = cando['Close'].rolling(window=14).mean()
        fig.add_trace(go.Scatter(x=cando.index, y=cando['MA14'], mode='lines', line=dict(color='blue', width=1.5), name='MA 14'),secondary_y=True)

    if ma50_checkbox:
        cando['MA50'] = cando['Close'].rolling(window=50).mean()
        fig.add_trace(go.Scatter(x=cando.index, y=cando['MA50'], mode='lines', line=dict(color='green', width=1.5), name='MA 50'),secondary_y=True)
        
    if ma100_checkbox:
        cando['MA100'] = cando['Close'].rolling(window=100).mean()
        fig.add_trace(go.Scatter(x=cando.index, y=cando['MA100'], mode='lines', line=dict(color='orange', width=1.5), name='MA 100'),secondary_y=True)

    if ema14_checkbox:
        cando['EMA14'] = ta.ema(cando['Close'], length=14)
        fig.add_trace(go.Scatter(x=cando.index, y=cando['EMA14'], mode='lines', line=dict(color='blue', width=1.5), name='EMA 14'),secondary_y=True)


    if ema50_checkbox:
        cando['EMA50'] = ta.ema(cando['Close'], length=50)
        fig.add_trace(go.Scatter(x=cando.index, y=cando['EMA50'], mode='lines', line=dict(color='green', width=1.5), name='EMA 50'),secondary_y=True)

    if ema100_checkbox:
        cando['EMA100'] = ta.ema(cando['Close'], length=100)
        fig.add_trace(go.Scatter(x=cando.index, y=cando['EMA100'], mode='lines', line=dict(color='orange', width=1.5), name='EMA 100'),secondary_y=True)

    # include a go.Bar trace for volumes

    fig.layout.yaxis2.showgrid=False
    fig.update_layout(xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)
except:
    st.warning("Stock not available")
    

#cando.reset_index(inplace=True)
#cando['Date'] = cando['Date'].dt.strftime('%Y/%m/%d')





