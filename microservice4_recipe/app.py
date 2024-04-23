from flask import Flask, jsonify, render_template, request, redirect
import requests
from redis import Redis

app = Flask(__name__)
redis = Redis(host='localhost', port=6379)

def get_selected_items():
    selected_items = []
    for item_id in redis.smembers('selected_items'):
        item = next((item for item in available_items if item['id'] == int(item_id.decode('utf-8'))), None)
        if item:
            selected_items.append(item)
    return selected_items

@app.route('/', methods=['GET'])
def main_page():
    return render_template('recipe.html')

# Your API key for Spoonacular
api_key = 'ffaeea8303ac4006bac35629dc34f9a7'

@app.route('/recipes', methods=['GET'])
def get_recipes():
    # Fetch selected items from Redis
    items = [item.decode('utf-8') for item in redis.smembers('selected_items')]

    ingredients_string = ','.join(items)

    # Call Spoonacular API to fetch recipes
    url = f'https://api.spoonacular.com/recipes/findByIngredients?ingredients={ingredients_string}&number=2&apiKey={api_key}'

    params = {
        'apiKey': api_key,
        'number': 5,  # Fetch 5 random recipes
        'instructionsRequired': True  # Include instructions in the response
    }
    response = requests.get(url, params=params)

@app.route('/random-recipes', methods=['GET'])
def get_random_recipes_page():
    return render_template('random-recipes.html')

@app.route('/random-recipes', methods=['GET'])
def get_random_recipes():
    # Call Spoonacular API to fetch random recipes
    url = 'https://api.spoonacular.com/recipes/random'
    params = {
        'apiKey': api_key,
        'number': 5,  # Fetch 5 random recipes
        'instructionsRequired': True  # Include instructions in the response
    }
    response = requests.get(url, params=params)

    # Return the response from Spoonacular API
    if response.status_code == 200:
        recipes = response.json()['recipes']
        # Extract relevant information for each recipe
        formatted_recipes = []
        for recipe in recipes:
            recipe_info = {
                'title': recipe['title'],
                'ingredients': [{'name': ingredient['name'], 'quantity': ingredient['amount'], 'unit': ingredient['unit']} for ingredient in recipe['extendedIngredients']],
                'steps': recipe['instructions'].split('\n') if 'instructions' in recipe else []
            }
            formatted_recipes.append(recipe_info)
        return jsonify(formatted_recipes)
    else:
        return jsonify({'error': 'Failed to fetch recipes'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
