from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from . import db
import pandas as pd


views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/process-statements')
@login_required
def process_statements():
    return render_template("process_statements.html", user=current_user)

@views.route('/view-statements')
@login_required
def view_statements():
    return render_template("view_statements.html", user=current_user)

@views.route('/manage-data', methods=['GET', 'POST'])
@login_required
def manage_data():
    table_names = db.metadata.tables.keys()

    if request.method == 'POST':
        table = request.form.get('table')
        if table and table in table_names:  # Check if the selected table exists
            df = pd.read_sql_table(table, db.engine)
            column_names = list(df.columns)
            rows = df.values.tolist()
            return render_template("manage_data.html", user=current_user, table_names=table_names, column_names=column_names, rows=rows)

    return render_template("manage_data.html", user=current_user, table_names=table_names)


@views.route('/settings')
@login_required
def settings():
    return render_template("settings.html", user=current_user)