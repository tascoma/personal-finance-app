import pandas as pd
import sqlite3
import os

# Connect to CSVs
chart_of_accounts_df = pd.read_csv(os.path.join('sqlite_setup', 'chart_of_accounts.csv'))
mcc_list_df = pd.read_csv(os.path.join('sqlite_setup', 'mcc_list.csv'))

# Connect to database
connection = sqlite3.connect('personal-finance.db')

# Insert data to database
chart_of_accounts_df.to_sql("chart_of_accounts", connection, if_exists="replace", index=False)
mcc_list_df.to_sql("mcc_list", connection, if_exists="replace", index=False)

# Commit the changes and close the connection
connection.commit()
connection.close()