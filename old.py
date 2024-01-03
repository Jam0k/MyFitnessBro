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

@app.route('/nutrition/meals/create-food')
def addFood():
    return render_template('create-food.html')

# Get food items in /nutrition/meals/browse-foods.

@app.route('/get-foods', methods=['GET'])
def get_foods():
    try:
        foods = FoodItem.query.all()
        foods_data = [{
            'id': food.id,
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

@app.route('/create-food', methods=['POST'])
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