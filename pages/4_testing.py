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
    


buy_record_df = pd.concat([buy_record_df, buy_data], ignore_index=True)

st.write(buy_record)

