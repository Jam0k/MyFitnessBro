from flask_sqlalchemy import SQLAlchemy

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