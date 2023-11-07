import pandas as pd
import sqlite3


def create_account_balance_history_table(unadjusted_trial_balance: pd.DataFrame, adjusted_trial_balance: pd.DataFrame) -> pd.DataFrame:
    """Update the account balance history table with the current account balance.

    Args:
        connection (sqlite3): Connection to the database
        unadjusted_trial_balance (pd.DataFrame): Unadjusted trial balance
        adjusted_trial_balance (pd.DataFrame): Adjusted trial balance

    Returns:
        pd.DataFrame: Account balance history
    """
    adjusted_trial_balance_filtered = adjusted_trial_balance[adjusted_trial_balance['account_type'].isin(['Asset', 'Liability', 'Equity'])].copy()
    unadjusted_trial_balance_filtered = unadjusted_trial_balance[unadjusted_trial_balance['account_type'].isin(['Revenue', 'Deduction', 'Expense'])].copy()
    account_balance_history_df = pd.concat([adjusted_trial_balance_filtered, unadjusted_trial_balance_filtered])
    account_balance_history_df = account_balance_history_df.drop(columns=['account_balance'])
    account_balance_history_df = account_balance_history_df.rename(columns={'trial_balance_date': 'balance_date'})
    account_balance_history_df = account_balance_history_df.rename(columns={'ending_balance': 'account_balance'})
    account_balance_history_df['balance_id'] = account_balance_history_df['balance_date'].astype(str) + '-' + account_balance_history_df['account_code'].astype(str)
    account_balance_history_df = account_balance_history_df[['balance_id', 'balance_date', 'account_code', 'account', 'account_balance']].reset_index(drop=True)
    return account_balance_history_df
    

def update_chart_of_accounts_table(connection: sqlite3, adjusted_trial_balance: pd.DataFrame) -> pd.DataFrame:
    """Update the chart of accounts table with the current account balance.

    Args:
        connection (sqlite3): Connection to the database
        adjusted_trial_balance (pd.DataFrame): Adjusted trial balance

    Returns:
        pd.DataFrame: Chart of accounts
    """
    chart_of_accounts_df = pd.read_sql_query("SELECT * FROM chart_of_accounts", connection)
    chart_of_accounts_df = pd.merge(chart_of_accounts_df, adjusted_trial_balance[['account_code', 'ending_balance', 'trial_balance_date']], on='account_code', how='left')
    chart_of_accounts_df = chart_of_accounts_df.drop(columns=['account_balance'])
    chart_of_accounts_df = chart_of_accounts_df.drop(columns=['balance_date'])
    chart_of_accounts_df = chart_of_accounts_df.rename(columns={'ending_balance': 'account_balance'})
    chart_of_accounts_df = chart_of_accounts_df.rename(columns={'trial_balance_date': 'balance_date'})
    return chart_of_accounts_df