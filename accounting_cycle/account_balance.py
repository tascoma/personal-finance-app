import pandas as pd
import sqlite3


def update_account_balance_history(connection: sqlite3, trial_balance: pd.DataFrame) -> None:
    """Update the account balance history table with the current account balance.

    Args:
        connection (sqlite3): Connection to the database
        trial_balance (pd.DataFrame): Trial balance

    Returns:
        None
    """
    pass

