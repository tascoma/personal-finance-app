import streamlit as st
import pandas as pd
import sqlite3


def main():
    st.set_page_config(page_title="Upload and Preview Statements", layout="wide")
    st.title('Personal Finance App')
    connection = sqlite3.connect('personal-finance.db')
    df = pd.read_sql_query("SELECT * from general_ledger", connection)
    chart_of_accounts_df = pd.read_sql_query("SELECT * from chart_of_accounts", connection)
    chart_of_accounts_df = chart_of_accounts_df[['gl_code', 'account_type']]
    df = pd.merge(df, chart_of_accounts_df, on='gl_code', how='left')
    df = df[df['account_type'].isin(['Revenue', 'Expense', 'Deduction'])]
    df['transaction_date'] = pd.to_datetime(df['transaction_date'])
    df['month_name'] = df['transaction_date'].dt.month_name()
    months = df['month_name'].unique()
    month = st.selectbox('Select Month', months)
    st.header(f'{month} Profit and Loss')
    df = df[df['month_name'] == month]
    df = df.groupby(['gl_code', 'account', 'account_type']).agg({'amount': 'sum'}).reset_index()
    st.dataframe(df, width=2500)

    total_revenue = round(df[df['account_type'] == 'Revenue']['amount'].sum(), 2)
    total_deduction = round(df[df['account_type'] == 'Deduction']['amount'].sum(), 2)
    total_take_home = round(total_revenue - total_deduction, 2)
    total_expense = round(df[df['account_type'] == 'Expense']['amount'].sum(), 2)
    total_profit = round(total_take_home - total_expense, 2)

    st.subheader(f'Total Revenue: {total_revenue}')
    st.subheader(f'Total Deduction: {total_deduction}')
    st.subheader(f'Total Take Home: {total_take_home}')
    st.subheader(f'Total Expense: {total_expense}')
    st.subheader(f'Total Profit: {total_profit}')

    


if __name__ == "__main__":
    main()