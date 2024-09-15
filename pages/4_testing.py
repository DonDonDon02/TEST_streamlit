import streamlit as st
import pandas as pd
import datetime
import yfinance as yf

st.set_page_config(layout="wide")

# Cache the symbols for S&P 500 and Nasdaq
@st.cache_data
def get_sp500_symbols():
    sp500_csv = pd.read_csv('https://raw.githubusercontent.com/datasets/s-and-p-500-companies/main/data/constituents.csv')
    return sp500_csv

@st.cache_data
def get_nasdaq_symbols():
    nasdaq_csv = pd.read_csv('https://raw.githubusercontent.com/datasets/nasdaq-listings/master/data/nasdaq-listed.csv')
    return nasdaq_csv

# Sidebar to choose between S&P 500 and Nasdaq
chosen = st.sidebar.radio('Select Market', ("S&P 500", "Nasdaq"))

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

# Date inputs for buying and selling
buy_date = st.sidebar.date_input("Buy Date", datetime.date(2019, 1, 2))
sell_date = st.sidebar.date_input("Sell Date", datetime.date.today())

# Cache the stock price fetching function
@st.cache_data
def fetch_stock_price(symbol, start_date, end_date):
    stock = yf.Ticker(symbol)
    data = stock.history(period='1d', start=start_date, end=end_date)
    if data.empty:
        st.warning(f"No data found for {symbol}. This symbol may be delisted.")
        return pd.DataFrame()  # Return an empty DataFrame
    data.reset_index(inplace=True)
    data['Date'] = data['Date'].dt.strftime('%Y/%m/%d')
    data["Symbol"] = symbol
    data = data.drop(columns=['Dividends', 'Stock Splits'])
    data = data.round(2)
    return data

# Initialize session state for buy and sell records
if 'buy_record' not in st.session_state:
    st.session_state.buy_record = pd.DataFrame(columns=['Symbol', 'Date', 'Close', 'Number of Shares', 'Total Value'])
    
if 'sell_record' not in st.session_state:
    st.session_state.sell_record = pd.DataFrame(columns=['Symbol', 'Date', 'Close', 'Number of Shares', 'Total Value'])

# Function to add new row to the buy record
def add_buy_record(symbol, date, close, number_of_shares, total_value):
    new_row = {'Symbol': symbol, 'Date': date, 'Close': close, 'Number of Shares': number_of_shares, 'Total Value': total_value}
    st.session_state.buy_record = st.session_state.buy_record._append(new_row, ignore_index=True)

# Function to add new row to the sell record
def add_sell_record(symbol, date, close, number_of_shares, total_value):
    new_row = {'Symbol': symbol, 'Date': date, 'Close': close, 'Number of Shares': number_of_shares, 'Total Value': total_value}
    st.session_state.sell_record = st.session_state.sell_record._append(new_row, ignore_index=True)

# User input for buying shares
col1, col2 = st.columns(2)

with col1:
    st.header("Buy Shares")
    buy_data = fetch_stock_price(options, buy_date, buy_date + datetime.timedelta(days=1))
    if not buy_data.empty:
        st.write(buy_data[['Date', 'Close', 'Symbol']])
        number_of_shares_buy = st.number_input("Number of Shares to Buy", min_value=1, step=1)
        if st.button("Buy"):
            buy_code = buy_data['Symbol'].iloc[0]
            buy_date_value = buy_data['Date'].iloc[0]
            buy_close_value = buy_data['Close'].iloc[0]
            total_value_buy = number_of_shares_buy * buy_close_value
            add_buy_record(buy_code, buy_date_value, buy_close_value, number_of_shares_buy, total_value_buy)
            st.success(f"Bought {number_of_shares_buy} shares of {options} at {buy_close_value}")

    with st.expander("Show Buy Record"):
        st.write(st.session_state.buy_record)

# User input for selling shares
with col2:
    st.header("Sell Shares")
    sell_data = fetch_stock_price(options, sell_date, sell_date + datetime.timedelta(days=1))
    if not sell_data.empty:
        st.write(sell_data[['Date', 'Close', 'Symbol']])
        number_of_shares_sell = st.number_input("Number of Shares to Sell", min_value=1, step=1)
        if st.button("Sell"):
            sell_code = sell_data['Symbol'].iloc[0]
            sell_date_value = sell_data['Date'].iloc[0]
            sell_close_value = sell_data['Close'].iloc[0]
            total_value_sell = number_of_shares_sell * sell_close_value
            add_sell_record(sell_code, sell_date_value, sell_close_value, number_of_shares_sell, total_value_sell)
            st.success(f"Sold {number_of_shares_sell} shares of {options} at {sell_close_value}")

    with st.expander("Show Sell Record"):
        st.write(st.session_state.sell_record)

# Group buy records
grouped_buy = st.session_state.buy_record.groupby('Symbol').agg({
    'Number of Shares': 'sum',
    'Total Value': 'sum',
}).reset_index()

grouped_buy['Avg Buy Price'] = grouped_buy['Total Value'] / grouped_buy['Number of Shares']

# Group sell records
grouped_sell = st.session_state.sell_record.groupby('Symbol').agg({
    'Number of Shares': 'sum',
    'Total Value': 'sum',
}).reset_index()

grouped_sell['Avg Sell Price'] = grouped_sell['Total Value'] / grouped_sell['Number of Shares']

# Merge buy and sell records to calculate the portfolio
portfolio = pd.merge(grouped_buy, grouped_sell, on='Symbol', how='left', suffixes=('_Buy', '_Sell'))

portfolio['Shares Held'] = portfolio['Number of Shares_Buy'] - portfolio['Number of Shares_Sell'].fillna(0)
portfolio['Holding Value'] = portfolio['Total Value_Buy'] - portfolio['Total Value_Sell'].fillna(0)
portfolio['Difference in Value'] = portfolio['Total Value_Sell'].fillna(0) - portfolio['Total Value_Buy']
portfolio['Difference in Shares'] = portfolio['Number of Shares_Sell'].fillna(0) - portfolio['Number of Shares_Buy']

# Display the portfolio
st.header("Portfolio Summary")
st.write(portfolio[['Symbol', 'Shares Held', 'Holding Value', 'Difference in Value', 'Difference in Shares']])

# Reset records button
if st.sidebar.button("Reset All Records"):
    st.session_state.buy_record = pd.DataFrame(columns=['Symbol', 'Date', 'Close', 'Number of Shares', 'Total Value'])
    st.session_state.sell_record = pd.DataFrame(columns=['Symbol', 'Date', 'Close', 'Number of Shares', 'Total Value'])
    st.success("All records have been reset.")