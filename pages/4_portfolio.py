import streamlit as st 
import pandas as pd
import datetime
import yfinance as yf 
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.express as px


st.set_page_config(layout="wide")

@st.cache_data
def get_sp500_symbols():
    sp500_csv = pd.read_csv('https://raw.githubusercontent.com/datasets/s-and-p-500-companies/main/data/constituents.csv')
    return sp500_csv

@st.cache_data
def get_nasdaq_symbols():
    nasdaq_csv = pd.read_csv('https://raw.githubusercontent.com/datasets/nasdaq-listings/master/data/nasdaq-listed.csv')
    return nasdaq_csv

chosen = st.sidebar.radio('Select', ("S&P 500", "Nasdaq"))

if chosen == 'S&P 500':
    options = st.sidebar.selectbox(
        "Select S&P 500 Symbol",
        get_sp500_symbols()['Symbol'].unique().tolist(),
    )
else:  # chosen == 'Nasdaq'
    options = st.sidebar.selectbox(
        "Select Nasdaq Symbol",
        get_nasdaq_symbols()['Symbol'].unique().tolist(),
    )
    
@st.cache_data
def get_stock_info(ticker):
    stock = yf.Ticker(ticker)
    
    # Fetch historical market data
   
    
    # Fetch other info
    return stock.info

buy_date = st.sidebar.date_input("Buy Date", datetime.date(2019, 1, 2))
buy_date_next = buy_date + datetime.timedelta(days=1)

sell_date = st.sidebar.date_input("Sell Date", datetime.date.today())
sell_date_next = sell_date + datetime.timedelta(days=1)

@st.cache_data
def fetch_stock_price(symbol, start_date, end_date):
    stock = yf.Ticker(symbol)
    data = stock.history(period='1d', start=start_date, end=end_date)
    if data.empty:
        st.warning(f"No data found for {symbol}.Try not select weekend.")
        return pd.DataFrame()  # Return an empty DataFrame
    data.reset_index(inplace=True)
    data['Date'] = data['Date'].dt.strftime('%Y/%m/%d')
    data["Symbol"] = symbol
    data = data.drop(columns=['Dividends', 'Stock Splits'])
    data = data.round(2)
    return data



tickerData = yf.Ticker(options) # Get ticker data
cando = tickerData.history(period='1d', start=buy_date, end=sell_date)

if not cando.empty:
    st.title(f'{options} - {get_stock_info(options)["longName"]}')

 
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    




    fig.add_trace(go.Candlestick(x=cando.index,
                    open=cando['Open'], high=cando['High'],
                    low=cando['Low'], close=cando['Close'],name = 'K'),
                secondary_y=True)

    fig.add_trace(go.Bar(x=cando.index, y=cando['Volume'], 
                              marker=dict(color=['green' if close >= open else 'red' for close, open in zip(cando['Close'], cando['Open'])]),
                              name='Volume',opacity=0.5))
    
    fig.layout.yaxis2.showgrid=False
    fig.update_layout(xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)
    
else:
    st.warning("not availber")

# Initialize session state 
if 'buy_record' not in st.session_state:
    st.session_state.buy_record = pd.DataFrame(columns=['Symbol', 'Date', 'Close', 'Number of Shares', 'Total Value'])
    
if 'sell_record' not in st.session_state:
    st.session_state.sell_record = pd.DataFrame(columns=['Symbol', 'Date', 'Close', 'Number of Shares', 'Total Value'])


def add_buy_record(symbol, date, close, number_of_shares, total_value):
    new_row = {'Symbol': symbol, 'Date': date, 'Close': close, 'Number of Shares': number_of_shares, 'Total Value': total_value}
    st.session_state.buy_record = st.session_state.buy_record._append(new_row, ignore_index=True)

def add_sell_record(symbol, date, close, number_of_shares, total_value):
    new_row = {'Symbol': symbol, 'Date': date, 'Close': close, 'Number of Shares': number_of_shares, 'Total Value': total_value}
    st.session_state.sell_record = st.session_state.sell_record._append(new_row, ignore_index=True)

col1, col2 = st.columns(2)

with col1:
    buy_data = fetch_stock_price(options, buy_date, buy_date_next)
    number_of_shares_buy = st.number_input("Number of Shares to Buy", min_value=1, step=1)

    if not buy_data.empty:
        buy_code = buy_data['Symbol'].iloc[0]
        buy_date_value = buy_data['Date'].iloc[0]
        buy_close_value = buy_data['Close'].iloc[0]
        total_value_buy = number_of_shares_buy * buy_close_value

        st.write(buy_data[['Date', 'Close', 'Symbol']])
        if st.button("Buy"):
            add_buy_record(buy_code, buy_date_value, buy_close_value, number_of_shares_buy, total_value_buy)

    with st.expander("Show Buy Record"):
        st.write(st.session_state.buy_record)

with col2:
    sell_data = fetch_stock_price(options, sell_date, sell_date_next)
    number_of_shares_sell = st.number_input("Number of Shares to Sell", min_value=1, step=1)

    if not sell_data.empty:
        sell_code = sell_data['Symbol'].iloc[0]
        sell_date_value = sell_data['Date'].iloc[0]
        sell_close_value = sell_data['Close'].iloc[0]
        total_value_sell = number_of_shares_sell * sell_close_value

        st.write(sell_data[['Date', 'Close', 'Symbol']])
        if st.button("Sell"):
            add_sell_record(sell_code, sell_date_value, sell_close_value, number_of_shares_sell, total_value_sell)
                

    with st.expander("Show Sell Record"):
        st.write(st.session_state.sell_record)


col1 ,col2 = st.columns(2)
with col1 :

    grouped_buy = st.session_state.buy_record.groupby('Symbol').agg({
        'Number of Shares': 'sum',
        'Total Value': 'sum',
    }).reset_index()

    grouped_buy['Avg Price'] = grouped_buy['Total Value'] / grouped_buy['Number of Shares']

    st.title('holding')
    st.write(grouped_buy)

with col2:
    grouped_sell = st.session_state.sell_record.groupby('Symbol').agg({
        'Number of Shares': 'sum',
        'Total Value': 'sum',
    }).reset_index()

    grouped_sell['Avg Price'] = grouped_sell['Total Value'] / grouped_sell['Number of Shares']

    st.title('selling')
    st.write(grouped_sell)
    

portfolio = pd.merge(grouped_buy, grouped_sell, on='Symbol', how='left', suffixes=('_Buy', '_Sell'))

portfolio['Shares Held'] = portfolio['Number of Shares_Buy'] - portfolio['Number of Shares_Sell'].fillna(0)
portfolio['Holding Value'] = portfolio['Total Value_Buy'] - portfolio['Total Value_Sell'].fillna(0)
portfolio['Difference in Value'] = portfolio['Total Value_Sell'].fillna(0) - portfolio['Total Value_Buy']
portfolio['Difference in Shares'] = portfolio['Number of Shares_Sell'].fillna(0) - portfolio['Number of Shares_Buy']

#portfolio
st.header("Portfolio Summary")
st.write(portfolio[['Symbol', 'Shares Held', 'Holding Value', 'Difference in Value', 'Difference in Shares']])

portfolio_with_shares = portfolio[portfolio['Shares Held'] > 0]


fig = px.pie(
    portfolio_with_shares, 
    values='Holding Value', 
    names='Symbol', 
    title='Portfolio Stock Value Distribution',
    hover_data=['Holding Value'],
    labels={'Holding Value': 'Stock Value'},
)

fig.update_traces(textinfo='label+percent', textposition='inside', showlegend=True)

# Display the pie chart in Streamlit
st.plotly_chart(fig)

# Reset button
if st.sidebar.button("Reset All Records"):
    st.session_state.buy_record = pd.DataFrame(columns=['Symbol', 'Date', 'Close', 'Number of Shares', 'Total Value'])
    st.session_state.sell_record = pd.DataFrame(columns=['Symbol', 'Date', 'Close', 'Number of Shares', 'Total Value'])
    st.success("All records have been reset.")