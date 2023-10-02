import pandas as pd
import numpy as np
from .utilities import *


def removing_duplicates(df):
    keywords = ['WAL-MART ASSOCS. PAYROLL', 'CARDMEMBER SERV WEB PYMT']
    mask = df['Description'].str.contains('|'.join(keywords))
    return df[~mask]


def creating_credit_entries(df, gl_code, account_name):
    df = df[df['transaction'] == 'DEBIT'].reset_index(drop=True).copy()
    df['amount'] = df['amount'] / -1
    df['gl_code'] = gl_code
    df['account'] = account_name
    df['sub_order_col'] = 2
    return df[['transaction_date', 'gl_code', 'account', 'description', 'amount', 'order_col', 'sub_order_col']]


def creating_debit_entries(df, gl_code, account_name):
    df = df[df['transaction'] == 'CREDIT'].reset_index(drop=True).copy()
    df['gl_code'] = gl_code
    df['account'] = account_name
    df['sub_order_col'] = 1
    return df[['transaction_date', 'gl_code', 'account', 'description', 'amount', 'order_col', 'sub_order_col']]


def process_bank_statements(df):
    df['amount'] = df['Amount'].str.replace('$', '')
    df['amount'] = df['amount'].str.replace(',', '')
    df['amount'] = df['amount'].astype('float')
    df['transaction'] = np.where(df['amount'] < 0, 'DEBIT', 'CREDIT')
    df['amount'] = df['amount'].abs()
    df = removing_duplicates(df).reset_index(drop=True)
    df['transaction_date'] = pd.to_datetime(df['Date'])
    df['description'] = df['Description']
    df['gl_code'] = np.nan
    df['account'] = np.nan
    df = df[['transaction_date', 'gl_code', 'account', 'description', 'amount', 'transaction']]
    df = df.sort_values(by='transaction_date').reset_index(drop=True)
    df['order_col'] = df.index + 1
    df['sub_order_col'] = np.where(df['transaction'] == 'DEBIT', 1, 2)
    credit_entries_df = creating_credit_entries(df,100101,'Free Checking Bank OZK')
    debit_entries_df = creating_debit_entries(df,100101,'Free Checking Bank OZK')
    df = pd.concat([df, credit_entries_df, debit_entries_df]).reset_index(drop=True)
    df = df.sort_values(by=['order_col', 'sub_order_col']).reset_index(drop=True)
    df = creating_transaction_id(df, 'bank')
    df = df[['transaction_id', 'transaction_date', 'gl_code', 'account', 'description', 'amount']]
    return df