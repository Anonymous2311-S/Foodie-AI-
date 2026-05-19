from flask import Flask, render_template, request, jsonify
import sqlite3
import os
import shutil

base_dir = os.path.abspath(os.path.dirname(__file__))
template_dir = os.path.join(base_dir, 'templates')
static_dir = os.path.join(base_dir, 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

def get_db_connection():
    # Vercel environment is read-only, so we use /tmp which is writable
    original_db_path = os.path.join(os.path.dirname(__file__), 'food.db')
    tmp_db_path = '/tmp/food.db'
    
    # Check if we are running in a read-only environment (like Vercel)
    # If not on Vercel, we can just use the original path, but using /tmp is safe everywhere for this simple app
    # Actually, Windows doesn't have /tmp, so we use an OS-independent temp dir
    import tempfile
    temp_dir = tempfile.gettempdir()
    tmp_db_path = os.path.join(temp_dir, 'food.db')
    
    if not os.path.exists(tmp_db_path) and os.path.exists(original_db_path):
        shutil.copy2(original_db_path, tmp_db_path)
        
    conn = sqlite3.connect(tmp_db_path)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/recommend', methods=['POST'])
def recommend():
    data = request.json
    
    # Base query
    query = "SELECT * FROM recipes WHERE 1=1"
    params = []
    
    # 1. Diet constraints
    if data.get('vegetarian'):
        query += " AND is_vegetarian = 1"
    if data.get('vegan'):
        query += " AND is_vegan = 1"
    if data.get('gluten_free'):
        query += " AND is_gluten_free = 1"
        
    # 2. Cuisine constraint
    cuisine = data.get('cuisine')
    if cuisine and cuisine != 'Any':
        query += " AND cuisine = ?"
        params.append(cuisine)
        
    # 3. Calories constraint
    max_calories = data.get('max_calories')
    if max_calories:
        query += " AND calories <= ?"
        params.append(int(max_calories))
        
    # Order by somewhat randomized or by lowest calories if health-focused
    query += " ORDER BY calories ASC LIMIT 10"
    
    conn = get_db_connection()
    recipes = conn.execute(query, params).fetchall()
    conn.close()
    
    # Convert to list of dicts
    result = []
    for r in recipes:
        result.append({
            'id': r['id'],
            'recipe_name': r['recipe_name'],
            'cuisine': r['cuisine'],
            'calories': r['calories'],
            'is_vegetarian': bool(r['is_vegetarian']),
            'is_vegan': bool(r['is_vegan']),
            'is_gluten_free': bool(r['is_gluten_free']),
            'ingredients': r['ingredients'],
            'image_url': r['image_url']
        })
        
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
