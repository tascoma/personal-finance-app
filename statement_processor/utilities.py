import pandas as pd
import sqlite3


def posting_to_database(df: pd.DataFrame, connection: sqlite3.Connection, table_name: str, if_exists = 'append') -> None:
    """
    Post data to database.
    
    Args:
        df (pd.DataFrame): DataFrame
        connection (sqlite3.Connection): Connection to the database
        table_name (str): Table name
        if_exists (str): What to do if the table already exists. Default is 'append'.
    """
    df.to_sql(table_name, connection, if_exists=if_exists, index=False)
    connection.commit()