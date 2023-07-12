import pandas as pd
import os


def create_df(selected_files):
    dfs = []
    for file in selected_files:
        df = pd.read_csv(os.path.join('uploads', file))
        dfs.append(df)
    return pd.concat(dfs).reset_index(drop=True)

def creating_credit_entries(df, gl_code, account_name):
    df = df[df['CREDIT'].isnull()].reset_index(drop=True).copy()
    df['GL_Code'] = gl_code
    df['Account'] = account_name
    df['Sub_Order_Col'] = 2
    df = df.rename(columns={'DEBIT': 'CREDIT', 'CREDIT': 'DEBIT'})
    return df[['Date', 'GL_Code', 'Account', 'Description', 'DEBIT', 'CREDIT', 'Order_Col', 'Sub_Order_Col']]

def creating_debit_entries(df, gl_code, account_name):
    df = df[df['DEBIT'].isnull()].reset_index(drop=True).copy()
    df['GL_Code'] = gl_code
    df['Account'] = account_name
    df['Sub_Order_Col'] = 1
    df = df.rename(columns={'DEBIT': 'CREDIT', 'CREDIT': 'DEBIT'})
    return df[['Date', 'GL_Code', 'Account', 'Description', 'DEBIT', 'CREDIT', 'Order_Col', 'Sub_Order_Col']]

def move_files_to_processed(selected_files):
    for file in selected_files:
        source_path = os.path.join("uploads", file)
        destination_path = os.path.join("processed", file)
        os.rename(source_path, destination_path)    

def missing_gl_check(df):
    null_count = df['GL_Code'].isnull().sum()
    return null_count


def missing_mcc(df):
    df = df[df['GL_Code'].isnull()]
    return print(df)


def debit_credit_check(df):
    debit_total = df['DEBIT'].sum()
    credit_total = df['CREDIT'].sum()
    return debit_total == credit_total


def creating_journal_entry_outputs(df, type, config, cwd):
    df['Month_Num'] = df['Date'].dt.month
    df['Transaction_ID'] = type + '-' + \
        df['Month_Num'].astype("str") + '-' + (df.index + 1).astype("str")
    df['Month'] = df['Date'].dt.strftime('%b').str.lower()
    months = df['Month'].unique()
    file_path = os.path.join(cwd, config.get(
        "data_outputs_directory", "JOURNAL_ENTRIES"))
    month_num = 1
    for month in months:
        file_df = df[df['Month'] == month]
        file_df = file_df[['Transaction_ID', 'Date', 'GL_Code',
                           'Account', 'Description', 'DEBIT', 'CREDIT']]
        file_name = f'{month_num}_{type}_{month}_entries.csv'
        file_df.to_csv(os.path.join(file_path, file_name), index=False)
        month_num += 1
