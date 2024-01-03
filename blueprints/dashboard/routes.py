from flask import Blueprint, render_template

# Create a blueprint for the dashboard routes
dashboard_blueprint = Blueprint('dashboard', __name__)

# Define routes within the dashboard blueprint
@dashboard_blueprint.route('/dashboard')
def dashboard():
    return render_template('dashboard/dashboard.html')

# You can add more routes here for the dashboard if needed
