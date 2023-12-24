from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from webapp import db, UPLOAD_FOLDER, ALLOWED_EXTENSIONS
import pandas as pd
import os
from werkzeug.utils import secure_filename
import statement_processor
import logging

logger = logging.getLogger(__name__)
close_books_bp = Blueprint('close_books_bp', __name__)


# Pick a month and year to close the books
# Webapp filters for general ledger for the month and year
# Create unadjusted trial balance
# Create adjusting/closing entries
# Create adjusted trial balance
# Update Account Balance History
# Update Chart of Accounts

@close_books_bp.route('/close-books', methods=['GET', 'POST'])
@login_required
def close_books():




    return render_template('close_books.html', user=current_user)