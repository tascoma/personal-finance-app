import sqlite3


def update_row(connection: sqlite3.Connection, table_name: str, id_column_name: str, id: str, column_name: str, new_value) -> None:
    """
    Updates a row in a table in the database.

    Args:
        connection (sqlite3.Connection): The connection to the database.
        table_name (str): The name of the table to update.
        id_column_name (str): The name of the column that contains the id of the row to update.
        id (str): The id of the row to update.
        column_name (str): The name of the column to update.
        new_value ([type]): The new value for the column.
    """
    connection.execute(f"UPDATE {table_name} SET {column_name} = '{new_value}' WHERE {id_column_name} = '{id}'")
    connection.commit()