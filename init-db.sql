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
