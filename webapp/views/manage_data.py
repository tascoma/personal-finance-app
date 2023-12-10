from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from webapp import db
from webapp import UPLOAD_FOLDER
from webapp import ALLOWED_EXTENSIONS
import pandas as pd
import os
from werkzeug.utils import secure_filename
import statement_processor


manage_data_bp = Blueprint('manage_data', __name__)

@manage_data_bp.route('/manage-data', methods=['GET', 'POST'])
@login_required
def manage_data():
    table_names = db.metadata.tables.keys()
    table_name = None
    if request.method == 'POST':
        table_name = request.form.get('table')
        if table_name:
            return redirect(url_for('manage_data_bp.view_data', table_name=table_name))
    return render_template("manage_data.html", user=current_user, table_names=table_names, table_name=table_name)


@manage_data_bp.route('/manage-data/view-data/<table_name>', methods=['GET', 'POST'])
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
                return redirect(url_for('manage_data_bp.view_data', table_name=table_name))
    return render_template("manage_data_table.html", user=current_user, table_names=table_names, table_name=table_name, column_names=column_names, rows=rows)