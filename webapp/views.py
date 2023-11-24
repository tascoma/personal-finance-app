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
        table_name = request.form.get('table')
        if table_name:
            return redirect(url_for('views.view_data', table_name=table_name))
    return render_template("manage_data.html", user=current_user, table_names=table_names)


@views.route('/manage-data/view-data/<table_name>', methods=['GET', 'POST'])
@login_required
def view_data(table_name):
    table_names = db.metadata.tables.keys()
    df = pd.read_sql_table(table_name, db.engine)
    column_names = list(df.columns)
    rows = df.values.tolist()
    if request.method == 'POST':
        if 'table' in request.form:
            table_name = request.form.get('table')
            if table_name:
                return redirect(url_for('views.view_data', table_name=table_name))
    return render_template("manage_data.html", user=current_user, table_names=table_names, table_name=table_name, column_names=column_names, rows=rows)


@views.route('/settings')
@login_required
def settings():
    return render_template("settings.html", user=current_user)