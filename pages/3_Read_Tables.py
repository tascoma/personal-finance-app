import streamlit as st
import pandas as pd
import sqlite3


# Set up the Streamlit page
st.title("Read Tables")
connection = sqlite3.connect('personal-finance.db')
tables = ['chart_of_accounts', 'general_ledger', 'mcc_list', 'paystub_list']
table_name = st.selectbox("Select a Table", tables)

# Define the query based on the selected table
if table_name == 'general_ledger':
    start_date = st.date_input("Start Date")
    end_date = st.date_input("End Date")
    df = pd.read_sql(f"SELECT * FROM {table_name} WHERE transaction_date BETWEEN '{start_date}' AND '{end_date}'", connection)
elif table_name == 'chart_of_accounts':
    st.subheader("GL Code Ranges")
    st.write("100000 - 199999: Assets")
    st.write("200000 - 299999: Liabilities")
    st.write("300000 - 399999: Equity")
    st.write("400000 - 499999: Revenue")
    st.write("500000 - 599999: Deductions")
    st.write("600000 - 699999: Expenses")
    start_gl_account = st.number_input("Start GL Account")
    end_gl_account = st.number_input("End GL Account")
    df = pd.read_sql(f"SELECT * FROM {table_name} WHERE gl_code BETWEEN {start_gl_account} AND {end_gl_account}", connection)
else:
    df = pd.read_sql(f"SELECT * FROM {table_name}", connection)

# Display the dataframe and the number of rows
st.dataframe(df, width=2500)
connection.close()
st.write(f"Number of rows: {len(df)}")