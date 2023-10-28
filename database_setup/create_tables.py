import sqlite3
import os

# Connect to the database
connection = sqlite3.connect(os.path.join("data","personal-finance.db"))
cursor = connection.cursor()

# Create the chart_of_accounts table
cursor.execute('''CREATE TABLE IF NOT EXISTS chart_of_accounts (
    account_code INTEGER PRIMARY KEY,
    account TEXT,
    account_type TEXT,
    account_subtype TEXT
)''')

# Create the mcc_list table
cursor.execute('''CREATE TABLE IF NOT EXISTS mcc_list (
    mcc INTEGER PRIMARY KEY,
    description TEXT,
    account_code INTEGER,
    FOREIGN KEY (account_code) REFERENCES chart_of_accounts(account_code)
)''')

# Create the paystub_list table
cursor.execute('''CREATE TABLE IF NOT EXISTS paystub_list (
    item_id INTEGER PRIMARY KEY,
    item TEXT,
    account_code INTEGER,
    FOREIGN KEY (account_code) REFERENCES chart_of_accounts(account_code)
)''')

# Create general_ledger table
cursor.execute('''CREATE TABLE IF NOT EXISTS general_ledger (
    transaction_id TEXT PRIMARY KEY,
    transaction_date DATE,
    account_code INTEGER,
    account TEXT,
    description TEXT,
    type TEXT,
    amount DECIMAL,
    FOREIGN KEY (account_code) REFERENCES chart_of_accounts(account_code)
)''')

# Commit the changes and close the connection
connection.commit()
connection.close()