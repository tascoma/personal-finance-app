import pandas as pd
from pandas import DataFrame
import tabula
from .utilities import *


def find_earnings(df: DataFrame) -> DataFrame:
    """
    This function takes a DataFrame as input and returns a new DataFrame containing earnings data.
    """
    df = df[['Unnamed: 0', 'Unnamed: 3', 'transaction_date']]
    df = df.rename(columns={'Unnamed: 0': 'item', 'Unnamed: 3': 'amount'})
    df = df[1:]
    df = df.dropna().reset_index(drop=True)
    df = df.query("item != 'Total' and item != 'TAX' and item != 'EARNINGS'")
    return df


def find_deductions(df: DataFrame) -> DataFrame:
    """
    This function takes a DataFrame as input and returns a new DataFrame containing deductions data.
    """
    df = df[['Unnamed: 4', 'Unnamed: 5', 'transaction_date']]
    df = df.rename(columns={'Unnamed: 4': 'item', 'Unnamed: 5': 'amount'})
    df = df[1:]
    df = df.dropna().reset_index(drop=True)
    df = df.query("item != 'Total' and item != 'DEDUCTIONS' and item != 'CURRENT'")
    return df


def cash_entry(df: DataFrame) -> DataFrame:
    """
    This function takes a DataFrame as input and returns a new DataFrame containing cash entry data.
    """
    total_income = df[df['category'] == 'Income']['amount'].sum()
    total_expense = df[df['category'] != 'Income']['amount'].sum()
    total_cash = total_income - total_expense
    total_cash = round(total_cash, 2)
    date = df['transaction_date'].unique()
    cash_entry_df = pd.DataFrame({
        'transaction_date': date,
        'gl_code': [100101],
        'account': ['Free Checking Bank OZK'],
        'description': ['cash entry'],
        'amount': [total_cash]
    })
    df = df[['transaction_date', 'gl_code', 'account', 'description', 'amount']]
    result_df = pd.concat([df, cash_entry_df], ignore_index=True)
    return result_df


def process_paystub(pdf, connection):
    """
    This function takes a PDF file and a database connection as input and returns a DataFrame containing processed paystub data.
    """
    paystub_list_df = pd.read_sql_query("SELECT * FROM paystub_list", connection)
    chart_of_accounts_df = pd.read_sql("SELECT * FROM chart_of_accounts", connection)   
    df = tabula.read_pdf(pdf, pages='all', area=[396, 36, 756, 612], guess=False)
    df = pd.concat(df).reset_index(drop=True)
    df['transaction_date'] = pdf[-14:-4]
    df['transaction_date'] = pd.to_datetime(df['transaction_date']).dt.date
    earnings_df = find_earnings(df)
    deductions_df = find_deductions(df)
    df = pd.concat([earnings_df, deductions_df]).reset_index(drop=True)
    df['description'] = df['item']
    df = pd.merge(df, paystub_list_df, how='left', on='item')
    df = pd.merge(df, chart_of_accounts_df, how='left', on='gl_code')
    df = df[['transaction_date', 'gl_code', 'account', 'description', 'category', 'amount']]
    df['amount'] = df['amount'].str.replace('$', '')
    df['amount'] = df['amount'].str.replace(',', '')
    df['amount'] = df['amount'].astype(float)
    df = cash_entry(df)
    df = creating_transaction_id(df, 'ps')
    return df