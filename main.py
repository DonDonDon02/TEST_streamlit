import streamlit as st
st.title("Donavan ,Test")

import pyodbc
import os 
from dotenv import load_dotenv
import pandas as pd




load_dotenv()



# server = os.getenv('DATABASE_SER')
# database = 'mySampleDatabase'
# username = os.getenv('DATABASE_USERNAME')
# password = os.getenv('DATABASE_PASSWORD')
# driver = '{ODBC Driver 18 for SQL Server}'

server = st.secrets['DATABASE_SER']
database = 'donavan02_1'
username = st.secrets['DATABASE_USERNAME']
password = st.secrets['DATABASE_PASSWORD']
driver = '{ODBC Driver 17 for SQL Server}'


#with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
#    with conn.cursor() as cursor:
#        # Execute the query
#        cursor.execute('''
#      SELECT TOP (1000) [id]
#      ,[date]
#      ,[open]
#      ,[high]
#      ,[low]
#      ,[close]
#      ,[volume]
#      ,[code]
#      ,[diff]
#  FROM [dbo].[sp500_stock_data]
          
#        ''')
#        # Fetch all rows
#        rows = cursor.fetchall()
#        # Convert to DataFrame
#        df = pd.DataFrame.from_records(rows, columns=[desc[0] for desc in cursor.description])




st.write("Hello")


