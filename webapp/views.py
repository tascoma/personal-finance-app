from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from . import db
from . import UPLOAD_FOLDER
from . import ALLOWED_EXTENSIONS
import pandas as pd
import os
from werkzeug.utils import secure_filename

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@views.route('/process-statements', methods=['GET', 'POST'])
@login_required
def process_statements():
    filename = None
    filenames = os.listdir(UPLOAD_FOLDER)
    if request.method == 'POST':
        if 'filename' in request.form:
            filename = request.form.get('filename')
            if filename:
                return redirect(url_for('views.preview_statement', filename=filename))
        if 'file' not in request.files:
            flash('No file part', category='error')
            return render_template("process_statements.html", user=current_user, filenames=filenames, filename=filename)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file', category='error')
            return render_template("process_statements.html", user=current_user, filenames=filenames, filename=filename)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            flash('File uploaded successfully!', category='success')
            return render_template("process_statements.html", user=current_user, filenames=filenames, filename=filename)
    return render_template("process_statements.html", user=current_user, filenames=filenames, filename=filename)


@views.route('/process-statements/<filename>', methods=['GET', 'POST'])
@login_required
def preview_statement(filename):
    filenames = os.listdir(UPLOAD_FOLDER)
    df = pd.read_csv(os.path.join(UPLOAD_FOLDER, filename))
    column_names = list(df.columns)
    rows = df.values.tolist()
    if request.method == 'POST':
        if 'filename' in request.form:
            filename = request.form.get('filename')
            if filename:
                return redirect(url_for('views.preview_statement', filenames=filenames, filename=filename))
        if 'file' not in request.files:
            flash('No file part', category='error')
            return render_template("process_statements.html", user=current_user, filenames=filenames, filename=filename)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file', category='error')
            return render_template("process_statements.html", user=current_user, filenames=filenames, filename=filename)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            flash('File uploaded successfully!', category='success')
            return render_template("process_statements.html", user=current_user, filename=filename)
    return render_template("process_statements.html", user=current_user, filenames=filenames, filename=filename, column_names=column_names, rows=rows)


@views.route('/view-statements')
@login_required
def view_statements():
    return render_template("view_statements.html", user=current_user)


@views.route('/manage-data', methods=['GET', 'POST'])
@login_required
def manage_data():
    table_names = db.metadata.tables.keys()
    table_name = None
    if request.method == 'POST':
        table_name = request.form.get('table')
        if table_name:
            return redirect(url_for('views.view_data', table_name=table_name))
    return render_template("manage_data.html", user=current_user, table_names=table_names, table_name=table_name)


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