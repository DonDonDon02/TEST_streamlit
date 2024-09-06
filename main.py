import streamlit as st
st.title("Hello")

import pyodbc
import os 
from dotenv import load_dotenv
import pandas as pd



load_dotenv()



server = os.getenv('DATABASE_SER')
database = 'mySampleDatabase'
username = os.getenv('DATABASE_USERNAME')
password = os.getenv('DATABASE_PASSWORD')
driver = '{ODBC Driver 18 for SQL Server}'
 
with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
    with conn.cursor() as cursor:
        # Execute the query
        cursor.execute('''
            SELECT TOP 20 pc.Name as CategoryName, p.name as ProductName
            FROM SalesLT.ProductCategory pc
            JOIN SalesLT.Product p
            ON pc.productcategoryid = p.productcategoryid;
        ''')

        # Fetch all rows
        rows = cursor.fetchall()

        # Convert to DataFrame
        df = pd.DataFrame.from_records(rows, columns=[desc[0] for desc in cursor.description])

# Display the DataFrame


st.write(df)




