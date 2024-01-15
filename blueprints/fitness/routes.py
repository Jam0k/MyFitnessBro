from flask import Blueprint, render_template, request, jsonify, redirect, url_for, jsonify
from models import Exercise, ExerciseLog, WorkoutPlan, FoodItem, Meal, MealFoodItem, FoodMealLog, db
import json
from decimal import Decimal
from datetime import date, datetime
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


@fitness_blueprint.route('/exercises-and-workouts/get-workout-plan/<int:workout_plan_id>')
def get_workout_plan(workout_plan_id):
    workout_plan = WorkoutPlan.query.get(workout_plan_id)
    if workout_plan:
        workout_plan_data = {
            'id': workout_plan.id,
            'name': workout_plan.name,
            'created_at': workout_plan.created_at.isoformat(),
            'exercises': [
                exercise.to_dict() for exercise in workout_plan.exercises
            ]
        }
        return jsonify(workout_plan_data)
    return jsonify({'error': 'Workout plan not found'}), 404


@fitness_blueprint.route('/exercises-and-workouts/update-workout-plan/<int:workout_plan_id>', methods=['POST'])
def update_workout_plan(workout_plan_id):
    data = request.get_json()
    workout_plan = WorkoutPlan.query.get(workout_plan_id)
    if workout_plan:
        workout_plan.name = data.get('name', workout_plan.name)
        
        # Update exercises list as needed
        if 'exercises' in data:
            updated_exercise_ids = set(map(int, data['exercises']))
            current_exercise_ids = set(exercise.id for exercise in workout_plan.exercises)
            
            # Add new exercises to the workout plan
            for exercise_id in updated_exercise_ids - current_exercise_ids:
                exercise = Exercise.query.get(exercise_id)
                if exercise:
                    workout_plan.exercises.append(exercise)
            
            # Remove exercises that are no longer in the updated list
            for exercise_id in current_exercise_ids - updated_exercise_ids:
                exercise = Exercise.query.get(exercise_id)
                if exercise:
                    workout_plan.exercises.remove(exercise)

        db.session.commit()
        return jsonify({'message': 'Workout plan updated successfully'})
    return jsonify({'error': 'Workout plan not found'}), 404



@fitness_blueprint.route('/exercises-and-workouts/delete-workout-plan/<int:workout_plan_id>', methods=['DELETE'])
def delete_workout_plan(workout_plan_id):
    workout_plan = WorkoutPlan.query.get(workout_plan_id)
    if workout_plan:
        db.session.delete(workout_plan)
        db.session.commit()
        return jsonify({'message': 'Workout plan deleted successfully'})
    return jsonify({'error': 'Workout plan not found'}), 404


@fitness_blueprint.route('/exercises-and-workouts/delete-exercise/<int:exercise_id>', methods=['DELETE'])
def delete_exercise(exercise_id):
    exercise = Exercise.query.get(exercise_id)
    if exercise:
        db.session.delete(exercise)
        db.session.commit()
        return jsonify({'message': 'Exercise deleted successfully'})
    return jsonify({'error': 'Exercise not found'}), 404

@fitness_blueprint.route('/exercises-and-workouts/get-exercise/<int:exercise_id>')
def get_exercise(exercise_id):
    exercise = Exercise.query.get(exercise_id)
    if exercise:
        return jsonify(exercise.to_dict())
    return jsonify({'error': 'Exercise not found'}), 404

@fitness_blueprint.route('/exercises-and-workouts/update-exercise/<int:exercise_id>', methods=['POST'])
def update_exercise(exercise_id):
    data = request.get_json()
    exercise = Exercise.query.get(exercise_id)
    if exercise:
        exercise.name = data.get('name', exercise.name)
        exercise.category = data.get('category', exercise.category)

        # Handle integer fields with a utility function
        exercise.duration_minutes = convert_to_int(data.get('duration_minutes'), default=exercise.duration_minutes)
        exercise.sets = convert_to_int(data.get('sets'), default=exercise.sets)
        exercise.reps = convert_to_int(data.get('reps'), default=exercise.reps)
        exercise.calories_burned = convert_to_int(data.get('calories_burned'), default=exercise.calories_burned)

        # For numeric/decimal fields
        weight_lifted = data.get('weight_lifted')
        exercise.weight_lifted = Decimal(weight_lifted) if weight_lifted else exercise.weight_lifted

        exercise.notes = data.get('notes', exercise.notes)

        db.session.commit()
        return jsonify({'message': 'Exercise updated successfully'})
    return jsonify({'error': 'Exercise not found'}), 404

def convert_to_int(value, default=None):
    try:
        return int(value) if value not in ['', None] else default
    except ValueError:
        return default




@fitness_blueprint.route('/exercises-and-workouts/log-exercise', methods=['GET', 'POST'])
def logExercise():
    if request.method == 'POST':
        # Parse JSON data from the request
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Invalid JSON data'}), 400

        exercise_ids = data.get('exercise_ids', [])
        log_date = data.get('date')

        if not exercise_ids or not log_date:
            return jsonify({'error': 'Missing required data'}), 400

        # Create ExerciseLog entries for the selected exercises and log date
        for exercise_id in exercise_ids:
            exercise_log = ExerciseLog(exercise_id=exercise_id, log_date=log_date)
            db.session.add(exercise_log)

        db.session.commit()
        return jsonify({'message': 'Exercise(s) logged successfully'}), 200

    # Fetch exercises from the database
    exercises = Exercise.query.all()

    # Get today's date as a default date
    today_date = date.today().isoformat()

    return render_template('fitness/exercises-and-workouts/exercise/log-exercise.html', exercises=exercises, today_date=today_date)



# Define routes within the fitness blueprint
@fitness_blueprint.route('/exercises-and-workouts/log-workout')
def logWorkout():
    return render_template('fitness/exercises-and-workouts/workout/log-workout.html')

@fitness_blueprint.route('/exercises-and-workouts/update-workout-plan/<int:workout_plan_id>', methods=['POST'])
def updateWorkoutPlan(workout_plan_id):
    data = request.get_json()
    workout_plan = WorkoutPlan.query.get(workout_plan_id)
    if workout_plan:
        workout_plan.name = data.get('name', workout_plan.name)
        # Handle any other updatable fields here

        db.session.commit()
        return jsonify({'message': 'Workout plan updated successfully'})
    return jsonify({'error': 'Workout plan not found'}), 404
