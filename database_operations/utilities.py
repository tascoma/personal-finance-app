import pandas as pd
import sqlite3


def remove_duplicates(connection: sqlite3.Connection, table_name: str) -> (int, int):
    """
    Removes duplicate rows from a table in the database.

    Args:
        connection (sqlite3.Connection): Connection object to the database.
        table_name (str): Name of the table to be processed.

    Returns:
        (int, int): A tuple containing the number of duplicate rows before and after the removal.
    """
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", connection)
    num_of_dups = df.duplicated().sum()
    df = df.drop_duplicates()
    num_of_dups_drop = df.duplicated().sum()
    df.to_sql(table_name, connection, if_exists='replace', index=False)
    return num_of_dups, num_of_dups_drop


def identify_missing_data(connection: sqlite3.Connection, table_name: str) -> pd.DataFrame:
    """
    Identifies missing data in a table in the database.

    Args:
        connection (sqlite3.Connection): Connection object to the database.
        table_name (str): Name of the table to be processed.

    Returns:
        pd.DataFrame: A pandas DataFrame containing the missing data.
    """
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", connection)
    df = df[df.isnull().any(axis=1)]
    return df