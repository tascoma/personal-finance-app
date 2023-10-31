import pandas as pd
import sqlite3


def read_chart_of_accounts(connection: sqlite3.Connection, account_code_start: int = None, account_code_end: int = None, account_type: str = None, account_subtype: str = None) -> pd.DataFrame:
    """
    Reads data from the chart_of_accounts table in the database.

    Args:
        connection (sqlite3.Connection): Connection object to the database.
        account_code_start (str, optional): Starting account code of the accounts to be retrieved. Defaults to None.
        account_code_end (str, optional): Ending account code of the accounts to be retrieved. Defaults to None.
        account_type (str, optional): Type of the accounts to be retrieved. Defaults to None.
        account_subtype (str, optional): Subtype of the accounts to be retrieved. Defaults to None.

    Returns:
        pd.DataFrame: A pandas DataFrame containing the retrieved data.
    """
    sql = 'SELECT * FROM chart_of_accounts WHERE 1=1'
    conditions = []
    params = []

    if account_code_start is not None:
        conditions.append(f"account_code >= ?")
        params.append(account_code_start)
    if account_code_end is not None:
        conditions.append(f"account_code <= ?")
        params.append(account_code_end)
    if account_type is not None:
        conditions.append(f"account_type = ?")
        params.append(account_type)
    if account_subtype is not None:
        conditions.append(f"account_subtype = ?")
        params.append(account_subtype)

    if conditions:
        sql += ' AND ' + ' AND '.join(conditions)

    df = pd.read_sql_query(sql, connection, params=params)
    return df


def read_general_ledger(connection: sqlite3.Connection, transaction_id: str, beg_date: str = None, end_date: str = None, account_code_start: int = None, account_code_end: int = None, type: str = None) -> pd.DataFrame:
    """
    Reads data from the general_ledger table in the database.

    Args:
        connection (sqlite3.Connection): Connection object to the database.
        beg_date (str, optional): Beginning date of the transactions to be retrieved (format: 'YYYY-MM-DD'). Defaults to None.
        end_date (str, optional): End date of the transactions to be retrieved (format: 'YYYY-MM-DD'). Defaults to None.
        account_code_start (str, optional): Starting account code of the transactions to be retrieved. Defaults to None.
        account_code_end (str, optional): Ending account code of the transactions to be retrieved. Defaults to None.
        type (str, optional): Type of the transactions to be retrieved. Defaults to None.

    Returns:
        pd.DataFrame: A pandas DataFrame containing the retrieved data.
    """
    sql = 'SELECT * FROM general_ledger WHERE 1=1'
    conditions = []
    params = []

    if transaction_id is not None:
        conditions.append(f"transaction_id = ?")
        params.append(transaction_id)
    if beg_date is not None:
        conditions.append(f"transaction_date >= ?")
        params.append(beg_date)
    if end_date is not None:
        conditions.append(f"transaction_date <= ?")
        params.append(end_date)
    if account_code_start is not None:
        conditions.append(f"account_code >= ?")
        params.append(account_code_start)
    if account_code_end is not None:
        conditions.append(f"account_code <= ?")
        params.append(account_code_end)
    if type is not None:
        conditions.append(f"type = ?")
        params.append(type)

    if conditions:
        sql += ' AND ' + ' AND '.join(conditions)

    df = pd.read_sql_query(sql, connection, params=params)
    return df


def read_mcc_list(connection: sqlite3.Connection) -> pd.DataFrame:
    """
    Reads data from the mcc_list table in the database.

    Args:
        connection (sqlite3.Connection): Connection object to the database.

    Returns:
        pd.DataFrame: A pandas DataFrame containing the retrieved data.
    """
    df = pd.read_sql_query("SELECT * FROM mcc_list", connection)
    return df


def read_paystub_list(connection: sqlite3.Connection) -> pd.DataFrame:
    """
    Reads data from the paystub_list table in the database.

    Args:
        connection (sqlite3.Connection): Connection object to the database.

    Returns:
        pd.DataFrame: A pandas DataFrame containing the retrieved data.
    """
    df = pd.read_sql_query("SELECT * FROM paystub_list", connection)
    return df