import streamlit as st 
import pandas as pd
import datetime
import yfinance as yf 

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

buy_date = st.sidebar.date_input("Buy Date", datetime.date(2019, 1, 2))
buy_date_next = buy_date + datetime.timedelta(days=1)

sell_date = st.sidebar.date_input("Sell Date", datetime.date.today())
sell_date_next = sell_date + datetime.timedelta(days=1)

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

# Initialize session state to store a DataFrame
if 'buy_record' not in st.session_state:
    st.session_state.buy_record = pd.DataFrame(columns=['Symbol', 'Date', 'Close', 'Number of Shares', 'Total Value'])
    
if 'sell_record' not in st.session_state:
    st.session_state.sell_record = pd.DataFrame(columns=['Symbol', 'Date', 'Close', 'Number of Shares', 'Total Value'])

# Function to add new row to DataFrame
def add_buy_record(symbol, date, close, number_of_shares, total_value):
    new_row = {'Symbol': symbol, 'Date': date, 'Close': close, 'Number of Shares': number_of_shares, 'Total Value': total_value}
    st.session_state.buy_record = st.session_state.buy_record._append(new_row, ignore_index=True)

def add_sell_record(symbol, date, close, number_of_shares, total_value):
    new_row = {'Symbol': symbol, 'Date': date, 'Close': close, 'Number of Shares': number_of_shares, 'Total Value': total_value}
    st.session_state.sell_record = st.session_state.sell_record._append(new_row, ignore_index=True)

# User input for buying
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
    

profo = pd.DataFrame({
    'Symbol': grouped_buy['Symbol'],
    'Shares Held': grouped_buy['Number of Shares'] - (grouped_sell['Number of Shares'] if not grouped_sell['Number of Shares'].empty else 0),
    'Holding Value': grouped_buy['Total Value'],
    'Selling Value': grouped_sell['Total Value'],
    'Difference in Value': grouped_sell['Total Value'] - grouped_buy['Total Value'],
    'Difference in Shares': grouped_sell['Number of Shares'] - grouped_buy['Number of Shares']
})

st.write(profo)

# Reset button
if st.sidebar.button("Reset All Records"):
    st.session_state.buy_record = pd.DataFrame(columns=['Symbol', 'Date', 'Close', 'Number of Shares', 'Total Value'])
    st.session_state.sell_record = pd.DataFrame(columns=['Symbol', 'Date', 'Close', 'Number of Shares', 'Total Value'])
    st.success("All records have been reset.")