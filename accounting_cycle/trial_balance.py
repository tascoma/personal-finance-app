import pandas as pd
import numpy as np
import sqlite3
import os


def check_debits_credits_equal(df: pd.DataFrame) -> bool:
    """
    Checks if the DEBITS and CREDITS are equal for each account in the trial balance.

    Args:
        df (pd.DataFrame): The trial balance DataFrame.
    
    Returns:
        bool: True if DEBITS and CREDITS are equal, False otherwise.
    """
    debit_total = round(df['DEBIT'].sum(), 2)
    credit_total = round(df['CREDIT'].sum(), 2)
    if debit_total != credit_total:
        print(f'DEBITS and CREDITS are not equal. DEBITS: {debit_total}, CREDITS: {credit_total}')
        return False
    else:
        print(f'DEBITS and CREDITS are equal. DEBITS: {debit_total}, CREDITS: {credit_total}')
    return True


def calculate_ending_balance(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates the ending balance for each account in the trial balance.

    Args:
        df (pd.DataFrame): The trial balance DataFrame.
    
    Returns:
        pd.DataFrame: The trial balance DataFrame with the ending balance calculated.
    """
    account_types = df['account_type'].unique()
    for account_type in account_types:
        if account_type in ['Asset', 'Deduction', 'Expense']:
            df.loc[df['account_type'] == account_type, 'ending_balance'] = df['account_balance'] + df['DEBIT'] - df['CREDIT']
        elif account_type in ['Liability', 'Equity', 'Revenue']:
            df.loc[df['account_type'] == account_type, 'ending_balance'] = df['account_balance'] + df['CREDIT'] - df['DEBIT']
        else:
            continue
    return df


def create_unadjusted_trial_balance_df(connection: sqlite3.Connection, month_name: str) -> pd.DataFrame:
    """
    Creates an unadjusted trial balance DataFrame.

    Args:
        connection (sqlite3.Connection): Connection to the database.
        month_name (str): Month name.
    
    Returns:
        pd.DataFrame: The unadjusted trial balance DataFrame.
    """
    chart_of_accounts_df = pd.read_sql_query("SELECT * FROM chart_of_accounts", connection)
    general_ledger_df = pd.read_sql_query("SELECT * FROM general_ledger", connection)
    general_ledger_df['month_name'] = pd.to_datetime(general_ledger_df['transaction_date']).dt.month_name()
    general_ledger_df = general_ledger_df[general_ledger_df['month_name'] == month_name]
    general_ledger_df['abs_amount'] = general_ledger_df['amount'].abs()
    general_ledger_pivot_df = general_ledger_df.pivot_table(index=['month_name', 'account_code', 'account'], columns='type', values='abs_amount', aggfunc='sum', fill_value=0).reset_index()
    trial_balance_df = general_ledger_pivot_df.merge(chart_of_accounts_df, on=['account_code', 'account'], how='left')
    trial_balance_df = trial_balance_df[['account_code', 'account', 'account_type', 'account_balance', 'DEBIT', 'CREDIT']]
    trial_balance_df = calculate_ending_balance(trial_balance_df)
    return trial_balance_df


def create_adjusted_trial_balance_df(connection: sqlite3.Connection) -> pd.DataFrame:
    pass



connection = sqlite3.connect(os.path.join('data', 'personal-finance.db'))
df = create_unadjusted_trial_balance_df(connection, 'January')

print(df)
check_debits_credits_equal(df)