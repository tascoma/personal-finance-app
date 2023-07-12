import pandas as pd
import numpy as np
from .utilities import *
import os

def process_creditcard_statements(selected_files):
    df = create_df(selected_files)
    coa_mcc_df = pd.read_csv(os.path.join('tables', 'coa_mcc_link_table.csv'))
    df['Amount'] = df['Amount'].astype('float').abs()
    df = df.pivot_table(index=['Date', 'Name', 'Memo'], columns='Transaction', values='Amount')
    df = df.reset_index()
    df[['Memo', 'MCC', 'Blank']] = df['Memo'].str.split(';', expand=True)
    df['MCC'] = df['MCC'].str[-4:]
    df['MCC'] = df['MCC'].astype('int')
    df = pd.merge(df,
                  coa_mcc_df,
                  how='left',
                  on='MCC')
    df['Date'] = pd.to_datetime(df['Date'])
    df['Description'] = df['MCC_Description'] + ': ' + df['Name']
    df = df[['Date', 'GL_Code', 'Account', 'Description', 'DEBIT', 'CREDIT']]
    df = df.round(2)
    df = df.sort_values(by='Date').reset_index(drop=True)
    df['Order_Col'] = df.index + 1
    df['Sub_Order_Col'] = np.where(df['DEBIT'].isnull(), 2, 1)
    credit_entries_df = creating_credit_entries(df,200101,'EdwardJones MasterCard')
    debit_entries_df = creating_debit_entries(df,200101,'EdwardJones MasterCard')
    df = pd.concat([df, credit_entries_df, debit_entries_df]).reset_index(drop=True)
    df = df.sort_values(by=['Order_Col', 'Sub_Order_Col']).reset_index(drop=True)
    df = df[['Date', 'GL_Code', 'Account', 'Description', 'DEBIT', 'CREDIT']]
    return df