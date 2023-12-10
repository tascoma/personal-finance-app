import sqlite3
import os

connection = sqlite3.connect(os.path.join('instance', 'personal-finance-app.db'))
cursor = connection.cursor()
cursor.execute("DELETE FROM general_ledger")
cursor.execute("DELETE FROM account_balance_history")
connection.commit()
cursor.close()