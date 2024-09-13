import streamlit as st

# Initialize session state
if 'data' not in st.session_state:
    st.session_state['data'] = []

# Function to add data to session state
def add_data(new_data):
    st.session_state.data.append(new_data)

# User input to add data
user_input = st.text_input("Enter some data")

if st.button("Add Data"):
    add_data(user_input)
    st.write(f"Data stored: {st.session_state.data}")