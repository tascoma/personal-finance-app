from flask import Blueprint, render_template
from flask_login import login_required, current_user
import logging

logger = logging.getLogger(__name__)

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)