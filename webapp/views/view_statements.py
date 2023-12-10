from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user


view_statements_bp = Blueprint('view_statements', __name__)


@view_statements_bp.route('/view-statements')
@login_required
def view_statements():
    return render_template("view_statements.html", user=current_user)