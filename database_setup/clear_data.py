import sqlite3
import os

connection = sqlite3.connect(os.path.join('data', 'personal-finance.db'))
cursor = connection.cursor()
cursor.execute("DELETE FROM general_ledger")
cursor.execute("DELETE FROM account_balance_history")
cursor.execute("DELETE FROM chart_of_accounts")
connection.commit()
cursor.close()