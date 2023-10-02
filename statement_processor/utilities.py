import pandas as pd
import os


def creating_transaction_id(df, statement):
    df['month_num'] = df['transaction_date'].dt.month
    df['transaction_id'] = statement + '-' + df['month_num'].astype("str") + '-' + (df.index + 1).astype("str")
    return df[['transaction_id', 'transaction_date', 'gl_code', 'account', 'description', 'amount', 'order_col', 'sub_order_col']]
