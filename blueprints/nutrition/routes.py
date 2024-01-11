from flask import Blueprint, render_template, request, jsonify, redirect, url_for, jsonify
from models import FoodItem, Meal, MealFoodItem, FoodMealLog, db
import json
from decimal import Decimal
from datetime import datetime
from collections import defaultdict
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
    today = datetime.now().strftime("%Y-%m-%d")
    return render_template('nutrition/meals-and-food/food/add-food.html', today=today)


@nutrition_blueprint.route('/meals-and-foods/log-food', methods=['POST'])
def logFood():
    try:
        data = request.get_json()
        new_log = FoodMealLog(
            food_item_id=data['food_item_id'],
            serving_count=data['serving_count'],
            log_date=datetime.strptime(data['log_date'], '%Y-%m-%d'),
            meal_type=data['meal_type']  # Include meal_type in the logged data
        )
        db.session.add(new_log)
        db.session.commit()
        return jsonify({'message': 'Food logged successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@nutrition_blueprint.route('/meals-and-foods/get-all-food-items', methods=['GET'])
def getAllFoodItems():
    try:
        food_items = FoodItem.query.all()
        food_items_data = [item.to_dict() for item in food_items]
        return jsonify(food_items_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500



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

        # Data for the table
        table_data = []

        for item in food_items_data:
            item_macros = {
                'calories': item.calories * item.serving_count if item.calories else 0,
                'fat': item.total_fat * item.serving_count if item.total_fat else 0,
                'carbs': item.total_carbohydrate * item.serving_count if item.total_carbohydrate else 0,
                'sugars': item.total_sugars * item.serving_count if item.total_sugars else 0,
                'protein': item.total_protein * item.serving_count if item.total_protein else 0
            }

            # Convert Decimal to float for JSON serialization
            for key in item_macros:
                if isinstance(item_macros[key], Decimal):
                    item_macros[key] = float(item_macros[key])

            # Add to total macros
            for key, value in item_macros.items():
                macros[f'total_{key}'] += value

            # Add item to table data
            table_data.append({
                'name': item.name,
                'calories': round(item_macros['calories'], 1),
                'fat': round(item_macros['fat'], 1),
                'carbs': round(item_macros['carbs'], 1),
                'sugars': round(item_macros['sugars'], 1),
                'protein': round(item_macros['protein'], 1)
            })

        # Prepare JSON data for the pie chart
        chart_data = {
            'labels': ['Fat', 'Carbs', 'Sugars', 'Protein'],
            'datasets': [{
                'data': [float(macros['total_fat']), float(macros['total_carbs']), 
                         float(macros['total_sugars']), float(macros['total_protein'])],
                'backgroundColor': ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0']
            }]
        }

        # Return combined JSON data
        return jsonify({'chartData': chart_data, 'tableData': table_data})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@nutrition_blueprint.route('/meals-and-foods/get-meal/<int:id>', methods=['GET'])
def getMeal(id):
    try:
        meal = Meal.query.get_or_404(id)
        food_items = MealFoodItem.query.filter_by(meal_id=id).join(FoodItem, MealFoodItem.food_item_id == FoodItem.id).all()

        food_items_data = []
        for fi in food_items:
            food_items_data.append({
                'id': fi.food_item_id,
                'name': fi.food_item.name,
                'serving_count': str(fi.serving_count),
                'serving_size': fi.food_item.serving_size
            })

        return jsonify({
            'id': meal.id,
            'name': meal.name,
            'food_items': food_items_data
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@nutrition_blueprint.route('/meals-and-foods/update-meal/<int:id>', methods=['POST'])
def updateMeal(id):
    try:
        data = request.get_json()
        meal = Meal.query.get_or_404(id)

        # Update meal name
        meal.name = data['name']

        # IDs of food items to be updated or added
        updated_or_new_food_item_ids = {item['id'] for item in data['food_items']}
        
        # IDs of food items to be deleted
        deleted_food_item_ids = set(data['deleted_food_items'])

        # Delete MealFoodItem records for deleted food items
        MealFoodItem.query.filter(
            MealFoodItem.meal_id == id,
            MealFoodItem.food_item_id.in_(deleted_food_item_ids)
        ).delete(synchronize_session='fetch')

        # Update existing and add new MealFoodItem records
        for item in data['food_items']:
            meal_food_item = MealFoodItem.query.filter_by(
                meal_id=id, food_item_id=item['id']
            ).first()

            if meal_food_item:
                meal_food_item.serving_count = item['serving_count']
            else:
                new_meal_food_item = MealFoodItem(
                    meal_id=id,
                    food_item_id=item['id'],
                    serving_count=item['serving_count']
                )
                db.session.add(new_meal_food_item)

        db.session.commit()
        return jsonify({'message': 'Meal updated successfully'})

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@nutrition_blueprint.route('/meals-and-foods/log-meal', methods=['POST'])
def logMeal():
    try:
        # Parse data from the incoming request
        data = request.get_json()
        meal_id = data['meal_id']
        meal_type = data['meal_type']
        log_date = datetime.strptime(data['log_date'], '%Y-%m-%d')

        # Create a new MealLog instance
        new_meal_log = FoodMealLog(
            meal_id=meal_id,
            meal_type=meal_type,
            log_date=log_date
        )

        # Add to the database and commit
        db.session.add(new_meal_log)
        db.session.commit()

        return jsonify({'message': 'Meal logged successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@nutrition_blueprint.route('/meals-and-foods/get-all-meals', methods=['GET'])
def getAllMeals():
    try:
        meals = Meal.query.all()
        meals_data = []
        for meal in meals:
            food_items_data = db.session.query(
                FoodItem.name, MealFoodItem.serving_count
            ).join(MealFoodItem, FoodItem.id == MealFoodItem.food_item_id)\
             .filter(MealFoodItem.meal_id == meal.id).all()

            meal_dict = meal.to_dict()
            meal_dict['food_items'] = [
                {'name': fi.name, 'serving_count': str(fi.serving_count)} for fi in food_items_data
            ]
            meals_data.append(meal_dict)
        
        return jsonify({'meals': meals_data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@nutrition_blueprint.route('/meals-and-foods/add-meal')
def addMeal():
    today = datetime.now().strftime("%Y-%m-%d")
    return render_template('nutrition/meals-and-food/meal/add-meal.html', today=today)

# Tracker Routes

@nutrition_blueprint.route('/tracking', methods=['GET'])
def tracking():
    # Get the date from the request or use today's date as default
    date_str = request.args.get('date', datetime.now().date().isoformat())

    # Convert the string to a datetime object if it's not already
    try:
        selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        # If the conversion fails, use today's date
        selected_date = datetime.now().date()

    meal_type_order = ['breakfast', 'lunch', 'dinner', 'snacks']
    meal_type_data = {mt: {'meals': [], 'foods': []} for mt in meal_type_order}
    grand_total = {'calories': 0, 'total_fat': 0, 'total_carbohydrate': 0, 'total_sugars': 0, 'total_protein': 0}

    logs = db.session.query(
        FoodMealLog.id.label('food_meal_log_id'),
        FoodMealLog.meal_type,
        Meal.name.label('meal_name'),
        Meal.id.label('meal_id'),
        FoodItem.name.label('food_item_name'),
        FoodItem.calories,
        FoodItem.total_fat,
        FoodItem.total_carbohydrate,
        FoodItem.total_sugars,
        FoodItem.total_protein,
        FoodMealLog.serving_count
    ).outerjoin(Meal, FoodMealLog.meal_id == Meal.id)\
    .outerjoin(FoodItem, FoodMealLog.food_item_id == FoodItem.id)\
    .filter(FoodMealLog.log_date == selected_date)\
    .all()

    # Process logs for meals and food items
    for log in logs:
        # Process meal logs
        if log.meal_id:
            meal = Meal.query.get(log.meal_id)
            if meal:
                total_nutrition = {'calories': 0, 'total_fat': 0, 'total_carbohydrate': 0, 'total_sugars': 0, 'total_protein': 0}
                for mfi in meal.meal_food_item_assoc:
                    food_item = mfi.food_item
                    serving_count = Decimal(mfi.serving_count)
                    # Calculate nutrition values
                    for key in total_nutrition.keys():
                        attr_value = getattr(food_item, key, 0) or 0
                        total_nutrition[key] += round(Decimal(attr_value) * serving_count, 1)
                log_data = log._asdict()
                log_data.update(total_nutrition)
                meal_type_data[log.meal_type]['meals'].append(log_data)
                for key in total_nutrition:
                    grand_total[key] += total_nutrition[key]
        
        # Process food item logs
        elif log.food_item_name:
            food_log_data = log._asdict()
            serving_count = Decimal(food_log_data['serving_count'])
            for key in ['calories', 'total_fat', 'total_carbohydrate', 'total_sugars', 'total_protein']:
                food_log_data[key] = round(Decimal(food_log_data[key]) * serving_count, 1)
            meal_type_data[log.meal_type]['foods'].append(food_log_data)
            for key in grand_total.keys():
                grand_total[key] += food_log_data[key]

    # Round grand total values
    for key in grand_total:
        grand_total[key] = round(grand_total[key], 1)

    return render_template('nutrition/tracking/tracking.html', 
                           meal_type_data=meal_type_data, 
                           grand_total=grand_total,
                           selected_date=selected_date)

@nutrition_blueprint.route('/delete_entry/<int:id>', methods=['POST'])
def delete_entry(id):
    # Assuming you have a model for your 'FoodMealLog' table
    entry_to_delete = FoodMealLog.query.get(id)

    if entry_to_delete:
        # Delete the entry from the database
        db.session.delete(entry_to_delete)
        db.session.commit()

    # Redirect back to the tracking page or any other appropriate page
    return redirect(url_for('nutrition.tracking'))
