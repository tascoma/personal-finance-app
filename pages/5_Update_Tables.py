import streamlit as st
import pandas as pd
import sqlite3

# Set up the Streamlit page
st.title("Update database")
connection = sqlite3.connect('personal-finance.db')
tables = ['chart_of_accounts', 'general_ledger', 'mcc_list', 'paystub_list']
table_name = st.selectbox("Select a Table", tables)

chart_of_accounts_df = pd.read_sql(f"SELECT * FROM chart_of_accounts", connection)
gl_codes = chart_of_accounts_df['gl_code'].unique()
accounts = chart_of_accounts_df['account'].unique()

df = pd.read_sql(f"SELECT * FROM {table_name}", connection)
st.dataframe(df, width=1000)

if table_name == 'general_ledger':
    row_index = st.number_input("Enter the row index to update", min_value=0, max_value=len(df)-1, step=1)
    df = df.iloc[row_index]
    st.dataframe(df, width=1000)
    transaction_id = st.text_input("Transaction ID")
    transaction_date = st.date_input("Transaction Date")
    gl_code = st.selectbox("Select a GL Code", gl_codes)
    account = st.selectbox("Select an Account", accounts)
    description = st.text_input("Description")
    amount = st.number_input("Amount")