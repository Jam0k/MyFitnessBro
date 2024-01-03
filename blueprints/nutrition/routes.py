from flask import Blueprint, render_template

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
