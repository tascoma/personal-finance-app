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
    selected_table = False
    columns = []
    rows = []

    if request.method == 'POST':
        table_name = request.form.get('table')
        selected_table = db.metadata.tables.get(table_name)
        
        if selected_table:
            df = pd.read_sql_table(table_name, db.engine)
            columns = list(df.columns)
            rows = df.values.tolist()
        
        elif 'add' in request.form:
            print("Adding data to table")
            # Logic to add new data to the selected table
            
        elif 'edit' in request.form:
            print("Editing data in table")
            # Logic to edit data in the selected table

        # Handle delete logic similarly
        
    return render_template("manage_data.html", user=current_user, table_names=table_names, selected_table=selected_table, columns=columns, rows=rows)



@views.route('/settings')
@login_required
def settings():
    return render_template("settings.html", user=current_user)