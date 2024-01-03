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