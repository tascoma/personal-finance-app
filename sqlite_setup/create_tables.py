import sqlite3

# Connect to the database
connection = sqlite3.connect("personal-finance.db")
cursor = connection.cursor()

# Create the chart_of_accounts table
cursor.execute('''CREATE TABLE IF NOT EXISTS chart_of_accounts (
    gl_code INTEGER PRIMARY KEY,
    account TEXT,
    category TEXT,
    account_type TEXT,
    account_classification TEXT,
    nature TEXT
)''')

# Create the mcc_list table
cursor.execute('''CREATE TABLE IF NOT EXISTS mcc_list (
    mcc INTEGER PRIMARY KEY,
    description TEXT,
    gl_code INTEGER,
    FOREIGN KEY (gl_code) REFERENCES chart_of_accounts(gl_code)
)''')

# Create the paystub_list table
cursor.execute('''CREATE TABLE IF NOT EXISTS paystub_list (
    item_id INTEGER PRIMARY KEY,
    item TEXT,
    gl_code INTEGER,
    FOREIGN KEY (gl_code) REFERENCES chart_of_accounts(gl_code)
)''')

# Create general_ledger table
cursor.execute('''CREATE TABLE IF NOT EXISTS general_ledger (
    transaction_id TEXT PRIMARY KEY,
    transaction_date DATE,
    gl_code INTEGER,
    account TEXT,
    description TEXT,
    amount DECIMAL,
    FOREIGN KEY (gl_code) REFERENCES chart_of_accounts(gl_code)
)''')

# Commit the changes and close the connection
connection.commit()
connection.close()