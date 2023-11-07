import numpy as np
import pandas as pd
import sqlite3


def creating_credit_entries(df: pd.DataFrame, account_code: int, account_name: str) -> pd.DataFrame:
    """
    This function creates credit entries for a given DataFrame, GL code, and account name.
    
    Args:
        df (pd.DataFrame): The DataFrame to create credit entries for.
        account_code (int): The GL code to assign to the credit entries.
        account_name (str): The name of the account to assign to the credit entries.
    
    Returns:
        pd.DataFrame: A DataFrame containing the credit entries.
    """
    df = df[df['type'] == 'DEBIT'].reset_index(drop=True).copy()
    df['account_code'] = account_code
    df['account'] = account_name
    df['type'] = 'CREDIT'
    df['sub_order_col'] = 2
    return df[['transaction_date', 'account_code', 'account', 'description', 'type', 'amount', 'order_col', 'sub_order_col']]


def creating_debit_entries(df: pd.DataFrame, account_code: int, account_name: str) -> pd.DataFrame:
    """
    This function creates debit entries for a given DataFrame, GL code, and account name.
    
    Args:
        df (pd.DataFrame): The DataFrame to create debit entries for.
        account_code (int): The GL code to assign to the debit entries.
        account_name (str): The name of the account to assign to the debit entries.
    
    Returns:
        pd.DataFrame: A DataFrame containing the debit entries.
    """
    df = df[df['type'] == 'CREDIT'].reset_index(drop=True).copy()
    df['account_code'] = account_code
    df['account'] = account_name
    df['type'] = 'DEBIT'
    df['sub_order_col'] = 1
    return df[['transaction_date', 'account_code', 'account', 'description', 'type', 'amount', 'order_col', 'sub_order_col']]


def process_creditcard_statement(df: pd.DataFrame, connection: sqlite3.Connection) -> pd.DataFrame:
    """
    This function processes credit card statements for a given DataFrame and database connection.
    
    Args:
        df (pd.DataFrame): The DataFrame containing the credit card statements to process.
        connection (sqlite3.Connection): The database connection to use for querying MCC list and chart of accounts.
    
    Returns:
        pd.DataFrame: A DataFrame containing the processed credit card statements.
    """
    mcc_list_df = pd.read_sql_query("SELECT * FROM mcc_list", connection)
    chart_of_accounts_df = pd.read_sql("SELECT * FROM chart_of_accounts", connection)
    
    df['amount'] = df['Amount'] / -1
    df[['Memo', 'MCC', 'Blank']] = df['Memo'].str.split(';', expand=True)
    df['MCC'] = df['MCC'].str[-4:]
    df['MCC'] = df['MCC'].astype('int')
    df = pd.merge(df, mcc_list_df, how='left', left_on='MCC', right_on='mcc')
    df = pd.merge(df, chart_of_accounts_df, how='left', on='account_code')
    df['transaction_date'] = pd.to_datetime(df['Date'])
    df['description'] = (df['description'] + ': ' + df['Name']).str.strip()
    df = df.rename(columns={'Transaction': 'type'})
    df = df[['transaction_date', 'account_code', 'account', 'description', 'type', 'amount']]
    df = df.sort_values(by='transaction_date').reset_index(drop=True)
    df['order_col'] = df.index + 1
    df['sub_order_col'] = np.where(df['type'] == 'DEBIT', 1, 2)
    
    credit_entries_df = creating_credit_entries(df, 200101, 'EdwardJones MasterCard')
    debit_entries_df = creating_debit_entries(df, 200101, 'EdwardJones MasterCard')
    df = pd.concat([df, credit_entries_df, debit_entries_df]).reset_index(drop=True)
    df = df.sort_values(by=['order_col', 'sub_order_col']).reset_index(drop=True)
    df = df[['transaction_date', 'account_code', 'account', 'description', 'type', 'amount']]
    df['transaction_date'] = pd.to_datetime(df['transaction_date']).dt.strftime('%Y-%m-%d')
    df['transaction_id'] = 'cc' + '-' + df['transaction_date'].astype("str") + '-' + (df.index + 1).astype("str")
    df =  df[['transaction_id', 'transaction_date', 'account_code', 'account', 'description', 'type', 'amount']]
    return df