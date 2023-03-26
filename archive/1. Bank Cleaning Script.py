import pandas as pd

df = pd.read_csv('')

# changing 'date' field to date data type
df['Date'] = pd.to_datetime(df['Date'])

# creating month dataframe
months_dic = {}
months = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]
month_num = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
months_dic['Month_Num'] = month_num
months_dic['Month'] = months
months = pd.DataFrame(months_dic)

# creating transaction ID
df['Month_Num'] = pd.DatetimeIndex(df['Date']).month.astype(str)
df['Transaction_ID'] = 'BS' + df['Month_Num'] + (df.index + 1).astype(str)

# joining month dataframe to GL data
df['Month_Num'] = df['Month_Num'].astype(int)
df = pd.merge(df, months, on='Month_Num', how='left')

# changing 'Amount' field to int data type
df['Amount'] = df['Amount'].str.replace('$', '', regex=True)
df['Amount'] = df['Amount'].str.replace(',', '', regex=True)
df['Amount'] = df['Amount'].astype(float)

# creating 'type' field with condition
df.loc[(df['Amount'] >= 0), 'Type'] = 'CREDIT'
df.loc[(df['Amount'] < 0), 'Type'] = 'DEBIT'

# changing amount to absolute value
df['Amount'] = abs(df['Amount'])

# creating fields
df['Account'] = df['Description']
df['GL_Code'] = ''
df['Source'] = 'Bank'

# organizing column headers
df = df[['Transaction_ID', 'Source', 'Month', 'Date',
         'GL_Code', 'Account', 'Type', 'Amount']]

# copying data to create credit entries
credit_entries = df.loc[df['Type'] == 'DEBIT'].copy()
credit_entries['GL_Code'] = 1001
credit_entries['Account'] = 'Free Checking Bank OZK'
credit_entries['Type'] = 'CREDIT'

# copying data to create debit entries
debit_entries = df.loc[df['Type'] == 'CREDIT'].copy()
debit_entries['GL_Code'] = 1001
debit_entries['Account'] = 'Free Checking Bank OZK'
debit_entries['Type'] = 'DEBIT'

# appending data together
df = pd.concat([df, credit_entries, debit_entries])

# sorting values
df = df.sort_values(by=['Date', 'Transaction_ID', 'Type'], ascending=[
                    True, True, False], ignore_index=True)

# checking if debits = credits
debits = df.loc[df['Type'] == 'DEBIT'].copy()
debit_total = debits['Amount'].sum()
credits = df.loc[df['Type'] == 'CREDIT'].copy()
credit_total = credits['Amount'].sum()

if debit_total == credit_total:
    print(df)
    df.to_csv('', index=False)
else:
    print('Debits do not equal credits!')
