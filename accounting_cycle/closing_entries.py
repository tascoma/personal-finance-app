import pandas as pd
import numpy as np
import sqlite3


def create_credit_entry(df: pd.DataFrame, account_code: int, account: str, income_summary_amount: int) -> pd.DataFrame:
    """Create credit entry.

    Args:
        df (pd.DataFrame): DataFrame
        income_summary_amount (int): Income summary amount

    Returns:
        pd.DataFrame: Credit entry
    """
    df['account_code'] = account_code
    df['account'] = account
    df['type'] = 'CREDIT'
    df['amount'] = income_summary_amount
    df['sub_order_col'] = 2
    return df[['account_code', 'account', 'description', 'type', 'amount', 'order_col', 'sub_order_col']]


def create_debit_entry(df: pd.DataFrame, account_code: int, account: str, income_summary_amount: int) -> pd.DataFrame:
    """Create debit entry.

    Args:
        df (pd.DataFrame): DataFrame
        income_summary_amount (int): Income summary amount

    Returns:
        pd.DataFrame: Debit entry
    """
    df['account_code'] = account_code
    df['account'] = account
    df['type'] = 'DEBIT'
    df['amount'] = income_summary_amount
    df['sub_order_col'] = 1
    return df[['account_code', 'account', 'description', 'type', 'amount', 'order_col', 'sub_order_col']]


def create_closing_entries(trial_balance: pd.DataFrame) -> pd.DataFrame:
    """Create closing entries.

    Args:
        trial_balance (pd.DataFrame): Trial balance

    Returns:
        pd.DataFrame: Closing entries
    """
    account_types = ['Revenue', 'Deduction', 'Expense']
    dfs = []
    for account_type in account_types:
        entry = []
        total_account = trial_balance[trial_balance['account_type'] == account_type]['ending_balance'].sum()
        df = trial_balance[trial_balance['account_type'] == account_type]
        df = df[['account_code', 'account', 'ending_balance']]
        df['description'] = f'Closing Entries for {account_type} accounts'
        if account_type == 'Revenue':
            df['type'] = 'DEBIT'
        else:
            df['type'] = 'CREDIT'
        df = df.rename(columns={'ending_balance': 'amount'})
        df = df[['account_code', 'account', 'description', 'type', 'amount']]
        df['order_col'] = df.index + 1
        df['sub_order_col'] = np.where(df['type'] == 'DEBIT', 1, 2)
        if account_type == 'Revenue':
            income_summary_entry_df = create_credit_entry(df, 700001, 'Income Summary', total_account)
        else:
            income_summary_entry_df = create_debit_entry(df, 700001, 'Income Summary', total_account)
        entry.append(df)
        entry.append(income_summary_entry_df)
        entry_df = pd.concat(entry)
        entry_df = entry_df.sort_values(by=['order_col', 'sub_order_col']).reset_index(drop=True)
        entry_df = entry_df[['account_code', 'account', 'description', 'type', 'amount']]
        dfs.append(entry_df)
    closing_entries_df = pd.concat(dfs).reset_index(drop=True)
    

    return closing_entries_df


def update_chart_of_accounts(connection: sqlite3, closing_entries: pd.DataFrame) -> None:
    pass