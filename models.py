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