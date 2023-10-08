import pandas as pd
from pandas import DataFrame


def creating_transaction_id(df: DataFrame, statement) -> DataFrame:
    df['transaction_date'] = pd.to_datetime(df['transaction_date'])
    df['month_num'] = df['transaction_date'].dt.month
    df['day_num'] = df['transaction_date'].dt.day
    df['transaction_id'] = statement + '-' + df['month_num'].astype("str") + '-' + df['day_num'].astype('str') + '-' + (df.index + 1).astype("str")
    return df[['transaction_id', 'transaction_date', 'gl_code', 'account', 'description', 'amount']]


def missing_gl_code(df: DataFrame) -> DataFrame:
    df = df[df['gl_code'].isna()]
    return df