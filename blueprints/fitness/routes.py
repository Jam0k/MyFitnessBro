from flask import Blueprint, render_template, request, jsonify, redirect, url_for, jsonify
from models import Exercise, FoodItem, Meal, MealFoodItem, FoodMealLog, db
import json
from decimal import Decimal
from datetime import datetime
from collections import defaultdict

# Create a blueprint for the fitness routes
fitness_blueprint = Blueprint('fitness', __name__, url_prefix='/fitness')

# Define routes within the fitness blueprint
@fitness_blueprint.route('/')
def fitness_home():
    return render_template('fitness/fitness-home.html')

# Define routes within the fitness blueprint
@fitness_blueprint.route('/exercises-and-workouts')
def exercisesAndWorkoutsHome():
    return render_template('fitness/exercises-and-workouts/exercises-and-workouts-home.html')

# Define a route within the fitness blueprint to handle exercise creation
@fitness_blueprint.route('/exercises-and-workouts/create-exercise', methods=['GET', 'POST'])
def create_exercise():
    if request.method == 'POST':
        # Extract data from the form
        name = request.form['name']
        category = request.form['category']
        duration_minutes = request.form.get('duration', type=int)
        sets = request.form.get('sets', type=int)
        reps = request.form.get('reps', type=int)
        weight_lifted = request.form.get('weight_lifted', type=Decimal)
        calories_burned = request.form.get('calories_burned', type=int)
        notes = request.form['notes']
        log_date = datetime.strptime(request.form['log_date'], '%Y-%m-%d').date()

        # Create a new exercise object and save it to the database
        exercise = Exercise(
            name=name,
            category=category,
            duration_minutes=duration_minutes,
            sets=sets,
            reps=reps,
            weight_lifted=weight_lifted,
            calories_burned=calories_burned,
            notes=notes,
            log_date=log_date
        )
        db.session.add(exercise)
        db.session.commit()

        return redirect(url_for('fitness.exercisesAndWorkoutsHome'))

    return render_template('fitness/exercises-and-workouts/exercise/create-exercise.html')


# Define a route to get exercise data in JSON format
@fitness_blueprint.route('/exercises-and-workouts/get-exercises')
def get_exercises():
    exercises = Exercise.query.all()

    # Convert exercises to a list of dictionaries
    exercise_data = [
        {
            'name': exercise.name,
            'category': exercise.category,
            'duration_minutes': exercise.duration_minutes,
            'sets': exercise.sets,
            'reps': exercise.reps,
            'weight_lifted': str(exercise.weight_lifted),
            'calories_burned': exercise.calories_burned,
            'log_date': exercise.log_date.isoformat()
        }
        for exercise in exercises
    ]

    return jsonify({'data': exercise_data})

# Define routes within the fitness blueprint
@fitness_blueprint.route('/exercises-and-workouts/browse-exercise')
def browse_exercise():
    return render_template('fitness/exercises-and-workouts/exercise/browse-exercise.html')

