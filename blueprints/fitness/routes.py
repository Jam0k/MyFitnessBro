from flask import Blueprint, render_template

# Create a blueprint for the fitness routes
fitness_blueprint = Blueprint('fitness', __name__)

# Define routes within the fitness blueprint
@fitness_blueprint.route('/fitness')
def fitness_home():
    return render_template('fitness/fitness-home.html')

# You can add more routes here for the fitness section if needed
