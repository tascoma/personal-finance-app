import pandas as pd
import numpy as np
from .utilities import *


def removing_duplicates(df: DataFrame) -> DataFrame:
    keywords = ['WAL-MART ASSOCS. PAYROLL', 'CARDMEMBER SERV WEB PYMT']
    mask = df['Description'].str.contains('|'.join(keywords))
    return df[~mask]


def fill_in(df: DataFrame) -> DataFrame:
    keywords_finserv = ['zelle', 'venmo', 'paypall']
    keywords_rent = ['pinnacle']
    keyword_edwardjones = ['edward jones']
    keyword_coinbase = ['coinbase']
    df['description'] = df['description'].str.lower()
    mask_finserv_positive = df['description'].str.contains('|'.join(keywords_finserv)) & (df['transaction'] == 'CREDIT')
    mask_finserv_negative = df['description'].str.contains('|'.join(keywords_finserv)) & (df['transaction'] == 'DEBIT')
    mask_rent = df['description'].str.contains('|'.join(keywords_rent))
    mask_edwardjones = df['description'].str.contains('|'.join(keyword_edwardjones))
    mask_coinbase = df['description'].str.contains('|'.join(keyword_coinbase))
    df['account'] = df['account'].astype(str)
    df.loc[mask_finserv_positive, 'gl_code'] = 400105
    df.loc[mask_finserv_positive, 'account'] = 'Venmo, Paypall, Zelle Cash in'
    df.loc[mask_finserv_negative, 'gl_code'] = 601020
    df.loc[mask_finserv_negative, 'account'] = 'Misc - Venmo, Paypall, Zelle Cash Out'
    df.loc[mask_rent, 'gl_code'] = 600101
    df.loc[mask_rent, 'account'] = 'Rent Expense'
    df.loc[mask_coinbase, 'gl_code'] = 100204
    df.loc[mask_coinbase, 'account'] = 'Cryptocurrency'
    df.loc[mask_edwardjones, 'gl_code'] = 100201
    df.loc[mask_edwardjones, 'account'] = 'EdwardJones'
    return df


def creating_credit_entries(df:DataFrame, gl_code, account_name) -> DataFrame:
    df = df[df['transaction'] == 'DEBIT'].reset_index(drop=True).copy()
    df['amount'] = df['amount'] / -1
    df['gl_code'] = gl_code
    df['account'] = account_name
    df['sub_order_col'] = 2
    return df[['transaction_date', 'gl_code', 'account', 'description', 'amount', 'order_col', 'sub_order_col']]


def creating_debit_entries(df:DataFrame, gl_code, account_name) -> DataFrame:
    df = df[df['transaction'] == 'CREDIT'].reset_index(drop=True).copy()
    df['gl_code'] = gl_code
    df['account'] = account_name
    df['sub_order_col'] = 1
    return df[['transaction_date', 'gl_code', 'account', 'description', 'amount', 'order_col', 'sub_order_col']]


def process_bank_statements(df:DataFrame) -> DataFrame:
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
    df = fill_in(df)
    credit_entries_df = creating_credit_entries(df,100101,'Free Checking Bank OZK')
    debit_entries_df = creating_debit_entries(df,100101,'Free Checking Bank OZK')
    df = pd.concat([df, credit_entries_df, debit_entries_df]).reset_index(drop=True)
    df = df.sort_values(by=['order_col', 'sub_order_col']).reset_index(drop=True)
    df = df[['transaction_date', 'gl_code', 'account', 'description', 'amount']]
    df = creating_transaction_id(df, 'bank')
    return df