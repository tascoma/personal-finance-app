import pandas as pd

df = pd.read_csv("")
mcc = pd.read_excel("Tables\CoA_MCC_Linking_Table.xlsx")

# changing amount to absolute value
df['Amount'] = abs(df['Amount'])

# filtering out service fee
df = df.loc[df['Memo'] != '00000;']

# splitting 'memo' field and getting the MCC code
df['MCC'] = df['Memo'].str.split(";").str[1].str[-4:]

# changing data 'MCC' from object to int to perform left join
df['MCC'] = df['MCC'].astype(int)

# joining chart of accounts with MCC code to credit card data
df = pd.merge(df, mcc, on="MCC", how='left')

# changing column heading for type
df['Type'] = df['Transaction']

# changing data type for 'GL Code' to join data
df['GL_Code'] = df['GL_Code'].astype(int)

# creating month dataframe
months_dic = {}
months = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]
month_num = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
months_dic['Month_Num'] = month_num
months_dic['Month'] = months
months = pd.DataFrame(months_dic)

# ordering data in chronoligical order
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values(by=['Date'], ascending=True, ignore_index=True)

# creating transaction ID
df['Month_Num'] = pd.DatetimeIndex(df['Date']).month.astype(str)
df['Transaction_ID'] = 'CC' + df['Month_Num'] + (df.index + 1).astype(str)

# joining month dataframe to GL data
df['Month_Num'] = df['Month_Num'].astype(int)
df = pd.merge(df, months, on='Month_Num', how='left')

# creating source column
df['Source'] = 'Credit Card'

# cleaning amount column
# df['Amount'].round(2)
# print(df)

# organizing column headers
df = df[['Transaction_ID', 'Source', 'Month', 'Date',
         'GL_Code', 'Account', 'Type', 'Amount']]

# copying data to create credit entries
credit_entries = df.loc[df['Type'] == 'DEBIT'].copy()
credit_entries['GL_Code'] = 2001
credit_entries['Account'] = 'EdwardJones MasterCard'
credit_entries['Type'] = 'CREDIT'

# copying data to create debit entries
debit_entries = df.loc[df['Type'] == 'CREDIT'].copy()
debit_entries['GL_Code'] = 2001
debit_entries['Account'] = 'EdwardJones MasterCard'
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

print(debit_total)
print(credit_total)

if debit_total == credit_total:
    print(df)
    df.to_csv('', index=False)
else:
    print('Debits do not equal credits!')
