import sqlite3
import os

def setup_database():
    db_path = "food.db"
    
    if os.path.exists(db_path):
        os.remove(db_path)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create recipes table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS recipes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        recipe_name TEXT NOT NULL,
        cuisine TEXT NOT NULL,
        calories INTEGER NOT NULL,
        is_vegetarian BOOLEAN NOT NULL,
        is_vegan BOOLEAN NOT NULL,
        is_gluten_free BOOLEAN NOT NULL,
        ingredients TEXT NOT NULL,
        image_url TEXT NOT NULL
    )
    """)
    
    # Sample Data
    recipes = [
        ("Paneer Butter Masala", "Indian", 450, True, False, True, "Paneer, Butter, Tomato, Cream, Spices", "https://images.unsplash.com/photo-1585937421612-70a008356fbe?q=80&w=600"),
        ("Chicken Biryani", "Indian", 600, False, False, True, "Chicken, Rice, Spices, Yogurt", "https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?q=80&w=600"),
        ("Margherita Pizza", "Italian", 800, True, False, False, "Pizza dough, Tomato sauce, Mozzarella, Basil", "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?q=80&w=600"),
        ("Spaghetti Aglio e Olio", "Italian", 420, True, True, False, "Spaghetti, Garlic, Olive oil, Chili flakes", "https://images.unsplash.com/photo-1551183053-bf91a1d81141?q=80&w=600"),
        ("Caprese Salad", "Italian", 250, True, False, True, "Tomato, Mozzarella, Basil, Balsamic glaze", "https://images.unsplash.com/photo-1592417817098-8fd3d9eb14a5?q=80&w=600"),
        ("Zucchini Noodles with Pesto", "Italian", 310, True, True, True, "Zucchini, Basil pesto, Pine nuts, Olive oil", "https://images.unsplash.com/photo-1593504049359-74330189a345?q=80&w=600"),
        ("Tofu Stir-fry", "Chinese", 350, True, True, True, "Tofu, Broccoli, Bell peppers, Soy sauce", "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?q=80&w=600"),
        ("Beef Burger", "American", 700, False, False, False, "Beef patty, Buns, Lettuce, Tomato, Cheese", "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?q=80&w=600"),
        ("Vegan Buddha Bowl", "Global", 400, True, True, True, "Quinoa, Sweet potato, Chickpeas, Avocado, Tahini", "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?q=80&w=600"),
        ("Quinoa Salad", "Global", 320, True, True, True, "Quinoa, Cucumber, Tomato, Feta, Lemon dressing", "https://images.unsplash.com/photo-1505253758473-96b7015fcd40?q=80&w=600"),
        ("Grilled Salmon", "American", 450, False, False, True, "Salmon, Asparagus, Lemon, Butter", "https://images.unsplash.com/photo-1467003909585-2f8a72700288?q=80&w=600"),
        ("Mushroom Risotto", "Italian", 550, True, False, True, "Arborio rice, Mushrooms, Parmesan, Broth", "https://images.unsplash.com/photo-1473093295043-cdd812d0e601?q=80&w=600")
    ]
    
    cursor.executemany("""
    INSERT INTO recipes (recipe_name, cuisine, calories, is_vegetarian, is_vegan, is_gluten_free, ingredients, image_url)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, recipes)
    
    conn.commit()
    conn.close()
    
    print("Database setup complete. Added 12 sample recipes.")

if __name__ == '__main__':
    setup_database()
