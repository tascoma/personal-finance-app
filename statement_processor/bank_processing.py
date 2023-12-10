import pandas as pd
import numpy as np


def removing_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Removes duplicate transactions from the DataFrame based on a list of keywords.

    Args:
        df (DataFrame): The DataFrame containing the bank transactions.

    Returns:
        DataFrame: The DataFrame with duplicate transactions removed.
    """
    keywords = ['WAL-MART ASSOCS. PAYROLL', 'CARDMEMBER SERV WEB PYMT']
    mask = df['Description'].str.contains('|'.join(keywords))
    return df[~mask]


def fill_in(df: pd.DataFrame) -> pd.DataFrame:
    """
    Fills in missing values for the 'account_code' and 'account' columns based on a list of keywords.

    Args:
        df (DataFrame): The DataFrame containing the bank transactions.

    Returns:
        DataFrame: The DataFrame with missing values filled in.
    """
    keywords_finserv = ['zelle', 'venmo', 'paypall']
    keywords_rent = ['pinnacle']
    keyword_edwardjones = ['edward jones']
    keyword_coinbase = ['coinbase']
    df['description'] = df['description'].str.lower()
    mask_finserv_positive = df['description'].str.contains('|'.join(keywords_finserv)) & (df['type'] == 'CREDIT')
    mask_finserv_negative = df['description'].str.contains('|'.join(keywords_finserv)) & (df['type'] == 'DEBIT')
    mask_rent = df['description'].str.contains('|'.join(keywords_rent))
    mask_edwardjones = df['description'].str.contains('|'.join(keyword_edwardjones))
    mask_coinbase = df['description'].str.contains('|'.join(keyword_coinbase))
    df['account'] = df['account'].astype(str)
    df.loc[mask_finserv_positive, 'account_code'] = 400105
    df.loc[mask_finserv_positive, 'account'] = 'Venmo, Paypall, Zelle Cash in'
    df.loc[mask_finserv_negative, 'account_code'] = 601020
    df.loc[mask_finserv_negative, 'account'] = 'Misc - Venmo, Paypall, Zelle Cash Out'
    df.loc[mask_rent, 'account_code'] = 600101
    df.loc[mask_rent, 'account'] = 'Rent Expense'
    df.loc[mask_coinbase, 'account_code'] = 100204
    df.loc[mask_coinbase, 'account'] = 'Cryptocurrency'
    df.loc[mask_edwardjones, 'account_code'] = 100201
    df.loc[mask_edwardjones, 'account'] = 'EdwardJones'
    return df


def creating_credit_entries(df: pd.DataFrame, account_code: int, account_name: str) -> pd.DataFrame:
    """
    Creates credit entries for the DataFrame based on a GL code and account name.

    Args:
        df (DataFrame): The DataFrame containing the bank transactions.
        account_code (int): The GL code to use for the credit entries.
        account_name (str): The account name to use for the credit entries.

    Returns:
        DataFrame: The DataFrame with credit entries added.
    """
    df = df[df['type'] == 'DEBIT'].reset_index(drop=True).copy()
    df['amount'] = df['amount'] / -1
    df['account_code'] = account_code
    df['account'] = account_name
    df['type'] = 'CREDIT'
    df['sub_order_col'] = 2
    return df[['transaction_date', 'account_code', 'account', 'description', 'type', 'amount', 'order_col', 'sub_order_col']]


def creating_debit_entries(df: pd.DataFrame, account_code, account_name) -> pd.DataFrame:
    """
    Creates debit entries for the DataFrame based on a GL code and account name.

    Args:
        df (DataFrame): The DataFrame containing the bank transactions.
        account_code (int): The GL code to use for the debit entries.
        account_name (str): The account name to use for the debit entries.

    Returns:
        DataFrame: The DataFrame with debit entries added.
    """
    df = df[df['type'] == 'CREDIT'].reset_index(drop=True).copy()
    df['account_code'] = account_code
    df['account'] = account_name
    df['type'] = 'DEBIT'
    df['sub_order_col'] = 1
    return df[['transaction_date', 'account_code', 'account', 'description', 'type', 'amount', 'order_col', 'sub_order_col']]


def process_bank_statement(df: pd.DataFrame) -> pd.DataFrame:
    """
    Processes bank statements by removing duplicates, filling in missing values, and creating credit and debit entries.

    Args:
        df (DataFrame): The DataFrame containing the bank transactions.

    Returns:
        DataFrame: The processed DataFrame with transaction IDs added.
    """
    df['amount'] = df['Amount'].str.replace('$', '')
    df['amount'] = df['amount'].str.replace(',', '')
    df['amount'] = df['amount'].astype('float')
    df['type'] = np.where(df['amount'] < 0, 'DEBIT', 'CREDIT')
    df['amount'] = df['amount'].abs()
    df = removing_duplicates(df).reset_index(drop=True)
    df['transaction_date'] = pd.to_datetime(df['Date'])
    df['description'] = df['Description']
    df['account_code'] = np.nan
    df['account'] = np.nan
    df = df[['transaction_date', 'account_code', 'account', 'description', 'type', 'amount']]
    df = df.sort_values(by='transaction_date').reset_index(drop=True)
    df['order_col'] = df.index + 1
    df['sub_order_col'] = np.where(df['type'] == 'DEBIT', 1, 2)
    df = fill_in(df)

    credit_entries_df = creating_credit_entries(df, 100101, 'Free Checking Bank OZK')
    debit_entries_df = creating_debit_entries(df, 100101, 'Free Checking Bank OZK')
    df = pd.concat([df, credit_entries_df, debit_entries_df]).reset_index(drop=True)

    df = df.sort_values(by=['order_col', 'sub_order_col']).reset_index(drop=True)
    df['transaction_date'] = pd.to_datetime(df['transaction_date']).dt.strftime('%Y-%m-%d')
    df['transaction_id'] = 'bank' + '-' + df['transaction_date'].astype("str") + '-' + (df.index + 1).astype("str")
    df =  df[['transaction_id', 'transaction_date', 'account_code', 'account', 'description', 'type', 'amount']]
    return df