import streamlit as st
import pandas as pd
import sqlite3


# Set up the Streamlit page
st.title("Delete Journal Entries")
conn = sqlite3.connect('personal-finance.db')
df = pd.read_sql_query("SELECT * from general_ledger", conn)

duplicates = df[df.duplicated()]
num_duplicates = len(duplicates)
st.write(f"Number of duplicate rows: {num_duplicates}")

if num_duplicates > 0:
    st.write("Duplicate rows:")
    st.dataframe(duplicates, width=2500)

    if st.button("Remove duplicate rows"):
        num_rows_before = len(df)
        st.write(f"Number of rows before removing duplicates: {num_rows_before}")
        df = df.drop_duplicates()
        num_rows_removed = num_rows_before - len(df)
        st.write(f"Number of rows removed: {num_rows_removed}")
        num_rows_after = len(df)
        st.write(f"Number of rows after removing duplicates: {num_rows_after}")
        df.to_sql('general_ledger', conn, if_exists='replace', index=False)