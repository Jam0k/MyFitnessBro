from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = SQLAlchemy()

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

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "serving_size": str(self.serving_size),
            "calories": self.calories,
            "total_fat": str(self.total_fat),
            "total_carbohydrate": str(self.total_carbohydrate),
            "total_sugars": str(self.total_sugars),
            "total_protein": str(self.total_protein)
        }

# New Meal model
class Meal(db.Model):
    __tablename__ = 'meals'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    food_items = db.relationship('FoodItem', secondary='meal_food_items', backref=db.backref('meals', lazy='dynamic'))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

# New MealFoodItem model (junction table)
class MealFoodItem(db.Model):
    __tablename__ = 'meal_food_items'

    meal_id = db.Column(db.Integer, db.ForeignKey('meals.id'), primary_key=True)
    food_item_id = db.Column(db.Integer, db.ForeignKey('food_items.id'), primary_key=True)
    serving_count = db.Column(db.Numeric(5,2))

    meal = db.relationship('Meal', backref=db.backref('meal_food_item_assoc'))
    food_item = db.relationship('FoodItem', backref=db.backref('meal_food_item_assoc'))

class FoodMealLog(db.Model):
    __tablename__ = 'food_meal_logs'

    id = db.Column(db.Integer, primary_key=True)
    food_item_id = db.Column(db.Integer, db.ForeignKey('food_items.id'))
    meal_id = db.Column(db.Integer, db.ForeignKey('meals.id'))  # Add this line
    serving_count = db.Column(db.Numeric(5, 2))
    log_date = db.Column(db.Date, nullable=False)
    meal_type = db.Column(db.String(50))  # Type of meal (breakfast, lunch, etc.)

    food_item = db.relationship('FoodItem', backref=db.backref('logs', lazy='dynamic'))
    meal = db.relationship('Meal', backref=db.backref('meal_logs', lazy='dynamic'))  # Add this relationship

    def to_dict(self):
        return {
            'id': self.id,
            'food_item_id': self.food_item_id,
            'meal_id': self.meal_id,  # Include this field
            'serving_count': str(self.serving_count),
            'log_date': self.log_date.isoformat(),
            'meal_type': self.meal_type
        }

# New Exercise model
class Exercise(db.Model):
    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(100))
    duration_minutes = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    reps = db.Column(db.Integer)
    weight_lifted = db.Column(db.Numeric(5, 2))
    calories_burned = db.Column(db.Integer)
    notes = db.Column(db.Text)
    log_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'duration_minutes': self.duration_minutes,
            'sets': self.sets,
            'reps': self.reps,
            'weight_lifted': str(self.weight_lifted),
            'calories_burned': self.calories_burned,
            'notes': self.notes,
            'log_date': self.log_date.isoformat(),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }