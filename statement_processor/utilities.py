import pandas as pd
import sqlite3


def posting_to_gl(df: pd.DataFrame, connection: sqlite3.Connection, table_name: str) -> None:
    """
    This function posts the input DataFrame to the input SQLite table.
    
    Args:
        df: DataFrame - input DataFrame containing transaction data
        connection: Connection - SQLite database connection
        table_name: str - SQLite table name
    """
    df.to_sql(table_name, connection, if_exists='append', index=False)
    connection.commit()