from . import db    
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    password = db.Column(db.String(150))
    permission = db.Column(db.String(150))
    general_ledger = db.relationship('GeneralLedger')
    account_balance_history = db.relationship('AccountBalanceHistory')


class ChartOfAccounts(db.Model):
    account_code = db.Column(db.Integer, primary_key=True)
    account = db.Column(db.String(150))
    account_type = db.Column(db.String(150))
    account_subtype = db.Column(db.String(150))
    account_balance = db.Column(db.DECIMAL)
    mcc_list = db.relationship('MCCList')
    paystub_list = db.relationship('PaystubList')
    general_ledger = db.relationship('GeneralLedger')
    account_balance_history = db.relationship('AccountBalanceHistory')


class MCCList(db.Model):
    mcc = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(500))
    account_code = db.Column(db.Integer, db.ForeignKey('chart_of_accounts.account_code'))


class PaystubList(db.Model):
    item_id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(150))
    account_code = db.Column(db.Integer, db.ForeignKey('chart_of_accounts.account_code'))


class GeneralLedger(db.Model):
    transaction_id = db.Column(db.Text, primary_key=True)
    transaction_date = db.Column(db.Date)
    account_code = db.Column(db.Integer, db.ForeignKey('chart_of_accounts.account_code'))
    account = db.Column(db.String(150))
    description = db.Column(db.String(500))
    type = db.Column(db.String(150))
    amount = db.Column(db.DECIMAL)
    id = db.Column(db.Integer, db.ForeignKey('user.id'))


class AccountBalanceHistory(db.Model):
    balance_id = db.Column(db.Text, primary_key=True)
    balance_date = db.Column(db.Date)
    account_code = db.Column(db.Integer, db.ForeignKey('chart_of_accounts.account_code'))
    account = db.Column(db.String(150))
    account_balance = db.Column(db.DECIMAL)
    id = db.Column(db.Integer, db.ForeignKey('user.id'))