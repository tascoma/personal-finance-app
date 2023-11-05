import pandas as pd
import sqlite3
import os

# Connect to CSVs
initial_journal_entries_df = pd.read_csv(os.path.join('database_setup', 'balance_history.csv'))

# Connect to database
connection = sqlite3.connect(os.path.join("data","personal-finance.db"))

# Insert data to database
initial_journal_entries_df.to_sql("account_balance_history", connection, if_exists="replace", index=False)

# Commit the changes and close the connection
connection.commit()
connection.close()