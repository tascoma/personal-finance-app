import os
import configparser
import pandas as pd

cwd = os.path.dirname(__file__)

# Initializing Configuration
config = configparser.ConfigParser()
config_path = os.path.join(cwd, "../docs/config.ini")
config.read(config_path)

# Reading creditcard data
CREDITCARD_DIRECTORY = os.path.join(cwd, config.get(
    "data_inputs_directory", "CREDITCARD_DIRECTORY"))
creditcard_files = os.listdir(CREDITCARD_DIRECTORY)

creditcard_paths = []
for file in creditcard_files:
    path = os.path.join(CREDITCARD_DIRECTORY, file)
    creditcard_paths.append(path)

dfs = []
for path in creditcard_paths:
    df = pd.read_csv(path)
    dfs.append(df)

creditcard_df = pd.concat(dfs).reset_index(drop=True)

# Reading table data
COA_DATA = config.get('table_files', 'COA_DATA')
MONTH_DATA = config.get('table_files', 'MONTH_DATA')
coa_mcc_df = pd.read_excel(os.path.join(
    cwd, COA_DATA), sheet_name='coa_mcc_link_table')
month_df = pd.read_excel(os.path.join(
    cwd, MONTH_DATA))

# ETL
creditcard_df['Date'] = pd.to_datetime(creditcard_df['Date'])
creditcard_df['Amount'] = creditcard_df['Amount'].abs()
creditcard_df = creditcard_df.pivot_table(
    index=['Date', 'Name', 'Memo'], columns='Transaction', values='Amount')
creditcard_df = creditcard_df.reset_index()
creditcard_df[['Memo', 'MCC', 'Blank']
              ] = creditcard_df['Memo'].str.split(';', expand=True)
creditcard_df['MCC'] = creditcard_df['MCC'].str[-4:]
creditcard_df['MCC'] = creditcard_df['MCC'].astype('int')

creditcard_df = pd.merge(creditcard_df,
                         coa_mcc_df,
                         how='left',
                         on='MCC')

creditcard_df['Description'] = creditcard_df['MCC_Description'] + \
    ': ' + creditcard_df['Name']
creditcard_df = creditcard_df[['Date', 'GL_Code',
                               'Account', 'Description', 'DEBIT', 'CREDIT']]
creditcard_df = creditcard_df.round(2)

# Creating credit entries
credit_entries = creditcard_df[creditcard_df['CREDIT'].isnull()].reset_index(
    drop=True).copy()
credit_entries['GL_Code'] = 200101
credit_entries['Account'] = 'EdwardJones MasterCard'
credit_entries = credit_entries.rename(
    columns={'DEBIT': 'CREDIT', 'CREDIT': 'DEBIT'})
credit_entries = credit_entries[[
    'Date', 'GL_Code', 'Account', 'Description', 'DEBIT', 'CREDIT']]

# Creating debit entries
debit_entries = creditcard_df[creditcard_df['DEBIT'].isnull()].reset_index(
    drop=True).copy()
debit_entries['GL_Code'] = 200101
debit_entries['Account'] = 'EdwardJones MasterCard'
debit_entries = debit_entries.rename(
    columns={'DEBIT': 'CREDIT', 'CREDIT': 'DEBIT'})
debit_entries = debit_entries[['Date', 'GL_Code',
                               'Account', 'Description', 'DEBIT', 'CREDIT']]

# Appending debit and credit entries
creditcard_df = pd.concat(
    [creditcard_df, credit_entries, debit_entries]).reset_index(drop=True)

creditcard_df['Month_Num'] = creditcard_df['Date'].dt.month
creditcard_df = creditcard_df.sort_values(by='Date').reset_index(drop=True)
creditcard_df['Transaction_ID'] = 'cc-' + creditcard_df['Month_Num'].astype(
    "str") + '-' + (creditcard_df.index + 1).astype("str")

creditcard_df = pd.merge(creditcard_df,
                         month_df,
                         on='Month_Num',
                         how='left')

months = creditcard_df['Month'].unique()
file_path = os.path.join(cwd, config.get(
    "data_outputs_directory", "JOURNAL_ENTRIES"))
month_num = 1
for month in months:
    df = creditcard_df[creditcard_df['Month'] == month]
    df = df[['Transaction_ID', 'Date', 'GL_Code',
             'Account', 'Description', 'DEBIT', 'CREDIT']]
    file_name = f'{month_num}_creditcard_{month}_entries.csv'
    df.to_csv(os.path.join(file_path, file_name), index=False)
    month_num += 1
