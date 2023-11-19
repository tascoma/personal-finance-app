from flask import Blueprint, render_template
from flask_login import login_required, current_user


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

@views.route('/view-data')
@login_required
def view_data():
    return render_template("view_data.html", user=current_user)

@views.route('/settings')
@login_required
def settings():
    return render_template("settings.html", user=current_user)