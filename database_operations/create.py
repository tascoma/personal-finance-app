import pandas as pd
import sqlite3


def column_header_list(connection: sqlite3.Connection, table_name: str) -> list:
    """
    Returns a list of column headers in a table in the database.

    Args:
        connection (sqlite3.Connection): Connection object to the database.
        table_name (str): Name of the table to be processed.

    Returns:
        list: A list of column headers.
    """
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", connection)
    return list(df.columns)


def create_values(column_list: list) -> pd.DataFrame:
    """
    Creates a pandas DataFrame containing the values of a row to be created.

    Args:
        column_list (list): A list of column headers.
    
    Returns:
        pd.DataFrame: A pandas DataFrame containing the values of a row to be created.
    """
    values = []
    for column in column_list:
        value = input(f"Enter {column}: ")
        values.append(value)
    df = pd.DataFrame([values], columns=column_list)
    return df


def create_row(connection: sqlite3.Connection, table_name: str, number_of_rows: int) -> None:
    """
    Creates a row in a table in the database.

    Args:
        connection (sqlite3.Connection): Connection object to the database.
        table_name (str): Name of the table to be processed.
        number_of_rows (int): Number of rows to be created.
    """
    dfs = []
    column_list = column_header_list(connection, table_name)
    for _ in range(number_of_rows):
        df = create_values(column_list)
        dfs.append(df)
    df = pd.concat(dfs)
    df.to_sql(table_name, connection, if_exists='append', index=False)