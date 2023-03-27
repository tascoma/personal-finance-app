import pandas as pd

# use these lines when using pc
bank = pd.read_csv('')
credit_card = pd.read_csv('')
paystub = pd.read_excel('')

# # use these lines when using mac
# bank = pd.read_csv('Bank/Bank_Data_Cleaned.csv')
# credit_card = pd.read_csv('Credit Card/Credit_Card_Cleaned.csv')
# paystub = pd.read_excel('Paystub/Oct Paystub Entries.xlsx')

# cleaning data
# bank['Date'] = pd.to_datetime(bank['Date'])
# credit_card['Date'] = pd.to_datetime(paystub['Date'])
# paystub['Date'] = pd.to_datetime(paystub['Date'])

paystub['Date'] = paystub['Date'].astype(str)

print(bank)
print(credit_card)
print(paystub)

print(bank.dtypes)
print(credit_card.dtypes)
print(paystub.dtypes)

# appending data
df = pd.concat([bank, credit_card, paystub])

# checking if debits = credits
debits = df.loc[df['Type'] == 'DEBIT'].copy()
debit_total = debits['Amount'].sum()
credits = df.loc[df['Type'] == 'CREDIT'].copy()
credit_total = credits['Amount'].sum()

# print(debit_total)
# print(credit_total)

if debit_total == credit_total:
    print(df)
    df.to_excel('', index=False)
else:
    print('Debits do not equal credits!')
