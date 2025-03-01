from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__) #dsdsdssd
app.secret_key = 'supersecretkey'

users, recipes = {}, []

# Dictionary to classify recipes based on dietary restrictions and cuisine
recipe_categories = {
    "Spaghetti Carbonara": {"dietary": "gluten", "cuisine": "Italian"},
    "Tacos": {"dietary": "none", "cuisine": "Mexican"},
    "Chicken Salad": {"dietary": "healthy", "cuisine": "American"},
    "Vegetable Salad": {"dietary": "vegetarian", "cuisine": "Asian"},
    "Pancakes": {"dietary": "flour", "cuisine": "American"},
    "Sushi": {"dietary": "healthy", "cuisine": "Asian"}
}

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        if name:
            session['name'] = name
            return redirect(url_for('preferences'))
    return render_template('home.html')

@app.route('/preferences', methods=['GET', 'POST'])
def preferences():
    if 'name' not in session:
        return redirect(url_for('home'))

    if request.method == 'POST':
        dietary = request.form.get('dietary')
        cuisine = request.form.get('cuisine')
        meals = request.form.get('meals')
        if dietary and meals and cuisine:
            users[session['name']] = {
                'dietary': dietary,
                'cuisine': cuisine,
                'meals': meals
            }
            return redirect(url_for('recipe_input'))
    return render_template('preferences.html')

@app.route('/recipe_input', methods=['GET', 'POST'])
def recipe_input():
    if 'name' not in session:
        return redirect(url_for('home'))

    if request.method == 'POST':
        recipe_name = request.form.get('recipe_name', '').strip()
        ingredients = request.form.get('ingredients', '').strip()
        if recipe_name and ingredients:
            recipes.append({'name': recipe_name, 'ingredients': ingredients})
            return redirect(url_for('recipe_plan'))
    return render_template('recipe_input.html')

@app.route('/recipe_plan')
def recipe_plan():
    if 'name' not in session:
        return redirect(url_for('home'))

    user_prefs = users.get(session['name'], {})
    preferred_cuisine = user_prefs.get('cuisine', '').lower()
    dietary_restriction = user_prefs.get('dietary', '').lower()

    # Filter recipes based on user's preferences
    filtered_recipes = []
    for recipe in recipes:
        recipe_name = recipe["name"]
        category = recipe_categories.get(recipe_name, {"dietary": "none", "cuisine": "unknown"})

        # Check if the recipe matches the user's preferences
        cuisine_match = preferred_cuisine in category["cuisine"].lower() if preferred_cuisine else True
        dietary_match = dietary_restriction in category["dietary"].lower() if dietary_restriction else True

        if cuisine_match and dietary_match:
            filtered_recipes.append(recipe)

    return render_template('recipe_plan.html', user_prefs=user_prefs, recipes=filtered_recipes)

if __name__ == '__main__':
    app.run(debug=True)
