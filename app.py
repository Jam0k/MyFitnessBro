from flask import Flask, render_template, send_from_directory, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import os
from dotenv import load_dotenv
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime


# Load environment variables
load_dotenv()

app = Flask(__name__)

# Database connection parameters
db_user = os.environ.get('POSTGRES_USER')
db_password = os.environ.get('POSTGRES_PASSWORD')
db_name = os.environ.get('POSTGRES_DB')
db_host = os.environ.get('POSTGRES_ENV')  # Docker service name for the database. Change to db for docker, and localhost for local testing.

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{db_host}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Log file size from .env or default to 10MB
log_file_size = int(os.getenv('LOG_FILE_SIZE', 10485760))

# Set up logging
log_file_path = os.path.join(os.getcwd(), 'app.log')
handler = RotatingFileHandler(log_file_path, maxBytes=log_file_size, backupCount=5)

# Define the formatter and set it for the handler
formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s')
handler.setFormatter(formatter)

# Add the handler to the app's logger
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

def test_db_connection():
    try:
        # Execute a simple query
        db.session.execute(text('SELECT 1'))
        app.logger.info("Connected to the database successfully.")
    except Exception as e:
        app.logger.error(f"Database connection failed: {e}")

class FoodItem(db.Model):
    __tablename__ = 'food_items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    serving_size = db.Column(db.String(100))
    calories = db.Column(db.Integer)
    total_fat = db.Column(db.Numeric(5,2))
    total_carbohydrate = db.Column(db.Numeric(5,2))
    total_sugars = db.Column(db.Numeric(5,2))
    total_protein = db.Column(db.Numeric(5,2))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp())

@app.route('/node_modules/<path:filename>')
def node_modules(filename):
    return send_from_directory('node_modules', filename)

@app.route('/')
def index():
    test_db_connection()
    return render_template('dashboard.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/nutrition')
def nutrition():
    return render_template('nutrition.html')

@app.route('/nutrition/meals')
def meals():
    return render_template('meals.html')

@app.route('/nutrition/meals/add-food')
def addFood():
    return render_template('add-food.html')

# Get food items in /nutrition/meals/browse-foods.

@app.route('/get-foods', methods=['GET'])
def get_foods():
    try:
        foods = FoodItem.query.all()
        foods_data = [{
            'food_name': food.name,
            'serving_size': food.serving_size,
            'calories': food.calories,
            'total_fat': str(food.total_fat),
            'total_carbohydrate': str(food.total_carbohydrate),
            'total_sugars': str(food.total_sugars),
            'total_protein': str(food.total_protein)
        } for food in foods]
        return jsonify(foods_data)
    except Exception as e:
        return jsonify({'error': str(e)})
    
# Add food items in /nutrition/meals/create-food.

@app.route('/add-food', methods=['POST'])
def add_food():
    try:
        # Extract data from form
        name = request.form.get('name')
        serving_size = request.form.get('serving_size')
        calories = request.form.get('calories')
        total_fat = request.form.get('total_fat')
        total_carbohydrate = request.form.get('total_carbohydrate')
        total_sugars = request.form.get('total_sugars')
        total_protein = request.form.get('total_protein')

        # Create new FoodItem object
        new_food = FoodItem(
            name=name, 
            serving_size=serving_size, 
            calories=calories,
            total_fat=total_fat, 
            total_carbohydrate=total_carbohydrate,
            total_sugars=total_sugars, 
            total_protein=total_protein
        )

        # Add to database
        db.session.add(new_food)
        db.session.commit()

        # Return success message
        return jsonify(message="Food item has been added successfully!")

    except Exception as e:
        # Handle errors
        return jsonify(message=f"An error occurred: {e}")

@app.route('/nutrition/meals/browse-foods')
def browseFoods():
    return render_template('browse-foods.html')










@app.route('/fitness')
def fitness():
    return render_template('fitness.html')


if __name__ == '__main__':
    app.run(debug=True)
