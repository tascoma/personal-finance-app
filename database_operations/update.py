import sqlite3


def update_row(connection: sqlite3.Connection, table_name: str, transaction_id: str, column_name: str, new_value) -> None:
    """
    Updates a row in a table in the database.

    Args:
        connection (sqlite3.Connection): Connection object to the database.
        table_name (str): Name of the table to be processed.
        transaction_id (str): Transaction ID of the row to be updated.
        column_name (str): Name of the column to be updated.
        new_value (str): New value of the column to be updated.
    """
    connection.execute(f"UPDATE {table_name} SET {column_name} = '{new_value}' WHERE transaction_id = '{transaction_id}'")
    connection.commit()