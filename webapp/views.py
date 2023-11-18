from flask import Blueprint, render_template


views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/process-statements')
def process_statements():
    return render_template("process_statements.html")

@views.route('/view-statements')
def view_statements():
    return render_template("view_statements.html")

@views.route('/view-data')
def view_data():
    return render_template("view_data.html")

@views.route('/settings')
def settings():
    return render_template("settings.html")