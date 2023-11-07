import numpy as np
import pandas as pd
import sqlite3
import tabula


def find_earnings(df: pd.DataFrame) -> pd.DataFrame:
    """
    This function takes a DataFrame as input and returns a new DataFrame containing earnings data.

    Args:
        df: DataFrame - input DataFrame containing paystub data

    Returns:
        pd.DataFrame: A DataFrame containing earnings data.
    """
    df = df[['Unnamed: 0', 'Unnamed: 3', 'transaction_date']]
    df = df.rename(columns={'Unnamed: 0': 'item', 'Unnamed: 3': 'amount'})
    df = df[1:]
    df = df.dropna().reset_index(drop=True)
    df = df.query("item != 'Total' and item != 'TAX' and item != 'EARNINGS'")
    return df


def find_deductions(df: pd.DataFrame) -> pd.DataFrame:
    """
    This function takes a DataFrame as input and returns a new DataFrame containing deductions data.

    Args:
        df: DataFrame - input DataFrame containing paystub data
    
    Returns:
        pd.DataFrame: A DataFrame containing deductions data.
    """
    df = df[['Unnamed: 4', 'Unnamed: 5', 'transaction_date']]
    df = df.rename(columns={'Unnamed: 4': 'item', 'Unnamed: 5': 'amount'})
    df = df[1:]
    df = df.dropna().reset_index(drop=True)
    df = df.query("item != 'Total' and item != 'DEDUCTIONS' and item != 'CURRENT'")
    return df


def cash_entry(df: pd.DataFrame) -> pd.DataFrame:
    """
    This function takes a DataFrame as input and returns a new DataFrame containing cash entry data.

    Args:
        df: DataFrame - input DataFrame containing paystub data

    Returns:
        pd.DataFrame: A DataFrame containing cash entry data.
    """
    total_income = df[df['account_subtype'] == 'Income']['amount'].sum()
    total_expense = df[df['account_subtype'] != 'Income']['amount'].sum()
    total_cash = total_income - total_expense
    total_cash = round(total_cash, 2)
    date = df['transaction_date'].unique()
    cash_entry_df = pd.DataFrame({
        'transaction_date': date,
        'account_code': [100101],
        'account': ['Free Checking Bank OZK'],
        'description': ['cash entry'],
        'type': ['DEBIT'],
        'amount': [total_cash]
    })
    df = df[['transaction_date', 'account_code', 'account', 'description', 'type', 'amount']]
    result_df = pd.concat([df, cash_entry_df], ignore_index=True)
    return result_df


def process_paystub(pdf, connection: sqlite3.Connection) -> pd.DataFrame:
    """
    This function processes paystubs for a given PDF and database connection.

    Args:
        pdf: PDF - PDF containing the paystub to process.
        connection: Connection - The database connection to use for querying paystub list and chart of accounts.

    Returns:
        pd.DataFrame: A DataFrame containing the processed paystub.
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
    df = pd.merge(df, chart_of_accounts_df, how='left', on='account_code')
    df = df[['transaction_date', 'account_code', 'account', 'description', 'amount', 'account_subtype']]
    df['amount'] = df['amount'].str.replace('$', '')
    df['amount'] = df['amount'].str.replace(',', '')
    df['amount'] = df['amount'].astype(float)
    df['type'] = np.where(df['account_subtype'] == 'Income', 'CREDIT', 'DEBIT')

    df = cash_entry(df)
    df['transaction_date'] = pd.to_datetime(df['transaction_date']).dt.strftime('%Y-%m-%d')
    df['transaction_id'] = 'ps' + '-' + df['transaction_date'].astype("str") + '-' + (df.index + 1).astype("str")
    df =  df[['transaction_id', 'transaction_date', 'account_code', 'account', 'description', 'type', 'amount']]
    return df