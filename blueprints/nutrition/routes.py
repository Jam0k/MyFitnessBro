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
def createNewFoodItem():
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
    search_query = request.args.get('search', '')
    try:
        if search_query:
            food_items = FoodItem.query.filter(FoodItem.name.ilike(f"%{search_query}%"))
        else:
            food_items = FoodItem.query.all()

        food_items_data = [item.to_dict() for item in food_items]
        
        return render_template('nutrition/meals-and-food/food/browse-food.html', food_items=food_items_data, search_query=search_query)
    except Exception as e:
        return render_template('nutrition/meals-and-food/food/browse-food.html', error=str(e))

    
@nutrition_blueprint.route('/meals-and-foods/edit-food/<int:id>', methods=['POST'])
def editFoodItem(id):
    data = request.get_json()  # Assuming you're sending JSON data
    food_item = FoodItem.query.get_or_404(id)
    
    # Update the food item with the data received
    food_item.name = data['name']
    food_item.serving_size = data['serving_size']
    food_item.calories = data['calories']
    food_item.total_fat = data['total_fat']
    food_item.total_carbohydrate = data['total_carbohydrate']
    food_item.total_sugars = data['total_sugars']
    food_item.total_protein = data['total_protein']

    db.session.commit()

    return jsonify({'message': 'Food item updated successfully'})

@nutrition_blueprint.route('/meals-and-foods/get-food/<int:id>')
def getFoodItem(id):
    food_item = FoodItem.query.get_or_404(id)
    return jsonify(food_item.to_dict())

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
