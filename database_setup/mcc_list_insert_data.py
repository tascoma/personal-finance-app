import pandas as pd
import sqlite3
import os

# Connect to CSVs
mcc_list_df = pd.read_csv(os.path.join('database_setup', 'mcc_list.csv'))

# Connect to database
connection = sqlite3.connect(os.path.join("data","personal-finance.db"))

# Insert data to database
mcc_list_df.to_sql("mcc_list", connection, if_exists="replace", index=False)

# Commit the changes and close the connection
connection.commit()
connection.close()