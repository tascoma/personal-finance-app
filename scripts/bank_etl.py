import pandas as pd
import numpy as np
import os
import add_package
import financialstatements


def processing_df(df):
    df['Date'] = pd.to_datetime(df['Date'])
    df['Amount'] = df['Amount'].str.replace('$', '', regex=False)
    df['Amount'] = df['Amount'].str.replace(',', '')
    df['Amount'] = df['Amount'].astype('float')
    df['DEBIT'] = np.where(df['Amount'] < 0, df['Amount'], np.nan)
    df['DEBIT'] = df['DEBIT'].abs()
    df['CREDIT'] = np.where(df['Amount'] > 0, df['Amount'], np.nan)
    df['GL_Code'] = np.nan
    df['Account'] = np.nan
    df = df.sort_values(by='Date').reset_index(drop=True)
    df['Order_Col'] = df.index + 1
    df['Sub_Order_Col'] = np.where(df['DEBIT'].isnull(), 2, 1)
    return df[['Date', 'GL_Code', 'Account', 'Description', 'DEBIT', 'CREDIT', 'Order_Col', 'Sub_Order_Col']]


def creating_credit_entries(df):
    df = df[df['CREDIT'].isnull()].reset_index(drop=True).copy()
    df['GL_Code'] = 100101
    df['Account'] = 'Free Checking Bank OZK'
    df['Sub_Order_Col'] = 2
    df = df.rename(columns={'DEBIT': 'CREDIT', 'CREDIT': 'DEBIT'})
    return df[['Date', 'GL_Code', 'Account', 'Description', 'DEBIT', 'CREDIT', 'Order_Col', 'Sub_Order_Col']]


def creating_debit_entries(df):
    df = df[df['DEBIT'].isnull()].reset_index(drop=True).copy()
    df['GL_Code'] = 100101
    df['Account'] = 'Free Checking Bank OZK'
    df['Sub_Order_Col'] = 1
    df = df.rename(columns={'DEBIT': 'CREDIT', 'CREDIT': 'DEBIT'})
    return df[['Date', 'GL_Code', 'Account', 'Description', 'DEBIT', 'CREDIT', 'Order_Col', 'Sub_Order_Col']]


def bank_etl(cwd, config):
    # Reading data
    BANK_DIRECTORY = os.path.join(cwd, config.get(
        "data_inputs_directory", "BANK_DIRECTORY"))
    paths = financialstatements.creating_input_paths(BANK_DIRECTORY)
    df = financialstatements.creating_df(paths)

    # Reading tables
    MONTH_DATA = os.path.join(cwd, config.get('table_files', 'MONTH_DATA'))
    month_df = pd.read_excel(MONTH_DATA)

    # ETL
    df = processing_df(df)
    credit_entries_df = creating_credit_entries(df)
    debit_entries_df = creating_debit_entries(df)
    df = pd.concat([df, credit_entries_df, debit_entries_df])
    df = df.sort_values(by=['Order_Col', 'Sub_Order_Col']
                        ).reset_index(drop=True)

    if financialstatements.debit_credit_check(df) == True:
        print("Debits equal credits.")
        type = 'bank'
        financialstatements.creating_output(df, month_df, type, config, cwd)
    else:
        print("Something went wrong")
