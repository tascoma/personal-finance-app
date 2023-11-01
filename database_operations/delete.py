import pandas as pd
import sqlite3


def delete_row(connection: sqlite3.Connection, table_name: str, transaction_id: str) -> pd.DataFrame:
    """
    Deletes a row from a table in the database.

    Args:
        connection (sqlite3.Connection): Connection object to the database.
        table_name (str): Name of the table to be processed.
        transaction_id (str): Transaction ID of the row to be deleted.
    
    Returns:
        pd.DataFrame: A pandas DataFrame containing the deleted row.
    """
    # Row to be deleted
    df = pd.read_sql_query(f"SELECT * FROM {table_name} WHERE transaction_id = '{transaction_id}'", connection)
    connection.execute(f"DELETE FROM {table_name} WHERE transaction_id = '{transaction_id}'")
    connection.commit()
    return df