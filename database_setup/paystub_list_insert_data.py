import pandas as pd
import sqlite3
import os

# Connect to CSVs
paystub_list_df = pd.read_csv(os.path.join('database_setup', 'paystub_list.csv'))

# Connect to database
connection = sqlite3.connect(os.path.join("instance","personal-finance-app.db"))

# Insert data to database
paystub_list_df.to_sql("paystub_list", connection, if_exists="replace", index=False)

# Commit the changes and close the connection
connection.commit()
connection.close()