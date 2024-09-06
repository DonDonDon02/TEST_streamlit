import streamlit as st
import yfinance as yf
import pandas as pd
import cufflinks as cf
import datetime
import ssl


ssl._create_default_https_context = ssl._create_unverified_context

# st.sidebar.subheader('Query parameters')
# start_date = st.sidebar.date_input("Start date", datetime.date(2019, 1, 1))
# end_date = st.sidebar.date_input("End date", datetime.date.today())



st.title("S&P 500\n -----")
sp500_csv_= pd.read_csv('https://raw.githubusercontent.com/datasets/s-and-p-500-companies/main/data/constituents.csv')
st.write(sp500_csv_)

st.title("Nasdaq\n -----")
nasdaq_csv_= pd.read_csv('https://raw.githubusercontent.com/datasets/nasdaq-listings/master/data/nasdaq-listed.csv')
st.write(nasdaq_csv_)
 
# tickerData = yf.Ticker("AAPL")
# data = tickerData.info
# st.write(data)


options = st.sidebar.multiselect(
    "S&P 500 GICS Sector",
    sp500_csv_["GICS Sector"].unique().tolist(),
    
)

options2 = st.sidebar.multiselect(
    "S&P GICS Sub-Industry",
    sp500_csv_["GICS Sub-Industry"].unique().tolist()  ,
    
)
st.sidebar.markdown("---")
if options or options2:
    st.title("S&P 500 filter \n -----")
    filtered_data = sp500_csv_[
        sp500_csv_["GICS Sector"].isin(options) | sp500_csv_["GICS Sub-Industry"].isin(options2)
    ]
    
    st.write(filtered_data,'\n -----')
    
    
    
