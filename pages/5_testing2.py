import streamlit as st 
import pandas as pd
import datetime
import yfinance as yf 

st.set_page_config(layout="wide")



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



buy_date = st.sidebar.date_input("buy_date", datetime.date(2019, 1, 2))
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




##################################### 
#####################################

# Initialize session state to store a DataFrame
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=['Code','Date', 'Close','Number of Shares','Total Value'])

# Function to add new row to DataFrame
def add_data(Code ,Date ,Close ,Number_of_Shares ,Total_Value ,):
    new_row = {'Code':Code ,'Date':Date, 'Close':Close,'Number of Shares':Number_of_Shares,'Total Value':Total_Value}
    st.session_state.df = st.session_state.df._append(new_row, ignore_index=True)

# User input for Name and Age

col1, col2= st.columns(2)

with col1:

    try:
        data = get_price(options,buy_date,buy_date_next)
    except:
        st.warning("weekend market close / Not avilble ")
    Number_of_Shares_ = st.number_input("Number_of_Shares_Buy", min_value=1, step=1)

    Code_buy = data['Code'].iloc[0]
    Date_buy = data['Date'].iloc[0]
    Close_buy = data['Close'].iloc[0]
    Number_of_Shares_buy = Number_of_Shares_
    Total_Value_buy = Number_of_Shares_ * Close_buy

    st.write(get_price(options,buy_date,buy_date_next))
    if st.button("Buy"):
        add_data(Code_buy ,Date_buy ,Close_buy ,Number_of_Shares_buy ,Total_Value_buy ,)



    with st.expander("Show buy record"):
        st.write(st.session_state.df)
        

with col2:

    try:
        data = get_price(options,buy_date,buy_date_next)
    except:
        st.warning("weekend market close / Not avilble ")
    Number_of_Shares_Sell = st.number_input("Number_of_Shares_Sell", min_value=1, step=1)

    Code_buy = data['Code'].iloc[0]
    Date_buy = data['Date'].iloc[0]
    Close_buy = data['Close'].iloc[0]
    Number_of_Shares_buy = Number_of_Shares_Sell
    Total_Value_buy = Number_of_Shares_Sell * Close_buy

    st.write(get_price(options,buy_date,buy_date_next))
    if st.button("Sell"):
        add_data(Code_buy ,Date_buy ,Close_buy ,Number_of_Shares_buy ,Total_Value_buy ,)



    with st.expander("Show sell record"):
        st.write(st.session_state.df)



grouped = st.session_state.df.groupby('Code').agg({
    'Number of Shares': 'sum',
    'Total Value': 'sum',

}).reset_index()

grouped['avg price'] = grouped['Total Value'] / grouped['Number of Shares']

st.write(' portfolio position')
st.write(grouped)




