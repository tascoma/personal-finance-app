import pandas as pd
import sqlite3
from .bank_processing import process_bank_statement
from .creditcard_processing import process_creditcard_statement
from .paystub_processing import process_paystub


def process_statement(filename: str, connection: sqlite3.Connection) -> pd.DataFrame:
    """
    This function parses the input list of files and returns a DataFrame containing transaction data.
    
    Args:
        files: list - list of files to parse
    
    Returns:
        DataFrame - output DataFrame containing transaction data
    """
    if ".csv" in filename and "creditcard" in filename:
        df = pd.read_csv(filename)
        df = process_creditcard_statement(df, connection)
    elif ".csv" in filename and "bank" in filename:
        df = pd.read_csv(filename)
        df = process_bank_statement(df)
    elif ".pdf" in filename:
        df = process_paystub(filename, connection)
    else:
        pass

    return df