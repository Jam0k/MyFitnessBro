from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from models import FoodItem, db

nutrition_blueprint = Blueprint('nutrition', __name__, url_prefix='/nutrition')

# Define nutrition routes

@nutrition_blueprint.route('/')
def nutrition_home():
    return render_template('nutrition/nutrition-home.html')

@nutrition_blueprint.route('/meals-and-foods')
def mealsAndFoods():
    return render_template('nutrition/meals-and-food/meals-and-food-home.html')

# Define food routes

@nutrition_blueprint.route('/meals-and-foods/create-food')
def createFood():
    return render_template('nutrition/meals-and-food/food/create-food.html')

@nutrition_blueprint.route('/create-new-food-item', methods=['POST'])
def create_food():
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

        return redirect(url_for('nutrition.createFood', message="Food item added successfully!"))

    except Exception as e:
        return redirect(url_for('nutrition.createFood', message=f"An error occurred: {e}"))

@nutrition_blueprint.route('/meals-and-foods/browse-food')
def browseFood():
    return render_template('nutrition/meals-and-food/food/browse-food.html')

@nutrition_blueprint.route('/meals-and-foods/add-food')
def addFood():
    return render_template('nutrition/meals-and-food/food/add-food.html')

# Define meal routes

@nutrition_blueprint.route('/meals-and-foods/create-meal')
def createMeal():
    return render_template('nutrition/meals-and-food/meal/create-meal.html')

@nutrition_blueprint.route('/meals-and-foods/browse-meal')
def browseMeal():
    return render_template('nutrition/meals-and-food/meal/browse-meal.html')

@nutrition_blueprint.route('/meals-and-foods/add-meal')
def addMeal():
    return render_template('nutrition/meals-and-food/meal/add-meal.html')
