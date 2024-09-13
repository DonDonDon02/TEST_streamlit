import streamlit as st
import pandas as pd

# Initialize session state to store a DataFrame
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=['Name', 'Age'])

# Function to add new row to DataFrame
def add_data(name, age):
    new_row = {'Name': name, 'Age': age}
    st.session_state.df = st.session_state.df._append(new_row, ignore_index=True)

# User input for Name and Age
name = st.text_input("Enter name")
age = st.number_input("Enter age", min_value=0, step=1)

if st.button("Add Data"):
    add_data(name, age)

# Display the DataFrame
st.write(st.session_state.df)