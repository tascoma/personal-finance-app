import pandas as pd
import sqlite3
from .bank_processing import process_bank_statement
from .creditcard_processing import process_creditcard_statement
from .paystub_processing import process_paystub


def parsing_statements(files: list, connection: sqlite3.Connection) -> pd.DataFrame:
    """
    This function parses the input list of files and returns a DataFrame containing transaction data.
    
    Args:
        files: list - list of files to parse
    
    Returns:
        DataFrame - output DataFrame containing transaction data
    """
    df_list = []
    for file in files:
        if ".csv" in file and "creditcard" in file:
            df = pd.read_csv(file)
            df = process_creditcard_statement(df, connection)
            df_list.append(df)
        elif ".csv" in file and "bank" in file:
            df = pd.read_csv(file)
            df = process_bank_statement(df)
            df_list.append(df)
        elif ".pdf" in file:
            df = process_paystub(file, connection)
            df_list.append(df)
        else:
            continue
    
    df = pd.concat(df_list, ignore_index=True).reset_index(drop=True)
    df = df.sort_values(by=['transaction_date', 'transaction_id']).reset_index(drop=True)
    return df