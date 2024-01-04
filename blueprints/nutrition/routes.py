from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from models import FoodItem, Meal, MealFoodItem, db
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


@nutrition_blueprint.route('/meals-and-foods/delete-food/<int:id>', methods=['POST'])
def deleteFoodItem(id):
    food_item = FoodItem.query.get_or_404(id)
    db.session.delete(food_item)
    db.session.commit()
    return jsonify({'message': 'Food item deleted successfully'})


@nutrition_blueprint.route('/meals-and-foods/add-food')
def addFood():
    return render_template('nutrition/meals-and-food/food/add-food.html')










# Define meal routes


@nutrition_blueprint.route('/meals-and-foods/create-meal')
def createMeal():
    try:
        # Fetch all food items from the database
        food_items = FoodItem.query.all()

        # Convert food items to a format suitable for the template
        food_items_data = [item.to_dict() for item in food_items]

        # Render the create-meal template with the food items data
        return render_template('nutrition/meals-and-food/meal/create-meal.html', food_items=food_items_data)

    except Exception as e:
        # Handle exceptions and possibly return an error message
        return render_template('nutrition/meals-and-food/meal/create-meal.html', error=str(e))
    
@nutrition_blueprint.route('/meals-and-foods/create-new-meal', methods=['POST'])
def createNewMeal():
    try:
        data = request.get_json()
        meal_name = data['name']
        food_items_data = data['food_items']

        new_meal = Meal(name=meal_name)
        db.session.add(new_meal)
        db.session.flush()  # To get the new meal's ID

        for item in food_items_data:
            food_id = int(item['id'])
            serving_count = float(item['serving_count'])  # Convert serving count to float

            meal_food_item = MealFoodItem(
                meal_id=new_meal.id,
                food_item_id=food_id,
                serving_count=serving_count
            )
            db.session.add(meal_food_item)

        db.session.commit()
        return jsonify({'message': 'Meal created successfully'})

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500





@nutrition_blueprint.route('/meals-and-foods/browse-meal')
def browseMeal():
    try:
        meals = Meal.query.all()
        meals_data = []

        for meal in meals:
            # Fetch associated food items and serving counts for each meal
            food_items_data = db.session.query(
                FoodItem.name, MealFoodItem.serving_count
            ).join(MealFoodItem, FoodItem.id == MealFoodItem.food_item_id)\
             .filter(MealFoodItem.meal_id == meal.id).all()

            # Format the food items and serving counts into a readable string
            food_items_str = ', '.join([f"{fi.name} ({fi.serving_count} servings)" for fi in food_items_data])

            meals_data.append({
                'id': meal.id,
                'name': meal.name,
                'food_items': food_items_str
            })

        return render_template('nutrition/meals-and-food/meal/browse-meal.html', meals=meals_data)
    except Exception as e:
        return render_template('nutrition/meals-and-food/meal/browse-meal.html', error=str(e))


    

    
@nutrition_blueprint.route('/meals-and-foods/delete-meal/<int:id>', methods=['POST'])
def deleteMeal(id):
    try:
        meal = Meal.query.get_or_404(id)
        
        # Delete associated MealFoodItem entries
        MealFoodItem.query.filter_by(meal_id=id).delete()

        # Delete the meal itself
        db.session.delete(meal)
        db.session.commit()

        return jsonify({'message': 'Meal deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500



@nutrition_blueprint.route('/meals-and-foods/get-macros/<int:id>')
def getMacros(id):
    try:
        meal = Meal.query.get_or_404(id)

        # Fetch associated food items
        food_items_data = db.session.query(
            FoodItem.name, FoodItem.calories, FoodItem.total_fat, 
            FoodItem.total_carbohydrate, FoodItem.total_sugars, FoodItem.total_protein, 
            MealFoodItem.serving_count
        ).join(MealFoodItem, FoodItem.id == MealFoodItem.food_item_id)\
         .filter(MealFoodItem.meal_id == id).all()

        # Initialize total macros
        macros = {'total_calories': 0, 'total_fat': 0, 'total_carbs': 0, 'total_sugars': 0, 'total_protein': 0}

        # Calculate total macros
        for item in food_items_data:
            macros['total_calories'] += item.calories * item.serving_count if item.calories else 0
            macros['total_fat'] += item.total_fat * item.serving_count if item.total_fat else 0
            macros['total_carbs'] += item.total_carbohydrate * item.serving_count if item.total_carbohydrate else 0
            macros['total_sugars'] += item.total_sugars * item.serving_count if item.total_sugars else 0
            macros['total_protein'] += item.total_protein * item.serving_count if item.total_protein else 0

        # Format the response with rounded numbers and clearer formatting
        formatted_response = f"""
            <strong>Calories:</strong> {round(macros['total_calories'], 1)}<br>
            <strong>Fat:</strong> {round(macros['total_fat'], 1)}g<br>
            <strong>Carbs:</strong> {round(macros['total_carbs'], 1)}g<br>
            <strong>Sugars:</strong> {round(macros['total_sugars'], 1)}g<br>
            <strong>Protein:</strong> {round(macros['total_protein'], 1)}g
        """

        return formatted_response

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@nutrition_blueprint.route('/meals-and-foods/get-meal/<int:id>', methods=['GET'])
def getMeal(id):
    try:
        meal = Meal.query.get_or_404(id)
        meal_data = {
            'name': meal.name,
            # Fetch associated food items and serving counts
            'food_items': [
                {'id': fi.food_item_id, 'name': fi.food_item.name, 'serving_count': fi.serving_count}
                for fi in meal.meal_food_item_assoc
            ]
        }
        return jsonify(meal_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@nutrition_blueprint.route('/meals-and-foods/update-meal/<int:id>', methods=['POST'])
def updateMeal(id):
    try:
        data = request.get_json()
        meal = Meal.query.get_or_404(id)

        # Update meal name
        meal.name = data['name']

        # Update serving counts for each food item
        for item_data in data['food_items']:
            meal_food_item = MealFoodItem.query.filter_by(meal_id=id, food_item_id=item_data['id']).first()
            if meal_food_item:
                meal_food_item.serving_count = item_data['serving_count']

        db.session.commit()
        return jsonify({'message': 'Meal updated successfully'})

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500




@nutrition_blueprint.route('/meals-and-foods/add-meal')
def addMeal():
    return render_template('nutrition/meals-and-food/meal/add-meal.html')
