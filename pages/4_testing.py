import streamlit as st 
import pandas as pd
import datetime
import yfinance as yf 

@st.cache_data
def getsp500_Symbol():
    sp500_csv_= pd.read_csv('https://raw.githubusercontent.com/datasets/s-and-p-500-companies/main/data/constituents.csv')
    return sp500_csv_


@st.cache_data
def nq_Symbol():
    nasdaq_csv_= pd.read_csv('https://raw.githubusercontent.com/datasets/nasdaq-listings/master/data/nasdaq-listed.csv')
    return nasdaq_csv_


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


buy_record = ["Date", "Open", "High", "Low", "Close", "Volume", "Code"]

buy_record_df = pd.DataFrame(columns=buy_record)

buy_date = st.sidebar.date_input("buy_date", datetime.date(2019, 1, 1))
buy_date_next = buy_date + datetime.timedelta(days=1)

sell_date = st.sidebar.date_input("sell_date", datetime.date.today())
sell_date_next = sell_date + datetime.timedelta(days=1)

    
@st.cache_data
def get_price(code,date1,date2):
    stock = yf.Ticker(code)
    data = stock.history(period='1d', start=date1, end=date2)
    if data.empty:
            st.warning(f"No data found for {code}. This symbol may be delisted.")
            return pd.DataFrame()  # Return an empty DataFrame
    data.reset_index(inplace=True)
    data['Date'] = data['Date'].dt.strftime('%Y/%m/%d')
    data["Code"] = code
    data = data.drop(columns=['Dividends', 'Stock Splits'])
    data = data.round(2)
    return data



buy_data = get_price(options,buy_date,buy_date_next)
st.write(buy_data)

sell_data = get_price(options,sell_date,sell_date_next)
st.write(sell_data)

diff = sell_data['Close'] -buy_data['Close']
st.write( diff)


def calculate_price_difference():
    latest_price = float(sell_data['Close'].iloc[0]) 
    previous_year_price = float(buy_data['Close'].iloc[0])
    price_difference = latest_price - previous_year_price
    percentage_difference = (price_difference / previous_year_price) * 100
    return price_difference, percentage_difference

price_difference,percentage_difference = calculate_price_difference()

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Price Difference (YoY)", f"${price_difference:.2f}", f"{percentage_difference:+.2f}%")
    
with col2:
    st.metric("Price Difference (YoY)",diff)
with col3:
    st.metric("52-Week High",diff)
with col4:
    st.metric("52-Week Low",diff)
    
########################################################################################################################

import streamlit as st
import yfinance as yf
import pandas as pd
import datetime

# Set up the main title and sidebar header
st.title("Stock Trading Simulation App")
st.sidebar.header("Configure Trading Simulation")

# Sidebar inputs for stock selection and date range
symbol = st.sidebar.text_input("Enter Stock Symbol", value='AAPL')
start_date = st.sidebar.date_input("Start Date", datetime.date(2020, 1, 1))
end_date = st.sidebar.date_input("End Date", datetime.date.today())

# Fetch stock data using yfinance
if symbol:
    data = yf.download(symbol, start=start_date, end=end_date)
    if not data.empty:
        st.subheader(f"Price Data for {symbol}")
        st.line_chart(data['Close'])
    else:
        st.error("No data found for the entered symbol.")

# Initialize session state to store portfolio information
if 'portfolio' not in st.session_state:
    st.session_state.portfolio = {
        'Cash': 10000,  # Starting cash balance
        'Positions': {},  # Dictionary to hold stock positions
        'Transaction History': []  # List to record transactions
    }

portfolio = st.session_state.portfolio

st.sidebar.subheader("Trading Actions")

# Input for buying stocks
buy_quantity = st.sidebar.number_input("Buy Quantity", min_value=1, value=10)
if st.sidebar.button("Buy"):
    if not data.empty:
        price = data['Close'][-1]
        cost = buy_quantity * price
        if portfolio['Cash'] >= cost:
            portfolio['Cash'] -= cost
            portfolio['Positions'][symbol] = portfolio['Positions'].get(symbol, 0) + buy_quantity
            portfolio['Transaction History'].append({
                'Type': 'Buy',
                'Symbol': symbol,
                'Quantity': buy_quantity,
                'Price': price,
                'Date': datetime.datetime.now()
            })
            st.sidebar.success(f"Bought {buy_quantity} shares of {symbol} at ${price:.2f}")
        else:
            st.sidebar.error("Insufficient cash to complete the purchase.")
    else:
        st.sidebar.error("No price data available to execute the trade.")

# Input for selling stocks
sell_quantity = st.sidebar.number_input("Sell Quantity", min_value=1, value=10)
if st.sidebar.button("Sell"):
    if not data.empty:
        if portfolio['Positions'].get(symbol, 0) >= sell_quantity:
            price = data['Close'][-1]
            revenue = sell_quantity * price
            portfolio['Cash'] += revenue
            portfolio['Positions'][symbol] -= sell_quantity
            portfolio['Transaction History'].append({
                'Type': 'Sell',
                'Symbol': symbol,
                'Quantity': sell_quantity,
                'Price': price,
                'Date': datetime.datetime.now()
            })
            st.sidebar.success(f"Sold {sell_quantity} shares of {symbol} at ${price:.2f}")
        else:
            st.sidebar.error(f"Not enough shares of {symbol} to sell.")
    else:
        st.sidebar.error("No price data available to execute the trade.")

# Display portfolio summary
st.header("Portfolio Summary")

# Display cash balance
st.write(f"**Cash Balance:** ${portfolio['Cash']:.2f}")

# Display current stock positions
if portfolio['Positions']:
    positions_df = pd.DataFrame.from_dict(
        portfolio['Positions'], orient='index', columns=['Quantity']
    )
    positions_df.index.name = 'Symbol'
    st.write("**Positions:**")
    st.table(positions_df)
else:
    st.write("No positions held.")

# Display transaction history
if portfolio['Transaction History']:
    history_df = pd.DataFrame(portfolio['Transaction History'])
    st.write("**Transaction History:**")
    st.table(history_df)
else:
    st.write("No transactions made yet.")
