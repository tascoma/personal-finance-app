import pandas as pd
from pandas import DataFrame


def creating_transaction_id(df: DataFrame, statement) -> DataFrame:
    """
    This function creates a unique transaction ID for each transaction in the input DataFrame.
    
    Args:
    - df: DataFrame - input DataFrame containing transaction data
    - statement: str - statement identifier
    
    Returns:
    - DataFrame - output DataFrame containing transaction ID, transaction date, GL code, account, description, and amount
    """
    df['transaction_date'] = pd.to_datetime(df['transaction_date'])
    df['month_num'] = df['transaction_date'].dt.month
    df['day_num'] = df['transaction_date'].dt.day
    df['transaction_id'] = statement + '-' + df['month_num'].astype("str") + '-' + df['day_num'].astype('str') + '-' + (df.index + 1).astype("str")
    return df[['transaction_id', 'transaction_date', 'gl_code', 'account', 'description', 'amount']]


def missing_gl_code(df: DataFrame) -> DataFrame:
    """
    This function filters the input DataFrame to only include transactions with missing GL codes.
    
    Args:
    - df: DataFrame - input DataFrame containing transaction data
    
    Returns:
    - DataFrame - output DataFrame containing transactions with missing GL codes
    """
    df = df[df['gl_code'].isna()]
    return df