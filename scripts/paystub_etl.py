import os
import add_package
import configparser
import pandas as pd
import numpy as np
import tabula
from financialstatements.utils import creating_input_paths
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
        tables = tabula.read_pdf(path, pages='all', area=[
                                 396, 36, 756, 612], guess=False)
        df = pd.concat(tables).reset_index(drop=True)
        df['Date'] = path[-14:-4]
        dfs.append(df)
    return pd.concat(dfs).reset_index(drop=True)


def find_deductions(df):
    df = df[['Unnamed: 4', 'Unnamed: 5', 'Date']]
    df = df.rename(columns={'Unnamed: 4': 'Item', 'Unnamed: 5': 'Amount'})
    df = df[1:]
    df = df.dropna().reset_index(drop=True)
    df = df.query(
        "Item != 'Total' and Item != 'DEDUCTIONS' and Item != 'CURRENT'")
    return df


def find_earnings(df):
    df = df[['Unnamed: 0', 'Unnamed: 3', 'Date']]
    df = df.rename(columns={'Unnamed: 0': 'Item', 'Unnamed: 3': 'Amount'})
    df = df[1:]
    df = df.dropna().reset_index(drop=True)
    df = df.query("Item != 'Total' and Item != 'TAX' and Item != 'EARNINGS'")
    return df


def processing_df(deductions_df, earnings_df, coa_purch_df):
    df = pd.concat([deductions_df, earnings_df]).reset_index(drop=True)
    df = pd.merge(df,
                  coa_purch_df,
                  on='Item',
                  how='left')
    df = df.rename(columns={'Item': 'Description'})
    df = df[['Date', 'GL_Code', 'Account', 'Description',
             'Amount', 'Category', 'Account_Type', 'Order_Col']]
    df['Date'] = pd.to_datetime(df['Date'])
    df['Amount'] = df['Amount'].str.replace('$', '', regex=False)
    df['DEBIT'] = np.where(df['Account_Type'].isin(
        ['Asset', 'Deduction']), df['Amount'], np.nan)
    df['CREDIT'] = np.where(df['Account_Type'] ==
                            'Revenue', df['Amount'], np.nan)
    df['DEBIT'] = df['DEBIT'].str.replace(',', '').astype('float')
    df['CREDIT'] = df['CREDIT'].str.replace(',', '').astype('float')
    return df


def creating_cash_entries(df):
    df_grouped = df.groupby('Date', as_index=False)[['DEBIT', 'CREDIT']].sum()
    df_grouped['DEBIT'] = df_grouped['CREDIT'] - df_grouped['DEBIT']
    df_grouped['CREDIT'] = np.nan
    df_grouped['GL_Code'] = 100101
    df_grouped['Account'] = 'Free Checking Bank OZK'
    df_grouped['Description'] = 'Cash from paystub'
    df_grouped['Amount'] = df_grouped['DEBIT']
    df_grouped['Category'] = 'Cash'
    df_grouped['Account_Type'] = 'Asset'
    df_grouped['Order_Col'] = 1
    df_grouped = df_grouped[['Date', 'GL_Code', 'Account', 'Description',
                             'Amount', 'Category', 'Account_Type', 'Order_Col', 'DEBIT', 'CREDIT']]
    return pd.concat([df, df_grouped]).reset_index(drop=True)


# Reading data
PAYSTUB_DIRECTORY = os.path.join(cwd, config.get(
    "data_inputs_directory", "PAYSTUB_DIRECTORY"))
paths = creating_input_paths(PAYSTUB_DIRECTORY)
df = creating_df(paths)

# Reading tables
COA_DATA = os.path.join(cwd, config.get('table_files', 'COA_DATA'))
MONTH_DATA = os.path.join(cwd, config.get('table_files', 'MONTH_DATA'))
coa_purch_df = pd.read_excel(COA_DATA, sheet_name='coa_paystub_link_table')
month_df = pd.read_excel(MONTH_DATA)

# ETL
deductions_df = find_deductions(df)
earnings_df = find_earnings(df)
df = processing_df(deductions_df, earnings_df, coa_purch_df)
df = creating_cash_entries(df)
df = df.sort_values(by=['Date', 'Order_Col']).reset_index(drop=True)

if debit_credit_check(df) == True:
    print("Debits equal credits.")
    type = 'paystub'
    creating_output(df, month_df, type, config, cwd)
else:
    print("Something went wrong")
