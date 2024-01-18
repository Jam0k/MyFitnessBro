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
    notes TEXT,  -- Optional notes or comments about the exercise
    log_date DATE NOT NULL,  -- Date of the exercise
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE exercise_logs (
    id SERIAL PRIMARY KEY,
    exercise_id INTEGER REFERENCES exercises(id),
    sets INTEGER NOT NULL,
    reps INTEGER NOT NULL,
    weight FLOAT,
    notes TEXT,
    log_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE CardioLog (
    id SERIAL PRIMARY KEY,
    activity VARCHAR(255) NOT NULL,
    duration INT,
    calories_burned INT,
    date DATE NOT NULL,
    notes TEXT -- TEXT type for potentially longer notes
);

CREATE TABLE goals (
    id SERIAL PRIMARY KEY,
    calories INT NOT NULL,
    fat DECIMAL(8, 2) NOT NULL, -- Using DECIMAL for decimal values
    carbohydrates DECIMAL(8, 2) NOT NULL,
    sugars DECIMAL(8, 2) NOT NULL,
    protein DECIMAL(8, 2) NOT NULL
);
