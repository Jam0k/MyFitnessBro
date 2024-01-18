from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = SQLAlchemy()


class FoodItem(db.Model):
    __tablename__ = "food_items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    serving_size = db.Column(db.String(100))
    calories = db.Column(db.Integer)
    total_fat = db.Column(db.Numeric(5, 2))
    total_carbohydrate = db.Column(db.Numeric(5, 2))
    total_sugars = db.Column(db.Numeric(5, 2))
    total_protein = db.Column(db.Numeric(5, 2))
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
            "total_protein": str(self.total_protein),
        }


# New Meal model
class Meal(db.Model):
    __tablename__ = "meals"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    food_items = db.relationship(
        "FoodItem",
        secondary="meal_food_items",
        backref=db.backref("meals", lazy="dynamic"),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


# New MealFoodItem model (junction table)
class MealFoodItem(db.Model):
    __tablename__ = "meal_food_items"

    meal_id = db.Column(db.Integer, db.ForeignKey("meals.id"), primary_key=True)
    food_item_id = db.Column(
        db.Integer, db.ForeignKey("food_items.id"), primary_key=True
    )
    serving_count = db.Column(db.Numeric(5, 2))

    meal = db.relationship("Meal", backref=db.backref("meal_food_item_assoc"))
    food_item = db.relationship("FoodItem", backref=db.backref("meal_food_item_assoc"))


class FoodMealLog(db.Model):
    __tablename__ = "food_meal_logs"

    id = db.Column(db.Integer, primary_key=True)
    food_item_id = db.Column(db.Integer, db.ForeignKey("food_items.id"))
    meal_id = db.Column(db.Integer, db.ForeignKey("meals.id"))  # Add this line
    serving_count = db.Column(db.Numeric(5, 2))
    meal_type = db.Column(db.String(50))  # Type of meal (breakfast, lunch, etc.)
    food_item = db.relationship("FoodItem", backref=db.backref("logs", lazy="dynamic"))
    meal = db.relationship(
        "Meal", backref=db.backref("meal_logs", lazy="dynamic")
    )  # Add this relationship
    log_date = db.Column(db.Date)  # Ensure this line is present and correctly defined

    def to_dict(self):
        return {
            "id": self.id,
            "food_item_id": self.food_item_id,
            "meal_id": self.meal_id,  # Include this field
            "serving_count": str(self.serving_count),
            "meal_type": self.meal_type,
            "log_date": self.log_date,
        }


# New Exercise model
class Exercise(db.Model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(100))
    notes = db.Column(db.Text)
    log_date = db.Column(db.Date, nullable=False, default=db.func.current_date())
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "notes": self.notes,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


class ExerciseLog(db.Model):
    __tablename__ = "exercise_logs"

    id = db.Column(db.Integer, primary_key=True)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    sets = db.Column(db.Integer, nullable=False)
    reps = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Float)
    notes = db.Column(db.Text)
    log_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    exercise = db.relationship('Exercise', backref=db.backref('logs', lazy=True))



class WorkoutPlan(db.Model):
    __tablename__ = "workout_plans"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    exercises = db.relationship(
        "Exercise",
        secondary="workout_plan_exercises",
        backref=db.backref("workout_plans", lazy=True),
    )


class WorkoutPlanExercise(db.Model):
    __tablename__ = "workout_plan_exercises"
    workout_plan_id = db.Column(
        db.Integer, db.ForeignKey("workout_plans.id"), primary_key=True
    )
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercises.id"), primary_key=True)



class CardioLog(db.Model):
    __tablename__ = "cardiolog"

    id = db.Column(
        db.Integer, primary_key=True
    )  # SERIAL in PostgreSQL is represented as Integer in SQLAlchemy
    activity = db.Column(db.String(255), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    calories_burned = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    notes = db.Column(db.Text)  # TEXT type for potentially longer notes

    def to_dict(self):
        return {
            "id": self.id,
            "activity": self.activity,
            "duration": self.duration,
            "calories_burned": self.calories_burned,
            "date": self.date.isoformat(),
            "notes": self.notes,
        }


class Goal(db.Model):
    __tablename__ = "goals"

    id = db.Column(db.Integer, primary_key=True)
    calories = db.Column(db.Integer, nullable=False)
    fat = db.Column(
        db.Numeric(8, 2), nullable=False
    )  # Using DECIMAL for decimal values
    carbohydrates = db.Column(db.Numeric(8, 2), nullable=False)
    sugars = db.Column(db.Numeric(8, 2), nullable=False)
    protein = db.Column(db.Numeric(8, 2), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "calories": self.calories,
            "fat": str(self.fat),
            "carbohydrates": str(self.carbohydrates),
            "sugars": str(self.sugars),
            "protein": str(self.protein),
        }
