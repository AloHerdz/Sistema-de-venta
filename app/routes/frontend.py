from flask import Blueprint, render_template

frontend_bp = Blueprint('frontend', __name__)

@frontend_bp.route('/')
def home():
    return render_template('login.html')

@frontend_bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
