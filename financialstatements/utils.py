import pandas as pd
import os


def creating_input_paths(directory):
    files = os.listdir(directory)
    paths = []
    for file in files:
        path = os.path.join(directory, file)
        paths.append(path)
    return paths


def creating_df(paths):
    dfs = []
    for path in paths:
        df = pd.read_csv(path)
        dfs.append(df)
    return pd.concat(dfs).reset_index(drop=True)


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


def creating_output(df, month_df, type, config, cwd):
    df['Month_Num'] = df['Date'].dt.month
    df['Transaction_ID'] = type + '-' + \
        df['Month_Num'].astype("str") + '-' + (df.index + 1).astype("str")
    df = pd.merge(df,
                  month_df,
                  on='Month_Num',
                  how='left')
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
