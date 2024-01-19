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
from models import Exercise, ExerciseLog, CardioLog, db
from decimal import Decimal
from datetime import date, datetime

# Create a blueprint for the progress routes
progress_blueprint = Blueprint("progress", __name__, url_prefix="/progress")

# Fitness Home
@progress_blueprint.route("/")
def progress_home():
    return render_template("progress/progress-home.html")