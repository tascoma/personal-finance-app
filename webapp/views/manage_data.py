from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from webapp import db
import pandas as pd
import logging

logger = logging.getLogger(__name__)
manage_data_bp = Blueprint('manage_data', __name__)

@manage_data_bp.route('/manage-data', methods=['GET', 'POST'])
@login_required
def manage_data():
    table_names = db.metadata.tables.keys()
    table_name = request.form.get('table-dropdown')
    if request.method == 'POST':
        if table_name:
            logger.info(f'Viewing data for table: {table_name}')
            return redirect(url_for('manage_data.view_data', table_name=table_name))
    return render_template("manage_data.html", user=current_user, table_names=table_names)


@manage_data_bp.route('/manage-data/view-data/<table_name>', methods=['GET', 'POST'])
@login_required
def view_data(table_name):
    table_names = db.metadata.tables.keys()
    try:
        df = pd.read_sql_table(table_name, db.engine)
        column_names = list(df.columns)
        rows = df.values.tolist()
    except Exception as e:
        logger.error(f'Error viewing data: {e}', exc_info=True)
        flash('Error viewing data', category='error')
        return render_template("manage_data_table.html", user=current_user, table_names=table_names, table_name=table_name)
    
    if request.method == 'POST':
        if 'table-dropdown' in request.form:
            table_name = request.form.get('table-dropdown')
            logger.info(f'Viewing data for table: {table_name}')
            return redirect(url_for('manage_data.view_data', table_name=table_name))
        elif 'edit-data' in request.form:
            row_id = request.form.get('row-id')
            logger.info(f'Editing data for row: {row_id}')
            return redirect(url_for('manage_data.edit_data', table_name=table_name, row_id=row_id))
        elif 'delete-data' in request.form:
            row_id = request.form.get('row-id')
            logger.info(f'Deleting data for row: {row_id}')
            return redirect(url_for('manage_data.view_data', table_name=table_name))
        elif 'add-data' in request.form:
            logger.info(f'Adding data for table: {table_name}')
            return redirect(url_for('manage_data.view_data', table_name=table_name))
        else:
            pass
    return render_template("manage_data_table.html", user=current_user, table_names=table_names, table_name=table_name, column_names=column_names, rows=rows)


@manage_data_bp.route('/manage-data/edit-data/<table_name>/<row_id>', methods=['GET', 'POST'])
@login_required
def edit_data(table_name, row_id):
    table_names = db.metadata.tables.keys()
    try:
        df = pd.read_sql_table(table_name, db.engine)
        column_names = list(df.columns)
        rows = df.values.tolist()

    except Exception as e:
        logger.error(f'Error editing data: {e}', exc_info=True)
        flash('Error editing data', category='error')
        return render_template("manage_data_table.html", user=current_user, table_names=table_names, table_name=table_name)
    
    return render_template("form.html", user=current_user, table_names=table_names, table_name=table_name, column_names=column_names, rows=rows)