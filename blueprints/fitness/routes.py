# Import necessary modules
from flask import (
    Blueprint,
    render_template,
    request,
    jsonify,
    redirect,
    url_for,
    jsonify,
)
from models import Exercise, ExerciseLog, WorkoutPlan, CardioLog, db
from decimal import Decimal
from datetime import date, datetime

# Create a blueprint for the fitness routes
fitness_blueprint = Blueprint("fitness", __name__, url_prefix="/fitness")

# Fitness Home
@fitness_blueprint.route("/")
def fitness_home():
    return render_template("fitness/fitness-home.html")


# Exercise and Workouts Routes
@fitness_blueprint.route("/exercises-and-workouts")
def exercisesAndWorkoutsHome():
    return render_template(
        "fitness/exercises-and-workouts/exercises-and-workouts-home.html"
    )

# Define a route to create a new exercise
@fitness_blueprint.route(
    "/exercises-and-workouts/create-exercise", methods=["GET", "POST"]
)
def create_exercise():
    if request.method == "POST":
        # Retrieve form data
        name = request.form["name"]
        category = request.form["category"]
        notes = request.form["notes"]

        # Create a new Exercise object
        exercise = Exercise(
            name=name,
            category=category,
            notes=notes,
        )

        # Add the exercise to the database
        db.session.add(exercise)
        db.session.commit()

        # Redirect to the exercises and workouts home page
        return redirect(url_for("fitness.exercisesAndWorkoutsHome"))

    # Render the create exercise template for GET request
    return render_template(
        "fitness/exercises-and-workouts/exercise/create-exercise.html"
    )


# Define a route to get exercise data in JSON format
@fitness_blueprint.route("/exercises-and-workouts/get-exercises")
def get_exercises():
    """
    Retrieves a list of exercises from the Exercise table and returns them as JSON.

    Returns:
        JSON: A JSON response containing the exercise data.
    """
    # Retrieve all exercises from the Exercise table
    exercises = Exercise.query.all()

    # Create a list of exercise data dictionaries
    exercise_data = [
        {
            "id": exercise.id,
            "name": exercise.name,
            "category": exercise.category,
            "notes": exercise.notes,
            "created_at": exercise.created_at.isoformat(),
            "updated_at": exercise.updated_at.isoformat(),
        }
        for exercise in exercises
    ]

    # Return the exercise data as JSON
    return jsonify({"data": exercise_data})


# Browse Exercise Page
@fitness_blueprint.route("/exercises-and-workouts/browse-exercise")
def browseExercise():
    return render_template(
        "fitness/exercises-and-workouts/exercise/browse-exercise.html"
    )


@fitness_blueprint.route(
    "/exercises-and-workouts/create-workout-plan", methods=["GET", "POST"]
)
def create_workout_plan():
    if request.method == "POST":
        # Parsing JSON data for POST request
        data = request.get_json()
        workout_name = data["workout_name"]
        selected_exercises_ids = data["selected_exercises"]
        selected_exercises = Exercise.query.filter(
            Exercise.id.in_(selected_exercises_ids)
        ).all()

        if selected_exercises:
            workout_plan = WorkoutPlan(name=workout_name, exercises=selected_exercises)
            db.session.add(workout_plan)
            db.session.commit()

        return redirect(url_for("fitness.exercisesAndWorkoutsHome"))

    # Handling GET request to render the page initially
    exercises = Exercise.query.all()
    return render_template(
        "fitness/exercises-and-workouts/workout/create-workout-plan.html",
        exercises=exercises,
    )


# Browse Workout Page
@fitness_blueprint.route("/exercises-and-workouts/browse-workout-plans")
def browseWorkout():
    return render_template(
        "fitness/exercises-and-workouts/workout/browse-workout-plan.html"
    )

# Get workout plans
@fitness_blueprint.route("/exercises-and-workouts/get-workout-plans")
def get_workout_plans():
    # Retrieve all workout plans from the database
    workout_plans = WorkoutPlan.query.all()

    # Prepare workout plan data in JSON format
    workout_plan_data = [
        {
            "id": workout_plan.id,
            "name": workout_plan.name,
            "created_at": workout_plan.created_at.isoformat(),
            "exercises": [
                {
                    "id": exercise.id,
                    "name": exercise.name,
                    "category": exercise.category,
                    "duration_minutes": exercise.duration_minutes,
                    "sets": exercise.sets,
                    "reps": exercise.reps,
                    "weight_lifted": str(exercise.weight_lifted),
                    "calories_burned": exercise.calories_burned,
                    "notes": exercise.notes,
                }
                for exercise in workout_plan.exercises
            ],
        }
        for workout_plan in workout_plans
    ]

    # Return the workout plan data as JSON response
    return jsonify({"data": workout_plan_data})


# Retrieve a specific workout plan by ID
@fitness_blueprint.route(
    "/exercises-and-workouts/get-workout-plan/<int:workout_plan_id>"
)
def get_workout_plan(workout_plan_id):
    workout_plan = WorkoutPlan.query.get(workout_plan_id)
    if workout_plan:
        # Prepare workout plan data in JSON format
        workout_plan_data = {
            "id": workout_plan.id,
            "name": workout_plan.name,
            "created_at": workout_plan.created_at.isoformat(),
            "exercises": [exercise.to_dict() for exercise in workout_plan.exercises],
        }
        return jsonify(workout_plan_data)
    # Return error message if workout plan is not found
    return jsonify({"error": "Workout plan not found"}), 404


# Update Workout Plan
@fitness_blueprint.route(
    "/exercises-and-workouts/update-workout-plan/<int:workout_plan_id>",
    methods=["POST"],
)
def update_workout_plan(workout_plan_id):
    data = request.get_json()
    workout_plan = WorkoutPlan.query.get(workout_plan_id)
    if workout_plan:
        workout_plan.name = data.get("name", workout_plan.name)

        # Update exercises list as needed
        if "exercises" in data:
            updated_exercise_ids = set(map(int, data["exercises"]))
            current_exercise_ids = set(
                exercise.id for exercise in workout_plan.exercises
            )

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
        return jsonify({"message": "Workout plan updated successfully"})
    return jsonify({"error": "Workout plan not found"}), 404


# Delete Workout Plan
@fitness_blueprint.route(
    "/exercises-and-workouts/delete-workout-plan/<int:workout_plan_id>",
    methods=["DELETE"],
)
def delete_workout_plan(workout_plan_id):
    workout_plan = WorkoutPlan.query.get(workout_plan_id)
    if workout_plan:
        db.session.delete(workout_plan)
        db.session.commit()
        return jsonify({"message": "Workout plan deleted successfully"})
    return jsonify({"error": "Workout plan not found"}), 404

# Delete Exercise
@fitness_blueprint.route(
    "/exercises-and-workouts/delete-exercise/<int:exercise_id>", methods=["DELETE"]
)
def delete_exercise(exercise_id):
    exercise = Exercise.query.get(exercise_id)
    if exercise:
        db.session.delete(exercise)
        db.session.commit()
        return jsonify({"message": "Exercise deleted successfully"})
    return jsonify({"error": "Exercise not found"}), 404

# Get Exercise
@fitness_blueprint.route("/exercises-and-workouts/get-exercise/<int:exercise_id>")
def get_exercise(exercise_id):
    exercise = Exercise.query.get(exercise_id)
    if exercise:
        return jsonify(exercise.to_dict())
    return jsonify({"error": "Exercise not found"}), 404

# Update Exercise
@fitness_blueprint.route(
    "/exercises-and-workouts/update-exercise/<int:exercise_id>", methods=["POST"]
)
def update_exercise(exercise_id):
    data = request.get_json()
    exercise = Exercise.query.get(exercise_id)
    if exercise:
        exercise.name = data.get("name", exercise.name)
        exercise.category = data.get("category", exercise.category)

        # Handle integer fields with a utility function
        exercise.duration_minutes = convert_to_int(
            data.get("duration_minutes"), default=exercise.duration_minutes
        )
        exercise.sets = convert_to_int(data.get("sets"), default=exercise.sets)
        exercise.reps = convert_to_int(data.get("reps"), default=exercise.reps)
        exercise.calories_burned = convert_to_int(
            data.get("calories_burned"), default=exercise.calories_burned
        )

        # For numeric/decimal fields
        weight_lifted = data.get("weight_lifted")
        exercise.weight_lifted = (
            Decimal(weight_lifted) if weight_lifted else exercise.weight_lifted
        )

        exercise.notes = data.get("notes", exercise.notes)

        db.session.commit()
        return jsonify({"message": "Exercise updated successfully"})
    return jsonify({"error": "Exercise not found"}), 404


def convert_to_int(value, default=None):
    try:
        return int(value) if value not in ["", None] else default
    except ValueError:
        return default

@fitness_blueprint.route("/exercises-and-workouts/log-exercise", methods=["GET", "POST"])
def log_exercise():
    if request.method == "POST":
        try:
            # Parse JSON data from the request
            data = request.get_json()

            # Validating the received data
            if not all(key in data for key in ["exercise_id", "sets", "reps", "date"]):
                return jsonify({"error": "Missing required data"}), 400

            # Creating a new ExerciseLog instance
            new_log = ExerciseLog(
                exercise_id=data["exercise_id"],
                sets=data["sets"],
                reps=data["reps"],
                weight=data.get("weight", 0),  # Defaulting to 0 if weight is not provided
                notes=data.get("notes", ""),  # Defaulting to an empty string if notes are not provided
                log_date=datetime.strptime(data["date"], "%Y-%m-%d")
            )

            # Adding the new log to the database session and committing
            db.session.add(new_log)
            db.session.commit()

            return jsonify({"message": "Exercise logged successfully"}), 201

        except Exception as e:
            # Handling any unexpected exceptions
            return jsonify({"error": str(e)}), 500

    else:  # GET request
        # Fetch exercises from the database
        exercises = Exercise.query.all()

        # Get today's date as a default date
        today_date = datetime.today().strftime('%Y-%m-%d')

        return render_template(
            "fitness/exercises-and-workouts/exercise/log-exercise.html",
            exercises=exercises,
            today_date=today_date
        )

# Log Workout
@fitness_blueprint.route("/exercises-and-workouts/log-workout", methods=["GET", "POST"])
def logWorkout():
    if request.method == "POST":
        # Parse JSON data from the request
        data = request.get_json()

        if not data:
            return jsonify({"error": "Invalid JSON data"}), 400

        workout_plan_ids = data.get("workout_plan_ids")
        log_date = data.get("date")

        if not workout_plan_ids or not log_date:
            return jsonify({"error": "Missing required data"}), 400

        # Create ExerciseLog entries for the selected workout plans and log date
        for workout_plan_id in workout_plan_ids:
            exercise_log = ExerciseLog(
                workout_plan_id=workout_plan_id, log_date=log_date
            )
            db.session.add(exercise_log)
        db.session.commit()

        return jsonify({"message": "Workout(s) logged successfully"}), 200

    # Fetch workout plans from the database
    workout_plans = WorkoutPlan.query.all()

    # Get today's date as a default date
    today_date = date.today().isoformat()

    return render_template(
        "fitness/exercises-and-workouts/workout/log-workout.html",
        workout_plans=workout_plans,
        today_date=today_date,
    )

# Update Workout Plan
@fitness_blueprint.route(
    "/exercises-and-workouts/update-workout-plan/<int:workout_plan_id>",
    methods=["POST"],
)
def updateWorkoutPlan(workout_plan_id):
    # Parse JSON data from the request
    data = request.get_json()

    # Retrieve the workout plan from the database
    workout_plan = WorkoutPlan.query.get(workout_plan_id)

    if workout_plan:
        # Update the workout plan with the provided data
        workout_plan.name = data.get("name", workout_plan.name)
        # Handle any other updatable fields here

        db.session.commit()
        return jsonify({"message": "Workout plan updated successfully"})
    return jsonify({"error": "Workout plan not found"}), 404

@fitness_blueprint.route("/tracking", methods=["GET", "POST"])
def tracking():
    current_date = datetime.now().strftime("%Y-%m-%d")

    if request.method == "POST":
        selected_date_str = request.form.get("date")
        selected_date = datetime.strptime(selected_date_str, "%Y-%m-%d") if selected_date_str else None

        exercise_logs = []
        cardio_logs = []

        if selected_date:
            # Query exercise logs for the selected date
            exercise_logs = ExerciseLog.query.filter(
                ExerciseLog.log_date == selected_date
            ).join(ExerciseLog.exercise).all()

            # Query cardio logs for the selected date
            cardio_logs = CardioLog.query.filter(
                CardioLog.date == selected_date
            ).all()

        exercise_logs_data = [
            {
                "name": log.exercise.name,
                "sets": log.sets,
                "reps": log.reps,
                "weight": log.weight,
                "notes": log.notes,
            }
            for log in exercise_logs
        ]

        cardio_logs_data = [
            {
                "name": log.name,
                "activity": log.activity,
                "duration": log.duration,
                "calories_burned": log.calories_burned,
                "notes": log.notes,
            }
            for log in cardio_logs
        ]

        return jsonify(
            {
                "exercise_logs": exercise_logs_data,
                "cardio_logs": cardio_logs_data,
                "current_date": current_date,
            }
        )

    return render_template("fitness/tracking/tracking.html", current_date=current_date)

# Cardio Routes
@fitness_blueprint.route("/cardio-and-aerobics")
def cardioAndAerobics():
    return render_template("fitness/cardio-and-aerobics/cardio-and-aerobics-home.html")

@fitness_blueprint.route("/cardio-and-aerobics/submit-cardio-log", methods=['POST'])
def submit_cardio_log():
    # Retrieve form data
    name = request.form.get('name')
    activity = request.form.get('activity')
    duration = request.form.get('duration', type=int)
    calories_burned = request.form.get('calories_burned', type=int)
    date = request.form.get('date')
    notes = request.form.get('notes')

    # Create a new CardioLog object
    cardio_log = CardioLog(
        name=name,
        activity=activity,
        duration=duration,
        calories_burned=calories_burned,
        date=datetime.strptime(date, '%Y-%m-%d').date() if date else None,
        notes=notes
    )

    # Add the cardio log to the database
    db.session.add(cardio_log)
    db.session.commit()

    # Redirect to a suitable page after submission
    return redirect(url_for('fitness.cardioAndAerobics'))


@fitness_blueprint.route("/cardio-and-aerobics/get-logs", methods=["POST"])
def get_cardio_logs():
    selected_date_str = request.form.get("date")
    selected_date = (
        datetime.strptime(selected_date_str, "%Y-%m-%d")
        if selected_date_str
        else None
    )

    cardio_logs = []

    if selected_date:
        # Query cardio logs for the selected date
        cardio_logs = CardioLog.query.filter(
            CardioLog.date == selected_date
        ).all()

    cardio_logs_data = [
        {
            "name": log.name,
            "activity": log.activity,
            "duration": log.duration,
            "date": log.date.isoformat(),
            "notes": log.notes
        }
        for log in cardio_logs
    ]

    return jsonify({"cardio_logs": cardio_logs_data})