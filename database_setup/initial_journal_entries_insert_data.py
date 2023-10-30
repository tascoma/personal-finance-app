import pandas as pd
import sqlite3
import os

# Connect to CSVs
initial_journal_entries_df = pd.read_csv(os.path.join('database_setup', 'initial_journal_entries.csv'))
initial_journal_entries_df['transaction_date'] = pd.to_datetime(initial_journal_entries_df['transaction_date'])
initial_journal_entries_df['transaction_date'] = initial_journal_entries_df['transaction_date'].dt.strftime('%Y-%m-%d')

# Connect to database
connection = sqlite3.connect(os.path.join("data","personal-finance.db"))

# Insert data to database
initial_journal_entries_df.to_sql("general_ledger", connection, if_exists="replace", index=False)

# Commit the changes and close the connection
connection.commit()
connection.close()