from flask import Blueprint, render_template

nutrition_blueprint = Blueprint('nutrition', __name__, url_prefix='/nutrition')

# Define routes within this blueprint
@nutrition_blueprint.route('/')
def nutrition_home():
    # Define the route logic
    return render_template('nutrition/nutrition-home.html')

@nutrition_blueprint.route('/meals-and-foods')
def mealsAndFoods():
    # Define the route logic
    return render_template('nutrition/meals-and-food/meals-and-food-home.html')

@nutrition_blueprint.route('/meals-and-foods/create-food')
def createFood():
    # Define the route logic
    return render_template('nutrition/meals-and-food/food/create-food.html')

# Define other routes for the nutrition category
