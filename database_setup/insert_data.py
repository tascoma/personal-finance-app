import pandas as pd
import sqlite3
import os

# Connect to CSVs
chart_of_accounts_df = pd.read_csv(os.path.join('database_setup', 'chart_of_accounts.csv'))
mcc_list_df = pd.read_csv(os.path.join('database_setup', 'mcc_list.csv'))
paystub_list_df = pd.read_csv(os.path.join('database_setup', 'paystub_list.csv'))
initial_journal_entries_df = pd.read_csv(os.path.join('database_setup', 'initial_journal_entries.csv'))

initial_journal_entries_df['transaction_date'] = pd.to_datetime(initial_journal_entries_df['transaction_date'])
initial_journal_entries_df['transaction_date'] = initial_journal_entries_df['transaction_date'].dt.strftime('%Y-%m-%d')

# Connect to database
connection = sqlite3.connect(os.path.join("data","personal-finance.db"))

# Insert data to database
chart_of_accounts_df.to_sql("chart_of_accounts", connection, if_exists="replace", index=False)
mcc_list_df.to_sql("mcc_list", connection, if_exists="replace", index=False)
paystub_list_df.to_sql("paystub_list", connection, if_exists="replace", index=False)
initial_journal_entries_df.to_sql("general_ledger", connection, if_exists="replace", index=False)

# Commit the changes and close the connection
connection.commit()
connection.close()