from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__) # creates a flask app
app.secret_key = 'supersecretkey'

users = {} # dictionary for user preferences
recipes = [] # a list for recipes

# dictionary to classify recipes based on dietary restrictions and cuisine
recipe_categories = {
    "Spaghetti": {"dietary": "gluten", "cuisine": "Italian"},
    "Shaurma": {"dietary": "none", "cuisine": "Turkish"},
    "Chicken Salad": {"dietary": "healthy", "cuisine": "American"},
    "Vegetable Salad": {"dietary": "vegetarian", "cuisine": "Asian"},
    "Cake": {"dietary": "flour", "cuisine": "American"},
    "Sushi": {"dietary": "healthy", "cuisine": "Asian"}
}

@app.route('/', methods=['GET', 'POST']) # define home page, allows GET and POST requests
def home():
    if request.method == 'POST':
        name = request.form.get('name', '').strip() #when user input name, take this name from the input field
        if name:
            session['name'] = name
            return redirect(url_for('preferences')) #if a name is entered, redirect to preferences page
    return render_template('home.html') 

@app.route('/preferences', methods=['GET', 'POST']) #define preferences page
def preferences():
    if 'name' not in session:
        return redirect(url_for('home')) #if there is no name in session, return to home page

    if request.method == 'POST':
        dietary = request.form.get('dietary') 
        cuisine = request.form.get('cuisine')
        meals = request.form.get('meals')
        if dietary and meals and cuisine: #if all fields are filled rightly, then keep it in dictionary
            users[session['name']] = {
                'dietary': dietary,
                'cuisine': cuisine,
                'meals': meals
            }
            return redirect(url_for('recipe_input')) #redirect to recipe input page
    return render_template('preferences.html')

@app.route('/recipe_input', methods=['GET', 'POST'])
def recipe_input():
    if 'name' not in session:
        return redirect(url_for('home'))

    if request.method == 'POST':
        recipe_name = request.form.get('recipe_name', '').strip() #takes recipe name and ingridients from the input field
        ingredients = request.form.get('ingredients', '').strip()
        if recipe_name and ingredients:
            recipes.append({'name': recipe_name, 'ingredients': ingredients}) #if recipe name and ingridients are valid, then store them in recipe list
            return redirect(url_for('recipe_plan')) #redirect to recipe plan page
    return render_template('recipe_input.html')

@app.route('/recipe_plan')
def recipe_plan():
    if 'name' not in session:
        return redirect(url_for('home'))

    user_prefs = users.get(session['name'], {}) #takes user preferences from dictionary
    preferred_cuisine = user_prefs.get('cuisine', '').lower()
    dietary_restriction = user_prefs.get('dietary', '').lower() #extracts preferences and compares it 

    #filter recipes based on user's preferences
    filtered_recipes = []
    for recipe in recipes:
        recipe_name = recipe["name"] #trying to find valid recipe name
        category = recipe_categories.get(recipe_name, {"dietary": "no", "cuisine": "no valid cuisine"}) #if dietary and cuisine are not valid, then show NONE and UKNOWN

        #check if the recipe matches the user's preferences
        cuisine_match = (
            preferred_cuisine in category["cuisine"].lower() 
            if preferred_cuisine 
            else True
        )
        dietary_match = (
            dietary_restriction in category["dietary"].lower() 
            if dietary_restriction 
            else True
        )

        if cuisine_match and dietary_match:
            filtered_recipes.append(recipe) #if cuisine and dietary match, then add to recipe list

    return render_template('recipe_plan.html', user_prefs=user_prefs, recipes=filtered_recipes)

if __name__ == '__main__':
    app.run(debug=True) #run the flask in debug mode
