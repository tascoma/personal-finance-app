import pandas as pd
import numpy as np


def create_credit_entry(account_code: int, account: str, account_type: str, income_summary_amount: int) -> pd.DataFrame:
    """Create credit entry.

    Args:
        df (pd.DataFrame): DataFrame
        income_summary_amount (int): Income summary amount

    Returns:
        pd.DataFrame: Credit entry
    """
    values = [[account_code, account, f'Closing Entries for {account_type} accounts', 'CREDIT', income_summary_amount]]
    df = pd.DataFrame(values, columns=['account_code', 'account', 'description', 'type', 'amount'])
    return df


def create_debit_entry(account_code: int, account: str, account_type: str, income_summary_amount: int) -> pd.DataFrame:
    """Create debit entry.

    Args:
        df (pd.DataFrame): DataFrame
        income_summary_amount (int): Income summary amount

    Returns:
        pd.DataFrame: Debit entry
    """
    values = [[account_code, account, f'Closing Entries for {account_type} accounts', 'DEBIT', income_summary_amount]]
    df = pd.DataFrame(values, columns=['account_code', 'account', 'description', 'type', 'amount'])
    return df


def create_income_summary_entry(total_list) -> pd.DataFrame:
    """Create income summary and retained earnings entries.

    Args:
        total_list (list): List of totals
    
    Returns:
        pd.DataFrame: Income summary and retained earnings entries
    """
    amount = total_list[0] - total_list[1] - total_list[2]
    values = [[700001, 'Income Summary', 'Closing Entries for Income Summary', 'DEBIT', (amount / -1)],
              [300102, 'Retained Earnings', 'Closing Entries for Retained Earnings', 'CREDIT', amount]]
    df = pd.DataFrame(values, columns=['account_code', 'account', 'description', 'type', 'amount'])
    return df


def create_closing_entries(trial_balance: pd.DataFrame, input_date) -> pd.DataFrame:
    """Create closing entries.

    Args:
        trial_balance (pd.DataFrame): Trial balance

    Returns:
        pd.DataFrame: Closing entries
    """
    account_types = ['Revenue', 'Deduction', 'Expense']
    dfs = []
    totals = []
    trial_balance = trial_balance[(trial_balance['DEBIT'] != 0.00) | (trial_balance['CREDIT'] != 0.00)].copy()
    for account_type in account_types:
        total_account = trial_balance[trial_balance['account_type'] == account_type]['ending_balance'].sum()
        totals.append(total_account)
        df = trial_balance[trial_balance['account_type'] == account_type].reset_index(drop=True)
        df = df[['account_code', 'account', 'ending_balance']]
        df['description'] = f'Closing Entries for {account_type} accounts'
        if account_type == 'Revenue':
            df['type'] = 'DEBIT'
        else:
            df['type'] = 'CREDIT'
        df = df.rename(columns={'ending_balance': 'amount'})
        df['amount'] = df['amount'] / -1
        df = df[['account_code', 'account', 'description', 'type', 'amount']]
        if account_type == 'Revenue':
            income_summary_entry_df = create_credit_entry(700001, 'Income Summary', account_type, total_account)
            dfs.append(df)
            dfs.append(income_summary_entry_df)
        else:
            income_summary_entry_df = create_debit_entry(700001, 'Income Summary', account_type, total_account)
            dfs.append(income_summary_entry_df)
            dfs.append(df)

    income_summary_entry_df = create_income_summary_entry(totals)
    dfs.append(income_summary_entry_df)
    closing_entries_df = pd.concat(dfs).reset_index(drop=True)
    closing_entries_df['transaction_date'] = input_date
    closing_entries_df['transaction_id'] = 'ce' + '-' + closing_entries_df['transaction_date'].astype(str) + '-' + (closing_entries_df.index + 1).astype(str)
    closing_entries_df = closing_entries_df[['transaction_id', 'transaction_date', 'account_code', 'account', 'description', 'type', 'amount']]

    return closing_entries_df