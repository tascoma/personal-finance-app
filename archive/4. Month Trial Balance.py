import pandas as pd

df = pd.read_excel('')

# checking if debits = credits
debits = df.loc[df['Type'] == 'DEBIT'].copy()
debit_total = debits['Amount'].sum()
credits = df.loc[df['Type'] == 'CREDIT'].copy()
credit_total = credits['Amount'].sum()

if debit_total == credit_total:
    # creating pivot table
    pt = df.pivot_table(
        index=['Month', 'GL_Code', 'Account'], columns='Type', aggfunc="sum", fill_value=0)

    # changing pivot table back to dataframe
    pt.columns = pt.columns.droplevel(0)
    pt.columns.name = None
    df = pt.reset_index()
    df = df[['Month', 'GL_Code', 'Account', 'DEBIT', 'CREDIT']]

    # joining account_type from COA to df
    COA = pd.read_excel('Tables\Chart of Accounts.xlsx')
    df = pd.merge(df, COA, on='GL_Code', how='left')
    df = df[['Month', 'GL_Code', 'Account_x', 'DEBIT', 'CREDIT', 'Account_Type']]
    df.rename(columns={'Account_x': 'Account'}, inplace=True)

    # getting amount for debit accounts
    debit_accounts = df.loc[(df['Account_Type'] == 'Asset') | (
        df['Account_Type'] == 'Expense') | (df['Account_Type'] == 'Deduction')].copy()
    debit_accounts['Amount'] = debit_accounts['DEBIT'] - \
        debit_accounts['CREDIT']
    debit_accounts = debit_accounts[['Month', 'GL_Code', 'Account', 'Amount']]

    # getting amount for credit accounts
    credit_accounts = df.loc[(df['Account_Type'] == 'Liability') | (
        df['Account_Type'] == 'Equity') | (df['Account_Type'] == 'Revenue')].copy()
    credit_accounts['Amount'] = credit_accounts['CREDIT'] - \
        credit_accounts['DEBIT']
    credit_accounts = credit_accounts[[
        'Month', 'GL_Code', 'Account', 'Amount']]

    # appending debit accounts and credit accounts
    df = pd.concat([debit_accounts, credit_accounts])
    df = df.sort_values(by=['GL_Code'], ascending=True, ignore_index=True)

    print(df)
    df.to_excel('', index=False)
else:
    print('Debits do not equal credits!')
