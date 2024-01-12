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
            'id': exercise.id,  # Include the ID field
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
def browseExercise():
    return render_template('fitness/exercises-and-workouts/exercise/browse-exercise.html')


@fitness_blueprint.route('/exercises-and-workouts/create-workout-plan', methods=['GET', 'POST'])
def create_workout_plan():
    if request.method == 'POST':
        # Parsing JSON data for POST request
        data = request.get_json()
        workout_name = data['workout_name']
        selected_exercises_ids = data['selected_exercises']
        selected_exercises = Exercise.query.filter(Exercise.id.in_(selected_exercises_ids)).all()

        if selected_exercises:
            workout_plan = WorkoutPlan(name=workout_name, exercises=selected_exercises)
            db.session.add(workout_plan)
            db.session.commit()

        return redirect(url_for('fitness.exercisesAndWorkoutsHome'))

    # Handling GET request to render the page initially
    exercises = Exercise.query.all()
    return render_template('fitness/exercises-and-workouts/workout/create-workout-plan.html', exercises=exercises)


# Define routes within the fitness blueprint
@fitness_blueprint.route('/exercises-and-workouts/browse-workout-plans')
def browseWorkout():
    return render_template('fitness/exercises-and-workouts/workout/browse-workout-plan.html')


@fitness_blueprint.route('/exercises-and-workouts/get-workout-plans')
def get_workout_plans():
    workout_plans = WorkoutPlan.query.all()

    workout_plan_data = [
        {
            'id': workout_plan.id,
            'name': workout_plan.name,
            'created_at': workout_plan.created_at.isoformat(),
            'exercises': [
                {
                    'id': exercise.id,
                    'name': exercise.name,
                    'category': exercise.category,
                    'duration_minutes': exercise.duration_minutes,
                    'sets': exercise.sets,
                    'reps': exercise.reps,
                    'weight_lifted': str(exercise.weight_lifted),
                    'calories_burned': exercise.calories_burned,
                    'notes': exercise.notes
                }
                for exercise in workout_plan.exercises
            ]
        }
        for workout_plan in workout_plans
    ]

    return jsonify({'data': workout_plan_data})
