import os
import add_package
import configparser
import pandas as pd
import numpy as np
from financialstatements.utils import creating_input_paths
from financialstatements.utils import missing_gl_check
from financialstatements.utils import missing_mcc
from financialstatements.utils import debit_credit_check
from financialstatements.utils import creating_output

cwd = os.path.dirname(__file__)

# Initializing Configuration
config = configparser.ConfigParser()
config_path = os.path.join(cwd, "../docs/config.ini")
config.read(config_path)


def creating_df(paths):
    dfs = []
    for path in paths:
        df = pd.read_csv(path)
        dfs.append(df)
    return pd.concat(dfs).reset_index(drop=True)


def joining_gl_codes(df, coa_mcc_df):
    df['Amount'] = df['Amount'].abs()
    df = df.pivot_table(index=['Date', 'Name', 'Memo'],
                        columns='Transaction', values='Amount')
    df = df.reset_index()
    df[['Memo', 'MCC', 'Blank']] = df['Memo'].str.split(';', expand=True)
    df['MCC'] = df['MCC'].str[-4:]
    df['MCC'] = df['MCC'].astype('int')
    df = pd.merge(df,
                  coa_mcc_df,
                  how='left',
                  on='MCC')
    return df


def processing_df(df):
    df['Date'] = pd.to_datetime(df['Date'])
    df['Description'] = df['MCC_Description'] + ': ' + df['Name']
    df = df[['Date', 'GL_Code', 'Account', 'Description', 'DEBIT', 'CREDIT']]
    df = df.round(2)
    df = df.sort_values(by='Date').reset_index(drop=True)
    df['Order_Col'] = df.index + 1
    df['Sub_Order_Col'] = np.where(df['DEBIT'].isnull(), 2, 1)
    return df


def creating_credit_entries(df):
    df = df[df['CREDIT'].isnull()].reset_index(drop=True).copy()
    df['GL_Code'] = 200101
    df['Account'] = 'EdwardJones MasterCard'
    df['Sub_Order_Col'] = 2
    df = df.rename(columns={'DEBIT': 'CREDIT', 'CREDIT': 'DEBIT'})
    return df[['Date', 'GL_Code', 'Account', 'Description', 'DEBIT', 'CREDIT', 'Order_Col', 'Sub_Order_Col']]


def creating_debit_entries(df):
    df = df[df['DEBIT'].isnull()].reset_index(drop=True).copy()
    df['GL_Code'] = 200101
    df['Account'] = 'EdwardJones MasterCard'
    df['Sub_Order_Col'] = 1
    df = df.rename(columns={'DEBIT': 'CREDIT', 'CREDIT': 'DEBIT'})
    return df[['Date', 'GL_Code', 'Account', 'Description', 'DEBIT', 'CREDIT', 'Order_Col', 'Sub_Order_Col']]


# Reading data
CREDITCARD_DIRECTORY = os.path.join(cwd, config.get(
    "data_inputs_directory", "CREDITCARD_DIRECTORY"))
paths = creating_input_paths(CREDITCARD_DIRECTORY)
df = creating_df(paths)

# Reading tables
COA_DATA = os.path.join(cwd, config.get('table_files', 'COA_DATA'))
MONTH_DATA = os.path.join(cwd, config.get('table_files', 'MONTH_DATA'))
coa_mcc_df = pd.read_excel(COA_DATA, sheet_name='coa_mcc_link_table')
month_df = pd.read_excel(MONTH_DATA)

# ETL
df = joining_gl_codes(df, coa_mcc_df)

if missing_gl_check(df) != 0:
    print("GL_Codes are missing, need to update the coa and mcc link table")
    missing_mcc(df)
else:
    print("No GL_Codes missing")

df = processing_df(df)
credit_entries_df = creating_credit_entries(df)
debit_entries_df = creating_debit_entries(df)
df = pd.concat([df, credit_entries_df, debit_entries_df]
               ).reset_index(drop=True)
df = df.sort_values(by=['Order_Col', 'Sub_Order_Col']).reset_index(drop=True)

if debit_credit_check(df) == True:
    print("Debits equal credits. Proceed to next phase")
else:
    print("Something went wrong")

type = 'creditcard'
creating_output(df, month_df, type, config, cwd)
