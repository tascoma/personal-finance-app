from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from webapp import db, UPLOAD_FOLDER, ALLOWED_EXTENSIONS
from webapp.models import GeneralLedger
import pandas as pd
import os
from werkzeug.utils import secure_filename
import statement_processor
import logging

logger = logging.getLogger(__name__)
process_statements_bp = Blueprint('process_statements_bp', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@process_statements_bp.route('/process-statements', methods=['GET', 'POST'])
@login_required
def process_statements():
    files = os.listdir(UPLOAD_FOLDER)
    file_name = request.form.get('file-dropdown')
    
    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(file_path)
                flash('File uploaded successfully', category='success')
                logger.info(f'File uploaded successfully: {filename}')
                files = os.listdir(UPLOAD_FOLDER)
                return render_template('process_statements.html', user=current_user, file_name=file_name, files=files)
            else:
                flash('Invalid file', category='error')
                logger.error('Invalid file upload')
                return render_template('process_statements.html', user=current_user, file_name=file_name, files=files)

        if file_name:
            logger.info(f'Previewing file: {file_name}')
            return redirect(url_for('process_statements_bp.preview_statement', file_name=file_name))
        
    return render_template('process_statements.html', user=current_user, file_name=file_name, files=files)

@process_statements_bp.route('/process-statements/<file_name>', methods=['GET', 'POST'])
@login_required
def preview_statement(file_name):
    files = os.listdir(UPLOAD_FOLDER)
    
    try:
        if ".pdf" in file_name:
            column_names = []
            rows = []
        else:
            df = pd.read_csv(os.path.join(UPLOAD_FOLDER, file_name))
            column_names = df.columns
            rows = df.values.tolist()
    except Exception as e:
        logger.error(f'Error reading CSV file: {e}')
        flash('Error reading CSV file', category='error')
        return render_template('preview_statement.html', user=current_user, file_name=file_name, files=files)

    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(file_path)
                flash('File uploaded successfully', category='success')
                logger.info(f'File uploaded successfully: {filename}')
                files = os.listdir(UPLOAD_FOLDER)
                return render_template('preview_statement.html', user=current_user, file_name=file_name, files=files, column_names=column_names, rows=rows)
            else:
                flash('Invalid file', category='error')
                return render_template('preview_statement.html', user=current_user, file_name=file_name, files=files, column_names=column_names, rows=rows)
        
        if "process-data" in request.form:
            logger.info(f'Processing file: {file_name}')
            return redirect(url_for('process_statements_bp.process_statement_data', file_name=file_name))

    return render_template('preview_statement.html', user=current_user, file_name=file_name, files=files, column_names=column_names, rows=rows)

@process_statements_bp.route('/process-statements/<file_name>/processed', methods=['GET', 'POST'])
@login_required
def process_statement_data(file_name):
    files = os.listdir(UPLOAD_FOLDER)
    
    try:
        if ".pdf" in file_name:
            column_names = []
            rows = []

            processed_df = statement_processor.process_statement(os.path.join(UPLOAD_FOLDER, file_name), db.engine)
            processed_column_names = processed_df.columns
            processed_rows = processed_df.values.tolist()
        else:
            df = pd.read_csv(os.path.join(UPLOAD_FOLDER, file_name))
            column_names = df.columns
            rows = df.values.tolist()
            
            processed_df = statement_processor.process_statement(os.path.join(UPLOAD_FOLDER, file_name), db.engine)
            processed_column_names = processed_df.columns
            processed_rows = processed_df.values.tolist()
    except Exception as e:
        logger.error(f'Error processing statement: {e}')
        flash('Error processing statement', category='error')
        return render_template('processed_statement.html', user=current_user, file_name=file_name, files=files)
    
    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(file_path)
                flash('File uploaded successfully', category='success')
                logger.info(f'File uploaded successfully: {filename}')
                files = os.listdir(UPLOAD_FOLDER)
                return render_template('processed_statement.html', user=current_user, file_name=file_name, files=files, column_names=column_names, rows=rows)
            else:
                flash('Invalid file', category='error')
                return render_template('processed_statement.html', user=current_user, file_name=file_name, files=files, column_names=column_names, rows=rows)

        if "commit-data" in request.form:
            try:
                # Application will commit the processed dataframe to the GeneralLedger table in the database
                processed_df.to_sql('general_ledger', db.engine, if_exists='append', index=False)
                logger.info(f'Processed statement data committed to database')
                flash('Processed statement data committed to database', category='success')
                return redirect(url_for('process_statements_bp.process_statements'))
            except Exception as e:
                logger.error(f'Error committing processed statement data to database: {e}', exc_info=True)
                flash('Error committing processed statement data to database', category='error')
                return redirect(url_for('process_statements_bp.process_statements'))

    return render_template('processed_statement.html', 
                           user=current_user, 
                           file_name=file_name, 
                           files=files, 
                           column_names=column_names, 
                           rows=rows, 
                           processed_column_names=processed_column_names, 
                           processed_rows=processed_rows)
