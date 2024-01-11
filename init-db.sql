CREATE TABLE food_items (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    serving_size VARCHAR(100),  -- e.g., '100g', '1 cup', etc.
    calories INTEGER,          -- Total calories
    total_fat DECIMAL(5,2),     -- Total fat in grams
    total_carbohydrate DECIMAL(5,2), -- Total carbohydrates in grams
    total_sugars DECIMAL(5,2),  -- Total sugars in grams
    total_protein DECIMAL(5,2),       -- Total Protein in grams
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE meals (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE meal_food_items (
    meal_id INTEGER REFERENCES meals(id),
    food_item_id INTEGER REFERENCES food_items(id),
    serving_count DECIMAL(5,2), -- Number of servings of this food item in the meal
    PRIMARY KEY (meal_id, food_item_id)
);

CREATE TABLE food_meal_logs (
    id SERIAL PRIMARY KEY,
    meal_type VARCHAR(100),  -- e.g., 'breakfast', 'lunch', 'dinner', 'snack'
    meal_id INTEGER REFERENCES meals(id),  -- NULL if logging an individual food item
    food_item_id INTEGER REFERENCES food_items(id),  -- NULL if logging a meal
    serving_count DECIMAL(5,2),  -- Number of servings (for individual food items)
    log_date DATE NOT NULL,  -- Date of the food/meal intake
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE exercises (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(100),  -- Exercise category, e.g., 'Strength', 'Flexibility', etc.
    duration_minutes INTEGER,  -- Duration of exercise in minutes
    sets INTEGER,  -- Number of sets (for strength training)
    reps INTEGER,  -- Number of repetitions per set (for strength training)
    weight_lifted DECIMAL(5,2),  -- Weight lifted in kilograms (for strength training)
    calories_burned INTEGER,  -- Estimated calories burned during the exercise
    notes TEXT,  -- Optional notes or comments about the exercise
    log_date DATE NOT NULL,  -- Date of the exercise
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the Workout Plans table
CREATE TABLE workout_plans (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the Workout Plan Exercises junction table
CREATE TABLE workout_plan_exercises (
    workout_plan_id INTEGER REFERENCES workout_plans(id),
    exercise_id INTEGER REFERENCES exercises(id),
    PRIMARY KEY (workout_plan_id, exercise_id)
);
