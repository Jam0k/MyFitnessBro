from flask import Blueprint, render_template, request, jsonify, redirect, url_for, jsonify
from models import Exercise, WorkoutPlan, FoodItem, Meal, MealFoodItem, FoodMealLog, db
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
            'notes': exercise.notes,  # Include the notes field
            'created_at': exercise.created_at.isoformat(),  # Include the created_at field
            'updated_at': exercise.updated_at.isoformat(),  # Include the updated_at field
        }
        for exercise in exercises
    ]

    return jsonify({'data': exercise_data})

# Define routes within the fitness blueprint
@fitness_blueprint.route('/exercises-and-workouts/browse-exercise')
def browse_exercise():
    return render_template('fitness/exercises-and-workouts/exercise/browse-exercise.html')


@fitness_blueprint.route('/exercises-and-workouts/create-workout-plan', methods=['GET', 'POST'])
def create_workout_plan():
    if request.method == 'POST':
        workout_name = request.form.get('workout_name')  # Capture workout plan name
        selected_exercises_ids = request.form.getlist('selected_exercises')
        selected_exercises = Exercise.query.filter(Exercise.id.in_(selected_exercises_ids)).all()

        if selected_exercises:
            workout_plan = WorkoutPlan(name=workout_name, exercises=selected_exercises)  # Include the name
            db.session.add(workout_plan)
            db.session.commit()

        return redirect(url_for('fitness.exercisesAndWorkoutsHome'))

    exercises = Exercise.query.all()
    return render_template('fitness/exercises-and-workouts/workout/create-workout-plan.html', exercises=exercises)

