import pandas as pd


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
